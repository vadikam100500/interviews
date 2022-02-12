import logging
from datetime import datetime as dt

import pytz
from pyrogram import Client

import extractor
from settings import API_HASH, API_ID, HANDLED_CHATS, TIME_ZONE, USER_NAME

# from pyrogram import Client, Filters, Message


app = Client(USER_NAME, api_id=API_ID, api_hash=API_HASH)


def today_extract_for_chat(chat_id: str) -> None:
    today_date = dt.utcnow().date()
    # today_extract = []
    for message in app.iter_history(chat_id):
        if dt.utcfromtimestamp(message.date).date() == today_date:
            # Добавь проверку на содержимое
            text_without_emoji = extractor.emoji_filter(message.text)
            if text_without_emoji:
                formated_message = (
                    extractor.extract_from_text(text_without_emoji)
                )
            # today_extract.append(formated_message)

    # extractor.delete_extract_container_folder(chat_id)


def actual_for_all():
    logging.info('Today all started')
    try:
        for handled_chat_id in HANDLED_CHATS:
            logging.info(f'Today {handled_chat_id} started')
            today_extract_for_chat(handled_chat_id)
    except Exception as e:
        logging.exception(e)
    logging.info('Today all finish')


def main():
    current_dt = dt.now(tz=pytz.timezone(TIME_ZONE))
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s:%(levelname)s]: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=f'logs/bot/{current_dt}.txt')
    app.start()
    actual_for_all()
    # Client.idle()
    app.stop()


if __name__ == '__main__':
    main()


# def get_chat_name(message: Message) -> str:
#     first_name = message.chat.first_name
#     if first_name:
#         return first_name
#     else:
#         title = message.chat.title
#         if title:
#             return title
#         else:
#             forward_sender = message.forward_sender_name
#             if forward_sender:
#                 return forward_sender
#             else:
#                 return '*chat name not found*'


# extractor.save_today_actual_xls(today_extract, chat_id)


# def get_msk_formatted_time(message_time) -> str:
#     moscow_tz = pytz.timezone(TIME_ZONE)
#     edit_time = dt.fromtimestamp(message_time, tz=moscow_tz)
#     return edit_time.strftime('%m-%d %H:%M:%S')


# @app.on_deleted_messages()
# def on_messages_delete(client, messages):
#     if len(messages) > 0:
#         force_in_mem_today_actual_for_all()


# @app.on_message(Filters.edited)
# def on_message_edited(client, message):
#     chat_id = message.chat.id
#     if chat_id in HANDLED_CHATS:
#         users = HANDLED_CHATS[chat_id]
#         for to in users:
#             try:
#                 if to == chat_id:
#                     forwarded_message = message
#                 else:
#                     forwarded_message = message.forward(chat_id=to, as_copy=True)
#                 forwarded_message.reply_text('Изменено в "%s"' % get_msk_formatted_time(message.edit_date))
#             except:
#                 logging.error('Error when forward to %s' % to)
#         if dt.utcfromtimestamp(message.date).date() == dt.today().date():
#             force_in_mem_today_actual_for_all()


# @app.on_message()
# def on_message(client, message):
#     chat_id = message.chat.id
#     if not message.empty and chat_id in HANDLED_CHATS:
#         users = HANDLED_CHATS[chat_id]
#         for to in users:
#             try:
#                 if to == chat_id:
#                     forwarded_message = message
#                 else:
#                     forwarded_message = message.forward(chat_id=to, as_copy=True)
#                 forwarded_message.reply_text('Новое сообщение из "%s"' % get_chat_name(message))
#             except:
#                 logging.error('Error when forward to %s' % to)
#         force_in_mem_today_actual_for_all()
