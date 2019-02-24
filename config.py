import json
from pathlib import Path

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

CONFIG_FILE_FULL_PATH = Path.joinpath(Path.home(), Path(".config/ccli.conf"))

provider_driver =
    {'aws': get_aws_driver,
     'digital_ocean': get_digital_ocean_driver
    }

def read_config():
    config_content = None
    config_file = CONFIG_FILE_FULL_PATH
    with open(config_file) as config:
        config_content = json.load(config)

    return config_content

def write_config(config):
    config_file_name = CONFIG_FILE_FULL_PATH
    with open(config_file_name) as config_file:
        # serialize json to config_file
    
def get_cloud_drivers(config):
    drivers = []
    for provider in config['provider']:
        drivers.append(provider_driver[provider.name](provider))

    return drivers

def get_aws_driver(aws_config):
    d = get_driver(Provider.EC2)
    access_key_id = aws_config["access_key_id"]
    access_key = aws_config["access_key"]
    # TODO: how to handle region, part of config?
    return d(access_key_id,  access_key, region='eu-central-1')

def get_digital_ocean_driver(digital_ocean_config):
    pass 

