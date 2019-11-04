import re
import sys

requests = []
specs = []
notfound = ''

with open(sys.argv[1], 'r') as f:
	requests = f.read().splitlines()
with open(sys.argv[2], 'r') as f:
	specs = f.read().splitlines()

for spec in specs:
	request_url = re.sub("{.*?}", r"([^/]+)", spec) + '$'
	possible_urls = list(filter(re.compile(request_url).match, requests))
	if not possible_urls:
		notfound += spec + ' '
if len(notfound) == 0:
	sys.exit(0)
else:
	sys.exit(notfound)
