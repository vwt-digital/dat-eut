strep=$(gcloud app logs read --limit=1000 | grep "INFO:auditlog.*Url: \(https://.*\) .*e2e-technical-user" | cut -d'|' -f 1 | cut -d" " -f2,7 | cut -d'/' -f1,4- | sed 's/https://' | sed 's/ /|/')
api=$(curl -s 'https://'$2'.appspot.com/openapi.json' | (python -c "import sys, json; print(' '.join(list(json.load(sys.stdin)['paths'].keys())))"))
touch requests.txt;touch specs.txt
for spec in $api;do echo $spec>>specs.txt;done
for req in $strep
do if [[ "$(echo $req|cut -d'|' -f1)">$1 ]];then echo $req|cut -d'|' -f2>>requests.txt;fi;done
script=$(python eac.py requests.txt specs.txt)
rm requests.txt;rm specs.txt
if [[ $script != 1 ]];then echo "EAC FAILED: Not all endpoints were tested";exit 1;else echo "EAC PASSED: All endpoints were tested";exit 0;fi