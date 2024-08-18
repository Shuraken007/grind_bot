from ..const import FieldType
from collections import OrderedDict
from .. import pretty_table_utils

class DbRender:
   def __init__(self, db_processor, db_processor_re):
      self.db_processor = db_processor
      self.db_processor_re = db_processor_re

   def reload_db(self, db_processor_re):
      self.db_processor_re = db_processor_re

   def get_known_fields_hash(self):
      known_fields = self.db_processor.get_known_fields()
      hash = {}
      for known_field in known_fields:
         hash[known_field.full_name.lower()] = known_field
         hash[known_field.name] = known_field
      return hash
   
   def db_names_to_full(self, db_names, known_fields):
      full_names = []
      for db_name in db_names:
         full_name = db_name
         if db_name in known_fields:
            full_name = known_fields[db_name].full_name
         full_names.append(full_name)
      return full_names
   
   def get_item_value(self, item, key, known_fields):
      val = getattr(item, key)
      if val is None:
         return "-"
      
      if key in known_fields:
         known_field = known_fields[key]
         if known_field.type == FieldType.enum:
            val = val.name
         elif known_field.is_pct:
            val = "{}%".format(str(val))
      return str(val)

   def get_bonus_name_value(self, item_bonus, known_fields):
      db_name = item_bonus.name
      str_value = item_bonus.str_value
      num_value = item_bonus.num_value      

      bonus_spec = known_fields[db_name]
      full_name = bonus_spec.full_name
      is_pct = bonus_spec.is_pct

      num_value = str(num_value)
      if is_pct:
         num_value += "%"

      title = f"{full_name}: {str_value}"
      if full_name == "talent":
         title = f"{str_value}"

      return title, num_value

   def get_bonuses_by_itemid(self, items, known_fields):
      item_bonuses_by_id = {}
      unique_bonuses_names = OrderedDict()
      for item in items:
         bonuses = self.db_processor_re.get_bonuses_by_item(item.id)

         converted_bonuses = {}
         for bonus in bonuses:
            full_name, value = self.get_bonus_name_value(bonus, known_fields)
            converted_bonuses[full_name] = value
            unique_bonuses_names[full_name] = True
         item_bonuses_by_id[item.id] = converted_bonuses
      unique_bonuses_names = list(unique_bonuses_names.keys())
      return item_bonuses_by_id, unique_bonuses_names

   def get_bonuses(self, items, known_fields):
      item_bonuses_by_id, unique_bonuses_names = self.get_bonuses_by_itemid(items, known_fields)
      arr_of_rows = []
      for item in items:
         row = []
         for bonus_name in unique_bonuses_names:
            bonus_config = item_bonuses_by_id.get(item.id, {})
            bonus_value = bonus_config.get(bonus_name, '-')
            row.append(bonus_value)

         arr_of_rows.append(row)
      return unique_bonuses_names, arr_of_rows

   def report(self, items, ctx):
      if len(items) == 0:
         ctx.report.msg.add("You haven't items, add them with !item_add !ia")

      all_col_names = self.db_processor.get_column_names(self.db_processor_re.engine.m.Item, exclude=['id', 'time', 'user_id'])
      not_null_col_names = pretty_table_utils.get_not_null_columns(items, all_col_names)
      known_fields = self.get_known_fields_hash()      
      full_names = self.db_names_to_full(not_null_col_names, known_fields)
      not_null_col_names.insert(0, 'id')
      full_names.insert(0, 'Id')

      unique_bonuses_names, bonus_arr_of_rows = self.get_bonuses(items, known_fields)
      title = full_names + unique_bonuses_names

      row_arr = []
      i = 0
      for item in items:
         arr = []
         for db_name in not_null_col_names:
            val = self.get_item_value(item, db_name, known_fields)
            arr.append(val)
         arr += bonus_arr_of_rows[i]
         row_arr.append(arr)
         i += 1

      pretty_table_utils.report_table(ctx, title, row_arr, is_inverted=True)