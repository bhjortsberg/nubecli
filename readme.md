# nubecli - cloud command line tool

A command line tool for managing virtual private servers (i.e. Cloud instances).

The tool can list, start, stop, delete and create nodes for different cloud
providers. To ease creation of node it is also possible to search for available
images.

## Supported providers

Currently Amazon Web Services (AWS) has full support, Digital Ocean is partly
supported.


# Install

Clone the repo and run `make install`

```
$ git clone <repo>
$ cd nubecli
$ make install
```


# Usage

The wanted operation is passed as a command to the tool. The help usage
shows the available commands.

```
$ nubecli -h
usage: nubecli [-h] Command ...

Manages nodes in cloud

optional arguments:
  -h, --help  show this help message and exit

Available commands:
  Command     Description
    list      List nodes (default)
    search    Search images matching name
    create    Create node
    start     Start nodes
    stop      Stop nodes
    delete    Delete nodes
    config    Configure providers
```

Every command has its own help.

```
$ nubecli search -h
usage: nubecli search [-h] image_name

positional arguments:
  image_name  Image name to search for, wildcards allowed

optional arguments:
  -h, --help  show this help message and exit
```

# Configuration

In order to use the tool the first thing to do is to configure provider(s).
Just do `nubecli config` and there will be a 'wizard' that guides through the
the configuration. If no configuration exist the config wizard will start
automatically when running the tool.

The configuration file is stored in `~/.config/nubecli.conf`.

## Profiles

A provider can have multiple profiles. This is useful if you have multiple
accounts at one provider.

## Example: Configuring AWS provider

For every provider you need some kind of API key. The keys needed differ
between cloud providers. For AWS you need something Amazon calls
`Access Key Id` and `Secret Access Key`. You find them in your account
information page.

```
$ nubecli config
Add provider (l to list available providers): l
Available providers:
aws, digital_ocean

Add provider (l to list available providers): aws
Configure AWS profiles:
Profile name (l to list existing profiles): l
Profiles:

Profile name (l to list existing profiles): default
access key id: <access_key_id>
secret access key: <secret_access_key>
default region: eu-central-1
Configure/modify more provider(s)? (y/n): n
$
```

# Running nubecli

Example: list nodes

```
$ nubecli
Profile               Node                     IPs               State      Created
digital_ocean:default test-node                111.222.33.44     running    2018-12-28T10:39:23+00:00
```


# Why the name nubecli

Nube is Spanish for cloud, then appended with cli which of course is a short
for Command Line Interface.

