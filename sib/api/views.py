import codecs
import csv
import datetime as dt

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.timezone import get_default_timezone, now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import APIDealSerializer

User = get_user_model()


class APIDeal(APIView):
    error_response_body = {
        'Status': 'Error',
        'Desc': None
    }
    error_status = status.HTTP_400_BAD_REQUEST
    ok_status = status.HTTP_200_OK

    def get(self, request):
        """
        Cached in local mem response of GET function.

        Return response like:
        {“response”: [{
            “username": <username>,
            "spent_money": <total_sum>:int,
            "gems": [<name of gems, that bought not only that user in top5>]
        },]
        If cache not fresh, return fresh data and cache it
        """
        try:
            is_not_fresh = cache.get('last_db_update') > cache.get('last_get')
        except TypeError:
            is_not_fresh = True
        if is_not_fresh:
            users = User.objects.all()[:5]
            serializer = APIDealSerializer(users, many=True)
            data_for_cache = {
                'data': serializer.data,
                'last_get': now(),
            }
            for key, value in data_for_cache.items():
                cache.set(key, value)
        return Response({'response': cache.get('data')}, status=self.ok_status)

    def post(self, request):
        """
        Work with csv file in request.

        Validate csv file.
        Itereate on it, work with every row.
        Validate data in row.
        Get or create User with validated username.
        Get or create Deal of thats User with validated data.
        Return "Status",
        if "Status": "Error", also return "Desc" with description of error.
        """
        validated_csv, error = self.validate_csv(request)
        if not validated_csv:
            return Response(error, status=self.error_status)
        for row in validated_csv:
            data, error = self.validate_data(row)
            if not data:
                return Response(error, status=self.error_status)
            username, item, total, quantity, date = data
            user, _ = User.objects.get_or_create(username=username)
            user.deals.get_or_create(item=item, total=total,
                                     quantity=quantity, date=date)
        return Response({'Status': 'OK - файл был обработан без ошибок'},
                        status=self.ok_status)

    def validate_csv(self, request):
        """
        Get file from request.
        Encode it to utf-8 and return data with OrderedDict's.
        """
        body = self.error_response_body
        try:
            file = request.data['deals']
        except (MultiValueDictKeyError, KeyError):
            body['Desc'] = ('Проверьте, что запрос соответствует '
                            'виду deals: <anyfile>, где deals '
                            'это ключ, anyfile, значение в виде файла')
            return None, body

        validators = (
            (self.is_csv(file), 'Проверьте, что высылаемый файл формата .csv'),
            (self.encode_csv(file), ('Проверьте, что данные в файле, '
                                     'соответсвуют формату csv'))
        )
        for (validator_method, message) in validators:
            if not validator_method:
                body['Desc'] = message
                return None, body
        return validators[1]

    def validate_data(self, row):
        """Get row and validate data in it."""
        body = self.error_response_body
        try:
            username = row['customer']
            item = row['item']
            total = int(row['total'])
            quantity = int(row['quantity'])
            date = self.date_lacalization(row['date'])
        except KeyError as exc:
            body['Desc'] = f'Проверьте, что в csv файле есть поле {exc.args}.'
            return None, body
        except ValueError as exc:
            body['Desc'] = ('Проверьте, что дынные '
                            f'соответсвуют типам {exc.args}')
            return None, body
        return (username, item, total, quantity, date), None

    def is_csv(self, file):
        """Return bool if type of file is csv."""
        try:
            return str(file)[-4:] == '.csv'
        except Exception:
            return False

    def encode_csv(self, file):
        """
        Decode csv file to utf-8 and
        return data with OrderedDict's if all right.
        """
        try:
            return csv.DictReader(codecs.iterdecode(file, 'utf-8'))
        except Exception:
            return None

    def date_lacalization(self, date):
        """Transform date:str to datetime and localize it."""
        time_obj = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        return get_default_timezone().localize(time_obj)
