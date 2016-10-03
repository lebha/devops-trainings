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

    def get_image_id(self, name):
        images = self.nova.images.list()
        for i in range(len(images)):
            if name == images[i].name:
                return images[i].id
        raise Exception('Image %s id not found' % name)

    def create_server(self, *args, **kwargs):
        return self.nova.servers.create(*args, **kwargs)


def get_stack_output(stack_name, output_name):
    return subprocess.check_output(['openstack', 'stack', 'output', 'show', '-c', 'output_value', '-f', 'value', stack_name, output_name]).strip('\n')

