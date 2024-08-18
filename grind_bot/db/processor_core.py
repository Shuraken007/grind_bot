### Feature One ###

# This class helps to not write each time:
# with self.engine.Session as s():
#    ....
#    s.commit()

# instead use decorator

# class A(DbProcessorCore):
#   @with_session
#   def some_db_request(self):

# Also it's possible to call lot of functions in one session:
# just call start_session / end_session to not auto open/close

### Feature Two ###
# making work with adding / removing items easier

from sqlalchemy.inspection import inspect
from ..const import CrudStatus

class PrimaryKeyError(Exception):
   pass

class FilterNotNullError(Exception):
   pass

def with_session(f):
   def wrapper(self, *args, **kwargs):
      if self.is_session_invoked_outer:
         return f(self, *args, **kwargs)
      
      self._start_session()
      result = f(self, *args, **kwargs)
      self._end_session()
   
      return result
   
   return wrapper

class DbProcessorCore:
   def __init__(self, engine):
      self.engine = engine
      self.is_session_invoked_outer = False
      self._is_opened = False
      self.s = None

   def _start_session(self):
      if self._is_opened:
         return
      
      self._is_opened = True
      self.s = self.engine.Session()

   def _end_session(self):
      if not self._is_opened:
         return
      self._is_opened = False
      if self.s.new or self.s.dirty or self.s.deleted:
         self.s.commit()
      self.s.close()

   def start_session(self):
      self._start_session()
      self.is_session_invoked_outer = True

   def end_session(self):
      self._end_session()
      self.is_session_invoked_outer = False

   def get_column_names(self, model, exclude=[]):
      columns = []
      for c_attr in model.__table__.columns:
         col_name = c_attr.name
         if col_name in exclude:
            continue
         columns.append(col_name)
      return columns

   def get_primary_keys(self, model):
      return [key.name for key in inspect(model).primary_key]
   
   def get_primary_keys_as_filters(self, model, hash, should_all_pk_exists=True):
      filters = {}
      for pk in self.get_primary_keys(model):
         if pk not in hash:
            if should_all_pk_exists:
               msg = "expected primary key {} for model {}".format(
                  pk, model.__tablename__
               )
               raise PrimaryKeyError(msg)
            continue
         filters[pk] = hash[pk]

      return filters
   
   def get_not_primary_keys_as_filters(self, model, hash, should_one_key_exists=True):
      filters = {}
      pk = self.get_primary_keys(model)
      for key in hash:
         if key in pk:
            continue
         filters[key] = hash[key]

      if len(filters) == 0 and should_one_key_exists:
         msg = "expected alt least one key for model {}".format(
            model.__tablename__
         )
         raise FilterNotNullError(msg)         

      return filters
   
   def get_all_objects(self, model):
      return self.s.query(model).all()
   
   def get_obj(self, model, hash, should_all_pk_exists=True):
      filters = self.get_primary_keys_as_filters(model, hash, should_all_pk_exists)
      item = self.s.query(model).filter_by(**filters).first()
      return item
   
   def get_obj_field(self, model, hash, field, should_all_pk_exists=True):
      filters = self.get_primary_keys_as_filters(model, hash, should_all_pk_exists)
      item = self.s.query(model).filter_by(**filters).first()
      if item is None:
         return None
      
      return getattr(item, field)
   
   def get_obj_or_create(self, model, hash, should_all_pk_exists = True):
      filters = self.get_primary_keys_as_filters(model, hash, should_all_pk_exists)
      item = self.s.query(model).filter_by(**filters).first()
      if item is None:
         item = model(**filters)
      return item
   
   def add_obj(self, model, hash, should_all_pk_exists=True):
      # run function to check if all primary keys in hash
      self.get_primary_keys_as_filters(model, hash, should_all_pk_exists)
      item = model(**hash)
      self.s.add(item)

   def add_or_modify_obj(self, model, hash, default_hash=None, should_all_pk_exists = True, should_one_key_exists=True):
      filters = self.get_primary_keys_as_filters(model, hash, should_all_pk_exists)
      item = self.s.query(model).filter_by(**filters).first()
      status = CrudStatus.modified

      if item is None:
         init_hash = hash
         if default_hash:
            init_hash = default_hash | filters
         item = model(**init_hash)
         status = CrudStatus.added

      not_pk_filter = self.get_not_primary_keys_as_filters(model, hash, should_one_key_exists)
      for k, v in not_pk_filter.items():
         setattr(item, k, v)
      
      self.s.add(item)
      return status

   def delete_obj(self, model, hash, should_all_pk_exists=True, should_item_exist=True):
      item = self.get_obj(model, hash, should_all_pk_exists)
      status = None
      if item is None:
         status = CrudStatus.not_found
      else:
         self.s.delete(item)
         status = CrudStatus.deleted
         
      return status