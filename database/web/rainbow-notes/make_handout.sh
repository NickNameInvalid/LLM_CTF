sed 's|- SITE=.*|- SITE=${SITE}|;s|- FLAG=.*|- FLAG=${FLAG}|' docker-compose.yml > docker-compose-for-handout.yml
tar --owner="arx" --group="arx" \
    -czvf handout.tar.gz chrome.json docker-compose-for-handout.yml web bot
