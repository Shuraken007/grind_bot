from collections import OrderedDict

# from .const import 
from .reaction import Reactions as r
from .controller_.role import Role
from .controller_.config import Config
from .controller_.known_field import KnownField
from .controller_.item import Item
from .controller_.trade import Trade
from .parser import ItemParser, KnownFieldParser, TradeParser

class Controller:
   def __init__(self, db_processor, db_processor_re, admin_id):
      self.db_processor = db_processor
      self.db_processor_re = db_processor_re
      self.view = {}
      self.user_roles = {}

      self.role = Role(db_processor, admin_id)
      self.config = Config(db_processor)
      self.known_field = KnownField(db_processor, db_processor_re, admin_id)
      self.item = Item(db_processor, db_processor_re, admin_id)
      self.trade = Trade(db_processor, db_processor_re, admin_id)

   def reload_db(self, db_processor_re):
      self.db_processor_re = db_processor_re
      self.known_field.reload_db(db_processor_re)
      self.item.reload_db(db_processor_re)
      self.trade.reload_db(db_processor_re)

#  Role Functions
   def add_user_role(self, user, user_role, ctx):
      self.role.add(user, user_role, ctx)

   def delete_user_role(self, user, ctx):
      self.role.delete(user, ctx)

   async def report_user_roles(self, bot, report):
      await self.role.report(bot, report)

#  Config functions
   def set_config(self, field, value, ctx):
      user = ctx.message.author
      self.config.set(user, field, value, ctx.report)

   def reset_config(self, ctx):
      user = ctx.message.author
      self.config.reset(user, ctx.report)

   def delete_config(self, ctx):
      user = ctx.message.author
      self.config.delete(user, ctx.report)

   def show_config(self, ctx):
      user = ctx.message.author
      self.config.show(user, ctx.report)

   def copy_config(self, user, ctx):
      to = ctx.message.author
      self.config.copy(user, to, ctx.report)

#  Known Field Functions
   def add_known_field(self, ctx):
      known_field_config_arr, is_success = KnownFieldParser.parse_lines(ctx)
      if not is_success:
         return
      
      self.known_field.add(known_field_config_arr, ctx)

   def delete_known_field(self, field_name, ctx):
      self.known_field.delete(field_name, ctx)
      ctx.bot.reload_db()

   async def report_known_fields(self, ctx):
      await self.known_field.report(ctx)

# Item Functions

   def item_add(self, ctx):
      known_field_config_arr, is_success = ItemParser.parse_lines(ctx)
      if not is_success:
         return
      self.item.add(known_field_config_arr, ctx)
      
   def item_edit(self, ctx):
      user = ctx.message.author


   def item_delete(self, ctx):
      user = ctx.message.author


   def item_report(self, ctx, item_id=None):
      user_id = ctx.message.author.id
      items = self.db_processor_re.get_items_by_user(user_id)
      self.item.report(items, ctx)

# Trade Functions

   def trade_add(self, ctx):
      trade_config_arr, is_success = TradeParser.parse_lines(ctx)
      if not is_success:
         return
      self.trade.add(trade_config_arr, ctx)
      
   def trade_edit(self, ctx):
      user = ctx.message.author


   def trade_delete(self, ctx):
      user = ctx.message.author


   def trade_report(self, ctx, trade_id=None):
      user_id = ctx.message.author.id
      trades = self.db_processor_re.get_trades_by_user(user_id)
      self.trade.report(trades, ctx)

