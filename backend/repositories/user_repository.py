from typing import List
from sqlalchemy.orm import Session
from backend.models.user import User
import uuid

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: uuid.UUID):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str, organization_id: uuid.UUID = None):
        query = self.db.query(User).filter(User.email == email)
        if organization_id:
            query = query.filter(User.organization_id == organization_id)
        return query.first()

    def create(self, email: str, name: str, organization_id: uuid.UUID, password_hash: str, context=None, role="user", is_active=True, email_verified=False):
        user = User(
            email=email,
            name=name,
            organization_id=organization_id,
            password_hash=password_hash,
            context=context,
            role=role,
            is_active=is_active,
            email_verified=email_verified
        )
        self.db.add(user)
        self.db.flush()
        return user

    def delete(self, user_id: uuid.UUID):
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        return True

    def update(self, user_id: uuid.UUID, **kwargs):
        user = self.get_by_id(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.db.flush()
        return user

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

    def get_all_in_org(self, organization_id: uuid.UUID) -> List[User]:
        return self.db.query(User).filter(User.organization_id == organization_id).all()

    def search_by_name(self, query: str, organization_id: uuid.UUID = None) -> List[User]:
        response = self.db.query(User).filter(User.name.ilike(f"%{query}%"))
        if organization_id:
            response = response.filter(User.organization_id == organization_id)
        return response.all()