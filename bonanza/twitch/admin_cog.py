import os

from twitchio.ext import commands

from bonanza.osu_api import OsuApiV2
from bonanza.twitch.bot import TwitchBot


class AdminCog(commands.Cog):
    def __init__(self, bot: TwitchBot):
        self.bot = bot
        self.api = OsuApiV2(os.getenv('OSU_CLIENT_ID'), os.getenv('OSU_CLIENT_SECRET'))

    @commands.command(name='startvote')
    async def hello(self, ctx: commands.Context, beatmap_id: int):
        if self.bot.requests_open:
            await ctx.send('A vote is already open.')
            return
        self.bot.current_beatmap = await self.api.get_beatmap(beatmap_id)
        self.bot.current_beatmapset = self.bot.current_beatmap['beatmapset']
        current_beatmap = f'{self.bot.current_beatmapset["artist"]} - {self.bot.current_beatmapset["title"]}'
        await ctx.send(f'Started voting for {current_beatmap}! Type 1-5 to rate this song!')
        self.bot.requests_open = True

    @commands.command(name='endvote')
    async def goodbye(self, ctx: commands.Context):
        if not self.bot.requests_open:
            await ctx.send('No vote is currently open.')
            return

        current_beatmap = f'{self.bot.current_beatmapset["artist"]} - {self.bot.current_beatmapset["title"]}'
        await ctx.send(f'Ended voting for {current_beatmap}.')
        self.bot.requests_open = False

    async def cog_check(self, ctx: commands.Context) -> bool:
        # twitch.tv/bangerbonanza = '413734571'
        return ctx.author.id == '413734571'


def prepare(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))
