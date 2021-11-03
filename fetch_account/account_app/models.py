from django.db import models
from django.db.models import Sum


# this model stores all transaction ever recorded into the system
# might be good to have date_modifed/date_added field for traceibility 
class TransactionList(models.Model):
    payerName = models.CharField(max_length=200)
    availablePoints = models.IntegerField()
    transactionDate = models.DateTimeField()

# this model stores our aggregated points grouped by payer name and transaction date
# we only have a unique record of payee per date in the database 
class AggregatePointList(models.Model):
    payerName = models.CharField(max_length=200)
    availablePoints = models.IntegerField()
    transactionDate = models.DateTimeField()

    def aggregate_points(self, rawData):
        aggData = rawData.objects.values('payerName','transactionDate').aggregate(Sum('availablePoints'))['availablePoints__sum']
        print (aggData)

# this model stores which records were redeemed when a user requests to spend thier points
class RedemedPointSummary(models.Model):
    payerName = models.CharField(max_length=200)
    availablePoints = models.IntegerField()