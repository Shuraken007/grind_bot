from collections import OrderedDict

class BaseStorage():
   def __init__(self):
      self.off = False
      self.amount = 0

   def get_amount(self):
      return self.amount

   def off(self):
      self.off = True

   def on(self):
      self.off = False

   def add(self, entity):
      raise Exception(f'abstract method')

   def get(self, key):
      raise Exception(f'abstract method')


class KeyStorage(BaseStorage):
   def __init__(self, name):
      super().__init__()
      self.data = {}
      self.name = name
      self.key = None

   def set_key(self, key):
      self.key = key
      if key in self.data:
         return
      self.data[key] = []

   def add(self, entity):
      if self.off:
         return
      if self.key is None:
         raise Exception(f'report key is not set for storage {self.name}')
      if type(entity) != list:
         entity = [entity]
      
      self.data[self.key].extend(entity)
      self.amount += len(entity)

   def get(self, key):
      if self.off:
         return None

      if key is None:
         raise Exception(f'key is not set on getting data for storage {self.name}')

      data = self.data.get(key, None)

      if data is None or len(data) == 0:
         return None

      return data
   
class KeyStorageUnique(BaseStorage):
   def __init__(self, name):
      super().__init__()
      self.data = {}
      self.name = name
      self.key = None

   def set_key(self, key):
      self.key = key
      if key in self.data:
         return
      self.data[key] = OrderedDict()

   def add(self, entity):
      if self.off:
         return
      if self.key is None:
         raise Exception(f'report key is not set for storage {self.name}')
      if type(entity) != list:
         entity = [entity]
      
      storage = self.data[self.key]
      for e in entity:
         if not e in storage:
            storage[e] = 0
         storage[e] += 1

      self.amount += len(entity)

   def get(self, key):
      if self.off:
         return None

      if key is None:
         raise Exception(f'key is not set on getting data for storage {self.name}')

      raw_data = self.data.get(key, None)

      if raw_data is None or len(raw_data.keys()) == 0:
         return None

      data = []
      for message, amount in raw_data.items():
         msg = message
         if amount > 1:
            msg += f': ({amount})'
         data.append(msg)

      return data

class ArrayStorageUnique(BaseStorage):
   def __init__(self):
      super().__init__()
      self.data = {}

   def add(self, entity):
      if self.off:
         return
      
      if type(entity) != list:
         entity = [entity]

      storage = self.data
      for e in entity:
         if not e in storage:
            storage[e] = 0
         storage[e] += 1

      self.amount += len(entity)

   def get(self):
      if self.off:
         return None

      if len(self.data.keys()) == 0:
         return None

      data = []
      for message, amount in self.data.items():
         msg = message
         if amount > 1:
            msg += f': ({amount})'
         data.append(msg)

      return data
   
class ArrayStorage(BaseStorage):
   def __init__(self):
      super().__init__()
      self.data = []

   def add(self, entity):
      if self.off:
         return
      
      if type(entity) != list:
         entity = [entity]

      self.data.extend(entity)
      self.amount += len(entity)

   def get(self):
      if self.off:
         return None

      if len(self.data) == 0:
         return None
   
      return self.data
   
class GroupedArrayStorage(BaseStorage):
   def __init__(self, limit, args_amount):
      super().__init__()
      self.limit = limit
      self.args_amount = args_amount
      self.groups = []
      self.args = []
      for i in range(self.args_amount):
         self.args.append([])

   def stock_to_group(self):
      data = []
      for i in range(self.args_amount):
         data.append(self.args[i])
         self.args[i] = []

      self.groups.append(data)

   def add(self, *args_tuple):
      if self.off:
         return
      args = list(args_tuple)
      if len(args) < self.args_amount:
         raise Exception('expected {} args, got {}'.format(self.args_amount, len(args)))
      
      for i in range(self.args_amount):
         if type(args[i]) != list:
            args[i] = [args[i]]
      
      for i in range(self.args_amount):
         if len(self.args[i]) + len(args[i]) > self.limit:
            self.stock_to_group()
            break

      for i in range(self.args_amount):
         self.args[i].extend(args[i])

      self.amount += 1

   def get(self):
      if self.off:
         return None

      for i in range(self.args_amount):
         if len(self.args[i]) > 0:
            self.stock_to_group()
            break

      if len(self.groups) == 0:
         return None

      return self.groups
   
class CounterStorage(BaseStorage):
   def __init__(self):
      super().__init__()
      self.data = {}

   def add(self, entity):
      if self.off:
         return
      
      if type(entity) != list:
         entity = [entity]

      for e in entity:
         if e not in self.data:
            self.data[e] = 0

         self.data[e] += 1
         self.amount += 1

   def get(self):
      if self.off:
         return None

      if len(self.data.keys()) == 0:
         return None
   
      return self.data

class Report:
   def set_key(self, key):
      self.key = key
      if key in self.keys:
         return

      self.keys.append(key)

      for storage in [self.msg, self.err, self.log]:
         storage.set_key(key)

      if key not in self.__inner_keys:
         self.reported_keys_amount += 1

   def dump_to_logger(self, logger):
      for key in self.keys:
         if data:= self.log.get(key):
            logger.dump_msg(data, 'log', mode='dump')

   def get_msg_arr_by_key(self, key, is_indent = False):
      msg_arr = []
      if messages:= self.msg.get(key):
         msg_arr.extend(messages)
      if errors:= self.err.get(key):
         msg_arr.extend(errors)
      
      if is_indent:
         msg_arr = ['\t' + x for x in msg_arr]

      return msg_arr
   
   def is_key_reported(self, key):
      if key in self.__inner_keys:
         return False
      
      if self.reported_keys_amount <= 1:
         return False

      return True

   def build_msg_arr(self):
      arr = []
      for key in self.keys:
         is_key_reported = self.is_key_reported(key)

         arr_by_key = self.get_msg_arr_by_key(key, is_indent = is_key_reported)
         if len(arr_by_key) == 0:
            continue
         if is_key_reported:
            arr.append(key + ':')

         arr.extend(arr_by_key)

      if reaction_data:= self.reaction_msg.get():
         if len(arr) > 0:
            arr.append('')
         arr.extend(reaction_data)

      if unique:= self.unique.get():
         arr.extend(unique)

      return arr

   def get_amount(self):
      amount = 0
      for storage in self.storages:
         amount += storage.get_amount()
      return amount

   def off(self):
      for storage in self.storages:
         storage.off()

      self.off = True

   def on(self):
      for storage in self.storages:
         storage.on()

      self.off = False

   def __init__(self):
      self.off = False

      self.msg = KeyStorage('msg')
      self.err = KeyStorage('err')
      self.log = KeyStorage('log')

      self.unique = ArrayStorageUnique()
      self.reaction = CounterStorage()
      self.reaction_msg = ArrayStorage()

      self.file = GroupedArrayStorage(10, 1)
      self.embed = GroupedArrayStorage(10, 1)
      self.embed_and_files = GroupedArrayStorage(2, 2)

      self.storages = [self.msg, self.err, self.log, self.unique, self.reaction_msg, self.reaction, self.file, self.embed, self.embed_and_files]

      self.keys = []

      self.reported_keys_amount = 0
      self.__default_key = 'default'
      self.__inner_keys = [self.__default_key]

      self.set_key(self.__default_key)