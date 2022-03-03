import os
import logging

from twitchio.ext import commands

from bonanza.database.votes import VotesDB

logger = logging.getLogger('banger.bonanza')


class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=os.getenv('TWITCH_ACCESS_TOKEN'), prefix='!')

        self.requests_open = False
        self.current_beatmap = None
        self.current_beatmapset = None
        self.db = VotesDB(os.getenv('DB_DIR', 'votes.db'))

    async def event_ready(self):
        logger.info(f'Successfully logged in as {self.nick}')
        await self.join_channels(['bangerbonanza'])
        await self.db.initialize_tables()
        self.load_module('bonanza.twitch.admin_cog')
        self.load_module('bonanza.twitch.voter_cog')
        logger.debug(f'Successfully initialized all modules!')

    async def event_message(self, message):
        if message.echo:
            return
        await self.wait_for_ready()
        await self.handle_commands(message)
        if self.requests_open:
            if len(message.content) == 1:
                beatmap_id = self.current_beatmap['id']
                await self.db.add_vote(user_id=message.author.id, song_id=beatmap_id,
                                       vote=message.content, username=message.author.name)
                logger.info(f'{message.author.name} voted for {beatmap_id} with {message.content}')
