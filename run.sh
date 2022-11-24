#!/usr/bin/env bash

docker stop testmanian
docker rm testmanian
docker run -d  --name testmanian  --net=host  -e testmanian_cfg=/work/testmanian/config.yaml  -v /work:/work py:testmanian --timeout 15

