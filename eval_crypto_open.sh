#!/bin/bash

for chal in database/crypto/*; do
    base_chal=$(basename "$chal")
    touch "./logging/$base_chal".txt
    echo "Solving $base_chal, see in the log file"
    python main.py "$chal" > "./logging/$base_chal".txt
done
