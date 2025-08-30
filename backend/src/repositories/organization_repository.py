from typing import List, Optional
from sqlalchemy.orm import Session
import uuid
from src.models.database.organization import Organization

class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, organization_id: uuid.UUID) -> Optional[Organization]:
        return self.db.query(Organization).filter(Organization.id == organization_id).first()

    def get_by_name(self, name: str) -> Optional[Organization]:
        return self.db.query(Organization).filter(Organization.name == name).first()

    def create(self, name: str, context: dict = None) -> Organization:
        organization = Organization(
            name=name,
            context=context or {}
        )
        self.db.add(organization)
        self.db.flush()
        return organization

    def update(self, organization_id: uuid.UUID, **kwargs) -> Optional[Organization]:
        organization = self.get_by_id(organization_id)
        if not organization:
            return None
        for key, value in kwargs.items():
            if hasattr(organization, key):
                setattr(organization, key, value)
        self.db.flush()
        return organization

    def delete(self, organization_id: uuid.UUID) -> bool:
        organization = self.get_by_id(organization_id)
        if not organization:
            return False
        self.db.delete(organization)
        return True

    def get_all(self) -> List[Organization]:
        return self.db.query(Organization).all()