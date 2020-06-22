import subprocess  # nosec
from typing import List, Dict
import urllib.request
import argparse
import json
import re
import sys


def requests_get(time: str = '') -> List:
    for request in subprocess.check_output(['gcloud', 'app', 'logs', 'read', '--limit=1000']).decode().split('\n'):  # nosec
        if 'openapi.json' in request:
            print(request)
    return [line.strip().split('?')[0] for line in subprocess.check_output(['gcloud', 'app', 'logs', 'read', '--limit=1000'])]  # nosec


def resources_get(domain: str) -> Dict:
    resources = {}

    with urllib.request.urlopen(f'https://{domain}.appspot.com/openapi.json') as url:  # nosec
        for resource, data in json.loads(url.read().decode())['paths'].items():
            resources[resource] = data.get('x-eac-ignore', False)

    return resources


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('domain', type=str, help='Domain to scan')
    parser.add_argument('time', type=str, help='Time to scan after', nargs='?')
    args = parser.parse_args()

    resources = resources_get(args.domain)
    requests = requests_get('13:00:00')

    if not resources:
        sys.exit('BREAKING: No resources found.')

    if not requests:
        print('WARNING: List of requests is empty.')

    output = {'ignored': 0, 'failed': 0}

    for resource, ignored in resources.items():
        request_url = re.sub("{.*?}", r"([^/]+)", resource) + '$'
        possible_urls = list(filter(re.compile(request_url).match, requests))

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
        sys.exit('Not all resources were tested')
    sys.exit('Every resource was either tested or ignored')
