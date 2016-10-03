# Openstack command line example

## Create a network from command line

**Edit** your info into example-openrc.sh **and** source it:

```
source example-openrc.sh
```

Set stack name: `export OS_STACK_NAME=python-stack`
Generate access keys for the stack:
- generate new rsa key (or use existing), example: `ssh-keygen -t rsa -b 4096 -N "" -f ${OS_STACK_NAME}.key`
- `export PUBLIC_KEY="$(cat ${OS_STACK_NAME}.key.pub)"`
- add private key to ssh agent: `ssh-add ${OS_STACK_NAME}.key`

**Create network with heat stack:**
```
openstack stack create -t stack.yml \
    --parameter "keypair_name=${OS_STACK_NAME}" \
    --parameter "public_key=${PUBLIC_KEY}" \
    ${OS_STACK_NAME}
```

**manage instances with python-novaclient:**
```
python manage_instances.py --help
```
