from django.db import models


class FilterNationality(models.Model):
    unverified_nationality = models.CharField(max_length=100)
    verified_nationality = models.CharField(max_length=100)
    score = models.FloatField()
    verified_status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('unverified_nationality', 'verified_nationality',)

    def __str__(self):
        return self.verified_nationality + '-' + str(self.verified_status)


class JobSeekerUserDetail(models.Model):
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.nationality