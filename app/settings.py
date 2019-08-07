import os
import yaml

from pathlib import Path

from utils import load_yml
from filtration import build_query_tree


def load_settings(exec_params):
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    CONFIGS_PATH = PROJECT_ROOT / 'configs'

    public = dict()

    CONFIG_FILES_PATHS = {
        'creds': CONFIGS_PATH / exec_params['creds_path'],
        'filtration_rules': CONFIGS_PATH / exec_params['filtration_path'],
    }

    public['CONFIG_FILES_PATHS'] = CONFIG_FILES_PATHS

    public.update(
            {section:load_yml(path) for (section, path) in CONFIG_FILES_PATHS.items()}
        )

    public['filter_query'] = build_query_tree(public['filtration_rules'])

    return public

