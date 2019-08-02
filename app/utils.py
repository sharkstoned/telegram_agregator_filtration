import warnings
import yaml

# todo: add validation
def update_config(config, update, filepath):
    updated = {**config, **update}

    with filepath.open(mode='w+') as file:
        file.write(yaml.dump(updated))

    config = updated


def load_yml(filepath):
    with filepath.open(mode='r') as stream:
        return yaml.safe_load(stream)


def validate_presence(data, necessary_attrs):
    keys = data.keys()
    for attr in necessary_attrs:
        if attr not in keys:
            raise Exception(f'No "{attr}" attribute in credentials file')


