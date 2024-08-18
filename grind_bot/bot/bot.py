#!python3
import inspect
import discord
from discord.ext import commands, tasks
import os 
import traceback

from .bot_util import init_ctx, MyCommandError, \
                     strict_channels, strict_users, response_by_report
from ..utils import get_mock_class_with_attr, \
                     profile_start, profile_end

from ..db.loader import EngineLoader
from ..db.processor import DbProcessor
from ..model import model
from ..db.processor_reload import DbProcessorReload
from ..model import model_reload

from ..controller import Controller
from ..const import UserRole as ur
from .. import parser
from ..helpo import help
from ..logger import Logger

async def preprocess(ctx):
   init_ctx(ctx)
   if ctx.bot.is_profile:
      profile_start(ctx)
   # ctx.bot.db_processor.start_session()

async def postprocess(ctx):
   if ctx.bot.is_profile and ctx.bot.pr:
      profile_end(ctx)

   await response_by_report(ctx)
   # ctx.bot.db_processor.end_session()

class MyBot(commands.Bot):

   def run(self):
      super(MyBot, self).run(self.config.token)

   def init_db(self):
      table_names = model.get_table_names()
      models = model.generate_models(table_names)
      self.engine = EngineLoader(models, self.config.db_connection_str)
      self.db_processor = DbProcessor(self.config.admin_id, self.engine)

   def init_db_reload(self):
      table_names = model_reload.get_table_names()
      models = model_reload.generate_models(table_names, self.db_processor)
      self.engine_re = EngineLoader(models, self.config.db_connection_str, is_debug=False)
      self.db_processor_re = DbProcessorReload(self.engine_re)

   def add_not_registered_self_commands(self):
      members = inspect.getmembers(self)
      for _, member in members:
         if isinstance(member, commands.Command):
               if member.parent is None:
                  self.add_command(member)      

   def __init__(self, *args, 
                  config = None, initial_extensions = [], 
               **kwargs):
      
      super(MyBot, self).__init__(*args, **kwargs)
      self.help_command = commands.DefaultHelpCommand(
         width=1000, 
         no_category = 'Default',
         command_attrs = {'aliases': ['h']}
      )
      self.config = config

      self.engine = None
      self.db_processor = None
      self.init_db()

      self.engine_re = None
      self.db_processor_re = None
      self.init_db_reload()

      self.controller = Controller(self.db_processor, self.db_processor_re, self.config.admin_id)
      self.logger = Logger('output')

      self.initial_extensions = initial_extensions

      self.is_profile = False
      self.pr = None

      # this part typically solved with decorators like `@bot.event`
      # but it required MyBot instance, which is bad design
      self.on_ready = self.event(self.on_ready)
      self.on_message = self.event(self.on_message)
      self._before_invoke = preprocess
      self._after_invoke = postprocess
      self.add_not_registered_self_commands()

   def reload_db(self):
      self.init_db_reload()
      self.controller.reload_db(self.db_processor_re)

   async def on_command_error(self, ctx, error):
      error_class_name = type(error).__name__
      if not error_class_name in ['CommandInvokeError'] and \
            error_class_name in commands.errors.__all__ or \
            isinstance(error, (MyCommandError)):
         
         await preprocess(ctx)
         if len(str(error)) > 0:
            # trace = traceback.TracebackException.from_exception(error)
            # trace_str = ''.join(trace.format())
            # ctx.report.err.add(trace_str)
            err_msg = f'{error_class_name}: {error}'
            ctx.report.err.add(err_msg)
            ctx.report.log.add({'exception': err_msg})

         await postprocess(ctx)
      else:
         await super().on_command_error(ctx, error)  # вызывает изначальное поведение on_error_message

   # override for help
   # !h user | !h User
   def get_cog(self, name):
      all_keys = self.cogs.keys()
      for k in all_keys:
         if k.lower() == name.lower():
            return super().get_cog(k)

      return super().get_cog(name)

   async def on_ready(self):
      print(f'We have logged in as {self.user}')
      for extension in self.initial_extensions:
         await self.load_extension(extension)

   # async def on_message(self, message):
   #    if message.author == self.user:
   #       return
         
   #    mock_ctx = get_mock_class_with_attr({"channel": message.channel, 'message': message, 'bot': self})
   #    await preprocess(mock_ctx)
      
   #    parser.parse_msg(mock_ctx, self)      
   #    await postprocess(mock_ctx)

   #    await self.process_commands(message)

   async def get_user_name_by_id(self, user_id):
      user_id = int(user_id)
      
      user = self.get_user(user_id)
      if user is None:
         try:
            user = await self.fetch_user(user_id)
         except:
            pass
      if user is None:
         return f'unknown name ({user_id} id)'
      name = user.global_name
      if name is None:
         name = user.name
      if name is None:
         name = str(user_id)
      return name