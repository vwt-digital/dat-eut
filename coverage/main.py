import subprocess  # nosec
from typing import List, Dict
from datetime import datetime
import urllib.request
import argparse
import json
import re
import sys


def requests_get(before_datetime: datetime, domain: str) -> List:
    requests = []

    for request in subprocess.check_output(['gcloud', 'app', 'logs', 'read', '--limit=1000']).decode().split('\n'):  # nosec
        if 'UPN: e2e-technical-user' in request:
            if datetime.strptime('/'.join(request.split(' ')[0:2]), '%Y-%m-%d/%H:%M:%S') > before_datetime:
                request_resource = re.search(f'{domain}.appspot.com(.*?)\s+', request) # noqa
                requests.append(request_resource.group(1).strip().split('?')[0])

    return requests


def resources_get(domain: str) -> Dict:
    resources = {}

    with urllib.request.urlopen(f'https://{domain}.appspot.com/openapi.json') as url:  # nosec
        for resource, data in json.loads(url.read().decode())['paths'].items():
            resources[resource] = data.get('x-eac-ignore', False)

    return resources


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Domain to scan')
    parser.add_argument('datetime', type=str, help='Datetime to scan after')
    args = parser.parse_args()
    resources = resources_get(args.domain)
    requests = requests_get(datetime.strptime(args.datetime, '%Y-%m-%d/%H:%M:%S'), args.domain)

    if not resources:
        print('BREAKING: No resources found.')
        sys.exit(1)

    output = {'ignored': 0, 'failed': 0}

    for resource, ignored in resources.items():
        possible_urls = []

        if requests:
            request_url = re.sub("{.*?}", r"([^/]+)", resource) + '$'
            possible_urls = list(filter(re.compile(request_url).match, requests))
        else:
            print('WARNING: List of requests is empty.')

        if ignored:
            print(f'\033[93m\t{resource} has been ignored\033[0m\n')
            output['ignored'] += 1

        if not possible_urls and not ignored:
            print(f'\033[91m\t{resource} has not been tested and is not ignored\033[0m\n')
            output['failed'] += 1

    passed = len(resources) - (output["ignored"] + output["failed"])
    print(f'Output:\n \
    Passed: {passed} ({round(passed / len(resources) * 100, 2)}%) \n \
    Ignored: {output["ignored"]} ({round(output["ignored"] / len(resources) * 100, 2)}%) \n \
    Failed: {output["failed"]} ({round(output["failed"] / len(resources) * 100, 2)}%)')

    if output['failed'] > 0:
        print('Not all resources were tested')
        sys.exit(1)

    print('Every resource was either tested or ignored')
    sys.exit(0)
