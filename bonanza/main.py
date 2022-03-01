import logging
import os

from bonanza.twitch.bot import TwitchBot

logger = logging.getLogger('banger.bonanza')
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO').upper())
loggers_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(process)d | %(name)s | %(funcName)s | %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S')

ch = logging.StreamHandler()
ch.setFormatter(loggers_formatter)
logger.addHandler(ch)

logger.propagate = False

if __name__ == '__main__':
    bot = TwitchBot()
    bot.run()
