import asyncio
from datetime import datetime
import os
import configparser
import commands
from database_commands import *
import sys

import pytz

from tgbot import TgBot
from telethon import TelegramClient
from telethon.sessions import StringSession
'''
Это список операций, которые умеет выполнять бот.

Операции, доступные пользователю:
    Каналы:
        1) Начать отслеживать новый канал
        2) Прекратить отслеживать определенный канал
    Сообщения:
        1) Получить сообщения с определнного канала за определенную дату
        TODO


Внутренние операции:
    Каналы:
        1) Найти канал - ищет канал по хэндлу (и добавляет его в бд, чтобы больше не искать)
        2) Провалидировать, что данные о канале в бд валидные (совпадение хэндла при одинаковом id)
    Сообщения:
        1) Получить сообщения за определенную дату
        2) Скачать все сообщения канала
        * Тут могут быть любые тяжелые операции с бд
        


Операции с базой данных:
    Каналы:
        отдельная таблица, содержащая информацию о канала каналах
        primary key - хэндл
        1) найти канал по хэндлу (channel or null)
        2) добавить канал
        3) пометить информацию о канале как неактуальную
    Запросы:
        отдельная таблица
        primary key - id, url запроса(не отличать http от https!!!), текущий статус
    Сообщения с каналов:
        primary key - id, id канала, само сообщение (реакции?)
        
Операции пользователя:
    1) add-channel/@handle - добавить канал в список с каналами
    2) get-all-channels - получить список всех каналов(id, handle, title)
    3) download-messages/date="11.03.2023", id="1"? - скачать сообщения с канала по id и дате
    4) get-messages/id - получает все сообщения из канала по id
'''

SESSION_NAME = 'ChatLoaderBot'

# gets api keys for telegram bot to log in
def get_api_keys():
    path = "../bot-password.txt"
    if os.path.isfile("bot-password.txt"):
        path = "bot-password.txt"
    with open(path, "r") as f:
        id = int(f.readline())
        hash = f.readline()
        return (id, hash)


# gets settings depend on the env
def get_settings():
    in_container = os.environ.get('IN_A_DOCKER_CONTAINER', False)
    sect = "Container" if in_container else "Development"
    path = '../Settings.ini'
    if os.path.isfile("Settings.ini"):
        path = "Settings.ini"

    parser = configparser.ConfigParser()
    parser.read(path)
    return parser[sect]


async def main():
    q = asyncio.Queue()
    upd = [asyncio.create_task(commands.update_requests(q)) for n in range(1)]
    handle = [asyncio.create_task(commands.handle_request(q)) for n in range(1)]
    await asyncio.gather(*upd)


if __name__ == '__main__':
    (api_id, api_hash) = get_api_keys()
    settings = get_settings()
    init_db(settings)
    #if f"{SESSION_NAME}.session" in os.listdir():
    #    os.remove(f"{SESSION_NAME}.session")
    commands.start(SESSION_NAME, api_id, api_hash)
    print(f'Bot stated.')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
