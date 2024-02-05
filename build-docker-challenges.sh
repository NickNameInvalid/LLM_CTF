#!/usr/bin/env bash

# Build main docker image
# sudo docker build -t ctfenv .

# Build docker image for each challenge
# for d in database/{pwn,crypto,misc}/*; do
#     if [ -d "$d" ]; then
#         echo "Building $d"
#         image_name=$(jq -r .container_image < "$d"/challenge.json)
#         docker build --platform linux/amd64 -t "$image_name" "$d"
#     fi
# done

for d in database/{pwn,crypto,misc}/*; do
    if [ -d "$d" ]; then
        echo "Building $d"
        image_name=$(jq -r .container_image < "$d"/challenge.json)
        sudo DOCKER_BUILDKIT=0 docker build --platform linux/arm64 --network=ctfnet -t "$image_name" "$d"
        # sudo docker network connect ctfnet "$image_name"
        sudo docker run -dit "$image_name" /bin/bash
    fi
done