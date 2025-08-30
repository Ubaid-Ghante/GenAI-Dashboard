from typing import List, Optional
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from src.models.database.transaction import Transaction

class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, transaction_id: uuid.UUID) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    def create(self, session_id: uuid.UUID, organization_id: uuid.UUID, user_id: uuid.UUID,
               expiry_at: datetime, graph_state: dict = None, logs: str = None) -> Transaction:
        transaction = Transaction(
            session_id=session_id,
            organization_id=organization_id,
            user_id=user_id,
            expiry_at=expiry_at,
            graph_state=graph_state or {},
            logs=logs
        )
        self.db.add(transaction)
        self.db.flush()
        return transaction

    def update(self, transaction_id: uuid.UUID, **kwargs) -> Optional[Transaction]:
        transaction = self.get_by_id(transaction_id)
        if not transaction:
            return None
        for key, value in kwargs.items():
            if hasattr(transaction, key):
                setattr(transaction, key, value)
        self.db.flush()
        return transaction

    def delete(self, transaction_id: uuid.UUID) -> bool:
        transaction = self.get_by_id(transaction_id)
        if not transaction:
            return False
        self.db.delete(transaction)
        return True

    def get_all(self) -> List[Transaction]:
        return self.db.query(Transaction).all()

    def get_all_for_session(self, session_id: uuid.UUID) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.session_id == session_id).all()

    def get_all_for_user(self, user_id: uuid.UUID) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.user_id == user_id).all()

    def get_all_for_organization(self, organization_id: uuid.UUID) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.organization_id == organization_id).all()

    def update_feedback(self, transaction_id: uuid.UUID, user_feedback: str, positive_feedback: bool) -> Optional[Transaction]:
        return self.update(transaction_id, 
                          user_feedback=user_feedback,
                          positive_feedback=positive_feedback)