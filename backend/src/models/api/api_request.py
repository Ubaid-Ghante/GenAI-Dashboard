from pydantic import BaseModel
from typing import List, Optional, Any

class DatabaseConnectionRequest(BaseModel):
    user_id: str
    organization_id: str
    name: str
    database: str
    url: str
    key: Optional[str] = None

    class Config:
        extra = 'allow'

class UserSessionRequest(BaseModel):
    user_id: str

 
    class Config:
        extra = 'allow'


class ChatRequest(BaseModel):
    session_id: str
    question: str
    user_context: Optional[dict]= {}
    chat_history: Optional[List[Any]] = []
    domain_selected: Optional[str] = ""
    domain_selection_prompt: Optional[str] = ""
    prompts_dict: Optional[dict] = {}

    class Config:
        extra = 'allow'
        json_schema_extra = {
            "example": {
                "session_id": "68eaf76a-ad6c-4eb6-a3ab-4f65a1da6623",
                "question": "What is the stock price of Apple?",
                "chat_history": [],
                "domain_selected": "sales",
                "domain_selection_prompt": "Please select one of the following domains: banking, finance, marketing and sales. Only respond with the domain name, do not include any other text."
            }
        }

