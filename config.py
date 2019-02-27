import json
from pathlib import Path

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

CONFIG_FILE_FULL_PATH = Path.joinpath(Path.home(), Path(".config/ccli.conf"))


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
    for provider in config['providers']:
        drivers += provider_driver[provider['name']](provider)

    return drivers

def get_aws_driver(aws_config):
    drivers = []
    d = get_driver(Provider.EC2)
    for profile in aws_config['profiles']:
        data = profile['data']
        access_key_id = data['access_key_id']
        secret_access_key = data["secret_access_key"]
        # TODO: how to handle region, part of config?
        drivers.append(d(access_key_id, secret_access_key, region='eu-central-1'))

    return drivers

def get_digital_ocean_driver(digital_ocean_config):
    drivers = []
    d = get_driver(Provider.DIGITAL_OCEAN)
    for profile in digital_ocean_config['profiles']:
        data = profile['data']
        access_token = data['access_token']
        drivers.append(d(access_token, api_version='v2'))

    return drivers

provider_driver = \
    {
     'aws': get_aws_driver,
     'digital_ocean': get_digital_ocean_driver
    }


def get_configuration(configuration, provider_name):
    p = [provider for provider in configuration['providers'] if provider['name'] == provider_name]
    return p[0]


def config_aws(configuration):
    try:
        provider = get_configuration(configuration, 'aws')
    except (KeyError,TypeError) as e:
        # No config exists, add a default one with empty profile
        provider = {'name':'aws', 'profiles': []}
        configuration = {'providers': [provider]}
    except IndexError as e:
        # This provider does not exist, perhaps other does
        provider = {'name':'aws', 'profiles': []}
        providers = configuration['providers']
        providers.append(provider)

    print("Configure AWS profiles:")
    def config_data():
        access_key_id = input('access key id: ')
        secret_access_key = input('secret access key: ')
        data = {'access_key_id': access_key_id, 'secret_access_key': secret_access_key}
        return data

    configure_profiles(provider, config_data)

    return configuration


def config_digital_ocean(configuration):
    try:
        provider = get_configuration(configuration, 'digital_ocean')
    except (KeyError,TypeError) as e:
        # No config exists, add a default one with empty profile
        provider = {'name':'digital_ocean', 'profiles': []}
        configuration = {'providers': [provider]}
    except IndexError as e:
        # This provider does not exist, perhaps other does
        provider = {'name':'digital_ocean', 'profiles': []}
        providers = configuration['providers']
        providers.append(provider)


    print("Configure DigitalOcean:")
    def config_data():
        access_token = input('access token: ')
        data = {'access_token': access_token}
        return data

    configure_profiles(provider, config_data)

    return configuration


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


provider_config = \
    {
        'aws': config_aws,
        'digital_ocean': config_digital_ocean
    }

def configure_provider(provider, configuration):
    try:
        config = provider_config[provider](configuration)
        return config
    except NotImplementedError as e:
        print(f"{e}")
    except KeyError as e:
        print(f"{e}")

    return None
