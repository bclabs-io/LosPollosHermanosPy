#!/bin/bash
set -euo pipefail # 強制處理任何錯誤
cd ~/app/LosPollosHermanosPy

echo "Rebuild & restart containers..."
docker compose down
docker compose build --no-cache
docker compose up -d

echo "Done."
