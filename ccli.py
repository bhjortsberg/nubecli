import argparse
from pathlib import Path
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver



def get_cloud_driver(access_key_id, access_key):
    d = get_driver(Provider.EC2)
    return d(access_key_id,  access_key, region='eu-central-1')

def read_aws_credentials():
    credentials_file = Path.joinpath(Path.home(), Path(".aws/credentials"))
    with open(credentials_file) as credentials:
        for line in credentials:
            data = line.split(' = ')
            if data[0].strip(' ') == 'aws_access_key_id':
                access_key_id = data[1].strip('\n')
            if data[0] == 'aws_secret_access_key':
                access_key = data[1].strip('\n')

    return access_key_id, access_key



def list_nodes(driver, args):
    
    nodes = driver.list_nodes()
    heading=["Node","IPs","State","Created"]
    row_fmt = "{:<8}{:<35}{:<18}{:<10}{:<25}"
    print(row_fmt.format("Count", *heading))

    count = 1

    for node in nodes:
        ip = ",".join(ip for ip in node.public_ips)
        data = [node.name, ip, node.state, node.created_at.isoformat()]
        print(row_fmt.format(f"{count}", *data))
        count += 1

def stop_node(driver, args):

    nodes = driver.list_nodes()
    name = args.node
    try:
       for node in nodes:
           if name == node.name:
               driver.ex_stop_node(node)
    except Exception as e:
        print({e})

def start_node(driver, args):

    nodes = driver.list_nodes()
    name = args.node

    try:
        for node in nodes:
            if name == node.name:
                driver.ex_start_node(node)
    except Exception as e:
        print({e})

def search_image(driver, args):

    image_name = args.image_name.lower()
    images = driver.list_images(ex_filters={'name': image_name})
    for image in images:
        print(image.name)

def main():
    argp = argparse.ArgumentParser(description="Manages nodes in cloud")
    sargp = argp.add_subparsers(title="Available commands", metavar="Command", help="Description", dest='command')
    list_parser = sargp.add_parser('list', help="List nodes (default)")
    list_parser.set_defaults(func=list_nodes)
    stop_parser = sargp.add_parser('stop', help="Stop nodes")
    stop_parser.add_argument('node', help="Node name")
    stop_parser.set_defaults(func=stop_node)
    start_parser = sargp.add_parser('start', help="Start nodes")
    start_parser.add_argument('node', help="Node name")
    start_parser.set_defaults(func=start_node)
    search_parser = sargp.add_parser('search', help="Search images matching name")
    search_parser.add_argument('image_name', help="Image name to search for, wildcards allowed")
    search_parser.set_defaults(func=search_image)

    args = argp.parse_args()

    access_key_id, access_key = read_aws_credentials()
    driver = get_cloud_driver(access_key_id, access_key)

    if args.command:
        args.func(driver, args)
    else:
        list_nodes(driver, args)

if __name__ == "__main__":
    main()

