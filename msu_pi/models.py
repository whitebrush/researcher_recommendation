from django.db import models
from django_pandas.managers import DataFrameManager

class ResearcherResearchProfile(models.Model):
    department = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    name = models.CharField(max_length=200)
    num_tokens = models.IntegerField()
    embedding = models.CharField(max_length=3000)
    objects = models.Manager()
    pobjects = DataFrameManager()  # Pandas-Enabled Manager

    def __str__(self):
        return f"{self.id} - {self.name} - {self.department} - description {self.description}"

