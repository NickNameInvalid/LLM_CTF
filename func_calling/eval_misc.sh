function cleanup_container {
    docker stop ctfenv &> /dev/null
    docker wait ctfenv &> /dev/null
    docker rm ctfenv &> /dev/null
    while docker container inspect ctfenv &> /dev/null ; do
        echo "Waiting for ctfenv to be removed..."
        sleep 1
    done
}

for model in gpt-3.5-turbo-1106 gpt-4-1106-preview ; do
    for chal in chals/misc/*/challenge.json; do
        chalname=$(basename "$(dirname "$chal")")
        for i in {1..10}; do
            log="logs/misc/${chalname}/conversation.${model}.${i}.json"
            if [ -f "${log}" ]; then
                printf '[%02d/10] skipping %s attempting %s; log exists\n' $i "${model}" "${chalname}"
                continue
            fi
            cleanup_container
            printf '[%02d/10] %s attempting %s\n' $i "${model}" "${chalname}"
            python llm_ctf_solve.py -d -M ${model} -m 30 -L "${log}" "${chal}"
        done
    done
done
