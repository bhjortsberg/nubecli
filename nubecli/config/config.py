import json
from pathlib import Path

from nubecli.config.aws_config import get_aws_driver, config_aws
from nubecli.config.digital_ocean_config import (get_digital_ocean_driver,
                                                 config_digital_ocean)


CONFIG_FILE_FULL_PATH = Path.joinpath(Path.home(), Path(".config/nubecli.conf"))

provider_driver = \
    {
     'aws': get_aws_driver,
     'digital_ocean': get_digital_ocean_driver
    }

provider_config = \
    {
        'aws': config_aws,
        'digital_ocean': config_digital_ocean
    }

def get_providers():
    return [provider for provider in provider_driver.keys()]

def read_config():
    config_content = None
    config_file = CONFIG_FILE_FULL_PATH
    try:
        with open(config_file) as config:
            config_content = json.load(config)
    except FileNotFoundError as e:
        print(f"No config file found: {e}. Will create a new")

    return config_content

def write_config(config):
    config_file_name = CONFIG_FILE_FULL_PATH
    with open(config_file_name, 'w') as config_file:
        # serialize json to config_file
        json.dump(config, config_file)

def get_cloud_drivers(config):
    drivers = []
    provider_names = []
    for provider in config['providers']:
        name = provider['name']
        d, profiles = provider_driver[name](provider)
        drivers += d
        provider_names += [f"{name}:{p}" for p in profiles]

    return zip(drivers, provider_names)



def configure_provider(provider, configuration):
    try:
        config = provider_config[provider](configuration)
        return config
    except NotImplementedError as e:
        print(f"{e}")
    except KeyError as e:
        print(f"{e}")

    return None
