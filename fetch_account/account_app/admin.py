from django.contrib import admin
from account_app import models

# Register your models here.
admin.site.register(models.TransactionList)
admin.site.register(models.AggregatePointList)
admin.site.register(models.RedemedPointSummary)
