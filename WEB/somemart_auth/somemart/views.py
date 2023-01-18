import json

from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Item, Review

from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from marshmallow import ValidationError

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import base64

class AddItemSchema(Schema):
    title = fields.Str(validate=Length(1, 64), required=True)
    description = fields.Str(validate=Length(1, 1024), required=True)
    price = fields.Int(validate=Range(1, 1000000), required=True)

@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def ForStuffUser(self, request):
        try:
            document = json.loads(request.body)
            schema = AddItemSchema(strict=True)
            data = schema.load(document)
            item = Item(title=data.get['title'], description=data.get['description'], price=data.get['price'])
            item.save()
            return JsonResponse({'id': item.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.messages}, status=400)

    def post(self, request):
        # Здесь должен быть ваш код
        if not request.user.is_authenticated:
            auth = request.META['HTTP_AUTHORIZATION']
            method, token = auth.split(' ')
            auth_decoded = base64.b64decode(token).decode('ascii')

            login = auth_decoded[0:auth_decoded.index(':')]
            password = auth_decoded[auth_decoded.index(':') + 1:]
            print(login)
            print(password)
            user = authenticate(username=login, password=password)
            if user is not None:
                if user.is_staff is not None:
                    self.ForStuffUser(request)
                else:
                    return HttpResponse(status=403)
            else:
                return HttpResponse(status=401)
        else:
            self.ForStuffUser(request)

class PostReviewSchema(Schema):
    text = fields.Str(validate=Length(1, 1024), required=True)
    grade = fields.Int(validate=Range(1, 10), required=True)

class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        # Здесь должен быть ваш код
        try:
            document = json.loads(request.body)
            schema = PostReviewSchema(strict=True)
            data = schema.load(document)
            item = get_object_or_404(Item, pk=int(item_id))
            review = Review(grade=data.data['grade'], text=data.data['text'], item=item)
            review.save()
            return JsonResponse({'id': review.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.messages}, status=400)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        # Здесь должен быть ваш код
        data = {
            'id': '',
            'title': '',
            'description': '',
            'price': '',
            'reviews': []
        }
        item = get_object_or_404(Item, pk=int(item_id))
        data['id'] = item.id
        data['title'] = item.title
        data['description'] = item.description
        data['price'] = item.price
        review = Review.objects.filter(item=item)

        try:
            review = review[::-1][:5]
        except:
            pass
        for r in review:
            data['reviews'].append({
                'id': r.id,
                'text': r.text,
                'grade': r.grade
            })

        return JsonResponse(data, status=200)
