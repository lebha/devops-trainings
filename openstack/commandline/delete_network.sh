#!/bin/bash

set -e

SUBNET_ID=$(neutron subnet-show os-subnet --field id -f value)

neutron router-interface-delete os-router $SUBNET_ID
neutron router-delete os-router
neutron net-delete os-network