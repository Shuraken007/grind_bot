from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as sa
from sqlalchemy import Integer, Column, DateTime, BigInteger, TypeDecorator, \
                        Boolean, String, Float, UniqueConstraint, Identity, \
                        ForeignKeyConstraint, ForeignKey
from datetime import datetime, timezone

from ..const import GameMode, \
   FieldType as ft

class Models:
   def __init__(self, Base, Item, Bonus):
      self.Base       = Base
      self.Item       = Item
      self.Bonus      = Bonus
      
def get_table_names():
   table_names = {
      'Item': 'item',
      'Bonus': 'bonus',
   }
   return table_names

map_known_field_type_to_sa_type = {
   ft.number: Integer,
   ft.float : Float,
   ft.string: String(255),
}

def get_columns_by_known_fields(known_fields_hash):
   columns = []
   for known_field in known_fields_hash:
      col = Column(
         known_field.name,
         map_known_field_type_to_sa_type[known_field.type],
         nullable=True
      )
      columns.append(col)
   return columns

def generate_models(table_names, db_processor_preload):

   class Base(DeclarativeBase):
      pass

   known_fields = db_processor_preload.get_known_fields()
   known_columns = get_columns_by_known_fields(known_fields)

   class Item(Base):
      __tablename__ = table_names['Item']
      id = Column(BigInteger, primary_key=True, server_default=Identity(start=1, cycle=True))
      __table_args__ = tuple(known_columns)

   class Bonus(Base):
      __tablename__ = table_names['Bonus']
      name      = Column(String(255), primary_key = True)
      str_value = Column(String(255))
      num_value = Column(Integer)
      item_id   = Column(BigInteger)

      item_fk  = ForeignKeyConstraint(
         [item_id], [Item.id], 
         ondelete = 'CASCADE', 
         onupdate = 'CASCADE',
         name = 'item_fk',
      )

   return Models(Base, Item, Bonus)
