from typing import Dict
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Index, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("idx_transactions_session_id", "session_id"),
        Index("idx_transactions_org_id", "organization_id"),
        Index("idx_transactions_user_id", "user_id"),
        {"schema": "chatbot"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    session_id = Column(UUID(as_uuid=True), ForeignKey("chatbot.sessions.id", ondelete="CASCADE"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("public.organizations.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)

    user_feedback = Column(String, nullable=True)
    positive_feedback = Column(Boolean, default=None)

    graph_state = Column(JSONB, default=dict)

    logs = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expiry_at = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    session = relationship("Session", backref="transactions")
    user = relationship("User", backref="transactions")
    organization = relationship("Organization", backref="transactions")

    def to_dict(self) -> Dict:
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "organization_id": str(self.organization_id),
            "user_id": str(self.user_id),
            "user_feedback": self.user_feedback,
            "positive_feedback": self.positive_feedback,
            "graph_state": self.graph_state,
            "logs": self.logs,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expiry_at": self.expiry_at.isoformat() if self.expiry_at else None,
            "organization": self.organization.to_dict() if self.organization else None,
            "user": self.user.to_dict() if self.user else None,
            "session": self.session.to_dict() if self.session else None,
        }
