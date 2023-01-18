#!/usr/bin/python3

import json
import requests
import os
import hashlib
  
with open('result.txt', 'rb') as f:
  hex_key = hashlib.md5(f.read())

with open('result.txt', 'r') as f:
  count = len(f.read().split(', '))

hex_key.hexdigest()

result = {
  "hex_key": hex_key.hexdigest(),
  "count": count
}

print(result)


coursera = {
  '1.2.3': {
    'key': '5HuaPXDAQj-iLV4QleeX6g',
    'part': 'zRohG'
  },
  '1.3.4': {
    'key': 'xFg5zhcDQF-F64MCpKbeQw',
    'part': 'WQOAw'
  },
  '1.4.3': {
    'key': 'QJpHVcKVR5O4wDdYmPCIlg',
    'part': 'xwxBU'
  },
}

task_id = '1.4.3'
email = 'bconskri@icloud.com' #input('Set your email:')
coursera_token = '1NoGhTIPdSZp4JVh' #input('Set coursera token: ')

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
  print ("Something went wrong, please have a look at the reponse of the grader")
  print ("-------------------------")
  print (response.text)
  print ("-------------------------")
