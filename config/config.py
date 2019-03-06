import json
from pathlib import Path

from config.aws_config import get_aws_driver, config_aws
from config.digital_ocean_config import (get_digital_ocean_driver,
                                         config_digital_ocean)


CONFIG_FILE_FULL_PATH = Path.joinpath(Path.home(), Path(".config/ccli.conf"))

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


def get_configuration(configuration, provider_name):
    p = [provider for provider in configuration['providers'] if provider['name'] == provider_name]
    return p[0]


def configure_profiles(provider, config_data):
    while True:
        profile_name = input('Profile name (l to list existing profiles): ')
        if profile_name == 'l':
            profiles_str = ", ".join([p['name'] for p in provider['profiles']])
            print("Profiles: " + profiles_str + "\n")
        else:
            break

    p = [profile for profile in provider['profiles'] if profile['name'] == profile_name]
    if len(p) > 0:
        profile = p[0]
        ans = input("Profile exists. Overwrite, delete or cancel (o,d,c)? ")
        if ans == 'o':
            profile['data'] = config_data()
        elif ans == 'd':
            provider['profiles'].remove(profile)
        elif ans == 'c':
            # Need to remove the provider again
            #abort = True
            pass

    else:
        # This profile did not exist, create one
        data = config_data()
        profile = {'name': profile_name, 'data': data}
        # and append to providers profiles
        provider['profiles'].append(profile)


def configure_provider(provider, configuration):
    try:
        config = provider_config[provider](configuration)
        return config
    except NotImplementedError as e:
        print(f"{e}")
    except KeyError as e:
        print(f"{e}")

    return None
