from telethon import TelegramClient
from telethon.sessions import StringSession


def connect(creds):
    # try connecting with session_id, otherwise authenticate
    try:
        session = StringSession(creds['session_id'])
        client = TelegramClient(session,
                                creds['api_id'],
                                creds['api_hash'])
        client.start()
    except KeyError:
        print('No existing session found. Authenticating user..')
        start_params = (creds['phone'],) if creds.get('phone') else tuple()
        client = TelegramClient(StringSession(),
                                creds['api_id'],
                                creds['api_hash'])
        client.start(*start_params)

    if client.is_connected():
        return client
    else:
        raise Exception('Client was not connected')
