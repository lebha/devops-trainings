# Elisa Docker Training

## Before Training
Prepare yourself by [installing Docker](INSTALLATION.md)

## Terms

Docker has two important entities to know.

### Images

A docker image is a definition of a container. It contains a base operating system and a filesystem on top of that.
The Definition of an image is called Dockerfile.

### Containers

A docker container is an instance of an image. When you run a container you basically launch an instance of your image.

## Docker Architecture Fundamentals

Docker consists of two components, client and server. Typical aliases for server are engine and daemon, but they all mean the same.
Docker works differently on different operating systems. On linux, docker server and client both run in localhost. On Mac OS X and Windows
docker client runs on localhost but you must create a virtual machine for the server. For this, we are going to use docker-machine.

## Docker Machine Guide

Docker Machine creates virtual machines and runs docker server on them. For an example, let's run a machine on virtualbox:
```
docker-machine create -d virtualbox slave
```
Docker Machine can use many different drivers. For example, you can just as well provision a docker server in Elisa SDC OpenStack.
We selected driver virtualbox with the -d (--driver) option. The name of the machine is slave, but could just as well be any other name of your choice.

After creating a machine, you must tell docker client where the server is running. The configuration happens in practice by setting environment variables.
You can print the necessary environment variable configuration for any virtual machine you have created with docker-machine by their name: `docker-machine env slave`.
Note that this command does not do anything, just prints the configuration for you.

You can set the environment variables by evaluating the output of the env command: `eval $(docker-machine env slave)`

Now the docker client knows that it has to pass any commands (via TCP) to the virtual machine that you created.

## Running Containers

At any time, you can check the commands that docker provides by:
```
docker help
```

Use `docker run` to run containers. For an example, you can instantly run nginx:
```
docker run -d --name mynginx nginx
```
We ran a container with name mynginx that is based on an image called nginx.
Nginx is an official docker image, publicly downloadable from [docker hub](https://hub.docker.com/). When you told your docker client to run nginx,
the docker server searched docker hub for an image with name nginx, downloaded it (on the virtual machine), and launched a container based on that image. The official nginx image
documentation is [here](https://hub.docker.com/_/nginx/).

**Modes:**
You can run docker containers in two different modes:
Here, we specified (with option -d) that we'd like to run nginx in **detached mode**. This means that it runs in the background and we do not see 
the stdout of the container.
The alternative is to run in **interactive mode** and allocating a text terminal (with options -it). This way you can see the stdout. Pressing ctrl+C will stop it.
To see stdout of detached containers, use `docker logs`: `docker logs mynginx`

**List containers:**
```
docker ps -a
```

**Stopping and starting containers:**
```
docker stop mynginx
docker start mynginx
```

**Removing a container:**
```
docker rm mynginx
```
Docker prevents removal of running containers. Use -f (--force) option if you want to override.

**Port Forwarding:**
To access a containerized web application we need to use port forwarding. In this example, we forward port 8080 of the docker server into mygninx container's port 80:
```
docker run -d --name mynginx -p 8080:80 nginx
```
Now we can access nginx in the port 8080 of the virtual machine running docker server. Retrieving machine ip: `docker-machine ip slave`. You can try if you can relaunch nginx on host port 80.

## Managing images


**Building your own image:**
It is very rare that you'd have to make a new image without a base. In this example, let's customize the nginx image. For this you must create a Dockerfile in this folder.
First, we want to start building on top of the official nginx image. Insert to Dockerfile:
```
FROM nginx
```
Second, we'd probably like to change our page to be the index page in nginx. For this, create a file called `index.html` and insert some valid html, like:
```
<p>This is my page</p>
```
Then, we must override the official index page with our own in Dockerfile:
```
COPY index.html /usr/share/nginx/html/index.html
```

Build your image and tag (-t) it with a name:
```
docker build -t custom-nginx .
```
The dot (this folder) is the build target. In this case, it tells docker to build an image based on the Dockerfile and files in this folder.

Run a container based on your custom image:
```
docker run -d --name mynginx -p 80:80 custom-nginx
```

**List images:**
```
docker images
```

**Removing images:**
```
docker rmi custom-nginx
```

**Downloading and uploading images:**
```
docker pull alpine
docker tag alpine myname/alpine
docker push myname/alpine # requires account at dockerhub
```

**Using Elisa docker registry:**
https://github.devcloud.elisa.fi/sdc/docker-auth/blob/master/docs/USAGE.md

## Volume mounts
In the build example we overrode image content at build time. As a result, all containers launched from our custom image have a custom index page.
Alternatively, we might want to override content at runtime. This can be achieved with a volume mount.
```
docker run -d --name mynginx -p 80:80 -v $(pwd)/index.html:/usr/share/nginx/html/index.html:ro nginx
```
We mount our index page into the official nginx container at runtime. The mount is read only (ro), so the container may not modify the file. Use
read write (rw) to give container write permissions on mounts. Mount sources only accept absolute paths.

## Mounting docker socket

Is known in web as Docker outside of Docker (DooD).
Alternatively, it is possible to run docker daemon in docker (DinD), but it's hasardous and can cause data corruption.


In very advanced setup, you might want to mount your docker socket. In practice, this means that the container can command docker to create images and sibling containers on the host.
To try this, make a file jenkins_dockerfile with content:
```
FROM jenkins

USER root
RUN apt-get update \
      && apt-get install -y sudo docker.io \
      && rm -rf /var/lib/apt/lists/*
RUN echo "jenkins ALL=NOPASSWD: ALL" >> /etc/sudoers
 
USER jenkins
RUN /usr/local/bin/install-plugins.sh git \
 && /usr/local/bin/install-plugins.sh robot \
 && /usr/local/bin/install-plugins.sh ansible
```

Build and run the custom jenkins image:
```
docker build -t myjenkins -f jenkins_dockerfile .
docker run -d -p 8080:8080 -p 50000:50000 --name myjenkins -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock myjenkins
```
Use `docker logs myjenkins` to retrieve admin password.
Access jenkins at `docker-machine ip slave` port 80.


```
Now you can use docker in containerized jenkins jobs (with sudo)
```

Volume mounts are a bit tricky with mounted daemons. The source lookup is done at the host, not inside the container. Example:

**Create a freestyle project called 'test'. Add 'execute shell' step:**
```
mkdir -p html
cat <<'EOF' > html/index.html
<p>mypage</p>
EOF
sudo docker run -d --name mynginx -v /var/lib/docker/volumes/jenkins_home/_data/workspace/test/html/:/usr/share/nginx/html/:ro -p 80:80 nginx
```

Cleanup:
```
docker rm -f myjenkins
docker volume ls
docker volume rm jenkins_home
```

## Docker Compose

Docker Compose can be used to launch an entire application of multiple containers at once.

[Docker Compose Instructions](docker_compose)

## Docker Swarm

Docker Swarm is a simple container orchestration tool for running containers in a cluster of machines.

[Docker Swarm Instructions](docker_swarm)

## Final Notes

The recommended platform for running applications at Elisa is [Kubernetes](http://kubernetes.io/).

Kubernetes is part of these trainings: [Training Material](../kubernetes).
For Kubernetes installation and usage, please check out [Elisa SDC Kubernetes Repository](https://github.devcloud.elisa.fi/sdc/kubernetes)




