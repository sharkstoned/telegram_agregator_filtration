import os
import yaml

from utils import load_yml


PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


ENV_FILES_PATHS = {
    'creds': os.path.join(PROJECT_ROOT, 'env', 'creds.yml'),
    'filtration_rules': os.path.join(PROJECT_ROOT, 'env', 'filtration.yml')
}


ENV = {section:load_yml(path) for (section,path) in ENV_FILES_PATHS}

