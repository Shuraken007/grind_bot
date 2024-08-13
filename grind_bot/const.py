import enum
import sqlalchemy as sa

DEFAULT_DB_NAME = 'greed.db'
MSG_CONSTRAINT = 2000 - len("```ansi\n\n```")

class GameMode(enum.IntEnum):
   normal = 0,
   hardcore = 1,

class FieldType(enum.IntEnum):
   number = 0,
   float  = 1,
   string = 2,

class UserRole(enum.IntEnum):
   banned = 0,
   nobody = 1,
   admin = 2,
   super_admin = 3,

   @classmethod
   def has_value(cls, value):
      return value in cls._value2member_map_ 

   @classmethod
   def next(cls, ct):
      v = ct.value + 1
      if not cls.has_value(v):
         return ct      
      return cls(v)

   @classmethod
   def prev(cls, ct):
      v = ct.value - 1
      if not cls.has_value(v):
         return ct
      return cls(v)

DEFAULT_USER_CONFIG = {
   'game_mode'     : GameMode.normal,
}

def color_to_str(color):
   res = ','.join([str(x) for x in color])
   return res

SERVER_DEFAULT_USER_CONFIG = {
   'game_mode': GameMode.normal.value,
}