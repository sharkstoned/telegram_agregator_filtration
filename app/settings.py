import os
import yaml

from pathlib import Path

from utils import load_yml
from filtration import build_query_tree


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS_PATH = PROJECT_ROOT / 'configs'


CONFIG_FILES_PATHS = {
    'creds': CONFIGS_PATH / 'creds.yml',
    'filtration_rules': CONFIGS_PATH / 'filtration.yml'
}


CONFIG = {section:load_yml(path) \
        for (section, path) in CONFIG_FILES_PATHS.items()}


FILTER_QUERY = build_query_tree(CONFIG['filtration_rules'])

