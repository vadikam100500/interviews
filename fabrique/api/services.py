from datetime import datetime
import logging
import os
import time

import requests
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from dotenv import load_dotenv

load_dotenv()

User = get_user_model()

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s:%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=f'logs/MailingManager/{now()}.txt')


class MailingManager(object):
    API_TOKEN = os.getenv('API_TOKEN')
    API_ENDPOINT = os.getenv('API_ENDPOINT')
    service_json = {
        "id": None,
        "phone": None,
        "text": None,
    }
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    RETRY_TIME = 10

    def __init__(self, tag, code, start_date, end_date, text, inst, mess_obj):
        self.tag = tag
        self.code = code
        self.start_date = start_date
        self.end_date = end_date
        self.text = text
        self.mailing_inst = inst
        self.Message = mess_obj

    def start(self):
        current_time = now()
        if self.start_date < current_time < self.end_date:
            try:
                users = User.objects.filter(tag=self.tag,
                                            operator_сode=self.code)
            except Exception as e:
                logging.exception(e)
                raise Exception('Создайте пользователей!!!')
            logging.INFO('Пользователи получены и отправлены на рассылку.')
            self.mail_ontime(users, current_time)
        if current_time > self.start_date:
            logging.INFO('Пользователи отправлены на отложенную рассылку.')
            self.mail_deferred()

    def mail_ontime(self, users, current_time):
        for user in users:
            try:
                mess = self.Message.objects.create(
                    send_time=current_time, status='S',
                    mailing=self.mailing_inst, contact=user)
                json = self.service_json.copy()
                json["id"] = mess.id
                json["phone"] = user.phone
                json["text"] = self.text
            except Exception as e:
                logging.exception(e)
            circle = 5
            while circle:
                try:
                    response = self.send_mail(mess.id, self.headers, json)
                    if response.status_code != 200 and circle == 1:
                        mess.update(status='N')
                    elif response.status_code == 200:
                        circle = 0
                except Exception as e:
                    logging.exception(e)
                    circle -= 1
                    time.sleep(self.RETRY_TIME)

    # @celery_app.task(bind=True, default_retry_delay=10 * 60)
    def send_mail(self, id, headers, json):
        try:
            return requests.post(f'{self.API_ENDPOINT}{id}', headers, json)
        except Exception as e:
            logging.exception(e)
            # self.retry(exc=e)

    def mail_deferred(self):
        # SORRY it's enough time to do this =(
        pass
