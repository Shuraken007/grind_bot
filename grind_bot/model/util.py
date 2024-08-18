from sqlalchemy import Integer, TypeDecorator

class EnumValueConverter(TypeDecorator):
   impl = Integer
   cache_ok = True

   def __init__(self, enum_cls, *args, **kwargs):
      self.enum_cls = enum_cls
      super(EnumValueConverter, self).__init__(*args, **kwargs)

   def process_bind_param(self, enum_value, dialect):
      if enum_value is None:
         return None
      return enum_value.value

   def process_result_value(self, value, dialect):
      if value is None:
         return None
      return self.enum_cls(value)