from django.db import models

# Create your models here.

class CleanNationality(models.Model):
    old_nationality = models.CharField(max_length=100)
    cleaned_nationality = models.CharField(max_length=100)
    score = models.FloatField()


    def __str__(self):
        return self.cleaned_nationality


class JobSeekerUserDetail(models.Model):
    nationality = models.CharField(max_length=100)
    score = models.FloatField(null=True)

#
# class JoSeekerCorrectedNationality(models.Model):
#     old_nationality = models.CharField(max_length=100)
#     probable_nationality = models.CharField(max_length=100)
#     score = models.FloatField()


    def __str__(self):
        return self.nationality