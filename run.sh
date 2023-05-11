#!/bin/sh -ex
docker run -it -e WORKER_APIKEY=${WORKER_APIKEY?} $(docker build -q .)
