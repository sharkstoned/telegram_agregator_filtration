import auth

from telethon import events

from settings import CONFIG, FILTER_QUERY
from utils import validate_presence
from filtration import check_message


# ===========================
# * initialization
# ===========================

# initial validation
validate_presence(CONFIG['creds'], ('api_id', 'api_hash'))
# todo: validate rules

client = auth.connect(CONFIG['creds'])

@client.on(events.NewMessage(incoming=True, chats=CONFIG['creds']['source_chats']))
async def handle_message(event):
    if check_message(event.message, FILTER_QUERY):
        for reciever in CONFIG['creds']['target_chats']:
            await client.send_message(int(reciever), event.message)

client.run_until_disconnected()

