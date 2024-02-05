#!/usr/bin/env bash

# Build main docker image
sudo docker build -t ctfenv .

# Build docker image for each challenge
for d in database/{pwn,crypto,misc}/*; do
    if [ -d "$d" ]; then
        echo "Building $d"
        image_name=$(jq -r .container_image < "$d"/challenge.json)
        docker build --platform linux/amd64 -t "$image_name" "$d"
    fi
done