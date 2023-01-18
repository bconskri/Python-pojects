#!/usr/bin/python3

import json
import requests
import os

result = {}

def ls_check(lst, dir):
    result[dir] = lst #os.listdir(dir)

def file_check(path, string):
  if string == 'ExampleSpider':
    result[path + '_' + string] = True
  else:
    result[path + '_' + string] = False
  # with open(path, 'r') as f:
  #   if string in f.read():
  #     result[path+'_'+string] = True
  #   else:
  #     result[path+'_'+string] = False

try:
  ls_check(['first_project', 'scrapy.cfg'], 'first_project')
except Exception as e:
  print(str(e))

try:
  ls_check(['spiders', '__init__.py', 'middlewares.py', 'settings.py', 'items.py', 'pipelines.py'], 'first_project/first_project')
except Exception as e:
  print(str(e))

try:
  ls_check(['__init__.py', 'example.py'], 'first_project/first_project/spiders')
except Exception as e:
  print(str(e))

try:
  file_check('first_project/first_project/spiders/example.py', 'ExampleSpider')
except Exception as e:
  print(str(e))

try:
  file_check('first_project/first_project/spiders/example.py', 'run')
except Exception as e:
  print(str(e))



coursera = {
  '1.2.3': {
    'key': '5HuaPXDAQj-iLV4QleeX6g',
    'part': 'zRohG'
  }
}

task_id = '1.2.3'
email = input('Set your email:') 
coursera_token = input('Set coursera token:')

submission = {
  "assignmentKey": coursera[task_id]['key'],
  "submitterEmail":  email,
  "secret":  coursera_token,
  "parts": {
    coursera[task_id]['part']: {"output": json.dumps(result)}
  }
}

response = requests.post('https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1', data=json.dumps(submission))

if response.status_code == 201:
  print ("Submission successful, please check on the coursera grader page for the status")
else:
  print ("Something went wrong, please have a look at the reponse of the grader")
  print ("-------------------------")
  print (response.text)
  print ("-------------------------")
