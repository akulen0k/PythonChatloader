"""

Этот класс обрабатывает команды пользователя
Классы очень сырой, пока поддерживается только одна команда

"""

from datetime import datetime
import time

from tgbot import TgBot
from database_commands import *
from urllib.parse import unquote


bot = TgBot


def start(name, api_id, api_hash):
    global bot
    bot = TgBot(name, api_id, api_hash)


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
        await asyncio.sleep(0.1)
        req = await read_request()
        if req is not None:
            await process_request(req)
            await q.put(req)


async def handle_request(q: asyncio.Queue) -> None:
    req = await q.get()
    print('handling request')
    try:
        query = await parse_http(req.url)
        if query is None:
            raise Exception("Invalid query")
        if query[0] == "api":
            if query[1] == 'add-channel':
                cur = await bot.find_channel(query[2])
                await add_channel(cur)
                req.answer = f"{cur.title} was successfully added to your channels"
            elif query[1] == 'show-messages':
                ch = await get_channel_by_id(int(query[2]))
                if ch is None:
                    raise Exception("Channel was not found into database")
                msg = await get_messages(ch.id)
                msg1 = [str(i) for i in msg]
                req.answer = msg1.__str__()
            elif query[1] == 'get-all-channels':
                channels = await get_all_channels()
                ch = [i.getChannel() for i in channels]
                req.answer = ch.__str__()
                print(f'got all channels')
            elif query[1] == 'download-messages':
                ch = await get_channel_by_id(int(query[2]))
                if ch is None:
                    raise Exception("Channel was not found into database")
                print(query)
                await bot.get_all_messages(ch.channel_id, ch.handle, start_date=datetime.strptime(query[3], '%d.%m.%Y %H:%M'),
                                           end_date=datetime.strptime(query[3], '%d.%m.%Y %H:%M'))
                req.answer = f'messages from {ch.channel_id} were successfully downloaded'
                print(f'downloaded messages from {ch.channel_id}')
            else:
                raise Exception("Invalid command")
        else:
            raise Exception("Invalid query")
        req.status = 200
    except Exception as e:
        req.answer = e.__str__()
        req.status = 500
    req.resp = datetime.now()
    print(req.get_value())
    await answer_request(req)
    q.task_done()


