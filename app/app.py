import argparse

from settings import load_settings


def main(settings):
    import auth

    from telethon import events

    from utils import validate_presence, update_config
    from filtration import check_message

    # ===========================
    # * initialization
    # ===========================

    # initial validation
    validate_presence(settings['creds'], ('api_id', 'api_hash'))
    # todo: validate rules

    client, session_is_new = auth.connect(settings['creds'])

    if session_is_new:
        update_config(settings['creds'],
                      {'session_id': client.session.save()},
                      settings['CONFIG_FILES_PATHS']['creds'])

    # ===========================
    # * listener
    # ===========================

    source_chats = [int(source) for source in settings['creds']['source_chats']]

    @client.on(events.NewMessage(chats=source_chats))
    async def handle_message(event):
        if check_message(event.message, settings['filter_query']):
            for reciever in settings['creds']['target_chats']:
                await client.forward_messages(int(reciever), event.message, event.from_id)

    client.run_until_disconnected()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--creds', dest='creds_path', type=str, default='creds.yml',
                        help='Path to creds config relative to "./configs" directory')
    parser.add_argument('--filt', dest='filtration_path', type=str, default='filtration.yml',
                        help='Path to filtration config relative to "./configs" directory')
    args = vars(parser.parse_args())

    settings = load_settings(args)

    main(settings)
