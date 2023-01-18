#!/usr/bin/python3

import json
import requests
import os
import hashlib
from os.path import exists

with open('result.txt', 'rb') as f:
  f.seek(0)
  hex_key = hashlib.md5(f.read())

with open('result.txt', 'r') as f:
  f.seek(0)
  count = len(f.read().split(', '))

hex_key.hexdigest()

result = {
  "hex_key": hex_key.hexdigest(),
  "count": count
}


coursera = {
  '1.2.3': {
    'key': '5HuaPXDAQj-iLV4QleeX6g',
    'part': 'zRohG'
  },
  '1.3.4': {
    'key': 'xFg5zhcDQF-F64MCpKbeQw',
    'part': 'WQOAw'
  }
}

task_id = '1.3.4'
email = input('Set your email:') 
coursera_token = input('Set coursera token: ')

submission = {
  "assignmentKey": coursera[task_id]['key'],
  "submitterEmail":  email,
  "secret":  coursera_token,
  "parts": {
    coursera[task_id]['part']: {"output": json.dumps(result)}
  }
}

# print(result)
response = requests.post('https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1', data=json.dumps(submission))

if response.status_code == 201:
  print ("Submission successful, please check on the coursera grader page for the status")
else:
  print ("Something went wrong, please have a look at the response of the grader")
  print ("-------------------------")
  print (response.text)
  print ("-------------------------")
