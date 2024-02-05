for model in gpt-3.5-turbo-1106 gpt-4-1106-preview ; do
    for chal in chals/forensics/*/challenge.json; do
        chalname=$(basename "$(dirname "$chal")")
        for i in {1..10}; do
            log="logs/forensics/${chalname}/conversation.${model}.${i}.json"
            if [ -f "${log}" ]; then
                printf '[%02d/10] skipping %s attempting %s; log exists\n' $i "${model}" "${chalname}"
                continue
            fi
            docker stop ctfenv
            docker wait ctfenv
            docker rm ctfenv
            while docker container inspect ctfenv >/dev/null 2>&1; do
                echo "Waiting for ctfenv to be removed..."
                sleep 1
            done
            printf '[%02d/10] %s attempting %s\n' $i "${model}" "${chalname}"
            python llm_ctf_solve.py -d -M ${model} -m 30 -L "${log}" "${chal}"
        done
    done
done
