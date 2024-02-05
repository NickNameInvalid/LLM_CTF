#!/bin/bash

# python main.py "./database/rev/rebug 2" "./prompts/prompts_open/rev/rebug2.txt"
# # python main.py "./database/rev/whataxor" "./prompts/prompts_open/rev/whataxor.txt"

# for chal in database/rev/*; do
#     python main.py "$chal" "./prompts/prompts_open/rev/rebug1.txt"
# done
for chal in database/rev/*; do
    base_chal=$(basename "$chal")
    touch "./logging/rev/$base_chal".txt
    echo "Solving $base_chal, see in the log file"
    python main.py "$chal" > "./logging/rev/$base_chal".txt
done