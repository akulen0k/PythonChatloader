import asyncio
import random
from datetime import datetime
import os
import configparser
import commands_test
from database_commands import *
import sys

from generate_tests import generate_test


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
    #await gen_test()
    q = asyncio.Queue()
    upd = [asyncio.create_task(commands_test.update_requests(q)) for n in range(1)]
    handle = [asyncio.create_task(commands_test.handle_request(q)) for n in range(1)]
    await asyncio.gather(*upd)
    #await q.join(*upd)
    #await generate_test(100)


async def gen_test():
    number = random.randint(30, 60)
    await generate_test(number)


def start_with_new():
    delete_all()


if __name__ == '__main__':
    (api_id, api_hash) = get_api_keys()
    settings = get_settings()
    init_db(settings)
    start_with_new()
    commands_test.start('../ChatLoaderBot', api_id, api_hash)
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)\
    print(f'Bot stated.')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

