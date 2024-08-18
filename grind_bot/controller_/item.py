# from ..const import UserRole as ur
from ..reaction import Reactions as r
from sqlalchemy.inspection import inspect
from ..db.render import DbRender
import prettytable
import re

from ..const import CrudStatus, FieldType
from .. import pretty_table_utils
from ..db.migrate import TableModifier
from ..utils import get_mock_class_with_attr
from ..util import text

class Item:
   def __init__(self, db_processor, db_processor_re, admin_id):
      self.db_processor = db_processor
      self.db_processor_re = db_processor_re
      self.admin_id = admin_id
      self.render = DbRender(db_processor, db_processor_re)

   def reload_db(self, db_processor_re):
      self.db_processor_re = db_processor_re
      self.render.reload_db(db_processor_re)


   def is_pct(self, val):
      return val.endswith('%')
   
   def to_number(self, val):
      if self.is_pct(val):
         val = val[:-1]
      if '.' in val:
         return float(val)
      else:
         return int(val)

   def is_value_pct_consistent(self, field_name, value, field_spec, ctx):
      is_consistent = True
      if self.is_pct(value) and not field_spec.is_pct:
         msg = "field {} must not be percent {} with '%'".format(field_name, value)
         ctx.report.err.add(msg)
         is_consistent = False
      elif not self.is_pct(value) and field_spec.is_pct:
         msg = "field {} must not be percent {}, without '%'".format(field_name, value)
         ctx.report.err.add(msg)
         is_consistent = False

      return is_consistent

   def add_new_bonus(self, config, known_fields, ctx):
      full_name = config['name']
      known_field = {
         'full_name': full_name,
         'name': text.full_name_to_name(full_name),
         'type': FieldType.bonus,
         'is_pct': self.is_pct(config['num_value']),
      }
      ctx.bot.controller.known_field.add(known_field, ctx)

      # too lazy to make request for known_fields with added bonus again
      # easier to add fake sqlalchemy item
      known_fields[full_name.lower()] = get_mock_class_with_attr(known_field)

   def add_to_bonuses(self, config, bonuses, known_fields, ctx):
      bonus = {}
      name = config['name']
      num_value = config['num_value']
      str_value = config['str_value']

      if name.lower() not in known_fields:
         self.add_new_bonus(config, known_fields, ctx)

      bonus_spec = known_fields[name.lower()]

      if not self.is_value_pct_consistent(name, num_value, bonus_spec, ctx):
         return

      num_value = self.to_number(num_value)
      bonus = {
         'name': text.full_name_to_name(name),
         'str_value': str_value,
         'num_value': num_value,
      }      
      bonuses.append(bonus)

   def add_to_item(self, config, item, known_fields, ctx):
      name = config['field']

      if name.lower() not in known_fields:
         msg = "Can't find field '{}' in table".format(name)
         ctx.report.err.add(msg)
         ctx.report.reaction.add(r.fail)
         return True

      field_spec = known_fields[name.lower()]
      value = config['value']

      if field_spec.type in [FieldType.number, FieldType.float]:
         if not self.is_value_pct_consistent(name, value, field_spec, ctx):
            return True
         value = self.to_number(value)
      
      db_name = field_spec.name
      item[db_name] = value
      return False

   def add(self, known_field_config_arr, ctx):
      item = {}
      bonuses = []
      known_fields = self.render.get_known_fields_hash()
      cannot_find_err_msg = False
      for known_field_config in known_field_config_arr:
         pat_type = known_field_config.pop('pat_type')
         if pat_type in ['bonus', 'talent']:
            self.add_to_bonuses(known_field_config, bonuses, known_fields, ctx)
         else:
            cannot_find_err_msg |= self.add_to_item(known_field_config, item, known_fields, ctx)

      if cannot_find_err_msg:
         ctx.report.err.add('to add new fields send field and screenshot to @Shuraken')

      user_id = ctx.message.author.id
      item['user_id'] = user_id
      item['time'] = ctx.message.created_at
      status = self.db_processor_re.add_item(item)
      if status == CrudStatus.modified:
         ctx.report.msg.add('item already existed, data updated')
         ctx.report.reaction.add(r.user_data_changed)

      added_item = self.db_processor_re.get_last_added_item_by_user(user_id)
      item_id = added_item.id
      for bonus in bonuses:
         bonus['item_id'] = item_id
         self.db_processor_re.add_bonus(bonus)         
      
   def delete(self, field_name, ctx):
      status = self.db_processor.delete_known_field(field_name)
      if status == CrudStatus.deleted:
         self.table_modifier.delete_column(field_name)
         ctx.report.reaction.add(r.ok)
      elif status == CrudStatus.not_found:
         ctx.report.reaction.add(r.fail)
         ctx.report.msg.add(f'field {field_name} not founded')

   def report(self, items, ctx):
      if len(items) == 0:
         ctx.report.msg.add("You haven't items, add them with !item_add !ia")

      self.render.report(items, ctx)