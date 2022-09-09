#!/usr/bin/env bash
set -Eeuo pipefail

echo "Userdata script did run" >> /tmp/script_confirmation.txt
#yum update -y
#yum install -y collectd
yum install -y amazon-cloudwatch-agent
#wget https://s3.us-east-1.amazonaws.com/amazoncloudwatch-agent-us-east-1/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
#rpm -U ./amazon-cloudwatch-agent.rpm
amazon-cloudwatch-agent-ctl -a start

yum install -y unzip
curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip
unzip awscliv2.zip
sudo ./aws/install

echo "PUPPERS"

useradd -m -d /opt/puppers -s /bin/bash puppers
usermod  -L puppers

touch /tmp/puppers.txt
curl -Lo /opt/puppers_0.0.6_linux_amd64.tar.gz \
https://github.com/natemarks/puppers/releases/download/v0.0.6/puppers_0.0.6_linux_amd64.tar.gz

mkdir -p /opt/puppers

tar -xzvf /opt/puppers_0.0.6_linux_amd64.tar.gz -C /opt/puppers

chown -R puppers:puppers /opt/puppers

runuser -l puppers -c "AWS_REGION=us-east-1 PUPPERS_SECRET_NAME=SecretA720EF05-YA1uGeVL9JKx nohup /opt/puppers/puppers &"

