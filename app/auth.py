import logging

from telethon import TelegramClient
from telethon.sessions import StringSession


logger = logging.getLogger('app')


def connect_user(creds):
    # try connecting with session_id, otherwise authenticate
    try:
        session = StringSession(creds['session_id'])
        client = TelegramClient(session,
                                creds['api_id'],
                                creds['api_hash'])
        client.start()

        if client.is_connected():
            logger.info('Client is connected using session.')
            return (client, False)
        else:
            logger.error('Client failed to connect using existing session')
            raise Exception('Error occured - client is not connected')

    except KeyError:
        logger.info('Session is not found. Trying to authenticate user.')
        start_params = (creds['phone'],) if creds.get('phone') else tuple()
        client = TelegramClient(StringSession(),
                                creds['api_id'],
                                creds['api_hash'])
        client.start(*start_params)

        if client.is_connected():
            logger.info('Client is authenticated and connected.')
            return (client, True)
        else:
            logger.error('Client failed to connect using authentication')
            raise Exception('Error occured - client is not connected')


def connect_bot(creds):
    bot = TelegramClient('bot',
                         creds['api_id'],
                         creds['api_hash'])

    bot.start(bot_token=creds['bot_token'])

    return bot
