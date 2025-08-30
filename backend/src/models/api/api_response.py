from pydantic import BaseModel
from typing import List, Optional, Any

class SessionResponse(BaseModel):
    id: str
    class Config:
        extra = 'allow'

class CreateDBConnResponse(BaseModel):
    status: str
    message: str
    db_connection_id: Optional[str] = None

    class Config:
        extra = 'allow'
