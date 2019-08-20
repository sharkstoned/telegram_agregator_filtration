import os
import sys
import yaml

from pathlib import Path

from utils import load_yml
from filtration import build_query_tree


def init_settings(exec_params):
    settings = dict()

    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    CONFIGS_PATH = PROJECT_ROOT / 'configs'

    CONFIG_FILES_PATHS = {
        'creds': CONFIGS_PATH / exec_params['creds_path'],
        'filtration_rules': CONFIGS_PATH / exec_params['filtration_path'],
        'db_connection': CONFIGS_PATH / 'db.yml',
        'sheets_data': CONFIGS_PATH / 'sheets_data.yml',
    }

    settings['PROJECT_ROOT'] = PROJECT_ROOT
    settings['CONFIGS_PATH'] = CONFIGS_PATH
    settings['CONFIG_FILES_PATHS'] = CONFIG_FILES_PATHS

    settings.update(
        {section:load_yml(path) for (section, path) in CONFIG_FILES_PATHS.items()}
    )

    # stored in json and parsed by oauth2
    settings['sheets_creds_path'] = CONFIGS_PATH / 'flatty_spreadsheets.json'

    settings['filter_query'] = build_query_tree(settings['filtration_rules'])

    # write to google sheet when number of voters exceed this threshold
    settings['sheet_write_threshold'] = 1

    settings['tel_regex'] = '\+\s\d+\s\d{2}\s\d{3}-\d{2}-\d{2}'
    settings['url_regex'] = 'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'


    module = sys.modules[__name__]
    for (key, val) in settings.items():
        setattr(module, key.upper(), val)


    return settings



