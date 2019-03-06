from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

def get_aws_driver(aws_config):
    drivers = []
    profiles = []
    d = get_driver(Provider.EC2)
    for profile in aws_config['profiles']:
        profiles.append(profile['name'])
        data = profile['data']
        access_key_id = data['access_key_id']
        secret_access_key = data["secret_access_key"]
        default_region = data["default_region"]
        drivers.append(d(access_key_id, secret_access_key, region=default_region))

    return drivers, profiles


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
        default_region = input('default region: ')
        data = {
            'access_key_id': access_key_id,
            'secret_access_key': secret_access_key,
            'default_region': default_region
            }
        return data

    configure_profiles(provider, config_data)

    return configuration

