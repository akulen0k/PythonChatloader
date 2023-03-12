import random
import string
import time

from telethon import TelegramClient
from date_comp import *
import pytz
from time import sleep
import asyncio
from telethon.tl.types import Channel
import database_commands
from telethon.sessions import StringSession
from Message import Message
from channel import ChannelBd


'''

В этом файле описан бот, который взаимодействует с telegram.
Бот умеет выполнять следующие команды:
    1) Найти канал по хэндлу (@*+)
    2) Получить сообщения из канала принадлежащие определенным дням
    3) Получить сообщения из канала в определенный день

'''


def generate_rndstr():
    n = random.randint(0, 100);
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


class TgBotTest:

    def __init__(self, session_name, api_id, api_hash):
        pass

    # gets all messages in certain date
    def get_messages_by_date(self, channel_id, date: datetime):  # sync!!!
        tomorrow = date + datetime.timedelta(days=1)
        messages = []

        n = random.randint(0, 10)

        for i in range(n):
            msg = Message(line=(random.randint(1, 10**9), channel_id, datetime.datetime.now(),
                                generate_rndstr()))
            messages.append(msg)

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

        for i in range(5):
            messages = self.get_messages_by_date(channel_id, start_date)
            if messages == -1:  # there won't be any messages further
                break
            if check_db and await database_commands.check_for_message(messages[-1]):
                return

            await database_commands.write_messages(messages)

            #start_date = start_date - datetime.timedelta(days=1)
            #sleep(1)

    # finds channel by handle in global chats or raises an exception
    async def find_channel(self, channel_handle: str):
        if len(channel_handle) == 0:
            raise Exception("Handle can't be empty")

        if channel_handle[0] != '@':
            raise Exception("Handle must starts with \'@\'")

        res = ChannelBd(lst=(random.randint(0, 10**9), random.randint(0, 10**9),
                             channel_handle, generate_rndstr()))

        return res