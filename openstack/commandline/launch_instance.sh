#!/bin/bash

if [[ -z $OS_KEYPAIR_NAME ]]; then
    echo "Please export OS_KEYPAIR_NAME and try again"
    exit 1
fi

INT_NET_ID=a2a84887-4915-42bf-aaff-2b76688a4ec7

server_name='instance'
flavor_name='m1.small'
image_name='phs-centos7-cloudimage-latest'
network_name='os-network'
pool_name='int-net'


openstack server create \
    --image $image_name \
    --flavor $flavor_name \
    --key-name $OS_KEYPAIR_NAME \
    --nic net-id=${network_name} \
    $server_name
