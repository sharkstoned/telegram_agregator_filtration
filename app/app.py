#! python

import argparse

from settings import init_settings


def main(settings):
    import logging
    import asyncio
    import auth
    import db

    from telethon import events
    from telethon.tl.custom import Button
    from utils import validate_presence, update_config
    from filtration import check_message


    logger = logging.getLogger('app')


    # ===========================
    # * initialization
    # ===========================

    logger.info('Application started')

    # initial validation
    validate_presence(settings['creds'], ('api_id', 'api_hash'))
    # todo: validate rules

    client, new_user_session = auth.connect_user(settings['creds'])

    if new_user_session:
        update_config(settings['creds'],
                      {'session_id': client.session.save()},
                      settings['CONFIG_FILES_PATHS']['creds'])

    bot = auth.connect_bot(settings['creds'])

    loop = asyncio.get_event_loop()

    # ===========================
    # * establish db connection
    # ===========================

    db_conn = loop.run_until_complete(db.establish_connction(settings['db_connection']))

    # ===========================
    # * listeners
    # ===========================

    source_chats = [int(source) for source in settings['creds']['source_chats']]
    allowed_chats = [int(id) for id in settings['creds']['allowed_chats']]
    button_text = 'Уже хочу! - '

    async def filter_message(msg):
        if check_message(msg, settings['filter_query']):
            logger.info('Found matching message')
            for reciever in allowed_chats:
                await bot.send_message(reciever, msg, buttons=Button.inline(button_text + '0'))


    @client.on(events.NewMessage(chats=source_chats))
    async def handle_message(event):
        await filter_message(event.message)


    @bot.on(events.NewMessage)
    async def send_placeholder(event):
        if event.chat_id not in allowed_chats:
            await event.respond('The bot is under development')


    @bot.on(events.CallbackQuery)
    async def handle_vote(event):
        if event.message_id is not None:
            voters_number = await db.trigger_vote(event.message_id, event.sender_id)
            await event.edit(buttons=Button.inline(button_text + str(voters_number)))


    # ===========================
    # * check unread messages
    # ===========================

    async def check_unread():
        for chat in source_chats:
            last_read_id = await db.get_latest_msg_id(chat)
            if last_read_id is not None:
                unread_messages = await client.get_messages(chat,
                                                            10000,
                                                            offset_id=int(last_read_id),
                                                            reverse=True)

                for msg in unread_messages:
                    await filter_message(msg)

    async def prepare_for_shutdown():
        for chat in source_chats:
            last_read_id = str(await client.get_messages(chat))[0].id
            await db.set_latest_msg_id(chat, last_read_id)

    loop.run_until_complete(check_unread())

    # ===========================
    # * running loop
    # ===========================

    logger.info('Bot is active.')
    logger.info('Listening for messages...')
    print('Press Ctrl-C to stop')

    try:
        loop.run_until_complete(asyncio.gather(
            client.disconnected,
            bot.disconnected
        ))
    except KeyboardInterrupt:
        loop.run_until_complete(prepare_for_shutdown())
        client.disconnect()
        bot.disconnect()
        db_conn.close()
        loop.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--creds', dest='creds_path', type=str, default='creds.yml',
                        help='Path to creds config relative to "./configs" directory')
    parser.add_argument('--filt', dest='filtration_path', type=str, default='filtration.yml',
                        help='Path to filtration config relative to "./configs" directory')
    args = vars(parser.parse_args())

    settings = init_settings(args)

    import app_logger # init logger

    main(settings)
