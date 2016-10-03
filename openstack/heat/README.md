# OpenStack Heat Example

## Create Network and Server with heat
1. Set heat stack name, examples: `export OS_STACK_NAME=test-stack`
2. Generate access keys for the stack:
     - generate new rsa key (or use existing), example: `ssh-keygen -t rsa -b 4096 -N "" -f ${OS_STACK_NAME}.key`
     - `export PUBLIC_KEY="$(cat ${OS_STACK_NAME}.key.pub)"`
     - add private key to ssh agent: `ssh-add ${OS_STACK_NAME}.key`
3. Launch the stack:   
    ```
    openstack stack create -t stack.yml \
        --parameter "keypair_name=${OS_STACK_NAME}" \
        --parameter "public_key=${PUBLIC_KEY}" \
        ${OS_STACK_NAME}
    ```
4. Access instance: `ssh -i ${OS_STACK_NAME}.key "sdc-user@"$(openstack stack output show -c output_value -f value $OS_STACK_NAME floating_ip)`

## Stack updates

Stacks can be updated by modifying the file and using 

## Advanced examples

For more advanced stack examples, see [kubernetes](https://github.devcloud.elisa.fi/sdc/kubernetes/tree/release-1.3.6) heat stacks

## Exercise

Prerequisites: create the stack

Try modifying stack.yml to allow traffic to port 80 and update stack:
```
openstack stack update -t stack.yml \
    --parameter "keypair_name=${OS_STACK_NAME}" \
    --parameter "public_key=${PUBLIC_KEY}" \
    ${OS_STACK_NAME}
```
Verify in horizon that security group has allowed access.
Optionally, you can run nginx with docker easily (connect with ssh first):
```
sudo yum update -y
sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
sudo yum install -y docker-engine
sudo systemctl start docker
sudo docker run -d -p 80:80 nginx
```

**Verify:**
You can verify that nginx is running with browser or with curl. 
First close ssh connection: `exit`
Get machine ip: `openstack stack output show -c output_value -f value $OS_STACK_NAME floating_ip`
Browser: try the ip
Curl: `curl $(openstack stack output show -c output_value -f value $OS_STACK_NAME floating_ip)`


## Cleanup

```
openstack stack delete $OS_STACK_NAME
```

