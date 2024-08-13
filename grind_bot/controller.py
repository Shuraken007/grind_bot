from collections import OrderedDict

# from .const import 
from .reaction import Reactions as r
from .controller_.role import Role
from .controller_.config import Config

class Controller:
   def __init__(self, db_processor, db_processor_re, admin_id):
      self.db_processor = db_processor
      self.db_processor_re = db_processor_re
      self.view = {}
      self.user_roles = {}

      self.role = Role(db_processor, admin_id)
      self.config = Config(db_processor)

   def reload_db(self, db_processor_re):
      self.db_processor_re = db_processor_re

#    Role Functions
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