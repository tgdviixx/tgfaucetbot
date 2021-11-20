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
import os

from codec.tg import ApplicationTgApp
from key import TG_API

ROOT = os.path.join(os.path.dirname(__file__))

# This can be your own ID, or one for a developer group/channel.
# You can use the /start command of this bot to see your chat id.
DEVELOPER_CHAT_ID = 681285432
ALSO_ALLOWED = [1010296833]

if __name__ == '__main__':
    allow = [DEVELOPER_CHAT_ID]
    allow.extend(ALSO_ALLOWED)
    app = ApplicationTgApp(ROOT, allow, dict(
        lock_token=False,
        collect_fee=False
    ))
    app.main(TG_API)

"""setup the data base schema
from codec.faucetcore import create_schema, oncedrop
create_schema()
oncedrop()
"""
