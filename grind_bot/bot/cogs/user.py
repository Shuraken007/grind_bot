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

	@strict_channels()
	@strict_users(ur.nobody)
	@commands.command(aliases=['ia'], brief = "add item", description = help['item_add'])
	async def item_add(self, ctx):
		self.bot.controller.item_add(ctx)

	@strict_channels()
	@strict_users(ur.nobody)
	@commands.command(aliases=['ie'], brief = "edit item", description = help['item_edit'])
	async def item_edit(self, ctx):
		self.bot.controller.item_edit(ctx)

	@strict_channels()
	@strict_users(ur.nobody)
	@commands.command(aliases=['id'], brief = "delete item", description = help['item_delete'])
	async def item_delete(self, ctx):
		self.bot.controller.item_delete(ctx)

	@strict_channels()
	@strict_users(ur.nobody)
	@commands.command(aliases=['ir'], brief = "report items", description = help['item_delete'])
	async def item_report(self, ctx):
		self.bot.controller.item_report(ctx)

	@strict_channels()
	@strict_users(ur.nobody)
	@commands.command(aliases=['ta'], brief = "add trade", description = help['trade_add'])
	async def trade_add(self, ctx):
		self.bot.controller.trade_add(ctx)

	@strict_channels()
	@strict_users(ur.nobody)
	@commands.command(aliases=['te'], brief = "edit trade", description = help['trade_edit'])
	async def trade_edit(self, ctx):
		self.bot.controller.trade_edit(ctx)

	@strict_channels()
	@strict_users(ur.nobody)
	@commands.command(aliases=['td'], brief = "delete trade", description = help['trade_delete'])
	async def trade_delete(self, ctx):
		self.bot.controller.trade_delete(ctx)

	@strict_channels()
	@strict_users(ur.nobody)
	@commands.command(aliases=['tr'], brief = "report trades", description = help['trade_delete'])
	async def trade_report(self, ctx):
		self.bot.controller.trade_report(ctx)

async def setup(bot):
	await bot.add_cog(UserCog(bot))