#!/usr/bin/python

import os
import subprocess

from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client as nova_client
from novaclient.exceptions import NotFound


class OpenStackLib(object):

    def __init__(self):
        authurl = os.environ['OS_AUTH_URL']
        if not authurl.endswith('/v3'):
            authurl += '/v3'
        auth = v3.Password(auth_url=authurl,
                           username=os.environ['OS_USERNAME'],
                           password=os.environ['OS_PASSWORD'],
                           project_name=os.environ['OS_PROJECT_NAME'],
                           user_domain_name=os.environ['OS_USER_DOMAIN_NAME'],
                           project_domain_name=os.environ['OS_USER_DOMAIN_NAME'])
        sess = session.Session(auth=auth)
        self.nova = nova_client.Client("2.8", 
                                  session=sess, 
                                  region_name=os.environ['OS_REGION_NAME'])
        
    def list_servers(self):
        return self.nova.servers.list()

    def get_flavor_id(self, name):
        flavors = self.nova.flavors.list()
        for i in range(len(flavors)):
            if name == flavors[i].name:
                return flavors[i].id
        raise Exception('Flavor %s id not found' % name)

    def create_server(self, *args, **kwargs):
        return self.nova.servers.create(*args, **kwargs)

def main():
    stack_name = os.environ['OS_STACK_NAME']
    subnet_id = subprocess.check_output(['openstack', 'stack', 'output', 'show', '-c', 'output_value', '-f', 'value', stack_name, 'subnet_id'])
    print subnet_id
    network_id = '33df3faf-bb46-4ce2-ace3-5fca7ead9659'
    subnet_id = "89b01de5-a61d-4fc6-a3a6-838c7dad03f3"
    key_name = stack_name
    lib = OpenStackLib()
    servers = lib.list_servers()
    print servers
    # lib.create_port(network_id, subnet_id)
    nics = [
            {
                "net-id":network_id,
                "fixed_ips": [
                    {
                        'subnet_id':subnet_id
                    }
                ]
            }
    ]

    lib.create_server('myserver',
                      image='80808c52-764e-48c1-aa15-6519781065dc',
                      flavor=lib.get_flavor_id('m1.small'),
                      security_groups=['457e5ff4-ae18-4429-bf84-2ef229a3c4d6'],
                      key_name=key_name,
                      availability_zone='zone-1',
                      nics=nics)
    # for s in servers:
    #     if s.name == 'myserver':
    #         s.delete()

if __name__ == '__main__':
    main()
