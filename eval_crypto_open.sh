#!/bin/bash

for chal in database/crypto/*; do
    base_chal=$(basename "$chal")
    touch "./logging/crypto/$base_chal".txt
    echo "Solving $base_chal, see in the log file"
    python main.py "$chal" > "./logging/crypto/$base_chal".txt
done

# touch "./logging/circles.txt"
# echo "Solving circles, see in the log file"
# python main.py ./database/crypto/circles > ./logging/circles.txt