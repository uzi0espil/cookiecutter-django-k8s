#!/bin/bash

IMAGE_TAG=${1:-"latest"}
IMAGES=()

images=$(docker-compose -f production.yml config | grep 'image: ' | cut -d':' -f 2 | tr -d '"')
for image in $images
do
  IMAGES+=("${image}":"${IMAGE_TAG}")
done

echo ${IMAGES[@]} | tr ' ' '\n'
