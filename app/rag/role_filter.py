"""Role-based RAG access control for Insurance Policy Advisory Copilot.

Filters retrieved insurance documents based on user role permissions.
"""

from langchain_core.documents import Document


ROLE_HIERARCHY = {
    "customer": 1,
    "agent": 2,
    "claims_officer": 3,
    "admin": 4,
}


DOCUMENT_ACCESS_RULES = {
    "insurance_faq.html": 1,
    "policy_terms.pdf": 1,
    "renewal_guidelines.html": 1,

    "product_details.pdf": 2,
    "premium_rules.xlsx": 2,

    "claim_process.pdf": 3,
    "claim_settlement_policy.pdf": 3,
    "fraud_guidelines.pdf": 3,

    "admin_config.pdf": 4,
}


DEFAULT_ACCESS_LEVEL = 1


def get_access_level(role: str) -> int:
    return ROLE_HIERARCHY.get(role, 1)



def get_document_clearance(source: str) -> int:
    filename = source.rsplit("/", 1)[-1]
    return DOCUMENT_ACCESS_RULES.get(
        filename,
        DEFAULT_ACCESS_LEVEL
    )



def filter_documents_by_role(
        documents: list[Document],
        user_role: str
) -> list[Document]:
    """Return only documents allowed for user's role."""

    user_level = get_access_level(user_role)

    return [
        doc for doc in documents
        if user_level >= get_document_clearance(
            doc.metadata.get("source", "")
        )
    ]



def enrich_metadata_with_access(
        documents: list[Document]
) -> list[Document]:
    """Add access level metadata during ingestion."""

    for doc in documents:
        doc.metadata["access_level"] = get_document_clearance(
            doc.metadata.get("source", "")
        )

    return documents



def get_role_description(role: str) -> str:

    return {
        "customer":
            "Customer - access to general insurance information",

        "agent":
            "Insurance agent - access to product and premium documents",

        "claims_officer":
            "Claims officer - access to claims and settlement documents",

        "admin":
            "Admin - unrestricted access",
    }.get(
        role,
        "Unknown role - restricted access"
    )