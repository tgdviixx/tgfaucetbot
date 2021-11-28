# !/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import datetime
import os

from moody import conf, Config

from codec.faucetcore import TokenKeeperX
from codec.tg import ApplicationTgApp
from key import TG_API, ALSO_ALLOWED, DEVELOPER_CHAT_ID

ROOT = os.path.join(os.path.dirname(__file__))


# This can be your own ID, or one for a developer group/channel.
# You can use the /start command of this bot to see your chat id.


class RSCFaucet(TokenKeeperX):
    def __init__(self, root: str):
        delta = datetime.timedelta(hours=0, minutes=2, seconds=0)
        super().__init__(root, "RSC", 0.1, delta)


class RSACacuetApp(ApplicationTgApp):

    def __init__(self, root_path: str, perm: list, options: dict = None):
        super().__init__(root_path, perm, options)

    def GetFaucetSystem(self) -> RSCFaucet:
        return RSCFaucet(self._rootpath)

    def Connect(self) -> Config:
        return conf.RSCMainnet()


def oncedrop():
    okf = RSCFaucet(ROOT)
    okf.flow("rsc", "0x734897283479278797879")


def create_schema():
    okf = RSCFaucet(ROOT)
    okf.removeTable()
    okf.sampleNewTable()
    okf.insertDataSample()
    okf.done()


def init():
    allow = [DEVELOPER_CHAT_ID]
    allow.extend(ALSO_ALLOWED)
    app = RSACacuetApp(ROOT, allow, dict(
        lock_token=False,
        collect_fee=False
    ))
    app.main(TG_API)


if __name__ == '__main__':
    init()
