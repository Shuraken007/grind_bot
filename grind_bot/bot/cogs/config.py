import discord
from discord.ext import commands
from typing import Literal, Optional

from ...const import UserRole as ur
from ...helpo import help, game_mode_values
from ..bot_util import strict_channels, strict_users
# from ..converter import 

class ConfigCog(commands.Cog, name='Settings', description = "Config commands - your settings"):

	def __init__(self, bot):
		self.bot = bot

	@strict_channels()
	@strict_users(ur.nobody)
	@commands.group(aliases=['conf', 'co'], brief = "manage your settings")
	async def config(self, ctx):
		if ctx.invoked_subcommand is None:
			self.bot.controller.show_config(ctx)

	@strict_channels()
	@strict_users(ur.nobody)
	@config.command(aliases=['r'], brief = "reset config to default")
	async def reset(self, ctx):
		self.bot.controller.reset_config(ctx)

	@strict_channels()
	@strict_users(ur.nobody)
	@config.command(aliases=['mode', 'm'], brief = "select mode")
	async def game_mode(self, ctx, game_mode: Literal['normal', 'n', 'hardcore', 'h', 'hard']  = help['game_mode_descr']):
		game_mode = game_mode.lower()
		game_mode_as_enum = game_mode_values.get(game_mode)
		if game_mode_as_enum is not None:
			self.bot.controller.set_config('game_mode', game_mode_as_enum, ctx)
		else:
			ctx.report.err.add(f'something gone wrong, unknown game_mode "{game_mode}"')

	@strict_channels()
	@strict_users(ur.nobody)
	@config.command(aliases=['d'], brief = "delete config from database")
	async def delete(self, ctx):
		self.bot.controller.delete_config(ctx)

	@strict_channels()
	@strict_users(ur.nobody)
	@config.command(brief = "copy config from another user")
	async def copy(self, ctx, user: discord.User):
		self.bot.controller.copy_config(user, ctx)

async def setup(bot):
	await bot.add_cog(ConfigCog(bot))