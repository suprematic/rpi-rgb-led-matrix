# 7C M1

## On the Build Server

### Set up cross building of ARM images

```shell
sudo apt install qemu-user-static
docker buildx create --name rpi
docker buildx use rpi
docker buildx inspect --bootstrap
```

### Build

```shell
git clone https://github.com/suprematic/rpi-rgb-led-matrix.git \
    --branch='7c/m1/dev' \
    --depth=1 \
    7c

cd c7

git clone https://bitbucket.org/suprematic/rpi-rgb-led-matrix-7c.git \
    --branch='master' \
    --depth=1 \
    bindings/python/7c

docker buildx build --platform linux/arm64 -t 7c . --output='type=oci,dest=./7c.oci'
```

Copy the image to the Raspberry PI.

## On Raspberry

Install Docker

```shell
apt-get install \
    -y \
    apt-transport-https \
    ca-certificates \
    software-properties-common
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
curl https://download.docker.com/linux/raspbian/gpg \
    -o /usr/share/keyrings/docker.gpg
echo 'deb [arch=arm64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/raspbian bullseye stable' >> /etc/apt/sources.list.d/docker.list 
apt-get update
apt-get upgrade
systemctl start docker.service

## Check the installation:

docker info
```

Load the image into the local Docker registry

```shell
docker load < 7c.oci
```

Tag the image

```shell
docker tag <image-hash> 7c
```

Run the docker container

```shell
docker run --rm --privileged -it 7c
```
