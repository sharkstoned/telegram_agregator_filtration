import os
import yaml

from utils import load_yml
from filtration import build_query_tree


PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


CONFIGS_PATH = os.path.join(PROJECT_ROOT, 'configs')


CONFIG_FILES_PATHS = {
    'creds': os.path.join(CONFIGS_PATH, 'creds.yml'),
    'filtration_rules': os.path.join(CONFIGS_PATH, 'filtration.yml')
}


CONFIG = {section:load_yml(path) for (section, path) in CONFIG_FILES_PATHS.items()}


FILTER_QUERY = build_query_tree(CONFIG['filtration_rules'])

