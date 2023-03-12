"""

Этот класс обрабатывает команды пользователя
Классы очень сырой, пока поддерживается только одна команда

"""

from datetime import datetime
import time

from tgbot_test import TgBotTest
from database_commands import *
from urllib.parse import unquote


bot = TgBotTest

def start(name, api_id, api_hash):
    global bot
    bot = TgBotTest(name, api_id, api_hash)


async def parse_http(req: str):
    req = unquote(req)
    req = req.split("//")
    if len(req) >= 2:
        req[1] = req[1].split("/")
        if len(req[1]) >= 2:
            return req[1][1], *req[1][2:]
    return None


async def update_requests(q: asyncio.Queue) -> None:
    while True:
        req = await read_request()
        if req is not None:
            await process_request(req)
            await q.put(req)


async def handle_request(q: asyncio.Queue) -> None:
    '''
    Операции пользователя:
    1) DONE add-channel/@handle - добавить канал в список с каналами
    2) DONE get-all-channels - получить список всех каналов(id, handle, title)
    3) download-messages/date="11.03.2023", id="1"? - скачать сообщения с канала по id и дате
    4) DONE get-messages/id - получает все сообщения из канала по id
    '''
    while True:
        req = await q.get()
        print(f"got req {req.id}")
        try:
            query = await parse_http(req.url)
            print(query)
            if query is None:
                raise Exception("Invalid query")
            if query[0] == "api":
                if query[1] == 'add-channel':
                    print(f'try to find and add-channel')
                    cur = await bot.find_channel(query[2])
                    await add_channel(cur)
                    req.answer = f"{cur.title} was successfully added to your channels"
                    print(f'added channel {cur.handle}')
                elif query[1] == 'get-messages':
                    print(f'trying to get messages from channel {int(query[2])}')
                    ch = await get_channel_by_id(int(query[2]))
                    if ch is None:
                        raise Exception("Channel was not found into database")
                    msg = await get_messages(ch.channel_id)
                    msg1 = [str(i) for i in msg]
                    req.answer = msg1.__str__()
                    print(f'got messages for {ch.channel_id}')
                elif query[1] == 'get-all-channels':
                    print(f'trying to get all channels')
                    channels = await get_all_channels()
                    ch = [i.getChannel() for i in channels]
                    req.answer = ch
                    print(f'got all channels')
                elif query[1] == 'download-messages':
                    print(f'downloading messages')
                    ch = await get_channel_by_id(int(query[2]))
                    if ch is None:
                        raise Exception("Channel was not found into database")
                    await bot.get_all_messages(ch.channel_id, start_date=datetime.strptime(query[3], '%d.%m.%Y %H:%M'),
                                               end_date=datetime.strptime(query[3], '%d.%m.%Y %H:%M'))
                    req.answer = f'messages from {ch.channel_id} were successfully downloaded'
                    print(f'download finished')
                else:
                    raise Exception("Invalid command")
            else:
                raise Exception("Invalid query")
            req.status = 200
        except Exception as e:
            print(e)
            req.answer = e.__str__()
            req.status = 500
        req.resp = datetime.now()
        await answer_request(req)
        print(f"finished req {req.id}")
        q.task_done()
