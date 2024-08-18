from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as sa
from sqlalchemy import Integer, Column, DateTime, BigInteger, TypeDecorator, \
                        Boolean, String, Float, UniqueConstraint, Identity, \
                        ForeignKeyConstraint, ForeignKey
from datetime import datetime, timezone
from .util import EnumValueConverter

from ..const import ItemTier, ItemRarity, ItemArmorType ,\
         FieldType as ft, TradeStatus


ItemTierValue = EnumValueConverter(ItemTier)
ItemRarityValue = EnumValueConverter(ItemRarity)
ItemArmorTypeValue = EnumValueConverter(ItemArmorType)
TradeStatusValue = EnumValueConverter(TradeStatus)

class Models:
   def __init__(self, Base, Item, Bonus, Trade):
      self.Base       = Base
      self.Item       = Item
      self.Bonus      = Bonus
      self.Trade      = Trade
      
def get_table_names():
   table_names = {
      'Item': 'item',
      'Bonus': 'bonus',
      'Trade': 'trade',
   }
   return table_names

map_known_field_type_to_sa_type = {
   ft.number: Integer,
   ft.float : Float,
   ft.string: String(255),
}

def generate_column_from_known_field(field_name, field_type):
   return Column(
      field_name,
      map_known_field_type_to_sa_type[field_type],
      nullable=True
   )

def get_columns_by_known_fields(known_fields_hash, exclude):
   columns = []
   for known_field in known_fields_hash:
      if known_field.type is ft.bonus:
         continue
      if known_field.name in exclude:
         continue
      col = generate_column_from_known_field(known_field.name, known_field.type)
      columns.append(col)
   return columns

def generate_models(table_names, db_processor_preload):

   class Base(DeclarativeBase):
      pass

   known_fields = db_processor_preload.get_known_fields()
   known_columns = get_columns_by_known_fields(known_fields, [ 'name','type','tier','rarity','armor_type'])

   class Item(Base):
      id = Column(Integer, primary_key=True, server_default=Identity(start=1, cycle=True))
      name = Column(String(255))
      type = Column(String(255))
      tier = Column(ItemTierValue)
      rarity = Column(ItemRarityValue)
      armor_type = Column(ItemArmorTypeValue)
      user_id   = Column(BigInteger)
      time      = Column(DateTime(timezone=True))
      __tablename__ = table_names['Item']
      __table_args__ = tuple(known_columns)

   class Trade(Base):
      __tablename__ = table_names['Trade']

      id = Column(Integer, primary_key=True, server_default=Identity(start=1, cycle=True))
      status = Column(TradeStatusValue, default = TradeStatus.open)
      
      item_id   = Column(BigInteger, primary_key=True)
      price = Column(Integer)
      user_id   = Column(BigInteger)
      note = Column(String(500))

      item_fk  = ForeignKeyConstraint(
         [item_id], [Item.id], 
         ondelete = 'CASCADE', 
         onupdate = 'CASCADE',
         name = 'item_fk',
      )

   class Bonus(Base):
      __tablename__ = table_names['Bonus']
      
      name      = Column(String(255), primary_key=True)
      str_value = Column(String(255), primary_key=True)
      num_value = Column(Integer)
      item_id   = Column(BigInteger, primary_key=True)

      item_fk  = ForeignKeyConstraint(
         [item_id], [Item.id], 
         ondelete = 'CASCADE', 
         onupdate = 'CASCADE',
         name = 'item_fk',
      )

   return Models(Base, Item, Bonus, Trade)
