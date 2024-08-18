import discord
from discord.ext import commands
from typing import Optional
import gc

from ...const import UserRole as ur
from ...helpo import help
from ..bot_util import strict_channels, strict_users
from ...utils import print_memory_tracker

class SuperAdminCog(commands.Cog, name='SuperAdmin', description = "SuperAdmin commands - manipulate with other admins data"):

    def __init__(self, bot):
        self.bot = bot
    
    @strict_channels()
    @strict_users(ur.super_admin)
    @commands.command(aliases=['aa'], brief = "add user with admin role - more commands available", description = help['addadmin_description'])
    async def adminadd(self, ctx, users: commands.Greedy[discord.User]):
        for user in users:
            ctx.report.set_key(f'{user.name}')
            self.bot.controller.add_user_role(user, ur.admin, ctx)

    @strict_channels()
    @strict_users(ur.super_admin)
    @commands.command(aliases=['ad'], brief = "delete user with admin", description = help['deleteadmin_description'])
    async def admindelete(self, ctx, users: commands.Greedy[discord.User]):
        for user in users:
            ctx.report.set_key(f'{user.name}')
            self.bot.controller.delete_user_role(user, ctx)

    @strict_channels()
    @strict_users(ur.super_admin)
    @commands.command(aliases=['dm'], brief = "dump memory objects")
    async def dumpmemory(self, ctx):
        print_memory_tracker(ctx)

    @strict_channels()
    @strict_users(ur.super_admin)
    @commands.command(aliases=['gc'], brief = "attempt to run garbage collector manually")
    async def gccollect(self, ctx):
        gc.collect()
        ctx.report.msg.add('collected')

    @strict_channels()
    @strict_users(ur.super_admin)
    @commands.command(aliases=['pro'], brief = "profile peformance")
    async def profile(self, ctx):
        if self.bot.is_profile == True:
            ctx.report.msg.add('profiling off')
            self.bot.is_profile = False
            self.bot.pr = None
        else:
            ctx.report.msg.add('profiling on')
            self.bot.is_profile = True
    
    @strict_channels()
    @strict_users(ur.super_admin)
    @commands.command(brief = "test")
    async def test(self, ctx):
        db = ctx.bot.db_processor_re
        m = db.engine.m.Item
        db.get_column_names(m)

async def setup(bot):
    await bot.add_cog(SuperAdminCog(bot))