from discord.ext.commands import Converter, BadArgument

from .bot_util import init_ctx
from ..reaction import Reactions

from ..const import FieldType

# class EnumConverter:
#    enum_cls = None
#    enum_hash = {}

#    def __init__(self, *args, **kwargs):
#       for item in self.enum_cls:
#          self.enum_hash[item.name] = item
      
#    def get_enum_value_from_str(self, val):
#       val = val.lower()
#       return self.enum_hash.get(val, None)
   
#    def convert(self, ctx, val):
#       init_ctx(ctx)
#       enum_val = self.get_enum_value_from_str(val)
#       if enum_val is None:
#          ctx.report.reaction.add(Reactions.fail)
#          msg = 'value {} is unknown, possible values: {}'.format(
#             val,
#             list(self.enum_hash.keys())
#          )
#          ctx.report.err.add(msg)
#          return None
      
#       return enum_val
   
# class FieldTypeConverter(EnumConverter):
#    enum_cls = FieldType