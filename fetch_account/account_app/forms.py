from django.forms import ModelForm
from . import models

class NewTransactionForm(ModelForm):

    class Meta:
        model = models.TransactionList
        fields = '__all__'