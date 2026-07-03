from langchain_core.tools import tool
from model import IntentResult

@tool
def classify_intent(customer_message: str) -> str:
    """
    classify the customer intent as per the message.
    always take input as customer question 
    return in the JSON format 
class IntentResult(BaseModel):
    intent: str = Field(description="cashless_hospitalization_query | reimbursement_dispute | insurance_scheme_query | complaint | general_faq")
    confidence: float = Field(ge=0, le=1)
    routing: str
    """

#print(classify_intent.name)
#print(classify_intent.description)
#print(classify_intent.invoke({"customer_message": "I get did not get full reimbursement of my domicilary claim"}))
