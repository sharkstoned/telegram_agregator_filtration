import warnings
import yaml

from settings import ENV, ENV_FILES_PATHS


class InvalidDataWarning(UserWarning):
    pass


# todo: rewrite abstract
def update_creds(data):
    # data validation
    for key, value in data.items():
        if value is None:
            warnings.warn(f'Credentials were not updated'
	        	  'due to incorrect data: "{key}" must not be None',
			  InvalidDataWarning)
            return
        if value == '':
            warnings.warn(f'Credentials were not updated'
	        	  'due to incorrect data: "{key}" must not be an empty string',
			  InvalidDataWarning)
            return

    updated = {**ENV['creds'], **data}

    with open(ENV_FILES_PATHS['credentials'], 'w+') as file:
        file.write(yaml.dump(updated))

    ENV['creds'] = updated


def load_yml(filepath):
    with open(filepath, 'r') as stream:
        return yaml.safe_load(stream)


def validate_presence(data, necessary_attrs):
    keys = data.keys()
    for attr in necessary_attrs:
        if attr not in keys:
            raise Exception(f'No "{attr}" attribute in credentials file')


def filtrate(rules, data):
    pass


def parse_message(body):

