# E2e Api Coverage Test

Test the coverage of an e2e test using an API spec
## Usage for cloudbuild

Use this command before running the e2e test:

```bash
(date '+%Y-%m-%d/%H:%M:%S')>start_datetime 
```
Add the following AFTER your e2e test:
```bash
- name: 'gcr.io/cloud-builders/gcloud'
  id: 'e2e api coverage request gathering'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      if [ "$BRANCH_NAME" == "develop" ]; then
        gcloud app logs read --limit=1000 > requests
      fi
   dir: 'yourdir/here'

- name: 'eu.gcr.io/vwt-p-gew1-dat-cloudbuilders/cloudbuilder-eac'
  id: 'e2e api coverage test'
  args: ['${PROJECT_ID}.appspot.com', '${BRANCH_NAME}', 'start_datetime_file', 'requests_file']
  dir: 'yourdir/here'

```

## Usage for local test

`main.py` has three arguments: 

domain: domain that will be used

datetime: datetime as string ('+%Y-%m-%d/%H:%M:%S')

gather_file (optional): file containing requests. If this is not passed, it will run and use `gcloud app logs read --limit=1000`.

<br>
Run this when using `main.py`:

```bash
python main.py domain_name.appspot.com start_datetime (gather_file)
```
When using the container:
```bash
docker run -v {files_location}:/workspace eu.gcr.io/vwt-p-gew1-dat-cloudbuilders/cloudbuilder-eac:latest domain_name develop /workspace/start_datetime (/workspace/requests)
```

## Ignore

You can ignore URLs from your API by adding the following to the spec URL in your yaml file:
```bash
    x-eac-ignore: True
```

Example:
```bash

  /url/to/ignore:
    get:
      parameters:
        - $ref: '#/components/parameters/step'
      responses:
        '200':
          description: Successful
    x-eac-ignore: True

```

Make sure it is linked to the URL directly (and also check Zally).
Make sure you are using connexxion version 2.2.0 or higher when using the ignore.

## Requirements
For this test to work, the application to be tested needs to use [FLASK Auditlog](https://github.com/vwt-digital/flask-auditlog) & have a valid e2e test running on develop.
The security_controller also needs to have the following in ```oAuth2```:
```
  ('upn', 'e2e-technical-user')
```

Make sure you are using connexxion version 2.2.0 or higher when using the ignore.
