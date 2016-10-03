#!/bin/bash

set -e

INT_NET_ID=a2a84887-4915-42bf-aaff-2b76688a4ec7

neutron net-create \
    os-network

neutron subnet-create \
    --ip-version 4 \
    --dns-nameserver 195.74.0.47 \
    --dns-nameserver 195.197.54.100 \
    --enable-dhcp \
    --subnetpool tenant-subnetpool4 \
    --name os-subnet \
    os-network

SUBNET_ID=$(neutron subnet-show os-subnet --field id -f value) 

neutron router-create \
    os-router

ROUTER_ID=$(neutron router-show os-router --field id -f value)

# params router-id subnet-id
neutron router-interface-add \
    $ROUTER_ID \
    $SUBNET_ID

# params router-id ext_net-id
neutron router-gateway-set \
    $ROUTER_ID \
    $INT_NET_ID
