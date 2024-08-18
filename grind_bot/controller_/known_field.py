# from ..const import UserRole as ur
from .. import pretty_table_utils

from ..reaction import Reactions as r
from ..const import CrudStatus, FieldType as ft
from ..db.migrate import TableModifier

class KnownField:
   def __init__(self, db_processor, db_processor_re, admin_id):
      self.db_processor = db_processor
      self.db_processor_re = db_processor_re
      self.admin_id = admin_id
      self.table_modifier = TableModifier(db_processor_re.engine, db_processor_re.engine.m.Item)

   def reload_db(self, db_processor_re):
      self.db_processor_re = db_processor_re
      self.table_modifier.reload_db(db_processor_re.engine, db_processor_re.engine.m.Item)

   def add_from_parser(self, known_field_config_arr, ctx):
      hash = {}
      for known_field_config in known_field_config_arr:
         for k, v in known_field_config.items():
            if k == 'pat_type':
               continue
            hash[k] = v      
      self.add(hash, ctx)

   def add(self, hash, ctx):
      hash['user_id'] = ctx.message.author.id
      hash['time'] = ctx.message.created_at
      status = self.db_processor.add_known_field(hash)
      if status == CrudStatus.modified:
         ctx.report.msg.add('field already existed, data updated')
         ctx.report.reaction.add(r.user_data_changed)
      else:
         if hash['type'] != ft.bonus:
            self.table_modifier.add_column(hash['name'], hash['type'])
         ctx.bot.reload_db()
         ctx.report.reaction.add(r.ok)
         msg = "new field {} appeared".format(hash['name'])
         ctx.report.msg.add(msg)

   def delete(self, field_name, ctx):
      known_field = self.db_processor.get_known_field(field_name)
      status = self.db_processor.delete_known_field(field_name)
      if status == CrudStatus.deleted:
         if known_field.type != ft.bonus:
            self.table_modifier.delete_column(field_name)
         ctx.report.reaction.add(r.ok)
      elif status == CrudStatus.not_found:
         ctx.report.reaction.add(r.fail)
         ctx.report.msg.add(f'field {field_name} not founded')

   async def report(self, ctx):
      known_fields = self.db_processor.get_known_fields()
      col_names = self.db_processor.get_column_names(self.db_processor.engine.m.KnownField)
      await pretty_table_utils.convert_db_model_to_table(known_fields, col_names, ctx)