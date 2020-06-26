#!/bin/bash

set -eo pipefail
if [ "$BRANCH_NAME" == "master" ]; then
   echo "Skipping e2e api coverage test in master branch"
   exit 0
fi
if [ ! -f /start_datetime ]; then
    echo "The start_datetime needs to be passed"
    exit 1
fi
python /coverage/main.py "${PROJECT_ID}" "$(</start_datetime)"
