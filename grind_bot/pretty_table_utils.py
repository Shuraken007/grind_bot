import prettytable

def process_user_name(user_name, processing_user_id, owner_user_id):
   arr = user_name.split(' ')
   name = arr[0]
   if processing_user_id == owner_user_id:
      name = "\033[0;31;40m" + name + "\033[0m"
   return name

async def get_user_name(user_id, ctx):
   user_name = await ctx.bot.get_user_name_by_id(user_id)
   user_name = process_user_name(user_name, user_id, ctx.message.author.id)
   return user_name

def table_to_report(t, report):
   msg = t.get_string()
   msg_arr = msg.split('\n')
   report.msg.add(msg_arr)

def get_not_null_columns(items, col_names):
   not_null_col_names = []
   for name in col_names:
      for item in items:
         val = getattr(item, name)
         if val is not None:
            not_null_col_names.append(name)
            break
   return not_null_col_names

async def get_item_field(item, key, ctx):
   val = getattr(item, key, "None")
   if key == 'user_id':
      val = await get_user_name( val, ctx )

async def get_ordered_fields_from_item(item, col_names, ctx):
   row = []
   for key in col_names:
      val = get_item_field(item, key, ctx)
      row.append(val)
   return row

def report_table(ctx, title, rows, is_inverted=False):
   tabl = None
   if is_inverted:
      tabl = prettytable.PrettyTable()
      tabl.add_column(title[0], title[1:])
   else:
      tabl = prettytable.PrettyTable(title)

   for row in rows:
      if is_inverted:
         tabl.add_column(row[0], row[1:])
      else:
         tabl.add_row(row)
   table_to_report(tabl, ctx.report)   

async def convert_db_model_to_table(items, col_names, ctx, is_inverted = False, title_column_field = ""):
   title = get_not_null_columns(items, col_names)
   # adding not null columns
   
   if is_inverted:
      tabl = prettytable.PrettyTable()
      tabl.add_column(title_column_field, title)
      
      for item in items:
         title_val = await get_item_field(item, title_column_field, ctx)
         column = await get_ordered_fields_from_item(item, title)
         tabl.add_column(title_val, column)
   else:
      tabl = prettytable.PrettyTable(title)

      for item in items:
         row = await get_ordered_fields_from_item(item, title)
         tabl.add_row(row)

   table_to_report(tabl, ctx.report)