from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from nubecli.config.common import get_configuration, configure_profiles

def get_digital_ocean_driver(digital_ocean_config):
    drivers = []
    profiles = []
    d = get_driver(Provider.DIGITAL_OCEAN)
    for profile in digital_ocean_config['profiles']:
        profiles.append(profile['name'])
        data = profile['data']
        access_token = data['access_token']
        drivers.append(d(access_token, api_version='v2'))

    return drivers, profiles


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


