import asyncio

import psycopg
from Message import Message
from Request import Request
from channel import Channel, ChannelBd

'''

Базы данных:
    1) requests - база, где будут храниться запросы пользователя и их статус коды
        id PRIMARY KEY SERIAL - id
        url TEXT NOT NULL - url запроса
        request_time timestamp NOT NULL - время запроса
        response_time timestamp NULL - время ответа(NULL - не обработан) 
        answer TEXT NULL - ответ от на запрос
        status INTEGER NULL - статус запроса (NULL - не обработан)
        
    2) messages - база данных, содержащая скачанные пользователем сообщения
        id PRIMARY KEY SERIAL - id(в базе данных!!!!)
        channel_id BIGINT NOTNULL - id канала
        date timestamp - время, в которое было написано сообщение
        message TEXT - само сообщение
        TODO добавить реакции/имя пользователя(если есть) и т.д.
    
    3) channels - база данных, содержащая каналы 
       id PRIMARY KEY SERIAL - id канала
       channel_id BIGINT NOT NULL - id канала в api телеграмма
       handle TEXT NOT NULL - хэндл канала (всегда начинается с @)
       title TEXT NOT NULL - название канала

'''

config = None


def init_db(cfg):
    global config
    config = cfg
    create_messages()
    create_request()
    create_channels()

def delete_all():
    with psycopg.connect(
            config["PostgresOptions"]) as aconn:
        with aconn.cursor() as acur:
            acur.execute(
                """DROP TABLE messages""")
            acur.execute(
                """DROP TABLE requests""")
            acur.execute(
                """DROP TABLE channels""")
    create_messages()
    create_request()
    create_channels()


def create_messages():  # creates messages table
    with psycopg.connect(
            config["PostgresOptions"]) as aconn:
        with aconn.cursor() as acur:
            acur.execute(
                """CREATE TABLE IF NOT EXISTS messages( 
                id SERIAL PRIMARY KEY, 
                channel_id BIGINT NOT NULL,
                date TIMESTAMP,
                message TEXT)""")


async def get_messages(channel_id: int):  # gets all messages by chatid
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            rows = await acur.execute(
                """SELECT * FROM messages WHERE 
                channel_id = %s""", (channel_id, ))
            res = await rows.fetchmany(100)  # <---- тут ограничение, потом что-нибудь придумаем
            if res is None:
                return []

            res1 = [Message(line=i) for i in res]
            return res1


# async def get_message   <--- тут любые запросы сообщений, любые операции


async def write_messages(messages: list):  # adds list of messages to database
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            for i in messages:
                await acur.execute(
                    """INSERT INTO messages (channel_id, date, message) 
                    VALUES (%s, %s, %s)""", (i.channel_id, i.date.strftime("%m.%d.%Y %H:%M:%S"), i.message, ))


async def check_for_message(message):  # returns True if message presented in database and else either
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            rows = await acur.execute(
                """SELECT * FROM messages WHERE 
                channel_id = %s AND date = %s AND message = %s""",
                (message.channel_id, message.date.strftime("%m.%d.%Y %H:%M:%S"), message.message, ))
            res = await rows.fetchone()
            if res is None or len(res) == 0:
                return False
            return True


def create_request():  # creates requests table
    with psycopg.connect(
            config["PostgresOptions"]) as aconn:
        with aconn.cursor() as acur:
            acur.execute(
                """CREATE TABLE IF NOT EXISTS requests(
                id SERIAL PRIMARY KEY,  
                url TEXT NOT NULL, 
                request_time TIMESTAMP NOT NULL, 
                response_time TIMESTAMP, 
                answer TEXT,
                status INTEGER)""")


async def read_request():  # gets first unprocessed request
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            req = await acur.execute(
                """SELECT * FROM requests WHERE 
                status is NULL""")
            req = await req.fetchone()
            if req is None:
                return req
            req = Request(req)
            return req


async def answer_request(response: Request):  # answers to request
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            req = await acur.execute(
                """SELECT * FROM requests WHERE 
                id = %s""", (response.id, ))
            req = await req.fetchone()
            if req is None:
                raise Exception(f"Request to response was not found: id = {response.id}")

            req = Request(req)
            if req.status != -1:
                raise Exception(f"Request to response was already handler: id = {response.id}")
            await acur.execute(
                """UPDATE requests SET 
                (response_time, answer, status) = (%s, %s, %s) 
                WHERE id = %s""", (response.resp.strftime("%m.%d.%Y %H:%M:%S"), response.answer, response.status,
                                   response.id, )
            )


async def process_request(req: Request):  # request in queue
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                """UPDATE requests SET 
                status = %s
                WHERE id = %s""", (-1, req.id, )
            )


async def generate_request(req: Request):  # only for testing
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                """INSERT INTO requests 
                (id, url, request_time) VALUES 
                (%s, %s, %s)""", (req.id, req.url, req.req, ))


def create_channels():  # creates messages table
    with psycopg.connect(
            config["PostgresOptions"]) as aconn:
        with aconn.cursor() as acur:
            acur.execute(
                """CREATE TABLE IF NOT EXISTS channels(
                id SERIAL PRIMARY KEY, 
                channel_id BIGINT NOT NULL,
                handle TEXT NOT NULL,
                title TEXT NOT NULL)""")


async def get_all_channels():
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            req = await acur.execute(
                """SELECT * FROM channels""")
            req = await req.fetchall()
            if req is None:
                return []

            ans = []
            for i in range(len(req)):
                ans.append(ChannelBd(lst=req[i]))
            return ans


async def get_channel(handle: str):
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            req = await acur.execute(
                """SELECT * FROM channels 
                WHERE handle = %s""", (handle, ))
            req = await req.fetchone()
            if req is None:
                return None

            return ChannelBd(lst=req)


async def get_channel_by_id(id: int):
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            req = await acur.execute(
                """SELECT * FROM channels 
                WHERE id = %s""", (id, ))
            req = await req.fetchone()
            if req is None:
                return None

            return ChannelBd(lst=req)


async def exists_channel(ch: ChannelBd):
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            rows = await acur.execute(
                """SELECT * FROM channels WHERE 
                channel_id = %s""",
                (ch.channel_id, ))
            res = await rows.fetchone()
            if res is None or len(res) == 0:
                return False
            return True


async def add_channel(ch: ChannelBd):
    if await exists_channel(ch):
        return
    async with await psycopg.AsyncConnection.connect(
            config["PostgresOptions"]) as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                """INSERT INTO channels 
                (channel_id, handle, title) VALUES (%s, %s, %s)""", (ch.channel_id, ch.handle, ch.title, ))
