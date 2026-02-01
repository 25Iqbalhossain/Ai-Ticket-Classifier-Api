from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.ticket import TicketInput, TicketOutput, TicketStatusUpdate
from app.services.ticket_service import TicketService
from app.services.ml_model import TicketClassifier
from app.core.config import settings

router = APIRouter(prefix="/tickets", tags=["Tickets"])

_classifier: TicketClassifier | None = None

def get_classifier() -> TicketClassifier:
    global _classifier
    if _classifier is None:
        _classifier = TicketClassifier(settings.MODEL_PATH)
        _classifier.load()
    return _classifier

@router.post("", response_model=TicketOutput)
def create_ticket(payload: TicketInput, db: Session = Depends(get_db)):
    service = TicketService(db, get_classifier())
    return service.create_ticket(payload.title, payload.description)

@router.get("", response_model=list[TicketOutput])
def list_tickets(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    service = TicketService(db, get_classifier())
    return service.list_tickets(limit=limit, offset=offset)

@router.get("/{ticket_id}", response_model=TicketOutput)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    service = TicketService(db, get_classifier())
    ticket = service.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.patch("/{ticket_id}/status", response_model=TicketOutput)
def update_status(ticket_id: int, payload: TicketStatusUpdate, db: Session = Depends(get_db)):
    service = TicketService(db, get_classifier())
    updated = service.update_status(ticket_id, payload.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated
