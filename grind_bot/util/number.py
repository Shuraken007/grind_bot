def validate_not_negative_integer(val):
   try:
      val = int(val)
   except:
      msg = f'expected to be integer, get {val}'
      return val, False, msg
   if val < 0:
      msg = f'expected to be >= 0, got {val}'
      return val, False, msg

   return val, True, ''