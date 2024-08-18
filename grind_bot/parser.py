import re
from pprint import pprint

from .const import FieldType, GameMode
from .reaction import Reactions as r
from .bot.bot_util import strict_channels_f, strict_users_f
from .const import UserRole as ur
from .converter import FieldTypeConverter, BoolConverter, \
            ItemTierConverter, ItemRarityConverter, ItemArmorTypeConverter
class AbstractClass(Exception):
   pass

class LineParser:
   pattern_hash = {}
   converter_config_arr = {}
   required_fields = []
   substitutions = []
   is_debug = False

   @classmethod
   def parsed_line_to_config(cls, values, pattern_type, ctx):
      raise AbstractClass('parsed_line_to_config must be redefined')

   @classmethod
   def msg_to_arr(cls, msg):
      msg = re.sub(r'![^\s]+', '', msg).strip()
      msg = msg.replace(";", "\n")
      arr = msg.split("\n")
      arr = list(map(str.strip, arr))
      return arr

   @classmethod
   def try_convert(cls, parsed_config, ctx):
      pat_type = parsed_config['pat_type']

      
      is_success_convert = True
      for converter_config in cls.converter_config_arr:
         if converter_config['pat_type'] != pat_type:
            continue
         key = converter_config['key']
         if key != parsed_config['field']:
            continue
      
         converter = converter_config['converter']
         converted_field, is_success = converter.convert(
            ctx, parsed_config['value']
         )
         
         if not is_success:
            is_success_convert = False
         else:
            parsed_config['value'] = converted_field
      
      return is_success_convert

   @classmethod
   def check_required_fields(cls, ctx, match_results):
      is_success = True
      for required_field in cls.required_fields:
         is_founded = False
         for result in match_results:
            if required_field in result:
               is_founded = True
               break
         if not is_founded:
            is_success = False
            error = "expected field {}".format(required_field)
            ctx.report.err.add(error)
            ctx.report.reaction.add(r.fail)

      if len(match_results) == 0:
         ctx.report.err.add('nothing added')
         ctx.report.reaction.add(r.fail)
         is_success = False

      return is_success

   @classmethod
   def parse_lines(cls, ctx):
      msg = ctx.message.content
      arr = cls.msg_to_arr(msg)
      match_results = []
      for item in arr:
         is_parsed = False
         for sub in cls.substitutions:
            item = re.sub(sub[0], sub[1], item, flags=re.I)
         for pat_type, pat in cls.pattern_hash.items():
            if match := pat.match(item):
               is_parsed = True
               founded = list(map(str.strip, match.groups()))
               parsed_arr = cls.parsed_line_to_config(founded, pat_type, ctx)
               for parsed in parsed_arr:
                  is_success = cls.try_convert(parsed, ctx)
                  if is_success:
                     match_results.append(parsed)
               break
         if not is_parsed:
            error = "can't parse line: {}".format(item)
            ctx.report.err.add(error)

      if cls.is_debug:
         pprint(match_results)

      is_success = cls.check_required_fields(ctx, match_results)
      return match_results, is_success
   
any_part = r"[^:]+"
not_number_part = r"[^\d]+"
talent_part = r"[^:]+(?<!all) talents?"
float_num = r"[\d\.]+"
interval_num = r"(\d+)\s*\-\s*(\d+)"
add_num = r"[\+\-][\d%]+"
slot = r"Slots?"

