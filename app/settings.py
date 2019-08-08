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
    }

    settings['PROJECT_ROOT'] = PROJECT_ROOT
    settings['CONFIGS_PATH'] = CONFIGS_PATH
    settings['CONFIG_FILES_PATHS'] = CONFIG_FILES_PATHS

    settings.update(
        {section:load_yml(path) for (section, path) in CONFIG_FILES_PATHS.items()}
    )

    settings['filter_query'] = build_query_tree(settings['filtration_rules'])


    module = sys.modules[__name__]
    for (key, val) in settings.items():
        setattr(module, key, val)


    return settings



