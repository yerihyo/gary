#!/usr/bin/env python3

import logging
import os

from functools import lru_cache, reduce

from discord import Client
from nose.tools import assert_true

from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.socialmedia.discord.discord_tool import DiscordTool, DiscordLogger
from gary.singleton.khala.gary_khala import GaryCommand
from gary.singleton.logger.gary_logger import GaryLogger

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
FILE_NAME = os.path.basename(FILE_PATH)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 5, FILE_DIR)


class DiscordClient:
    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def client(cls):
        client = Client()
        client.event(cls.on_ready)
        client.event(cls.on_message)
        return client

    @classmethod
    async def on_ready(cls):
        logger = GaryLogger.func_level2logger(cls.on_ready, logging.DEBUG)

        client = cls.client()
        logger.info({"client.user.name": client.user.name,
                     "client.user.id": client.user.id,
                     "client": client,
                     })

    @classmethod
    async def on_message(cls, message):
        # from henrique.main.singleton.khala.henrique_khala import HenriqueKhala
        # from khala.singleton.messenger.discord.internal.packet_discord import PacketDiscord
        # from khala.singleton.messenger.discord.internal.chatroom_discord import ChatroomDiscord
        # from henrique.main.singleton.khala.henrique_khala import HenriqueCommand

        logger = GaryLogger.func_level2logger(cls.on_message, logging.DEBUG)
        client = cls.client()
        text_in = message.content

        logger.debug({"message": message, })

        if DiscordTool.user_message2is_author(client.user, message):
            return

        text_out = GaryCommand.reply(text_in)
        if not text_out:
            return

        await message.channel.send(text_out)


def main():
    from gary.singleton.logger.gary_logger import GaryLogger

    # KhalaLogger.attach_stderr2loggers(logging.DEBUG)
    DiscordLogger.attach_stderr2loggers(logging.DEBUG)
    GaryLogger.attach_stderr2loggers(logging.DEBUG)

    start_discord()

def start_discord():
    from gary.singleton.env.gary_env import GaryEnv

    logger = GaryLogger.func_level2logger(start_discord, logging.DEBUG)
    logger.debug({"GaryEnv.env()": GaryEnv.env()})

    # HenriqueWarmer.warmup_all()

    # maybe update?
    # https://stackoverflow.com/a/50981577
    client = DiscordClient.client()
    discord_token = GaryEnv.key2value("DISCORD_TOKEN")
    logger.debug({"discord_token": discord_token})

    assert_true(discord_token)
    client.run(discord_token)


if __name__ == "__main__":
    main()
