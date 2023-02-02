#!/usr/bin/env bash
#set -Eeuo pipefail

while getopts f:e: flag
do
  case "${flag}" in
    f) file=${OPTARG};;
    e) env=${OPTARG};;
    ?)
      echo "script usage: java_bundle.sh [-f filename] [-e environment]" >&2
      exit 1
      ;;
  esac
done

echo "File name: $file";
echo "Environment: $env";

arr=("qeint" "staging" "production")

if [[ " ${arr[@]} " =~ " $env " ]]; then
  echo "$env is valid"
else
  echo "$env is invalid, please select from qeint, staging, or production"; exit
fi


if ( curl -o/dev/null -sfI "https://s3.amazonaws.com/applex.js.bundle.dev.imprivata.com.us.east.1/$file" ); then
  echo "$file exists"
else
  echo "$file does not exist, quitting"; exit
fi

echo "Getting $file from S3 bucket"

curl "https://s3.amazonaws.com/applex.js.bundle.dev.imprivata.com.us.east.1/$file" \
-Lo  ~/Downloads/javascript_bundle/"$file"

echo "Unzipping"

unzip ~/Downloads/javascript_bundle/"$file" -d ~/Downloads/javascript_bundle/"${file:0:-4}"

echo "Uploading"

if [[ $env == "qeint" || $env == "staging" ]]; then
  echo "Environment is $env"
  aws s3 cp ~/Downloads/javascript_bundle/"${file:0:-4}"/ \
  "s3://applex.js.bundle.dev.imprivata.com.us.east.1/${env}/v1/" --recursive
elif [[ $env == "production" ]]; then
  echo "Environment is $env"
  aws s3 cp ~/Downloads/javascript_bundle/"${file:0:-4}"/ \
  s3://applex.js.bundle.prod.imprivata.com.us.east.1/v1/ --recursive
else
  echo "Environment is invalid, use qeint, staging, or production"
fi
