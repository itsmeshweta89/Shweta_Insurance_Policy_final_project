import json
import re
from functools import lru_cache

from langchain_core.tools import tool

from .llm import get_llm
from .model import IntentResult

# Deterministic (non-LLM) keyword rules for Insurance Policy Co-pilot
# Priority order is critical: claims/fraud/cancellation must override generic policy queries.

_INTENT_RULES: list[tuple[str, list[str], str]] = [
    (
        "fraud_or_scam",
        [
            r"\bfraud\b", r"fake policy", r"scam", r"unauthoriz",
            r"someone else (used|bought) my policy",
            r"policy (tampered|forged)", r"identity theft",
        ],
        "fraud_investigation_team",
    ),
    (
        "claim_intent_or_status",
        [
            r"\bclaim\b", r"claim status", r"track claim", r"file a claim",
            r"hospital bill", r"accident claim", r"medical claim",
            r"claim rejected", r"claim approved", r"claim delay",
        ],
        "claims_processing_team",
    ),
    (
        "complaint_or_escalation",
        [
            r"\bcomplaint\b", r"not satisfied", r"frustrat", r"angry",
            r"bad service", r"worst experience", r"not resolved",
            r"escalate", r"still waiting", r"no response",
        ],
        "grievance_redressal",
    ),
    (
        "policy_cancellation_or_surrender",
        [
            r"cancel policy", r"close policy", r"surrender policy",
            r"stop policy", r"terminate policy", r"refund policy",
            r"policy cancellation", r"withdraw policy",
        ],
        "policy_cancellation_team",
    ),
    (
        "premium_payment_issue",
        [
            r"premium", r"payment failed", r"payment not received",
            r"auto debit failed", r"emi failed", r"due amount",
            r"late payment", r"receipt not generated",
        ],
        "billing_and_payments_team",
    ),
    (
        "policy_information_query",
        [
            r"\bpolicy\b", r"coverage", r"what does (it|this policy) cover",
            r"benefits", r"features", r"terms and conditions",
            r"sum insured", r"waiting period", r"exclusions",
        ],
        "policy_information_bot",
    ),
    (
        "renewal_or_lapse",
        [
            r"renew policy", r"policy renewal", r"expiry date",
            r"expired policy", r"lapsed policy", r"grace period",
        ],
        "renewal_team",
    ),
    (
        "agent_or_contact_request",
        [
            r"agent", r"advisor", r"call me", r"contact me",
            r"customer care", r"helpline", r"support number",
        ],
        "human_assistance_routing",
    ),
]

_DEFAULT_ROUTING = "general_support"


def _classify(customer_message: str) -> IntentResult:
    text = customer_message.lower()
    for intent, patterns, routing in _INTENT_RULES:
        matches = sum(1 for pattern in patterns if re.search(pattern, text))
        if matches:
            confidence = min(0.6 + 0.15 * matches, 0.98)
            return IntentResult(intent=intent, confidence=confidence, routing=routing)
    return IntentResult(intent="general_faq", confidence=0.5, routing=_DEFAULT_ROUTING)

@tool
def classify_intent(customer_message: str) -> str:
    """Deterministically classify the customer's message into an insurance
    intent category using keyword rules (no LLM call, fully reproducible).

    Use this to determine the customer's primary intent and route the
    request to the appropriate insurance team. High-priority intents such
    as fraud, claims, complaints, and policy cancellations are evaluated
    before general policy inquiries.

    This function does NOT answer questions about insurance policies or
    coverage details. Use the knowledge_retrieval tool for policy-specific
    information and FAQs.

    Returns a JSON string of:
    {
        "intent": <intent>,
        "confidence": <confidence>,
        "routing": <routing_team>
    }

    where intent is one of:
        - fraud_or_scam
        - claim_intent_or_status
        - complaint_or_escalation
        - policy_cancellation_or_surrender
        - premium_payment_issue
        - policy_information_query
        - renewal_or_lapse
        - agent_or_contact_request
        - general_faq
    """
    return _classify(customer_message).model_dump_json()

@lru_cache(maxsize=1)
def _get_rag_pipeline():
    from .rag.pipeline import RAGPipeline

    return RAGPipeline(llm=get_llm())


# Built eagerly at import time (main thread) rather than lazily on first
# tool call: chromadb's PersistentClient registry is not safe to populate
# from the worker thread LangGraph's ToolNode executes sync tools in.
_get_rag_pipeline()

@tool
def knowledge_retrieval(query: str) -> str:
    """Retrieve a grounded, cited answer from the insurance company's
    internal knowledge base (policy documents, coverage details,
    exclusions, premium payment rules, claim procedures, renewal policies,
    waiting periods, policy endorsements, cancellation/refund rules, and
    general FAQs) using retrieval-augmented generation (RAG).

    Use this whenever the customer asks a factual question about insurance
    products, policy benefits, claim eligibility, required documents,
    premium payments, renewals, coverage limits, exclusions, or any other
    information that should be answered from official policy documents
    rather than from the language model's memory.

    Example queries:
    - What is covered under my health insurance policy?
    - What documents are required to file a motor insurance claim?
    - Is cataract surgery covered?
    - What is the waiting period for pre-existing diseases?
    - How do I renew my policy?
    - Can I cancel my policy and receive a refund?
    - What happens if I miss a premium payment?
    """
    rag_answer = _get_rag_pipeline().answer(query)
    return json.dumps(
        {
            "answer": rag_answer.answer,
            "citations": rag_answer.citations,
        }
    )

@tool
def hitl_approval(action_type: str, description: str) -> str:
    """Request human-in-the-loop approval for a high-risk action.

    Call this when the customer requests:
    - Account closure
    - Large fund transfer (above Rs 50,000)
    - Card blocking/unblocking
    - Loan foreclosure
    - Any irreversible financial action

    The system will pause and wait for a human supervisor to approve or
    reject the action. Returns the decision result as JSON.

    Args:
        action_type: Type of action requiring approval (e.g. "account_closure", "large_transfer", "card_block")
        description: Brief description of what the customer is requesting
    """
    from .hitl import create_approval_request, wait_for_approval

    request = create_approval_request(
        session_id="current",
        action_type=action_type,
        description=description,
    )
    decision = wait_for_approval(request["request_id"], timeout=60)

    if decision["decision"] == "approved":
        return json.dumps({
            "status": "approved",
            "message": f"Action '{action_type}' has been approved by supervisor. Proceeding with: {description}",
            "approver": decision.get("approver", "supervisor"),
        })
    elif decision["decision"] == "rejected":
        return json.dumps({
            "status": "rejected",
            "message": f"Action '{action_type}' was rejected by supervisor. Reason: {decision.get('reason', 'Not specified')}",
        })
    else:
        return json.dumps({
            "status": "timeout",
            "message": "No supervisor response received within the time limit. Please try again or contact a branch representative.",
        })
