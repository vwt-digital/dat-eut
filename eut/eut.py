import re
import sys

requests = []
specs = []
notfound = ''

with open(sys.argv[1], 'r') as f:
	for line in f.readlines():
		requests.append(line)
with open(sys.argv[2], 'r') as f:
	for line in f.readlines():
		specs.append(line)

for spec in specs:
	request_url = re.compile(re.sub("{.*}", "[a-zA-Z0-9_]*", spec))
	possible_urls = list(filter(request_url.match, requests))
	if not possible_urls:
		notfound += spec + ' '
if len(notfound) == 0:
	sys.exit(True)
else:
	sys.exit(notfound)