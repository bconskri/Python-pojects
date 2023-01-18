import json
import os
import tempfile

import requests
from django.http import HttpResponse, HttpResponseServerError
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.conf import settings

from .models import Setting
from .form import ControllerForm
from .tasks import smart_home_manager

class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get(self, request, *args, **kwargs):
        HEADERS = {'Authorization': 'Bearer ' + settings.SMART_HOME_ACCESS_TOKEN}
        try:
            data = requests.get(settings.SMART_HOME_API_URL, headers=HEADERS)
            if not data.ok: return HttpResponse (content='error', status=502)
        except:
            return HttpResponse (content='error', status=502)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        #smart_home_manager()
        context = super(ControllerView, self).get_context_data()
        try:
            with open(os.path.join(tempfile.gettempdir(), 'controller.json')) as f:
                context['data'] = json.load(f)  # Current values
        except FileNotFoundError:
            context['data'] = {}
        return context

    def get_initial(self):
        try:
            with open(os.path.join(tempfile.gettempdir(), 'controller.json')) as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {'bedroom_light': False, 'bathroom_light': False}
        return {
            'bedroom_light': data['bedroom_light'],
            'bathroom_light': data['bathroom_light'],
            'hot_water_target_temperature': Setting.objects.get(controller_name='hot_water_target_temperature').value,
            'bedroom_target_temperature': Setting.objects.get(controller_name='bedroom_target_temperature').value
        }

    def form_valid(self, form):
        with open(os.path.join(tempfile.gettempdir(), 'form.json'), 'w') as f:
            json.dump({'bedroom_light': form.cleaned_data['bedroom_light'],
                       'bathroom_light': form.cleaned_data['bathroom_light']}, f)
        Setting.objects.filter(controller_name='hot_water_target_temperature').update(
                                value=form.cleaned_data['hot_water_target_temperature'])
        Setting.objects.filter(controller_name='bedroom_target_temperature').update(
                                value=form.cleaned_data['bedroom_target_temperature'])
        smart_home_manager()
        return super(ControllerView, self).form_valid(form)
