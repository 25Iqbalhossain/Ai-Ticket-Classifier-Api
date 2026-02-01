from pydantic import BaseModel, Field
from datetime import datetime

class TicketInput(BaseModel):
    title:str = Field(..., max_length=200)
    description: str = Field(..., max_length=2000)

class TicketOutput(BaseModel):
    id: int
    title: str
    description: str
    predicted_category: str
    status: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class TicketStatusUpdate(BaseModel):
    status: str = Field(pattern="^(open|closed)$")