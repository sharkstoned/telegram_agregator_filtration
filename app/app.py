import auth

from telethon import events

from settings import CONFIG, FILTER_QUERY , CONFIG_FILES_PATHS
from utils import validate_presence, update_config
from filtration import check_message


# ===========================
# * initialization
# ===========================

# initial validation
validate_presence(CONFIG['creds'], ('api_id', 'api_hash'))
# todo: validate rules

client = auth.connect(CONFIG['creds'])

update_config(CONFIG['creds'],
              {'session_id': client.session.save()},
              CONFIG_FILES_PATHS['creds'])

# ===========================
# * listener
# ===========================

source_chats = [int(source) for source in CONFIG['creds']['source_chats']]

@client.on(events.NewMessage(chats=source_chats))
async def handle_message(event):
    if check_message(event.message, FILTER_QUERY):
        for reciever in CONFIG['creds']['target_chats']:
            await client.forward_messages(int(reciever), event.message, event.from_id)

client.run_until_disconnected()

