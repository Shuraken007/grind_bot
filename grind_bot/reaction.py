import enum

class Reactions(enum.IntEnum):
   fail = 0,
   ok = 1,
   user_data_equal = 2,
   user_data_deleted = 3,
   user_data_new = 4,
   user_data_changed = 5,
   user_data_wrong = 6,

r = Reactions

emoji = {
   r.ok: "✅",
   r.fail: "❌",
   r.user_data_equal: "🟰",
   r.user_data_new: "➕",
   r.user_data_changed: "♻️",
   r.user_data_deleted: "➖",
   r.user_data_wrong: "⚠️",
   "0": "0️⃣",
   "1": "1️⃣",
   "2": "2️⃣",
   "3": "3️⃣",
   "4": "4️⃣",
   "5": "5️⃣",
   "6": "6️⃣",
   "7": "7️⃣",
   "8": "8️⃣",
   "9": "9️⃣",
}

report_emoji = {
   r.ok: "✅",
   r.fail: "❌",
   r.user_data_equal: "⩵",
   r.user_data_new: "➕",
   r.user_data_changed: "♻️",
   r.user_data_deleted: "➖",
   r.user_data_wrong: "⚠️",
   "0": "0️⃣",
   "1": "1️⃣",
   "2": "2️⃣",
   "3": "3️⃣",
   "4": "4️⃣",
   "5": "5️⃣",
   "6": "6️⃣",
   "7": "7️⃣",
   "8": "8️⃣",
   "9": "9️⃣",
}

def number_to_digits(number):
   return [str(x) for x in str(number)]

def process_reactions(reactions, report):
   emoji_arr = []
   for reaction, value in reactions.items():
      add_reaction_to_report(reaction, value, report)
      
      reaction_emoji_arr = build_emoji_arr(reaction, value)
      emoji_arr.extend(reaction_emoji_arr)

   return emoji_arr

not_reported_reactions = [r.ok]
not_reported_reactions_if_one = [r.fail]
def is_reaction_reported(reaction, value):
   if reaction in not_reported_reactions:
      return False
   if reaction in not_reported_reactions_if_one and value == 1:
      return False
   return True

def add_reaction_to_report(reaction, value, report):
   if not is_reaction_reported(reaction, value):
      return

   msg = '{} ({}) - {}' \
      .format(report_emoji[reaction], value, reaction.name)
   report.reaction_msg.add(msg)

def build_emoji_arr(reaction, value):
   reactions = [reaction]
   
   return [str(emoji[x]) for x in reactions]