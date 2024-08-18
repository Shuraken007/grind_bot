from datetime import datetime, timezone

from .processor_core import DbProcessorCore, with_session
from ..const import DEFAULT_USER_CONFIG, FieldType as ft
from ..util import text

class DbProcessor(DbProcessorCore):

   def __init__(self, admin_id, *args, **kwargs):
      super(DbProcessor, self).__init__(*args, **kwargs)
      self.admin_id = admin_id
      self.add_base_fields_from_item_model()

   def add_to_config(self, list, options, type, config):
      for option in options:
         for item in list:
            full_name = option['fmt'].format(item)
            db_name = text.full_name_to_name(full_name)
            config.append({'name': db_name, 'full_name': full_name, 'is_pct': option['is_pct'], 'type': type})

   def add_spells_to_config(self, config):
      spells = ['Blood', 'Poison', 'Arcane', 'Lightning', 'Fire', 'Ice']
      options = [
         {'fmt': 'Resist {}', 'is_pct': True},
         {'fmt': 'Absorb {}', 'is_pct': True},
         {'fmt': '{} Spell Power', 'is_pct': False},
         {'fmt': '{} Damage', 'is_pct': True},
         {'fmt': '{} Damage to Melee', 'is_pct': False},
         {'fmt': 'Enchance {}', 'is_pct': True},
         {'fmt': 'Enemy Resist {}', 'is_pct': True},
      ]
      self.add_to_config(spells, options, ft.number, config)

   def add_controls_to_config(self, config):
      controls = ['Stun', 'Fear', 'Paralyze', 'Silence']
      options = [
         {'fmt': 'Resist {}', 'is_pct': True},
      ]
      self.add_to_config(controls, options, ft.number, config)

   def add_resources_to_config(self, config):
      resources = ['Health', 'Mana', 'Spirit']
      options = [
         {'fmt': '{}', 'is_pct': False},
         {'fmt': '{} on Kill', 'is_pct': False},
         {'fmt': '{} Regen', 'is_pct': False},
         {'fmt': 'Maximum {}', 'is_pct': True},
      ]
      self.add_to_config(resources, options, ft.number, config)
      resources = ['Health', 'Mana']
      options = [
         {'fmt': '{} Leach', 'is_pct': False},
      ]
      self.add_to_config(resources, options, ft.number, config)
      resources = ['Mana', 'Spirit']
      options = [
         {'fmt': '{} When Damaged', 'is_pct': False},
      ]
      self.add_to_config(resources, options, ft.number, config)

   def add_enemy_type_to_config(self, config):
      enemy_types = ['Humanoids', 'Beasts', 'Undead', 'Demons', 'Dragonkin', 'Mystical', 'Giants']
      options = [
         {'fmt': 'Enchanced Damage vs {}', 'is_pct': True},
      ]
      self.add_to_config(enemy_types, options, ft.number, config)

   def add_mag_phys_to_config(self, config):
      dmg = ['Magical', 'Physical']
      options = [
         {'fmt': '{} Damage Reduced by', 'is_pct': False},
      ]
      self.add_to_config(dmg, options, ft.number, config)
      dmg = ['Physical']
      options = [
         {'fmt': 'Resist {}', 'is_pct': True},
      ]
      self.add_to_config(dmg, options, ft.number, config)


   def add_not_pct_to_config(self, config):
      items = [
         'Strength', 'Stamina', 'Agility', 'Dexterity', 'Wisdom', 'Intelligence', 'Charisma', 
         'All Stats', 'All Talents', 'All Passive Skills', 
         'Faster Cast Rate', 'Critical Hit',
         'Conjuration', 'Evocation', 'Alteration', 
         'Offence', 'Defence', 'Attack',  'Dodge', 'Parry', 
         'Piercing', 'Archery', 'Riposte',
         'Hand-to-Hand', 'Dual Wield',
         'One-hand Slash', 'Two-hand Slash', 'One-hand Blunt', 'Two-hand Blunt'
      ]
      for item in items:
         db_name = text.full_name_to_name(item)
         config.append({'name': db_name, 'full_name': item, 'is_pct': False, 'type': ft.number})

   def add_pct_to_config(self, config):
      items = [
         'All Resistances', 'All Status Resistances', 'All Spell Power',
         'Enchanced Damage', 'Enchanced Armor',
         'Chance to Block', 
         'Increased Block Rate',
         'Run Speed', 'Magic Find', 'Gold Find', 'Exp Find'
      ]
      for item in items:
         db_name = text.full_name_to_name(item)
         config.append({'name': db_name, 'full_name': item, 'is_pct': True, 'type': ft.number})

   @with_session
   def add_base_fields_from_item_model(self):
      config = [
         { 'name': 'name', 'full_name': 'Name', 'type': ft.string, 'is_pct': False, },
         { 'name': 'type', 'full_name': 'Type', 'type': ft.string, 'is_pct': False, },
         { 'name': 'tier', 'full_name': 'Tier', 'type': ft.enum, 'is_pct': False, },
         { 'name': 'rarity', 'full_name': 'Rarity', 'type': ft.enum, 'is_pct': False, },
         { 'name': 'damage_min', 'full_name': 'Damage Min', 'type': ft.number, 'is_pct': False, },
         { 'name': 'damage_max', 'full_name': 'Damage Max', 'type': ft.number, 'is_pct': False, },
         { 'name': 'speed', 'full_name': 'Speed', 'type': ft.float, 'is_pct': False, },
         { 'name': 'dps', 'full_name': 'Damage Per Second', 'type': ft.float, 'is_pct': False, },
         { 'name': 'proficiency', 'full_name': 'Proficiency', 'type': ft.string, 'is_pct': False, },
         { 'name': 'armor', 'full_name': 'Armor', 'type': ft.number, 'is_pct': False, },
         { 'name': 'armor_type', 'full_name': 'Armor Type', 'type': ft.enum, 'is_pct': False, },
         { 'name': 'slot', 'full_name': 'Slot', 'type': ft.string, 'is_pct': False, },
         { 'name': 'requires_level', 'full_name': 'Requires Level', 'type': ft.string, 'is_pct': False, },
         { 'name': 'set_name', 'full_name': 'Set Name', 'type': ft.string, 'is_pct': False, },
      ]
      self.add_spells_to_config(config)
      self.add_controls_to_config(config)
      self.add_resources_to_config(config)
      self.add_enemy_type_to_config(config)
      self.add_mag_phys_to_config(config)
      self.add_not_pct_to_config(config)
      self.add_pct_to_config(config)

      time = datetime.now(tz=timezone.utc)
      for item_spec in config:
         item = self.get_known_field(item_spec['name'])
         if item is not None:
            continue
         item_spec['user_id'] = self.admin_id
         item_spec['time'] = time
      
      self.mass_add_known_fields(config)

   @with_session
   def get_known_fields(self):
      return self.get_all_objects(
            self.engine.m.KnownField
      )

   def get_known_field(self, name):
      return self.get_obj(
         self.engine.m.KnownField,
         {'name': name}
      )
      
   @with_session
   def mass_add_known_fields(self, hash_arr):
      known_fields = self.get_known_fields()
      names_hash = {}
      for known_field in known_fields:
         names_hash[known_field.name] = True

      for hash in hash_arr:
         if hash['name'] in names_hash:
            continue
         item = self.engine.m.KnownField(**hash)
         self.s.add(item)
      self.s.commit()
   
   @with_session
   def add_known_field(self, hash):
      return self.add_or_modify_obj(
         self.engine.m.KnownField,
         hash
      )

   @with_session
   def delete_known_field(self, field_name):
      return self.delete_obj(
         self.engine.m.KnownField,
         {'name': field_name}
      )

   @with_session
   def add_user_role(self, user_id, role):
      return self.add_or_modify_obj(
         self.engine.m.Role,
         {'user_id': user_id, 'role': role}
      )

   @with_session
   def delete_user_role(self, user_id):
      return self.delete_obj(
         self.engine.m.Role,
         {'user_id': user_id}
      )

   @with_session
   def get_user_role(self, user_id):
      return self.get_obj_field(
         self.engine.m.Role,
         {'user_id': user_id},
         'role'
      )      

   @with_session
   def get_user_roles(self):
      return self.get_all_objects(self.engine.m.Role)

   @with_session
   def get_user_config(self, user_id):
      return self.get_obj(
         self.engine.m.UserConfig,
         {'user_id': user_id}
      )
   
   @with_session      
   def set_user_config(self, user_id, user_config_dict):
      user_config_dict |= {'user_id': user_id}
      return self.add_or_modify_obj(
         self.engine.m.UserConfig,
         user_config_dict,
         DEFAULT_USER_CONFIG
      )
      
   @with_session
   def delete_user_config(self, user_id):
      return self.delete_obj(
         self.engine.m.UserConfig,
         {'user_id': user_id}
      )