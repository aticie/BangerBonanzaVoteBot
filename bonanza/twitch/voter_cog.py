import datetime

from twitchio.ext import commands

from bonanza.twitch.bot import TwitchBot


class VoterCog(commands.Cog):
    def __init__(self, bot: TwitchBot):
        self.bot = bot
        self.command_cooldown = 30
        self.command_used_time = datetime.datetime.now() - datetime.timedelta(hours=1000)

    @commands.command(name='currentvote', aliases=['cv'])
    async def current_vote(self, ctx: commands.Context):
        if self.bot.requests_open:
            current_song = f'{self.bot.current_beatmapset["artist"]} - {self.bot.current_beatmapset["title"]}'
            await ctx.send(f'Currently voting for: {current_song}')
        else:
            await ctx.send('No voting in process.')

    async def cog_check(self, ctx: commands.Context) -> bool:
        if datetime.datetime.now() < self.command_used_time + datetime.timedelta(seconds=self.command_cooldown):
            return False
        else:
            self.command_used_time = datetime.datetime.now()
        return True


def prepare(bot: commands.Bot):
    bot.add_cog(VoterCog(bot))
