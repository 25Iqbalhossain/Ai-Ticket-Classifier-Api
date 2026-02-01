from sqlalchemy.orm import Session

from app.core.error import APPError
from app.models.ticket import Ticket
from app.repositories.ticket_repo import TicketRepository
from app.services.ml_model import TicketClassifier


class TicketService:
    def __init__(self, db: Session, classifier: TicketClassifier):
        self.repo = TicketRepository(db)
        self.classifier = classifier

    def create_ticket(self, title: str, description: str) -> Ticket:
        category = self.classifier.predict_category(f"{title}\n{description}")
        ticket = Ticket(
            title=title,
            description=description,
            predicted_category=category,
            status="open",
        )
        return self.repo.create(ticket)

    def list_tickets(self, limit: int = 50, offset: int = 0) -> list[Ticket]:
        return self.repo.list(limit=limit, offset=offset)

    def get_ticket(self, ticket_id: int) -> Ticket:
        ticket = self.repo.get(ticket_id)
        if not ticket:
            raise APPError("TICKET_NOT_FOUND", "Ticket not found", 404)
        return ticket

    def update_status(self, ticket_id: int, status: str) -> Ticket:
        ticket = self.repo.get(ticket_id)
        if not ticket:
            raise APPError("TICKET_NOT_FOUND", "Ticket not found", 404)

        # (optional) extra validation
        if status not in ("open", "closed"):
            raise APPError(
                "INVALID_STATUS",
                "Status must be 'open' or 'closed'",
                400,
                details={"allowed": ["open", "closed"], "got": status},
            )

        return self.repo.update_status(ticket, status)
