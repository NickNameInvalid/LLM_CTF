for model in gpt-3.5-turbo-1106 gpt-4-1106-preview gpt-4-0125-preview ; do
    for chal in chals/pwn/*/challenge.json; do
        chalname=$(basename "$(dirname "$chal")")
        for i in {1..10}; do
            log="logs/pwn/${chalname}/conversation.${model}.${i}.json"
            if [ -f "${log}" ]; then
                printf '[%02d/10] skipping %s attempting %s; log exists\n' $i "${model}" "${chalname}"
                continue
            fi
            printf '[%02d/10] %s attempting %s\n' $i "${model}" "${chalname}"
            python llm_ctf_solve.py -M ${model} -m 30 -L "${log}" "${chal}"
        done
    done
done
