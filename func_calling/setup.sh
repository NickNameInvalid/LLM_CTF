#!/usr/bin/env bash

# Build main docker image
docker build -t ctfenv .

# Build docker image for each challenge
for d in chals/crypto/*; do
    if [ -d "$d" ]; then
        image_name=$(jq -r .container_image < "$d"/challenge.json)
        docker build -t "$image_name" "$d"
    fi
done

# # Create network
# docker network create ctfnet

# # Download and unpack Ghidra
# wget https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.0_build/ghidra_11.0_PUBLIC_20231222.zip
# unzip ghidra_11.0_PUBLIC_20231222.zip
# rm ghidra_11.0_PUBLIC_20231222.zip

