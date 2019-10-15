# Endpoint Usage Test

This project is using Python 3 and Bash

## Usage

Copy the "Run EUT test" from cloudbuild.yaml. Run that below the e2e test, and add the following before your e2e test: 
```(date +%T)>../../eut/start_time```

Copy /eut into your config repo on the same level as your cloudbuild and config folder (Clone ./eut in ./eut).

Make sure the following variable is set and can be used in your cloudbuild:
```${PROJECT_ID}```

Make sure you use the right logging on your api. This needs to be logged:
```
INFO:auditlog:Request Url: {url} | IP: {ip} | User-Agent: {agent} | Response status: {code} | UPN: e2e-technical-user
```

## Project

The following in the cloudbuild has to run:
```
cd ../../eut
bash eut-pointed.sh $(<start_time) ${PROJECT_ID}
if [[ $? -ne 0 ]] ; then
	exit 1;
fi
```

The following is extra and can be moved:
```
rm -f ns-*.html
rm -rf node_modules
```