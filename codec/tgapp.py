# !/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.
#
"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation. Press Ctrl-C on the command line or
send a signal to the process to stop the bot.
"""
import html
import json
import logging
import traceback
from typing import Tuple

from telegram import Update, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackContext
)

import codec
from codec.BulkHeart import BulkHeart

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, FAUCETMODE = range(2)


class ApplicationTgApp(BulkHeart):
    def __init__(self, root_path: str, perm: list, options: dict = None):
        super().__init__(root_path, perm, options)
        self.__doc__ = "as"
        self.chat_id = 0
        self.initExpress(self.chat_id)

    def userId(self, update: Update) -> Tuple[bool, int]:
        user_chat_id = -1
        try:
            if update.message is not None:
                # from a text message
                user_chat_id = update.message.chat.id
            elif update.callback_query is not None:
                # from a callback message
                user_chat_id = update.callback_query.message.chat.id
        except AttributeError:
            user_chat_id = update.edited_message.from_user.id

        if user_chat_id > 0:
            user_chat_id = update.message.chat.id
            print("personal chat")
            if user_chat_id == self._developer:
                return (True, user_chat_id,)
            else:
                return (False, user_chat_id,)
        else:
            print("from group")
            user_chat_id = update.message.from_user.id

        print(f"User request from {user_chat_id}")
        return (True, user_chat_id,)

    def start(self, update: Update, context: CallbackContext) -> int:
        (yes, user) = self.userId(update)
        self.chat_id = user
        return FAUCETMODE

    def cmd_drop(self, update: Update, context: CallbackContext) -> int:
        (okuse, user) = self.userId(update)

        if okuse is True:
            hx = update.message.text
            y = hx.split(" ")
            assert1 = True
            assert2 = False
            if len(y) == 1:
                assert1 = False
            else:
                hx = hx.split(" ")[1]
                assert2 = self.check_address(hx)

            if assert2 and assert1:
                okff = self.GetFaucetSystem()
                res = okff.flow(str(user), hx)
                if res:
                    # drop to this address now..
                    ethResult = self.give_eth(hx, okff.GiveAmount)
                    if ethResult:
                        okff.faucet_done(hx)
                        reply_msg = codec.LINE01
                    else:
                        reply_msg = codec.LINE02
                else:
                    reply_msg = codec.LINE03
                okff.done()
            else:
                reply_msg = codec.LINE04
        else:
            reply_msg = codec.LINE05

        update.message.reply_text(reply_msg)
        return FAUCETMODE

    def commands(self) -> list:
        return [
            CommandHandler('coin', self.cmd_drop),
        ]

    def error_handler(self, update: object, context: CallbackContext) -> None:
        """Log the error and send a telegram message to notify the developer."""
        # Log the error before we do anything else, so we can see it even if something breaks.
        logger.error(msg="Exception while handling an update:", exc_info=context.error)
        # traceback.format_exception returns the usual python message about an exception, but as a
        # list of strings rather than a single string, so we have to join them together.
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = ''.join(tb_list)
        # Build the message with some markup and additional information about what happened.
        # You might need to add some logic to deal with messages longer than the 4096 character limit.
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            f'An exception was raised while handling an update\n'
            f'{html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}\n'
            f'chat_data = {html.escape(str(context.chat_data))}\n'
            f'user_data = {html.escape(str(context.user_data))}\n'
            f'<pre>{html.escape(tb_string)}</pre>'
        )

        # Finally, send the message
        context.bot.send_message(chat_id=self._developer, text=message, parse_mode=ParseMode.HTML)

    def main(self, api: str) -> None:
        """Run the bot."""
        # Create the Updater and pass it your bot's token.
        updater = Updater(api)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # Add conversation handler with the states CHOOSING, BASIC_REPLY and UPLOAD_REPLY
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', self.start),
                CommandHandler(codec.LCOMMANDplease, self.cmd_drop),
                CommandHandler(codec.LCOMMANDthankyou, self.cmd_drop),
            ],
            states={
                FAUCETMODE: [
                    CommandHandler(codec.LCOMMANDplease, self.cmd_drop),
                    CommandHandler(codec.LCOMMANDthankyou, self.cmd_drop),
                ],
            },
            fallbacks=self.commands()
        )

        dispatcher.add_handler(conv_handler)
        # dispatcher.add_handler(CallbackQueryHandler(self.bulk_handler_action))
        dispatcher.add_error_handler(self.error_handler)
        # Start the Bot
        updater.start_polling()
        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
