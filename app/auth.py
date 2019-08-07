from telethon import TelegramClient
from telethon.sessions import StringSession

from settings import CONFIG, CONFIG_FILES_PATHS
from utils import update_config


def connect(creds):
    # try connecting with session_id, otherwise authenticate
    if creds.get('session_id'):
        start_params = tuple()
        session = StringSession(creds['session_id'])
    else:
        print('No existing session found. Authenticating user..')
        start_params = (creds['phone'],) if creds.get('phone') else tuple()
        session = StringSession()

    client = TelegramClient(session,
                            creds['api_id'],
                            creds['api_hash'])
    client.start(*start_params)

    if client.is_connected():
        # todo: creds are already present in parameter
        update_config(CONFIG['creds'],
                {'session_id': client.session.save()},
                CONFIG_FILES_PATHS['creds'])
    else:
        raise Exception('Client was not connected')

    return client
