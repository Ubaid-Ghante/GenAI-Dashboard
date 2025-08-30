from typing import Dict
import uuid
from sqlalchemy import Column, String, UniqueConstraint, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", "organization_id", name="uq_email_org"),
        Index("idx_users_org_id", "organization_id"),
        Index("idx_users_email", "email"),
        {"schema": "public"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    context = Column(JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    organization_id = Column(UUID(as_uuid=True), ForeignKey("public.organizations.id", ondelete="CASCADE"), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    email_verified = Column(Boolean, default=False)

    organization = relationship("Organization", backref="users")

    def to_dict(self) -> Dict:
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "context": self.context,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "organization_id": str(self.organization_id),
            "is_active": self.is_active,
            "role": self.role,
            "email_verified": self.email_verified,
            "organization": self.organization.to_dict() if self.organization else None,
        }
