# e2e Api Coverage Test

This project is using Python 3 and Bash

## Usage

Before you run your e2e test, copy this into your cloudbuild.yaml:

```bash 
(date +%T)>start_time 
```
(Can also be 0 for global test without time restrictions)


Add the following AFTER your e2e test:

```bash

- name: 'gcr.io/cloud-builders/gcloud'
  entrypoint: 'bash'
  args:
  - '-c'
  - |
    if [ "$BRANCH_NAME" == "develop" ]; then
      curl -LJO https://raw.githubusercontent.com/vwt-digital/e2e-api-coverage/develop/test/eac.sh
      curl -LJO https://raw.githubusercontent.com/vwt-digital/e2e-api-coverage/develop/test/eac.py
      bash eac.sh $(<start_time) ${PROJECT_ID}
    fi
  dir: 'expenses/pipeline'

```

### What is it doing?

Copying the eac files. eac.sh will get the logs, eac.py with compare the requests to the specurls.

```bash
      curl -LJO https://raw.githubusercontent.com/vwt-digital/e2e-api-coverage/develop/test/eac.sh
      curl -LJO https://raw.githubusercontent.com/vwt-digital/e2e-api-coverage/develop/test/eac.py
```

Running the eac.sh with the time set before the e2e test and the project id.
```bash
 bash eac.sh $(<start_time) ${PROJECT_ID} 
```

## Ignore

You can ignore URLs from your API by adding the following to the spec URL in your yaml file:
```bash
    x-eac-ignore: true
```

Example:
```bash

  /url/to/ignore:
    get:
      parameters:
        - $ref: '#/components/parameters/step'
      responses:
        '200':
          description: Succesful
    x-eac-ignore: true

```

Make sure it is linked to the URL directly (and also check Zally).
Make sure you are using connexxion version 2.2.0 or higher when using the ignore.

## Requirements
For this test to work, the application to be tested needs to use [FLASH Auditlog](https://github.com/vwt-digital/flask-auditlog)
The security_controller also needs to have the following in ```info_from_oAuth2```:
```python
    if result is not None:
        g.user = result.get('upn', 'e2e-technical-user')
        g.token = result
```

Make sure you are using connexxion version 2.2.0 or higher when using the ignore.

## Explanation

### euc.sh
```bash
strep=$(gcloud app logs read --limit=1000 | grep "INFO:auditlog.*Url: \(https://.*\) .*e2e-technical-user" | cut -d'|' -f 1 | cut -d" " -f2,7 | cut -d'/' -f1,4- | sed 's/https://' | sed 's/ /|/')
```
Uses the gcloud app logs to get all the auditlogs from the e2e user.

```bash
api=$(curl -s 'https://'$2'.appspot.com/openapi.json' | (python -c "import sys, json; print(' '.join(list(json.load(sys.stdin)['paths'].keys())))"))
```
Uses the json from openapi to get the specurls.

```bash
script=$(python eac.py requests.txt specs.txt)
```
Runs eac.py with the requesturls and specurls.

### euc.py
```python
with open(sys.argv[1], 'r') as f:
	requests = f.read().splitlines()
with open(sys.argv[2], 'r') as f:
	specs = f.read().splitlines()
```
Opens the requests and specs files.

```python
	request_url = re.sub("{.*?}", r"([^/]+)", spec) + '$'
	possible_urls = list(filter(re.compile(request_url).match, requests))
```
Compares the spec urls with the request urls. The parameters with {} in specs will be changed to Regex. At the end of the url, a $ is added to mark the end of the url.
