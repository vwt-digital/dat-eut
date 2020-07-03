#!/bin/bash

set -eo pipefail
if [ "$2" == "master" ]; then
   echo "Skipping e2e api coverage test in master branch"
   exit 0
fi
if [ ! -f "$3" ]; then
    echo "The start_datetime needs to be passed"
    exit 1
fi

python /coverage/main.py "$1" "$(<"$3")"
