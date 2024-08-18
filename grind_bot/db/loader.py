import sqlalchemy as sa
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.inspection import inspect
from sqlite3 import Connection as SQLite3Connection

def get_engine(db_connection_str, is_debug):
   echo = is_debug
   engine = sa.create_engine(db_connection_str, echo = echo)
   print(f'created engine {engine.url}')
   if not database_exists(engine.url): create_database(engine.url)
   return engine

@sa.event.listens_for(sa.engine.Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

class EngineLoader:
   def __init__(self, models, db_connection_str, is_debug = False):
      self.m = models
      self.engine = get_engine(db_connection_str, is_debug)

      self.m.Base.metadata.create_all(self.engine)

      self.Session = self.get_session()

   def get_session(self):
      Session = sa.orm.sessionmaker()
      Session.configure(bind=self.engine)
      return Session

   def drop_tables(self):
      self.m.Base.metadata.drop_all(bind = self.engine)