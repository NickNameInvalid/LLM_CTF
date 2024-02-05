#!/bin/bash

for chal in database/misc/*; do
    base_chal=$(basename "$chal")
    touch "./logging/misc/$base_chal".txt
    echo "Solving $base_chal, see in the log file"
    python main.py "$chal" > "./logging/misc/$base_chal".txt
done
