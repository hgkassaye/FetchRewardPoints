# Generated by Django 3.2.6 on 2021-11-03 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0002_modifiedpointlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedemedPointSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payerName', models.CharField(max_length=200)),
                ('availablePoints', models.IntegerField()),
            ],
        ),
    ]