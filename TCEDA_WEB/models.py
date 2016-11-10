from __future__ import unicode_literals

from django.db import models


# Create your models here.

class EconomicSnapshot(models.Model):
    population = models.IntegerField(
        null=True,
    )
    houseHolds = models.IntegerField(
        null=True,
    )
    avgHouseIncome = models.IntegerField(
        null=True,
    )
    medianHomeValue = models.IntegerField(
        null=True,
    )
    employmentPop = models.IntegerField(
        null=True,
    )
    unemploymentPop = models.IntegerField(
        null=True,
    )
