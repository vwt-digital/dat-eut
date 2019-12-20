import re
import sys

requests = []
specs = []
found = []
ignored = []
notignored = []
notfound = ''

with open(sys.argv[1], 'r') as f:
	requests = f.read().splitlines()
with open(sys.argv[2], 'r') as f:
	specs = f.read().splitlines()
	specs = list(dict.fromkeys(specs))

for spec in specs:
	if spec[:10] == '[].IGNORE:':
		ignored.append((spec[10:]))
		continue
	request_url = re.sub("{.*?}", r"([^/]+)", spec) + '$'
	possible_urls = list(filter(re.compile(request_url).match, requests))
	if not possible_urls:
		notfound += spec + ' '
	else:
		found.append(spec)
if len(notfound) == 0:
	print(0)
	sys.exit('\nIgnored: ' +  str(int(100 + ((len(ignored) - len(specs)) / len(specs) * 100))) + '% '
		+ '\nFound All: ' + str(int(100 + ((len(found) - len(specs)) / len(specs) * 100))) + '% '
		+ '\nFound without Ignored: ' + str(int(100 + ((len(found) - (len(specs) - len(ignored))) / (len(specs) - len(ignored)) * 100))) + '% ')
else:
	print(1)
	sys.exit('\nIgnored: ' +  str(int(100 + ((len(ignored) - len(specs)) / len(specs) * 100))) + '% '
		+ '\nFound All: ' + str(int(100 + ((len(found) - len(specs)) / len(specs) * 100))) + '% '
		+ '\nFound without Ignored: ' + str(int(100 + ((len(found) - (len(specs) - len(ignored))) / (len(specs) - len(ignored)) * 100))) + '% '
		+ '\nNot found: '
		+ '\n' + notfound)
