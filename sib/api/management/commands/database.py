import csv
import datetime as dt

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.timezone import get_default_timezone

from api.models import Deal

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('data/deals.csv', 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:

                time_obj = dt.datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S.%f')
                timezone_date_time_obj = get_default_timezone().localize(time_obj)

                user, _ = User.objects.get_or_create(username=row['customer'])

                user.deals.get_or_create(item=row['item'],
                                         total=row['total'],
                                         quantity=row['quantity'],
                                         date=str(timezone_date_time_obj))

        self.stdout.write(self.style.SUCCESS('Successfully load data'))
