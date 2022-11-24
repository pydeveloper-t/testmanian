#!/usr/bin/env bash
git clone https://github.com/pydeveloper-t/testmanian.git .
cd ./testmanian
mkdir /work/testmanian
cp ./config.yaml /work/testmanian
sh ./build_docker.sh
docker stop testmanian
docker rm testmanian
docker run -d  --name testmanian  --net=host  -e testmanian_cfg=/work/testmanian/config.yaml  -v /work:/work py:testmanian --timeout 15

