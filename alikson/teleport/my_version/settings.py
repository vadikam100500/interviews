import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve()

# telegram
USER_NAME = os.getenv('USER_NAME')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

# DEBUG = os.getenv('DEBUG', default=False)


def comma_separated_list(value: str):
    return [x.strip() for x in value.split(',') if x.strip()]


TIME_ZONE = 'Europe/Moscow'

# Chats for parser
HANDLED_CHATS = comma_separated_list(os.getenv('HANDLED_CHATS'))

# Campanies for parser
COMPS = comma_separated_list(os.getenv('COMPS'))

EXTRA_WORDS = []


# # parser
# EXTRA_WORDS = [
#     'Silver', 'Bronze', 'Black',
#     'Blue', 'Pink'
# ]
# EXTRA_WORDS = [word.lower() for word in EXTRA_WORDS]


# # handler
# # recommendation for developer: use chat id's
# HANDLED_CHATS = {
#     #mitrion chat
#     -1001173851201: [631288367, 401959243,640495122],
#     #mitrion fallback
#     -1001381147394: [631288367, 401959243,640495122],
#     # extractor test
#     -409330338: [-409330338],
#     # 1000 trifles A01
# #    -1001449349991: [-1001255055406],
#     #Alikson +79816841206
# #    -1001394956746: [-1001255055406],
# }

