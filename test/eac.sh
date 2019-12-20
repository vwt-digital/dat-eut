#!/bin/bash
strep=$(gcloud logging read "stderr" --freshness="10m" --format=json | grep "INFO:auditlog.*Url: \(https://.*\) .*e2e-technical-user" | cut -d'|' -f 1 | cut -d" " -f3,8 | cut -d" " -f2,7 | cut -d'/' -f1,4- | sed 's/https://' | sed 's/ /|/')
api=$(curl -s 'https://'"$2"'.appspot.com/openapi.json' | (python3 -c "
import sys
import json
accepted_keys = ''
for key, item in json.load(sys.stdin)['paths'].items():
	if item.get('x-eac-ignore'):
		accepted_keys += '[].IGNORE:' + key + ' '
	else:
		accepted_keys += key + ' '
print(accepted_keys)"))
touch requests.txt;touch specs.txt
for spec in $api;do echo "$spec">>specs.txt;done
for req in $strep
do if [[ "$(echo "$req" | cut -d'|' -f1)" > $1 ]];then echo "$req"|cut -d'|' -f2>>requests.txt;fi;done
script=`python3 eac.py requests.txt specs.txt`
rm requests.txt;rm specs.txt
if [ $script = 0 ];then echo "EAC PASSED: All endpoints were tested";else echo "EAC FAILED: Not all endpoints were tested";exit 1;fi 