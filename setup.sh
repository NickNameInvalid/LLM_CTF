#!/usr/bin/env bash

# Build main docker image
sudo docker build -t ctfenv .

# Build docker image for each challenge
for d in database/{pwn,crypto}/*; do
    if [ -d "$d" ]; then
        echo "Building $d"
        image_name=$(jq -r .container_image < "$d"/challenge.json)
        docker build -t "$image_name" "$d"
    fi
done

# Create network
sudo docker network create ctfnet

# Download and unpack Ghidra
if [ ! -d ghidra_11.0_PUBLIC ]; then
    wget https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.0_build/ghidra_11.0_PUBLIC_20231222.zip
    unzip ghidra_11.0_PUBLIC_20231222.zip
    rm ghidra_11.0_PUBLIC_20231222.zip
fi
