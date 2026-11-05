#!/usr/bin/env bash
echo "Downloading all 12 AISC experiments..."
curl -sLO https://cli-t0km.onrender.com/downloads/labx_experiments.zip && unzip -q -o labx_experiments.zip && rm labx_experiments.zip
echo "[OK] All 12 experiments downloaded into $(pwd)!"
