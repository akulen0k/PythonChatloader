import time

from telethon import TelegramClient
from date_comp import *
import pytz
from time import sleep
import asyncio
from telethon.tl.types import Channel
import database_commands
from telethon.sessions import StringSession
from channel import ChannelBd

'''

В этом файле описан бот, который взаимодействует с telegram.
Бот умеет выполнять следующие команды:
    1) Найти канал по хэндлу (@*+)
    2) Получить сообщения из канала принадлежащие определенным дням
    3) Получить сообщения из канала в определенный день
     
'''


class TgBot:

    def __init__(self, session_name, api_id, api_hash):
        print(1)
        self.client = TelegramClient(session_name, api_id, api_hash)
        print(3)
        self.client.start()
        print(2)

    # gets all messages in certain date
    def get_messages_by_date(self, channel_id, date: datetime):  # sync!!!
        tomorrow = date + datetime.timedelta(days=1)
        messages = []

        for msg in self.client.iter_messages(Channel(channel_id), offset_date=tomorrow, wait_time=5):
            if date_is_less(msg.date, date):
                return messages
            if compare_dates(date, msg.date):
                messages.append(msg)
            time.sleep(5)

        if len(messages) == 0:
            return -1
        return messages

    # download all messages from chat
    # check_db - stops if found message that is presented in database
    async def get_all_messages(self, channel_id, start_date=None, end_date=None, check_db=True):
        if start_date is None:
            start_date = datetime.datetime.now(tz=pytz.utc)

        if end_date is None:
            end_date = start_date
            end_date = end_date - datetime.timedelta(weeks=4 * 12 * 10)

        if end_date > start_date:
            raise Exception("end_date can't be greater than start_date")

        while not compare_dates(start_date, end_date):
            messages = self.get_messages_by_date(channel_id, start_date)
            if messages == -1:  # there won't be any messages further
                break
            if check_db and (len(messages) == 0 or await database_commands.check_for_message(messages[-1])):
                return

            await database_commands.write_messages(messages)

            start_date = start_date - datetime.timedelta(days=1)
            sleep(1)

    # finds channel by handle in global chats or raises an exception
    async def find_channel(self, channel_handle: str):
        if len(channel_handle) == 0:
            raise Exception("Handle can't be empty")

        if channel_handle[0] != '@':
            raise Exception("Handle must starts with \'@\'")

        res = await self.client.get_entity(entity=channel_handle[1:])

        if res is None:
            raise Exception("Channels with this handle were not found")

        res = ChannelBd(res)

        return res
