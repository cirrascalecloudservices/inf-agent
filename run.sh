#!/bin/sh -ex
docker run -it --net=host -e FROM=${FROM?} -e TO=${TO?} -e WORKER_APIKEY=${WORKER_APIKEY?} $(docker build -q .)
