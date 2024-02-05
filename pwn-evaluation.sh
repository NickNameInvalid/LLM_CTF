#!/bin/bash

for chal in database/pwn/*; do
    base_chal=$(basename "$chal")
    touch "./logging/pwn/$base_chal".txt
    echo "Solving $base_chal, see in the log file"
    python main.py "$chal" > "./logging/pwn/$base_chal".txt
done