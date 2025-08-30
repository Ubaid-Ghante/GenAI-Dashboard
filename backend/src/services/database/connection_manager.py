
from src.config.logger_config import logger
from src.models.api.api_request import DatabaseConnectionRequest
from src.repositories.db_conn_repository import DatabaseConnectionRepository

from .relational import RelationalDatabaseClient

def create_new_db_conn(request: DatabaseConnectionRequest):
    try:
        db_client = RelationalDatabaseClient(**request.model_dump())
        
        if db_client.ping():
            repo = DatabaseConnectionRepository(db_client.get_client())
            config = request.model_dump()
            config.pop("name", None)
            config.pop("database", None)
            config.pop("organization_id", None)
            config.pop("user_id", None)
            try:
                repo.create(
                    name=request.name,
                    type=request.database,
                    config=config,
                    organization_id=request.organization_id,
                    user_id=request.user_id,
                    is_active=True
                )
            except Exception as e:
                logger.error(f"Error saving DB connection to repository: {e}")
                return {"status": "error", "message": "Failed to save database connection."}

            return {"status": "success", "message": "Database connection established successfully."}
        else:
            return {"status": "failure", "message": "Unable to connect to the database with provided details."}
    except Exception as e:
        logger.error(f"Error creating database Client: {e}")
        return {"status": "error", "message": "An error occurred while creating the database connection."}