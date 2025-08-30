import traceback

class RelationalDatabaseClient:
    def __init__(self, database: str, url: str, key: str, **kwargs):
        self.client = None
        self.url = url
        self.key = key
        self.database_type = database.lower()
        
        if self.database_type.lower() == "postgres":
            self.adapter = self.SQLAlchemyAdapter(self.url, **kwargs)
        else:
            raise ValueError(f"Unsupported vectorstore type: {self.database_type}")

    def get_client(self):
        return self.adapter.get_client()
    
    def run_transaction(self, func, *args, **kwargs):
        return self.adapter.run_transaction(func, *args, **kwargs)

    def ping(self):
        return self.adapter.ping()
        
    class SQLAlchemyAdapter:
        def __init__(self, url: str = None, **kwargs):
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker, scoped_session
            
            self.url = url
            self.kwargs = kwargs

            engine = create_engine(self.url, pool_size=20, pool_timeout=60, pool_recycle=299, isolation_level="READ COMMITTED")

            session_factory = sessionmaker(bind=engine)
            self.session = scoped_session(session_factory)
        
        def get_client(self):
            return self.session()
        
        def ping(self):
            session = None
            try:
                session = self.get_client()
                session.execute('SELECT 1')
                return True
            except Exception:
                return False
            finally:
                if session is not None:
                    session.close()
            
        def run_transaction(self, func, *args, **kwargs):
            db = self.get_client()
            close_db = True
            try:
                result = func(db, *args, **kwargs)
            except Exception as e:
                result = {"payload": traceback.format_exc()}
                if close_db:
                    db.rollback()
            finally:
                if close_db:
                    db.commit()
                    db.flush()
                    db.close()

            return result