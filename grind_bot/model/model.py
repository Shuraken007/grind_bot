from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as sa
from sqlalchemy import Integer, Column, DateTime, BigInteger, TypeDecorator, String
from datetime import datetime, timezone

from ..const import FieldType, GameMode, UserRole


class GameModeValue(TypeDecorator):
   impl = Integer
   cache_ok = True

   def process_bind_param(self, game_mode, dialect):
      return game_mode.value

   def process_result_value(self, value, dialect):
      return GameMode(value)
   
class UserRoleValue(TypeDecorator):
   impl = Integer
   cache_ok = True

   def process_bind_param(self, user_role, dialect):
      return user_role.value

   def process_result_value(self, value, dialect):
      return UserRole(value)

class FieldTypeValue(TypeDecorator):
   impl = Integer
   cache_ok = True

   def process_bind_param(self, field_type, dialect):
      return field_type.value

   def process_result_value(self, value, dialect):
      return FieldType(value)
   
class Models:
   def __init__(self, Base, KnownField, KnownBonus, UserConfig, Role):
      self.Base = Base
      self.KnownField = KnownField
      self.KnownBonus = KnownBonus
      self.UserConfig = UserConfig
      self.Role       = Role

def get_table_names():
   table_names = {
      'KnownField': 'known_field',
      'KnownBonus': 'known_bonus',
      'UserConfig': 'user_config',
      'Role'      : 'role',
   }
   return table_names

def generate_models(table_names):
   class Base(DeclarativeBase):
      pass

   class KnownField(Base):
      __tablename__ = table_names['KnownField']
      name = Column(String(255), primary_key = True)
      type = Column(FieldTypeValue)
      user_id    = Column(BigInteger)
      time       = Column(DateTime(timezone=True))

   class Role(Base): 
      __tablename__ = table_names['Role']
      user_id  = Column(BigInteger, primary_key = True)
      role     = Column(UserRoleValue, default = UserRole.nobody)

   class UserConfig(Base): 
      __tablename__ = table_names['UserConfig']
      user_id       = Column(BigInteger,   primary_key = True)
      game_mode     = Column(GameModeValue, default = GameMode.normal)

   class KnownBonus(Base):
      __tablename__ = table_names['KnownBonus']
      name = Column(String(255), primary_key = True)
      user_id    = Column(BigInteger)
      time       = Column(DateTime(timezone=True))

   return Models(Base, KnownField, KnownBonus, UserConfig, Role)