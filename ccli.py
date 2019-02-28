import argparse
from pathlib import Path
from libcloud.compute.base import NodeImage
from libcloud.compute.base import NodeAuthSSHKey

from config import (read_config, write_config,
                    get_cloud_drivers, get_providers,
                    configure_provider)



def read_aws_credentials(profile):
    credentials_file = Path.joinpath(Path.home(), Path(".aws/credentials"))
    profile_found = False
    access_key_id = None
    access_key = None
    with open(credentials_file) as credentials:
        for line in credentials:
            if profile_found:
                data = line.split(' = ')
                if data[0].strip(' ') == 'aws_access_key_id':
                    access_key_id = data[1].strip('\n')
                if data[0] == 'aws_secret_access_key':
                    access_key = data[1].strip('\n')
            if not profile_found:
                profile_found = profile in line
            if access_key_id and access_key:
                break

    if not (access_key_id and access_key):
        raise Exception(f"Failed to read credentials from {credentials_file}")

    return access_key_id, access_key



def list_nodes(drivers, args):
    
    nodes = [node for driver in drivers for node in driver.list_nodes()]
    heading=["Node","IPs","State","Created"]
    row_fmt = "{:<10}{:<35}{:<18}{:<11}{:<25}"
    print(row_fmt.format("Provider", *heading))

    count = 1

    for node in nodes:
        ip = ",".join(ip for ip in node.public_ips)
        data = [node.name, ip, node.state, node.created_at.isoformat()]
        print(row_fmt.format(f"{count}", *data))
        count += 1

def stop_node(drivers, args):

    nodes = [node for driver in drivers for node in driver.list_nodes()]
    name = args.node
    try:
       for node in nodes:
           if name == node.name:
               print("Stopping node...")
               driver.ex_stop_node(node)
    except Exception as e:
        print({e})

def start_node(driver, args):

    nodes = [node for driver in drivers for node in driver.list_nodes()]
    name = args.node

    try:
        for node in nodes:
            if name == node.name:
                print("Starting node...")
                driver.ex_start_node(node)
    except Exception as e:
        print(f"{e}")

def delete_node(driver, args):

    nodes = [node for driver in drivers for node in driver.list_nodes()]
    name = args.node
    ans = input(("This will delete the node, all data will be lost."
                " Are you sure you want to delete:") + f" \"{name}\" (y/n): ")
    if 'n' in ans:
        print("Ok, not doing anything!")
        return

    try:
       for node in nodes:
           if name == node.name:
               print("Deleting node...")
               driver.destroy_node(node)
    except Exception as e:
        print(f"{e}")

def search_image(drivers, args):

    providers = get_providers()
    provider_list = ", ".join([provider for provider in providers])
    driver_name = input("Search on provider {provider_list}")
    image_name = args.image_name.lower()
    images = driver.list_images(ex_filters={'name': image_name})
    for image in images:
        print(image.name)

def create_node(driver, args):

    # Need a NodeImage 
    # https://libcloud.readthedocs.io/en/latest/compute/api.html#libcloud.compute.base.NodeImage
    image = driver.list_images(ex_filters={'name': args.image_name})
    locations=driver.list_locations()
    while True:
        node_type = input("Node size (l for list of size types): ")
        if node_type == 'l':
            size_list = (size.id for size in driver.list_sizes(location=locations[0]))
            for size in size_list:
                print(size)
        else:
            break
    sizes = [size for size in driver.list_sizes() if size.id == node_type]
    print(sizes)


    while True:
        key_pair = input("Key pair (l for list for key pairs): ")
        if key_pair == 'l':
            key_list = (key.name for key in driver.list_key_pairs())
            for key in key_list:
                print(key)
        else:
            break

    name = input('Node name: ')
    try:
        print(f"Creating node \"{name}\"...")
        driver.create_node(name=name, ex_keyname=key_pair, ex_assign_public_ip=True, image=image[0], size=sizes[0])
        print("Node created!")
    except Exception as e:
        print(f"{e}")

def configure(args, configuration):

    providers = get_providers()

    while True:
        p = input("Add provider (l to list available providers): ")
        if p == 'l':
            print("Available providers:\n%s\n" % ", ".join([provider for provider in providers]))
            continue

        new_configuration = configure_provider(p, configuration)
        if not new_configuration:
            # Perhaps raise instead
            print(f"Failed to configure provider \"{p}\"")
            return
        write_config(new_configuration)
        ans = input('Configure/modify more provider(s)? (y/n): ')
        if ans != 'y':
            break


def main():
    argp = argparse.ArgumentParser(description="Manages nodes in cloud")
    sargp = argp.add_subparsers(title="Available commands", metavar="Command", help="Description", dest='command')
    argp.add_argument('--profile', default="default", help="Profile to use for credentials")
    list_parser = sargp.add_parser('list', help="List nodes (default)")
    list_parser.set_defaults(func=list_nodes)

    search_parser = sargp.add_parser('search', help="Search images matching name")
    search_parser.add_argument('image_name', help="Image name to search for, wildcards allowed")
    search_parser.set_defaults(func=search_image)

    create_parser = sargp.add_parser('create', help="Create node")
    create_parser.add_argument("image_name", help="Image name")
    create_parser.set_defaults(func=create_node)

    start_parser = sargp.add_parser('start', help="Start nodes")
    start_parser.add_argument('node', help="Node name")
    start_parser.set_defaults(func=start_node)

    stop_parser = sargp.add_parser('stop', help="Stop nodes")
    stop_parser.add_argument('node', help="Node name")
    stop_parser.set_defaults(func=stop_node)

    delete_parser = sargp.add_parser('delete', help="Delete nodes")
    delete_parser.add_argument('node', help="Node name")
    delete_parser.set_defaults(func=delete_node)

    config_parser = sargp.add_parser('config', help="Configure providers")
    config_parser.set_defaults(func=configure)

    args = argp.parse_args()

    configuration = read_config()
    
    if not configuration or args.command == "config":
        configure(args, configuration)
        return

    try:
        drivers = get_cloud_drivers(configuration)
        if args.command:
            args.func(drivers, args)
        else:
            list_nodes(drivers, args)
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    main()

