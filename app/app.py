import auth

from telethon import events

from settings import ENV
from utils import validate_presence


# ===========================
# * initialization
# ===========================

# initial validation
validate_presence(ENV['creds'], ('api_id', 'api_hash'))
# todo: validate rules

client = auth.connect(ENV['creds'])

@client.on(events.NewMessage(incoming=True, chats=ENV['creds']['source_chats']))
async def handle_message(event):
    # fitrate and repost
    pass
