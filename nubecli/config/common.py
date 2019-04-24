
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

