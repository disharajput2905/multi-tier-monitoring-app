#!/bin/bash
echo "======COMPOSE VALIDATION======"
sudo docker compose config -q && echo "Compose Configuration valid"

echo "=======SERVICE STATUS======="
sudo docker compose ps

echo "=======API HEALTH======="
curl -i --max-time 10 http://localhost/api/health


