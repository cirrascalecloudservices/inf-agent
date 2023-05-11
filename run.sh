#!/bin/sh -ex
docker run -it --net=host -e PIPELINE_ID=${PIPELINE_ID?} -e WORKER_APIKEY=${WORKER_APIKEY?} -e TO_URL=${TO_URL?} $(docker build -q .)
