import re, regex

from .const import FieldType, GameMode
from .reaction import Reactions as r
from .bot.bot_util import strict_channels_f, strict_users_f
from .const import UserRole as ur

def parse_msg(ctx, bot):   
   arr = ctx.message.content.split("\n")
   i = 1

   # map_type = bot.controller.detect_user_map_type(ctx.message.author, ctx, with_error = False)

   for e in arr:
      ctx.report.set_key(f'line {i}')
      i += 1
      # if match := MATCH_MAP.match(e):
         # map_type_alias = match.group(1)
         # map_type, is_new_version = validate_map_type(map_type_alias, ctx)
         # is_bug_converter = True
         # if not map_type:
         #    return
         # bot.controller.config.set(ctx.message.author, 'map_type', map_type, ctx.report)
      # else:
      #    ctx.report.log.add({'error': f'not match'})