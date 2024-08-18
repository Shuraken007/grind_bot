from discord.ext import commands

from .const import GameMode

game_mode_values = {
   'normal'  : GameMode.normal,
   'n'       : GameMode.normal,
   'hardcore': GameMode.hardcore,
   'h'       : GameMode.hardcore,
   'hard'    : GameMode.hardcore,
}

help = {
   
'addadmin_description': """
   add user with admin role - more commands available
   * check any users reports
   * find liars
   * remove users data
   * ban users for bot

   !addadmin @DearFreeHelper
   !aa @FirstUser @SecondUser
""",
'banadd_description': """
   dreams of any admin - ban hammer, hit them nightmare

   !banadd @SillyDebater
   !ba @SillyDebater @SmartAss5
""",
'deleteban_description': """
   unban somebody

   !bandelete @LuckyFirst
   !ba @BribeGiver3 @JudgeAcquitted2
""",
'deleteadmin_description': """
   delete user from admins
   !admindelete @SmartAss
   !ad @noname1 @noname2
""",
'adminlist_description': """
   check admin names and privilege lvl
""",
'game_mode_descr': commands.parameter(description=list(game_mode_values.keys())),
'known_field_add': """
   add new column to item table
   !known_field_add name type
   known types:
      - number
      - float
      - string
   !kfa fire_resistance number
""",
'known_field_delete': """
   delete column from item table
   !kfd fire_resistance
""",
'known_field_report': """
   report all known columns
   !kfr
""",
'item_add': """
""",
'item_edit': """
""",
'item_delete': """
""",
'item_delete': """
""",
'trade_add': """
""",
'trade_edit': """
""",
'trade_delete': """
""",
'trade_delete': """
""",
}