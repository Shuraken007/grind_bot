from .bot.bot_util import init_ctx
from .reaction import Reactions

from .const import FieldType, ItemTier, ItemRarity, ItemArmorType

class StraitConverter:
   hash = {}
   
   def __init__(self, hash):
      for k, v in hash.items():
         self.hash[k.lower()] = v

   def convert(self, ctx, val):
      init_ctx(ctx)
      if val.lower() not in self.hash:
         ctx.report.reaction.add(Reactions.fail)
         msg = 'value {} is unknown, possible values: {}'.format(
            val,
            list(self.hash.keys())
         )
         ctx.report.err.add(msg)
         return None, False
      
      return self.hash[val.lower()], True
   
class EnumConverter:
   enum_cls = None
   enum_hash = {}

   def __init__(self, enum_cls):
      self.enum_cls = enum_cls
      for item in self.enum_cls:
         self.enum_hash[item.name] = item
      
   def get_enum_value_from_str(self, val):
      val = val.lower()
      return self.enum_hash.get(val, None)
   
   def convert(self, ctx, val, err_debug = True):
      init_ctx(ctx)
      enum_val = self.get_enum_value_from_str(val)
      if enum_val is None:
         if not err_debug:
            return None, False
         ctx.report.reaction.add(Reactions.fail)
         msg = 'value {} is unknown, possible values: {}'.format(
            val,
            list(self.enum_hash.keys())
         )
         ctx.report.err.add(msg)
         return None, False
      
      return enum_val, True
   
FieldTypeConverter = EnumConverter(FieldType)
ItemTierConverter = EnumConverter(ItemTier)
ItemRarityConverter = EnumConverter(ItemRarity)
ItemArmorTypeConverter = EnumConverter(ItemArmorType)
BoolConverter = StraitConverter({'True': True, 'False': False})