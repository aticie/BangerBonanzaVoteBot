import json
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
        current_beatmap_id_tuple = await self.bot.db.get_current_beatmap_id()
        if current_beatmap_id_tuple is not None:
            await ctx.send('A vote is already open.')
            return

        async with OsuApiV2(self.osu_client_id, self.osu_client_secret) as osu_api:
            current_beatmap = await osu_api.get_beatmap(beatmap_id)
            await self.bot.db.set_current_beatmap(current_beatmap)

        current_beatmapset = current_beatmap['beatmapset']
        current_beatmap_text = f'{current_beatmapset["artist"]} - {current_beatmapset["title"]}'
        await ctx.send(f'Started voting for {current_beatmap_text}! Type 1-5 to rate this song!')

    @commands.command(name='endvote')
    async def goodbye(self, ctx: commands.Context):
        current_beatmap_object = await self.bot.db.get_current_beatmap()
        if current_beatmap_object is None:
            await ctx.send('No vote is currently open.')
            return

        current_beatmap_text = current_beatmap_object['beatmap_details']
        current_beatmap = json.loads(current_beatmap_text)
        current_beatmapset = current_beatmap['beatmapset']
        current_beatmap_text = f'{current_beatmapset["artist"]} - {current_beatmapset["title"]}'

        await self.bot.db.remove_current_beatmap()
        await ctx.send(f'Ended voting for {current_beatmap_text}.')

    async def cog_check(self, ctx: commands.Context) -> bool:
        """
        twitch.tv/bangerbonanza = '413734571'
        twitch.tv/heyronii = '68427964'
        twitch.tv/hallowatcher = '17289248'
        """
        return ctx.author.id == '413734571' or ctx.author.id == '68427964' or ctx.author.id == '17289248'


def prepare(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))
