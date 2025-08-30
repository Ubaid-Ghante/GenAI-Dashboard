from typing import List, Optional
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from src.models.database.session import Session

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, session_id: uuid.UUID) -> Optional[Session]:
        return self.db.query(Session).filter(Session.id == session_id).first()

    def create(self, user_id: uuid.UUID, organization_id: uuid.UUID, expiry_time: datetime,
               context: dict = None, status: str = "active", device_info: dict = None,
               ip_address: str = None) -> Session:
        session = Session(
            user_id=user_id,
            organization_id=organization_id,
            expiry_time=expiry_time,
            context=context or {},
            status=status,
            device_info=device_info or {},
            ip_address=ip_address
        )
        self.db.add(session)
        self.db.flush()
        return session

    def update(self, session_id: uuid.UUID, **kwargs) -> Optional[Session]:
        session = self.get_by_id(session_id)
        if not session:
            return None
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        self.db.flush()
        return session

    def delete(self, session_id: uuid.UUID) -> bool:
        session = self.get_by_id(session_id)
        if not session:
            return False
        self.db.delete(session)
        return True

    def get_all(self) -> List[Session]:
        return self.db.query(Session).all()

    def get_all_for_user(self, user_id: uuid.UUID) -> List[Session]:
        return self.db.query(Session).filter(Session.user_id == user_id).all()

    def get_all_for_organization(self, organization_id: uuid.UUID) -> List[Session]:
        return self.db.query(Session).filter(Session.organization_id == organization_id).all()

    def get_active_sessions(self, user_id: uuid.UUID = None) -> List[Session]:
        query = self.db.query(Session).filter(
            Session.status == "active",
            Session.expiry_time > datetime.utcnow()
        )
        if user_id:
            query = query.filter(Session.user_id == user_id)
        return query.all()