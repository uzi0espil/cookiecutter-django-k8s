#!/bin/bash

IMAGE_TAG=${1:-"latest"}

images=$(docker-compose -f production.yml config | grep 'image: ' | cut -d':' -f 2 | tr -d '"')
for image in $images
do
  docker tag "${image}" "${image}":"${IMAGE_TAG}"
  docker push "${image}":"${IMAGE_TAG}"
done
