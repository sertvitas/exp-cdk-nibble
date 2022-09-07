#!/usr/bin/env bash
set -Eeuo pipefail
echo "PUPPERS"
touch /tmp/puppers.txt
curl -Lo /opt/puppers_0.0.3_linux_amd64.tar.gz \
https://github.com/natemarks/puppers/releases/download/v0.0.3/puppers_0.0.3_linux_amd64.tar.gz

mkdir -p /opt/puppers

tar -xzvf /opt/puppers_0.0.3_linux_amd64.tar.gz -C /opt/puppers

nohup /opt/puppers/puppers &
