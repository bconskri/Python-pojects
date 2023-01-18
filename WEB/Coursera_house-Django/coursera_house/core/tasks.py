from __future__ import absolute_import, unicode_literals

import json
import os
import tempfile

from celery import task
from django.conf import settings
from django.core.mail import send_mail

from .models import Setting
import requests

HEADERS = {'Authorization': 'Bearer ' + settings.SMART_HOME_ACCESS_TOKEN}


def get_controllers_data():
    raw_data = requests.get(settings.SMART_HOME_API_URL, headers=HEADERS).json()['data']
    data = {controller['name']: controller['value'] for controller in raw_data}
    with open(os.path.join(tempfile.gettempdir(), 'controller.json'), 'w') as f:
        json.dump(data, f)
    return data


def post_response(changed_parameters):
    controllers = {'controllers': changed_parameters}
    if len(changed_parameters):
        print(requests.post(settings.SMART_HOME_API_URL,
                            data=json.dumps(controllers), headers=HEADERS).json()['status'])


class DecisionMaker:
    def resolve_form(self):
        try:
            with open(os.path.join(tempfile.gettempdir(), 'form.json')) as f:
                form_data = json.load(f)
            if form_data['bedroom_light'] != self.data['bedroom_light']:
                self.new_data['bedroom_light'] = form_data['bedroom_light']
            if form_data['bathroom_light'] != self.data['bathroom_light']:
                self.new_data['bathroom_light'] = form_data['bathroom_light']
        except FileNotFoundError:
            pass

    def __init__(self, data: dict):
        self.data = data
        self.bedroom_target_temperature = Setting.objects.get(controller_name='bedroom_target_temperature').value
        self.hot_water_target_temperature = Setting.objects.get(controller_name='hot_water_target_temperature').value
        self.new_data = {}
        self.is_leak = self.data['leak_detector']
        self.is_smoke = self.data['smoke_detector']
        self.is_manual = self.data['curtains'] == 'slightly_open'

    def check_leaks(self):
        if self.is_leak:
            self.new_data['hot_water'] = False
            self.new_data['cold_water'] = False
            send_mail(subject='Emergency situation', message='There is a water leak in your house!',
                  from_email='coursera_house@coursera.com', recipient_list=[settings.EMAIL_RECEPIENT, ])

    def check_smoke(self):
        if self.is_smoke:
            self.new_data['air_conditioner'] = False
            self.new_data['bedroom_light'] = False
            self.new_data['bathroom_light'] = False
            self.new_data['boiler'] = False
            self.new_data['washing_machine'] = 'off'

    def check_cold_water(self):
        if self.is_leak or ('cold_water' in self.new_data) or self.data['cold_water'] == False:
            self.new_data['boiler'] = False
            self.new_data['washing_machine'] = 'off'

    def check_hot_water(self):
        if self.data['cold_water']:
            if not self.is_leak and not self.is_smoke and \
                    self.data['boiler_temperature'] < self.hot_water_target_temperature * 0.9:
                self.new_data['boiler'] = True
            elif self.data['boiler_temperature'] > self.hot_water_target_temperature * 1.1:
                self.new_data['boiler'] = False

    def check_outdoor_light(self):
        if not self.is_manual:
            if self.data['outdoor_light'] < 50 and not self.data['bedroom_light']:
                self.new_data['curtains'] = 'open'
            #elif self.data['outdoor_light'] > 50 or (not self.is_smoke and self.data['bedroom_light']):
            elif self.data['outdoor_light'] > 50 or self.data['bedroom_light']:
                self.new_data['curtains'] = 'close'

    def check_bedroom(self):
        if not self.is_smoke and \
                self.data['bedroom_temperature'] > self.bedroom_target_temperature * 1.1:
            self.new_data['air_conditioner'] = True
        elif self.data['bedroom_temperature'] < self.bedroom_target_temperature * 0.9:
            self.new_data['air_conditioner'] = False

    def check_state_change(self):
        result_list = []
        for key in self.new_data:
            if self.new_data[key] != self.data[key]:
                result_list.append({'name': key, 'value': self.new_data[key]})
        return result_list


@task()
def smart_home_manager():
    decision_maker = DecisionMaker(get_controllers_data())
    decision_maker.resolve_form()
    decision_maker.check_leaks()
    decision_maker.check_smoke()
    decision_maker.check_cold_water()
    decision_maker.check_hot_water()
    decision_maker.check_outdoor_light()
    decision_maker.check_bedroom()
    post_response(decision_maker.check_state_change())
