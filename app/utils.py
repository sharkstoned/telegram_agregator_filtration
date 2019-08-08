import warnings
import yaml
import logging


logger = logging.getLogger('app')


# todo: add validation
def update_config(config, update, filepath):
    updated = {**config, **update}

    with filepath.open(mode='w+') as file:
        file.write(yaml.dump(updated))
        logger.info(f'Config "{filepath}" is updated')

    config = updated


def load_yml(filepath):
    with filepath.open(mode='r') as stream:
        return yaml.safe_load(stream)


def validate_presence(data, necessary_attrs):
    keys = data.keys()
    for attr in necessary_attrs:
        if attr not in keys:
            logger.error('Data validation failed: No "{attr}" attribute found.')
            raise ValueError(f'No "{attr}" attribute found')


