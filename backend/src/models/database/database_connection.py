from typing import Dict
import uuid
from sqlalchemy import Column, String, UniqueConstraint, DateTime, Boolean, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class DatabaseConnection(Base):
    __tablename__ = "database_conns"
    __table_args__ = (
        UniqueConstraint("name", "organization_id", "user_id", name="uq_dbconns_name_org_user"),
        Index("idx_dbconns_org_id", "organization_id"),
        Index("idx_dbconns_user_id", "user_id"),
        {"schema": "public"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)   # Connection name/alias
    type = Column(String, nullable=False)   # e.g., postgres, mysql, etc.
    config = Column(JSONB, default=dict)    # store db host, port, creds in encrypted form
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("public.organizations.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("public.users.id", ondelete="CASCADE"),
        nullable=False
    )

    is_active = Column(Boolean, default=True)

    # Relationships
    organization = relationship("Organization", backref="database_conns")
    user = relationship("User", backref="database_conns")

    def to_dict(self) -> Dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.type,
            "config": self.config,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "organization_id": str(self.organization_id),
            "user_id": str(self.user_id),
            "is_active": self.is_active,
            "organization": self.organization.to_dict() if self.organization else None,
            "user": self.user.to_dict() if self.user else None,
        }
