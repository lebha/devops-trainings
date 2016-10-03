from openstacklib import OpenStackLib, get_stack_output

import os
import argparse

def create(instance_name):
    stack_name = os.environ['OS_STACK_NAME']
    network_id = get_stack_output(stack_name, 'network_id')
    subnet_id = get_stack_output(stack_name, 'subnet_id')
    security_group_id = get_stack_output(stack_name, 'security_group_id')
    key_name = get_stack_output(stack_name, 'keypair_name')
    
    lib = OpenStackLib()

    print lib.list_servers()

    nics = [
        {
            'net-id': network_id,
            'fixed_ips': [
                {
                    'subnet_id':subnet_id
                }
            ]
        }
    ]
    print instance_name
    lib.create_server(name='kala',
                      image=lib.get_image_id('phs-centos7-cloudimage-latest'),
                      flavor=lib.get_flavor_id('m1.small'),
                      security_groups=[security_group_id],
                      key_name=key_name,
                      availability_zone='zone-1',
                      nics=nics)

def delete(instance_name):
    lib = OpenStackLib()
    for s in lib.list_servers():
        if s.name == instance_name:
            s.delete()

def main():
    parser = argparse.ArgumentParser(description='Argument Parser')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--create', action='store_true',
                        help='create instance')
    group.add_argument('-d', '--delete', action='store_true',
                        help='delete instance')
    group.add_argument('-l', '--list', action='store_true',
                        help='list instances')
    parser.add_argument('name', nargs='?', type=str, 
                        help='target instance name')
    args = parser.parse_args()
    if args.list:
        lib = OpenStackLib()
        print lib.list_servers()
        return
    elif not args.name:
        parser.print_help()
    elif args.delete:
        delete(args.name)
    elif args.create:
        print repr(args.name)
        create(args.name)

if __name__ == '__main__':
    main()