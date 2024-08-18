import re

def full_name_to_name(full_name):
   name = full_name.lower()
   name = re.sub("\s+", '_', name)
   name = re.sub("[^a-z_]+", '_', name)
   return name