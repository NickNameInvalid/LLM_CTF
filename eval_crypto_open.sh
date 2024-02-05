#!/bin/bash

for chal in database/rev/*; do
    python main.py "$chal" "./prompts/prompts_open/rev/rebug1.txt"
done
