from ..const import DEFAULT_USER_CONFIG
from ..reaction import Reactions
import prettytable

class Config:
   def __init__(self, db_processor):
      self.db_processor = db_processor

   def set(self, user, field, value, report):
      self.db_processor.set_user_config(user.id, {field: value})
      report.reaction.add(Reactions.ok)

   def reset(self, user, report):
      user_config = self.db_processor.get_user_config(user.id)
      default_config = {**DEFAULT_USER_CONFIG}

      default_config['game_mode'] = user_config.game_mode
      self.db_processor.set_user_config(user.id, default_config)
      report.reaction.add(Reactions.ok)

   def delete(self, user, report):
      self.db_processor.delete_user_config(user.id)
      report.reaction.add(Reactions.ok)

   def show(self, user, report):
      user_config = self.db_processor.get_user_config(user.id)
      if user_config is None:
         report.msg.add(f'no config settings')
         return

      keys = sorted(DEFAULT_USER_CONFIG.keys())

      tabl1 = prettytable.PrettyTable(['Main', 'Settings'])
      for key in keys:
         value = getattr(user_config, key)

         if value is None:
            value = 'None'

         tabl1.add_row([key, value])
      
      for t in [tabl1]:
         msg = t.get_string()
         msg_arr = msg.split('\n')
         report.msg.add(msg_arr)         

   def copy(self, copy_from, copy_to, report):
      user_config = self.db_processor.get_user_config(copy_from.id)
      if user_config is None:
         report.msg.add(f'user to copy from have not config')
         report.reaction.add(Reactions.fail)
         return

      new_config = {}
      for key in DEFAULT_USER_CONFIG.keys():
         if key == 'game_mode':
            continue
         value = getattr(user_config, key)
         new_config[key] = value

      self.db_processor.set_user_config(copy_to.id, new_config)
      report.reaction.add(Reactions.ok)