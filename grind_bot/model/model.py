from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as sa
from sqlalchemy import Column, DateTime, BigInteger, String, Boolean
from datetime import datetime, timezone

from .util import EnumValueConverter
from ..const import FieldType, GameMode, UserRole

FieldTypeValue = EnumValueConverter(FieldType)
GameModeValue = EnumValueConverter(GameMode)
UserRoleValue = EnumValueConverter(UserRole)

class Models:
   def __init__(self, Base, KnownField, UserConfig, Role):
      self.Base = Base
      self.KnownField = KnownField
      self.UserConfig = UserConfig
      self.Role       = Role

def get_table_names():
   table_names = {
      'KnownField': 'known_field',
      'UserConfig': 'user_config',
      'Role'      : 'role',
   }
   return table_names

def generate_models(table_names):
   class Base(DeclarativeBase):
      pass

   class KnownField(Base):
      __tablename__ = table_names['KnownField']
      name   = Column(String(255), primary_key = True)
      full_name = Column(String(255))
      type      = Column(FieldTypeValue)
      is_pct    = Column(Boolean, unique=False, default=False)
      user_id   = Column(BigInteger)
      time      = Column(DateTime(timezone=True))

   class Role(Base): 
      __tablename__ = table_names['Role']
      user_id  = Column(BigInteger, primary_key = True)
      role     = Column(UserRoleValue, default = UserRole.nobody)

   class UserConfig(Base): 
      __tablename__ = table_names['UserConfig']
      user_id       = Column(BigInteger,   primary_key = True)
      game_mode     = Column(GameModeValue, default = GameMode.normal)

   return Models(Base, KnownField, UserConfig, Role)