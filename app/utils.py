import warnings
import yaml

# todo: add validation
def update_config(config, update, file_path):
    updated = {**config, **update}

    with open(file_path, 'w+') as file:
        file.write(yaml.dump(updated))

    config = updated


def load_yml(filepath):
    with open(filepath, 'r') as stream:
        return yaml.safe_load(stream)


def validate_presence(data, necessary_attrs):
    keys = data.keys()
    for attr in necessary_attrs:
        if attr not in keys:
            raise Exception(f'No "{attr}" attribute in credentials file')


