from twitchio.ext import commands

from bonanza.twitch.bot import TwitchBot


class MyCog(commands.Cog):
    def __init__(self, bot: TwitchBot):
        self.bot = bot

    @commands.command(name='startvote')
    async def hello(self, ctx: commands.Context):
        if self.bot.requests_open:
            await ctx.send('A vote is already open.')
            return

        await ctx.send(f'Started voting for {self.bot.current_song}! You can type 1-5 to vote for this song.')
        self.bot.requests_open = True

    @commands.command(name='endvote')
    async def goodbye(self, ctx: commands.Context):
        if not self.bot.requests_open:
            await ctx.send('No vote is currently open.')
            return

        await ctx.send(f'Ended voting for the {self.bot.current_song}.')
        self.bot.requests_open = False

    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.is_mod


def prepare(bot: commands.Bot):
    # Load our cog with this module...
    bot.add_cog(MyCog(bot))
