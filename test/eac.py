import re
import sys

requests = []
specs = []
found = []
ignored = []
notignored = []
notfound = ''

with open(sys.argv[1], 'r') as f:
	requests = [line.strip().split('?')[0] for line in f]
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
	try:
		sys.exit('\nIgnored: ' +  str(round(((len(ignored) / len(specs)) * 100), 2)) + '% '
			+ '\nAPI Coverage: ' + str(round(((len(found) / len(specs)) * 100), 2)) + '% '
			+ '\nDirect Coverage: ' + str(round(((len(found) / (len(specs) - len(ignored))) * 100), 2)) + '% ')
	except ZeroDivisionError:
		sys.exit('No endpoints found')
else:
	print(1)
	sys.exit('\nIgnored: ' +  str(round(((len(ignored) / len(specs)) * 100), 2)) + '% '
		+ '\nAPI Coverage: ' + str(round(((len(found) / len(specs)) * 100), 2)) + '% '
		+ '\nDirect Coverage: ' + str(round(((len(found) / (len(specs) - len(ignored))) * 100), 2)) + '% '
		+ '\nNot found: '
		+ '\n' + notfound)
