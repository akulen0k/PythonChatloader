import asyncio
import random
from datetime import datetime
import os
import configparser
import commands_test
from database_commands import *
import sys

from src.generate_tests import generate_test


# gets api keys for telegram bot to log in
def get_api_keys():
    with open("../bot-password.txt", "r") as f:
        id = int(f.readline())
        hash = f.readline()
        return (id, hash)


# gets settings depend on the env
def get_settings():
    in_container = os.environ.get('IN_A_DOCKER_CONTAINER', False)
    sect = "Container" if in_container else "Development"

    parser = configparser.ConfigParser()
    parser.read('../Settings.ini')
    return parser[sect]


async def main():
    await gen_test()
    q = asyncio.Queue()
    upd = [asyncio.create_task(commands_test.update_requests(q)) for n in range(1)]
    handle = [asyncio.create_task(commands_test.handle_request(q)) for n in range(1)]
    await asyncio.gather(*upd)
    #await q.join(*upd)
    #await generate_test(100)


async def gen_test():
    number = random.randint(30, 60)
    await generate_test(number)

if __name__ == '__main__':
    (api_id, api_hash) = get_api_keys()
    settings = get_settings()
    init_db(settings)
    commands_test.start('../ChatLoaderBot', api_id, api_hash)
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

