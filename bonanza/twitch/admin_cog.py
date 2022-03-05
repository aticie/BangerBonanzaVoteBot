import os

from twitchio.ext import commands

from bonanza.osu_api import OsuApiV2
from bonanza.twitch.bot import TwitchBot


class AdminCog(commands.Cog):
    def __init__(self, bot: TwitchBot):
        self.bot = bot
        self.osu_client_id = os.environ.get('OSU_CLIENT_ID')
        self.osu_client_secret = os.environ.get('OSU_CLIENT_SECRET')

    @commands.command(name='startvote')
    async def hello(self, ctx: commands.Context, beatmap_id: int):
        if self.bot.requests_open:
            await ctx.send('A vote is already open.')
            return

        async with OsuApiV2(self.osu_client_id, self.osu_client_secret) as osu_api:
            self.bot.current_beatmap = await osu_api.get_beatmap(beatmap_id)
            self.bot.current_beatmapset = self.bot.current_beatmap['beatmapset']

        self.bot.db.set_current_beatmap(self.bot.current_beatmap)

        current_beatmap_text = f'{self.bot.current_beatmapset["artist"]} - {self.bot.current_beatmapset["title"]}'
        await ctx.send(f'Started voting for {current_beatmap_text}! Type 1-5 to rate this song!')
        self.bot.requests_open = True

    @commands.command(name='endvote')
    async def goodbye(self, ctx: commands.Context):
        if not self.bot.requests_open:
            await ctx.send('No vote is currently open.')
            return

        current_beatmap_text = f'{self.bot.current_beatmapset["artist"]} - {self.bot.current_beatmapset["title"]}'
        await ctx.send(f'Ended voting for {current_beatmap_text}.')
        self.bot.requests_open = False

    async def cog_check(self, ctx: commands.Context) -> bool:
        """
        twitch.tv/bangerbonanza = '413734571'
        twitch.tv/heyronii = '68427964'
        twitch.tv/hallowatcher = '17289248'
        """
        return ctx.author.id == '413734571' or ctx.author.id == '68427964' or ctx.author.id == '17289248'


def prepare(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))
