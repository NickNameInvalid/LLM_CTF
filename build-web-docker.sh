#!/bin/bash

for d in database/{web,}/*; do
    if [ -d "$d" ]; then
        echo "Building $d"
        image_name=$(jq -r .container_image < "$d"/challenge.json)
        sudo DOCKER_BUILDKIT=0 docker build --platform linux/amd64 --network=ctfnet -t "$image_name" "$d"
        # sudo docker network connect ctfnet "$image_name"
        sudo docker run -dit "$image_name" /bin/bash
    fi
done