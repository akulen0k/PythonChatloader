import datetime

from database_commands import *
import random
from tgbot_test import *


'''
Файл для создания тестов

'''

commands = ['add-channel', 'get-messages', 'get-all-channels', 'download-messages', 'fake_command']


def generate_url():
    url = "https://oursite.ru/api/"
    command_id = random.randint(0, len(commands) - 1)
    url = url + commands[command_id]
    if command_id == 0:
        url = url + '/@' + generate_rndstr()
    elif command_id == 1:
        url = url + '/' + str(random.randint(1, 3))
    elif command_id == 3:
        url = url + '/' + str(random.randint(0, 3)) + '/' + '20.03.2023 21:00'
    return url


async def generate_test(n : int):
    for _ in range(n):
        req = Request(lst=(random.randint(0, 10**9), generate_url(), datetime.datetime.now()))
        await generate_request(req)
        print(f"generated test {_}")