class ItemParser(LineParser):
   substitutions = [
      [r"^\s*Slots:", "Slot:"],
      [r"Damage To", "Damage vs"],
   ]
   pattern_hash = {
      'bonus': re.compile(rf"^\s*({add_num})({any_part}):({any_part})$"),
      'talent': re.compile(rf"^\s*({add_num})({talent_part})$", re.IGNORECASE),
      'plus': re.compile(rf"^\s*({add_num})({any_part})$"),
      'damage': re.compile(rf"^\s*(damage)\s*:\s*{interval_num}\s*$", re.IGNORECASE),
      'prof': re.compile(rf"^\s*(Proficiency)\s*:({any_part})$", re.IGNORECASE),
      'default': re.compile(rf"^\s*({any_part}):({any_part})$"),
      'default1': re.compile(rf"^\s*({not_number_part})\s*(\d+)\s*$"),
      'default2': re.compile(rf"^\s*(\d+)\s*({not_number_part})$"),
   }
   converter_config_arr = [
      {
         'pat_type': 'default',
         'key': 'tier',
         'converter': ItemTierConverter,
      },
      {
         'pat_type': 'default',
         'key': 'rarity',
         'converter': ItemRarityConverter,
      },
      {
         'pat_type': 'prof',
         'key': 'armor_type',
         'converter': ItemArmorTypeConverter,
      },
   ]
   
   is_debug = True

   @classmethod
   def parsed_line_to_config(cls, founded, pat_type, ctx):
      parsed = {
         'pat_type': pat_type,
      }
      if pat_type == 'bonus':
         parsed['name'] = founded[1]
         parsed['str_value'] = founded[2]
         parsed['num_value'] = founded[0]
      elif pat_type == 'talent':
         parsed['name'] = 'talent'
         parsed['str_value'] = founded[1]
         parsed['num_value'] = founded[0]
      elif pat_type in ['plus', 'default2']:
         parsed['field'] = founded[1]
         parsed['value'] = founded[0]
      elif pat_type in ['default', 'default1']:
         parsed['field'] = founded[0]
         parsed['value'] = founded[1]
      elif pat_type == 'damage':
         return [
            {
               'pat_type': pat_type,
               'field': 'damage_min',
               'value': founded[1],
            },
            {
               'pat_type': pat_type,
               'field': 'damage_max',
               'value': founded[2],
            }
         ]
      elif pat_type == 'prof':
         arr = [
            {
               'pat_type': pat_type,
               'field': founded[0],
               'value': founded[1],
            },
         ]
         _, is_armor_type = ItemArmorTypeConverter.convert(ctx, founded[1], err_debug = False)
         if is_armor_type:
            arr.append({
               'pat_type': pat_type,
               'field': 'armor_type',
               'value': founded[1],
            })
         return arr
      
      return [parsed]

str_field = r"(?:name|full_name|type)"
bool_name = r"(?:is_pct)"
any_part = r"[^:]+"
bool_val = r"(?:true|false)"

class KnownFieldParser(LineParser):
   pattern_hash = {
      'str_field': re.compile(rf"^\s*({str_field})\s*:({any_part})$"),
      'bool_field': re.compile(rf"^\s*({bool_name})\s*:\s*({bool_val})\s*$", re.IGNORECASE),
   }
   converter_config_arr = [
      {
         'pat_type': 'bool_field',
         'key': 'is_pct',
         'converter': BoolConverter,
      },
      {
         'pat_type': 'str_field',
         'key': 'type',
         'converter': FieldTypeConverter,
      },
   ]
   required_fields = ['name']
   is_debug = True

   @classmethod
   def parsed_line_to_config(cls, founded, pat_type, ctx):
      parsed = {
         'pat_type': pat_type,
         'field': founded[0],
         'value': founded[1],
      }
      parsed[founded[0]] = founded[1]
      return [parsed]

str_field = r"(?:name|full_name|type)"
bool_name = r"(?:is_pct)"
any_part = r"[^:]+"
bool_val = r"(?:true|false)"

class TradeParser(LineParser):
   pattern_hash = {
      'default': re.compile(rf"^\s*({any_part}):({any_part})$"),
      'note_string': re.compile(rf"^({any_part})$"),
   }
   required_fields = ['price']
   is_debug = True

   @classmethod
   def parsed_line_to_config(cls, founded, pat_type, ctx):
      parsed = {
         'pat_type': pat_type,
      }
      if pat_type == 'default':
         parsed['field'] = founded[0]
         parsed['value'] = founded[1]
      elif pat_type == 'note_string':
         parsed['field'] = 'note_string'
         parsed['value'] = founded[0]
      return [parsed]