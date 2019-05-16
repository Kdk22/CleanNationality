
from NationalityClean.models import FilterNationality
from ... import views
from NationalityClean.views import clean_data
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        final= clean_data()

        bulk_list = list()
        for each_user_data in final:
            bulk_list.append(
                FilterNationality(
                    unverified_nationality=each_user_data[0],
                    score = each_user_data[1],
                    verified_nationality=each_user_data[2]

                )
            )

        FilterNationality.objects.bulk_create(bulk_list)