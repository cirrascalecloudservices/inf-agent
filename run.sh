#!/bin/sh -ex
docker run -it --net=host -e WORKER_APIKEY=${WORKER_APIKEY?} $(docker build -q .)
