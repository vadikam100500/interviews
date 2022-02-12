#!/bin/bash
python3 -m venv venv && source venv/bin/activate && \
pip install -r requirements.txt && python3 bot.py


# На условиях, что установлен venv и pip
# смысла в скриптах с 1 командой не вижу, срипт и так будет
# запущен из терминала на подобие "sh <имя скрипта>",
# ну или с доп правами без sh


#  python3 public-server.py