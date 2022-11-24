#!/bin/bash
git clone https://github.com/pydeveloper-t/testmanian.git .
cd ./testmanian
mkdir /work/testmanian
cp ./config.yaml /work/testmanian
sh ./build_docker.sh
docker_image_name="py:testmanian"
docker stop $(docker ps -a -q --filter ancestor=$docker_image_name)
docker rm $(docker ps -a -q --filter ancestor=$docker_image_name)
docker rmi -f $docker_image_name
docker build -t $docker_image_name --no-cache .
