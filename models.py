from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    customer_name: str
    customer_email: str
    subject: str
    description: str
    priority: Optional[str] = "Medium"

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None
    priority: Optional[str] = None

class NoteOut(BaseModel):
    id: int
    ticket_id: str
    note_text: str
    created_at: str

class TicketOut(BaseModel):
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: str
    status: str
    priority: str
    created_at: str
    updated_at: str
