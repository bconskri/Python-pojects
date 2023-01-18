from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    price = models.PositiveIntegerField()


class Review(models.Model):
    grade = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=1024)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
