import enum
import sqlalchemy as sa

DEFAULT_DB_NAME = 'greed.db'
MSG_CONSTRAINT = 2000 - len("```ansi\n\n```")
MSG_WIDTH_CONSTRAINT = 70

class TradeStatus(enum.IntEnum):
   open = 0,
   close = 1,

class CrudStatus(enum.IntEnum):
   added = 0,
   modified = 1,
   deleted = 2,
   not_found = 3,

class GameMode(enum.IntEnum):
   normal = 0,
   hardcore = 1,

class FieldType(enum.IntEnum):
   number = 0,
   float  = 1,
   string = 2,
   enum = 4,
   bonus = 5,

class UserRole(enum.IntEnum):
   banned = 0,
   nobody = 1,
   admin = 2,
   super_admin = 3,

class ItemTier(enum.IntEnum):
   normal = 0,
   exceptional = 1,
   elite = 2,

class ItemRarity(enum.IntEnum):
   normal = 0,
   magic = 1,
   rare = 2,
   set = 3,
   unique = 4,
   legendary = 5,

class ItemArmorType(enum.IntEnum):
   cloth = 0,
   leather = 1,
   mail = 2,
   plate = 3,

DEFAULT_USER_CONFIG = {
   'game_mode'     : GameMode.normal,
}

def color_to_str(color):
   res = ','.join([str(x) for x in color])
   return res

SERVER_DEFAULT_USER_CONFIG = {
   'game_mode': GameMode.normal.value,
}