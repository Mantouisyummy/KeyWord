#!/usr/bin/python
# -*- coding: UTF-8 -*-

import asyncio
import logging
import os
from os import getenv

from colorlog import ColoredFormatter

from disnake import Intents
from disnake.ext.commands import CommandSyncFlags
from dotenv import load_dotenv

from core.bot import Bot


# pylint: disable=C0116
# pylint: disable=C0115


def main():    
    load_dotenv()

    setup_logging()

    main_logger = logging.getLogger("lava.main")

    loop = asyncio.new_event_loop()

    bot = Bot(
        logger=main_logger,
        command_prefix=getenv("PREFIX", "l!"), intents=Intents.all(), loop=loop,
        command_sync_flags=CommandSyncFlags.default()
    )

    load_extensions(bot)

    bot.run(os.environ["TOKEN"])

def setup_logging():
    """
    Set up the loggings for the bot 
    :return: None
    """
    formatter = ColoredFormatter(
        '%(asctime)s %(log_color)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filename="lava.log", encoding="utf-8", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        handlers=[stream_handler, file_handler], level=logging.INFO
    )


def load_extensions(bot: Bot) -> Bot:
    """
    Load extensions in extensions.json file
    :param bot: The bot to load the extensions to
    :return: The bot
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            bot.load_extension(f"cogs.{filename[:-3]}")

    return bot


if __name__ == "__main__":
    main()
