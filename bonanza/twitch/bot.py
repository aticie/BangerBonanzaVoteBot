import os
import logging

from twitchio.ext import commands

logger = logging.getLogger('banger.bonanza')


class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=os.getenv('TWITCH_ACCESS_TOKEN'), prefix='.')

        self.requests_open = True
        self.current_song = None
        self.db = None

    async def event_ready(self):
        logger.info(f'Successfully logged in as {self.nick}')

    async def event_message(self, message):
        if message.echo or not self.requests_open:
            return

        if len(message) == 1:
            await self.db.add_vote(message.author.name, message.content, self.current_song)
            logger.info(f'{message.author.name} voted for {self.current_song} with {message.content}')

    @commands.command(name='startvote')
    async def hello(self, ctx: commands.Context):
        if self.requests_open:
            await ctx.send('A vote is already open.')
            return

        await ctx.send(f'Started voting for {self.current_song}! You can type 1-5 to vote for this song.')
        self.requests_open = True

    @commands.command(name='endvote')
    async def goodbye(self, ctx: commands.Context):
        if not self.requests_open:
            await ctx.send('No vote is currently open.')
            return

        await ctx.send(f'Ended voting for the {self.current_song}.')
        self.requests_open = False
