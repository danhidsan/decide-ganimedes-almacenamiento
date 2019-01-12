#!/bin/bash
echo "$DOCKER_HUB_PASS" | docker login -u "$DOCKER_HUB_USER" --password-stdin
docker build ./docker
docker tag decide_web danhidsan/decide_web
docker push danhidsan/decide_web