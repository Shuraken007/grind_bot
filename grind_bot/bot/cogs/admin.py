import discord
from discord.ext import commands
from typing import Literal, Optional

from ...const import UserRole as ur, FieldType
from ...helpo import help
from ..bot_util import strict_channels, strict_users

class AdminCog(commands.Cog, name='Admin', description = "Admin commands - manipulate with other users data"):

    def __init__(self, bot):
        self.bot = bot
    
    @strict_channels()
    @strict_users(ur.admin)
    @commands.command(aliases=['al'], brief = "list user priveleges", description = help['adminlist_description'])
    async def adminlist(self, ctx):
        await self.bot.controller.report_user_roles(self.bot, ctx.report)

    @strict_channels()
    @strict_users(ur.admin)
    @commands.command(aliases=['ba'], brief = "ban user - no interraction with bot", description = help['banadd_description'])
    async def banadd(self, ctx, users: commands.Greedy[discord.User]):
        for user in users:
            ctx.report.set_key(f'{user.name}')
            self.bot.controller.add_user_role(user, ur.banned, ctx)

    @strict_channels()
    @strict_users(ur.admin)
    @commands.command(aliases=['bd'], brief = "delete user ban", description = help['deleteban_description'])
    async def bandelete(self, ctx, users: commands.Greedy[discord.User]):
        for user in users:
            ctx.report.set_key(f'{user.name}')
            self.bot.controller.delete_user_role(user, ctx)

    @strict_channels()
    @strict_users(ur.admin)
    @commands.command(aliases=['kfa'], brief = "known field add", description = help['known_field_add'])
    async def knownfieldadd(self, ctx):
        self.bot.controller.add_known_field(ctx)

    @strict_channels()
    @strict_users(ur.admin)
    @commands.command(aliases=['kfd'], brief = "known field delete", description = help['known_field_delete'])
    async def knownfielddelete(self, ctx, name: str):
        self.bot.controller.delete_known_field(name, ctx)

    @strict_channels()
    @strict_users(ur.admin)
    @commands.command(aliases=['kfr'], brief = "known field report", description = help['known_field_report'])
    async def knownfieldreport(self, ctx):
        await self.bot.controller.report_known_fields(ctx)

async def setup(bot):
    await bot.add_cog(AdminCog(bot))