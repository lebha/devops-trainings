# Openstack command line example

## Create a network from command line

Download your openrc V3 file from [OpenStack](https://api.elisa-sdc.fi/dashboard/project/access_and_security/) and source it:

```
source my-openrc.sh
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