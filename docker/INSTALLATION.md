# How to install Docker

## Installation

Docker toolbox is good, but may have an old version of docker-machine.
Thus, the recommended choice is to install docker-for-your-system.


### Windows

**You may install one or both of the choices below:**
- Download and install [Docker Toolbox](https://www.docker.com/products/docker-toolbox)
- Download and install stable version of [Docker for Windows](https://docs.docker.com/docker-for-windows/)

### Mac OS X

**You may install one or both of the choices below:**
- Download and install [Docker Toolbox](https://www.docker.com/products/docker-toolbox)
- Download and install stable version of [Docker for Mac](https://docs.docker.com/docker-for-mac/)


### Linux

Install [Docker Engine](https://docs.docker.com/engine/installation/)  
Install [Docker Compose](https://docs.docker.com/compose/install/)  
Install [Docker Machine](https://docs.docker.com/machine/install-machine/)


## Verify Installation

Docker-toolbox may install machine version 0.8.0. It is not sufficient.  
**IMPORTANT:** Versions must be equal or greater than these:
```
docker --version
Docker version 1.12.1, build 6f9534c
docker-machine --version
docker-machine version 0.8.1, build 41b3b25
docker-compose --version
docker-compose version 1.8.0, build f3628c7
```

**Verify that docker-machine works:**
```
docker-machine create -d virtualbox slave

eval $(docker-machine env slave)

docker version
Client:
 Version:      1.12.1
 API version:  1.24
 Go version:   go1.7.1
 Git commit:   6f9534c
 Built:        Thu Sep  8 10:31:18 2016
 OS/Arch:      darwin/amd64

Server:
 Version:      1.12.1
 API version:  1.24
 Go version:   go1.6.3
 Git commit:   23cf638
 Built:        Thu Aug 18 17:52:38 2016
 OS/Arch:      linux/amd64

docker run hello-world

docker-machine rm -f slave
```

You are ready for training.

Godspeed.
