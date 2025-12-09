#!/bin/bash

cd ~/app/LosPollosHermanosPy

echo "Rebuild & restart containers..."
docker compose down
docker compose build --no-cache
docker compose up -d

echo "Done."
