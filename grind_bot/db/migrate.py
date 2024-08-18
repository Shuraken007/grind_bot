from ..model.model_reload import generate_column_from_known_field
from sqlalchemy import text

class TableModifier:
   engine = None
   table_name = None

   def get_table(self, engine, model):
      self.engine = engine.engine
      self.table_name = model.__tablename__

   def __init__(self, engine, model):
      self.get_table(engine, model)

   def reload_db(self, engine, model):
      self.get_table(engine, model)

   def execute(self, query):
      with self.engine.connect() as conn:
         conn.execute(text(query))      

   def get_add_query(self):
      return 'ALTER TABLE {} ADD COLUMN {} {}'

   def add_column(self, name, type):
      sqlalchemy_col = generate_column_from_known_field(name, type)
      raw_column_type = sqlalchemy_col.type.compile(self.engine.dialect)      

      query = self.get_add_query().format(
         self.table_name,
         name,
         raw_column_type
      )
      self.execute(query)

   def get_delete_query(self):
      return 'ALTER TABLE {} DROP COLUMN {}'

   def delete_column(self, name):
      query = self.get_delete_query().format(
         self.table_name,
         name,
      )
      self.execute(query)