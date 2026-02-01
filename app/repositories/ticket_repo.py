from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.ticket import Ticket

class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, ticket: Ticket) -> Ticket:
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def get(self, ticket_id: int) -> Ticket | None:
        stmt = select(Ticket).where(Ticket.id == ticket_id)
        return self.db.execute(stmt).scalars().first()

    def list(self, limit: int = 50, offset: int = 0) -> list[Ticket]:
        stmt = select(Ticket).order_by(Ticket.id.desc()).limit(limit).offset(offset)
        return list(self.db.execute(stmt).scalars().all())

    def update_status(self, ticket: Ticket, status: str) -> Ticket:
        ticket.status = status
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
