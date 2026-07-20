"""
Specialist agents for Insurance Policy Advisory Copilot.

Each agent handles one insurance domain.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ..llm import get_llm


CLAIM_SYSTEM_PROMPT = """
You are an Insurance Claim Specialist.

You handle ONLY:
- claim filing process
- claim status
- required documents
- claim rejection reasons
- claim settlement process

Your expertise:
- Health insurance claims
- Motor insurance claims
- Reimbursement process
- Cashless claim process

Always use insurance policy documents as reference.

If the question is not about claims,
say "This is outside my specialization".
"""


POLICY_SYSTEM_PROMPT = """
You are an Insurance Policy Specialist.

You handle ONLY:
- policy coverage
- benefits
- exclusions
- waiting period
- sum insured
- policy terms

Your expertise:
- Health insurance policies
- Motor insurance policies
- Travel insurance policies
- Coverage details

Always provide answers based on policy documents.

If the question is not about policies,
say "This is outside my specialization".
"""


RENEWAL_SYSTEM_PROMPT = """
You are an Insurance Renewal Specialist.

You handle ONLY:
- policy renewal
- premium payment
- policy expiry
- policy lapse
- grace period

Your expertise:
- Renewal process
- Premium due dates
- Payment issues

Always provide answers based on official insurance rules.

If the question is not about renewal,
say "This is outside my specialization".
"""


class SpecialistAgent:

    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt
        self.chain = None

    def get_chain(self):
        if self.chain is None:
            self.chain = (
                ChatPromptTemplate.from_messages([
                    ("system", self.prompt),
                    ("human", "{query}\n\nContext:\n{context}"),
                ])
                | get_llm()
                | StrOutputParser()
            )
        return self.chain

    def invoke(self, query, context=""):
        chain = self.get_chain()

        response = chain.invoke({
            "query": query,
            "context": context
        })

        return response

# Create specialist agents

claim_agent = SpecialistAgent(
    "claim_specialist",
    CLAIM_SYSTEM_PROMPT
)

policy_agent = SpecialistAgent(
    "policy_specialist",
    POLICY_SYSTEM_PROMPT
)

renewal_agent = SpecialistAgent(
    "renewal_specialist",
    RENEWAL_SYSTEM_PROMPT
)

# Agent registry

SPECIALIST_REGISTRY = {
    "claim": claim_agent,
    "policy": policy_agent,
    "renewal": renewal_agent,
}

def route_to_specialist(intent, query, context=""):
    """
    Send query to correct specialist agent.
    """
    routing = {
        "claim_intent_or_status": "claim",
        "policy_information_query": "policy",
        "renewal_or_lapse": "renewal",
    }
    specialist = routing.get(intent)

    if specialist:
        agent = SPECIALIST_REGISTRY.get(specialist)
        if agent:
            return agent.invoke(query, context)

    return None