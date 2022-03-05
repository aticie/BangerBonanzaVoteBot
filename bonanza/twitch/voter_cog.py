import datetime
import json

from twitchio.ext import commands

from bonanza.twitch.bot import TwitchBot


class VoterCog(commands.Cog):
    def __init__(self, bot: TwitchBot):
        self.bot = bot
        self.command_cooldown = 30
        self.command_used_time = datetime.datetime.now() - datetime.timedelta(hours=1000)

    @commands.command(name='currentvote', aliases=['cv'])
    async def current_vote(self, ctx: commands.Context):
        current_beatmap_tuple = self.bot.db.get_current_beatmap()
        if current_beatmap_tuple is not None:
            current_beatmapset = json.loads(current_beatmap_tuple[0])['beatmapset']
            current_song = f'{current_beatmapset["artist"]} - {current_beatmapset["title"]}'
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
