from typing import List, Optional
from sqlalchemy.orm import Session
import uuid
from src.models.database.database_connection import DatabaseConnection

class DatabaseConnectionRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_by_id(self, db_conn_id: uuid.UUID) -> Optional[DatabaseConnection]:
		return self.db.query(DatabaseConnection).filter(DatabaseConnection.id == db_conn_id).first()

	def get_by_name(self, name: str, organization_id: uuid.UUID = None, user_id: uuid.UUID = None) -> Optional[DatabaseConnection]:
		query = self.db.query(DatabaseConnection).filter(DatabaseConnection.name == name)
		if organization_id:
			query = query.filter(DatabaseConnection.organization_id == organization_id)
		if user_id:
			query = query.filter(DatabaseConnection.user_id == user_id)
		return query.first()

	def create(self, name: str, type: str, config: dict, organization_id: uuid.UUID, user_id: uuid.UUID, is_active: bool = True) -> DatabaseConnection:
		db_conn = DatabaseConnection(
			name=name,
			type=type,
			config=config,
			organization_id=organization_id,
			user_id=user_id,
			is_active=is_active
		)
		self.db.add(db_conn)
		self.db.flush()
		return db_conn

	def update(self, db_conn_id: uuid.UUID, **kwargs) -> Optional[DatabaseConnection]:
		db_conn = self.get_by_id(db_conn_id)
		if not db_conn:
			return None
		for key, value in kwargs.items():
			if hasattr(db_conn, key):
				setattr(db_conn, key, value)
		self.db.flush()
		return db_conn

	def delete(self, db_conn_id: uuid.UUID) -> bool:
		db_conn = self.get_by_id(db_conn_id)
		if not db_conn:
			return False
		self.db.delete(db_conn)
		return True

	def get_all(self) -> List[DatabaseConnection]:
		return self.db.query(DatabaseConnection).all()

	def get_all_for_organization(self, organization_id: uuid.UUID) -> List[DatabaseConnection]:
		return self.db.query(DatabaseConnection).filter(DatabaseConnection.organization_id == organization_id).all()

	def get_all_for_user(self, user_id: uuid.UUID) -> List[DatabaseConnection]:
		return self.db.query(DatabaseConnection).filter(DatabaseConnection.user_id == user_id).all()
