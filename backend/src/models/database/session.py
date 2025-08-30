from typing import Dict
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Index, desc
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, object_session


from src.models.database.transaction import Transaction
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"
    __table_args__ = (
        Index("idx_sessions_user_id", "user_id"),
        Index("idx_sessions_org_id", "organization_id"),
        Index("idx_sessions_expiry_time", "expiry_time"),
        {"schema": "chatbot"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("public.organizations.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    expiry_time = Column(DateTime(timezone=True), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    context = Column(JSONB, default=dict)
    status = Column(String, nullable=False, default="active")
    device_info = Column(JSONB, default=dict)
    ip_address = Column(String, nullable=True)
        
    # 🔑 Relationships (auto-join)
    user = relationship("User", backref="sessions")
    organization = relationship("Organization", backref="sessions")

    @property
    def graph_state(self):
        db = object_session(self)
        if not db:
            return None
        latest_graph_state = (
            db.query(Transaction.graph_state)
            .filter(Transaction.session_id == self.id)
            .order_by(Transaction.created_at.desc())
            .limit(1)
            .scalar()
        )
        return latest_graph_state if latest_graph_state else None

    def to_dict(self) -> Dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "organization_id": str(self.organization_id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "expiry_time": self.expiry_time.isoformat() if self.expiry_time else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "context": self.context,
            "status": self.status,
            "device_info": self.device_info,
            "graph_state": self.graph_state,
            "organization": self.organization.to_dict() if self.organization else None,
            "user": self.user.to_dict() if self.user else None,
        }