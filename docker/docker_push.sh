#!/bin/bash
echo "$DOCKER_HUB_PASS" | docker login -u "$DOCKER_HUB_USER" --password-stdin
echo "Building Decide image"
docker build ./docker
docker tag decide_web danhidsan/decide_web
echo "Upload changes to Docker Hub"
docker push danhidsan/decide_web
echo "Image updated in Docker Hub"