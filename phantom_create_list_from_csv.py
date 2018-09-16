import argparse
import os.path
import getpass
import csv
import requests
import json
import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re
import sys

parser = argparse.ArgumentParser(description='Phantom Script to Create A Custom List from a CSV File.')
parser.add_argument('-f', '--file', required=False, help='Full path to the CSV file')
parser.add_argument('-ip', '--ip', required=False, help='IP Address of Phantom Server')
parser.add_argument('-u', '--user', required=False, help='User Name for Phantom Server')
parser.add_argument('-l', '--list', required=False, help='List Name to create in Phantom')
parser.add_argument('-d', '--debug', action='store_true', help='Turns on debugging of URL requests')


args = parser.parse_args()
args = vars(args)

if args['debug']:
	print('Debug On')
else:
	requests.packages.urllib3.disable_warnings()

file = ''
ip = ''
user = ''
pwd = ''
listname = ''

print('This script will create a custom list in Phantom based on a CSV file provided.')

def check_file_exists(filename):
	if os.path.isfile(filename) == False:
		print('File Not Found.')
		return False
	return True

def check_ip(s):
	a = s.split('.')
	if len(a) != 4:
		print('IP Address not valid: {}'.format(s))
		return False
	for x in a:
		if not x.isdigit():
			print('IP Address not valid: {}'.format(s))
			return False
		i = int(x)
		if i < 0 or i > 255:
			print('IP Address not valid: {}'.format(s))
			return False
	return True

if args['file'] is not None:
	file = args['file']
	if check_file_exists(file) == False:
		exit()
else:
	file = input('CSV file to add list from: ')
	if check_file_exists(file) == False:
		exit()
try:
	f = open(file)
	reader = csv.reader(f)
	list_data = list(reader)
except:
	print('Unable to open CSV file.')
	exit()

if args['ip'] is not None:
	ip = args['ip']
	if check_ip(ip) == False:
		exit()
else:
	ip = input('Phantom Server IP Address: ')
	if check_ip(ip) == False:
		exit()

if args['user'] is not None:
	user = args['user']
else:
	user = input('Phantom Server Username: ')

pwd = getpass.getpass('Phantom Server Password: ')

if args['list'] is not None:
	listname = args['list']
else:
	listname = input('Name of list to create in Phantom: ')

url = 'https://{}:{}@{}/rest/decided_list'.format(user, pwd, ip)

c ={'content': list_data, 'name': listname}
json_data = json.dumps(c)

try:
	r = requests.post(url, data=json_data, headers=None, verify=False)
except:
	print('Unable to contact the Phantom Server.  Please check IP address and whether the Phantom Server is accessible.')
	exit()

result = r.json()
if 'failed' in result:
	print('Failed to create list.')
	print(result['message'])
elif 'success' in result:
	print('List successfully created.')
else:
	print('Unknown result, please check Phantom interface to see if the list was created.')