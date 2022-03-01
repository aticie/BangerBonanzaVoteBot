import os
import logging

from twitchio.ext import commands

from bonanza.database.votes import VotesDB

logger = logging.getLogger('banger.bonanza')


class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=os.getenv('TWITCH_ACCESS_TOKEN'), prefix='!')

        self.requests_open = False
        self.current_song = None
        self.db = VotesDB(os.getenv('DB_DIR', 'votes.db'))

    async def event_ready(self):
        logger.info(f'Successfully logged in as {self.nick}')
        await self.join_channels([self.nick])
        await self.db.initialize_tables()
        self.load_module('bonanza.twitch.admin_cog')
        logger.debug(f'Successfully initialized all modules!')

    async def event_message(self, message):
        await self.wait_for_ready()
        await self.handle_commands(message)
        if message.echo or not self.requests_open:
            return

        if len(message) == 1:
            await self.db.add_vote(message.author.name, message.content, self.current_song)
            logger.info(f'{message.author.name} voted for {self.current_song} with {message.content}')
