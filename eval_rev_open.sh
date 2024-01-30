#!/bin/bash

# python main.py "./database/rev/rebug 1" "./prompts/prompts_open/rev/rebug1.txt"

for chal in database/rev/*; do
    python main.py "$chal" "./prompts/prompts_open/rev/rebug1.txt"
done
