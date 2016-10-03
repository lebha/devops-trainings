# Openstack command line example

## Prerequisites

- [Python2.7](https://www.python.org/downloads/)


## Recommended

- virtualenv: `pip install virtualenv`


## Create Python virtualenv (Optional)

NOTE: Working directory must be the folder where this README is located.

```
virtualenv venv-clients
source venv-clients/bin/activate
```

After the script, virtualenv is activated. To exit virtualenv:

```
deactivate
```

## Install OpenStack Python clients

```
pip install -r requirements.txt
```

## Create a network from command line

**Edit** your info into example-openrc.sh **and** source it:

```
source example-openrc.sh
```

Generate keypair: `nova keypair-add cmd > cmd.key`
Set permissions: `chmod 600 cmd.key`
Set keypair name in env: `export OS_KEYPAIR_NAME=cmd`

Create or delete network with neutron command line client:
```
./create_network.sh
./delete_network.sh
```

Launch or remove instance:
```
./launch_instance.sh
./remove_instance.sh
```

Godspeed.