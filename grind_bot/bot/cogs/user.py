from discord.ext import commands
from typing import Literal, Optional

from ...const import UserRole as ur
from ...helpo import help
# from ..converter import CoordsConverter, AliasConverter
from ... import parser
from ..bot_util import strict_channels, strict_users

class UserCog(commands.Cog, name='User', description = "User commands - manipulate with your own data"):

	def __init__(self, bot):
		self.bot = bot

	# @strict_channels()
	# @strict_users(ur.nobody)
	# @commands.command(aliases=['l', 'lead'], brief = "show player scores, depending on opening cells")
	# async def leaderboard(self, ctx, limit: Optional[int] = help['lead_limit']):
	# 	await self.bot.controller.show_leaderboard(ctx, limit)

async def setup(bot):
	await bot.add_cog(UserCog(bot))