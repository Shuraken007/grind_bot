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
from ..util import text, number

class Trade:
   def __init__(self, db_processor, db_processor_re, admin_id):
      self.db_processor = db_processor
      self.db_processor_re = db_processor_re
      self.admin_id = admin_id
      self.render = DbRender(db_processor, db_processor_re)

   def reload_db(self, db_processor_re):
      self.db_processor_re = db_processor_re
      self.render.reload_db(db_processor_re)

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

   def price_to_number(self, val, ctx):
      if type(val) == str and val.lower == 'inf':
         return -1, True
      
      val, is_ok, msg = number.validate_not_negative_integer(val)
      if not is_ok:
         ctx.report.err.add('price ' + msg)
         return val, False
      
      return val, True
   
   def item_to_number(self, val, ctx):
      val, is_ok, msg = number.validate_not_negative_integer(val)
      if not is_ok:
         ctx.report.err.add('item ' + msg)
         return val, False

      item = self.db_processor_re.get_item(val)
      if item is None:
         ctx.report.err.add(f'item {val} not existed')
         return val, False

      return val, True

   def add(self, trade_config_arr, ctx):
      trade = {}
      known_fields = {
         'price': self.price_to_number,
         'item': self.item_to_number,
      }
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