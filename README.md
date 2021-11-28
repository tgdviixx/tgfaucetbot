Auto-Reply-Telegram-TOKEN-Faucet-bot
========

Telethon
========

**Telethon** is an `asyncio
<https://docs.python.org/3/library/asyncio.html>`_ **Python 3** library
to interact with Telegram's API.

**If you're upgrading from Telethon pre-1.0 to 1.0, please make sure to read**
`this section of the documentation
<https://telethon.readthedocs.io/en/latest/extra/basic/asyncio-magic.html>`_,
or ``pip install telethon-sync`` which is compatible with `synchronous code
<https://github.com/LonamiWebs/Telethon/tree/sync>`_. Don't forget to remove
the asynchronous version (``pip uninstall telethon``) if you do install sync.

What is this?
-------------

It is a simple script to run the /faucet action in the BTC Faucet telegram bot.

Installing
----------


Execution
----------
  python3 tgoktinit.py

Trying something new
----------
Trying to manipulate the timestamp
```

import datetime

x = datetime.datetime.now()
now99 = datetime.datetime.now()
now1 = now99.strftime("%H:%M:%S")

time_1 = datetime.timedelta(hours=0, minutes=0, seconds=0)

s1 = now99.strftime("%H:%M:%S")
s2 = '09:00:00'
FMT = '%H:%M:%S'
tdelta = datetime.datetime.strptime(s1, FMT) - datetime.datetime.strptime(s2, FMT)
print(tdelta.total_seconds())
print(tdelta > time_1)

print(now99)


```


Key file format is going to be like this

```
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# exchange send coin
private_key = '---'
wallet_address = '---'
TG_API = "---------"
# This can be your own ID, or one for a developer group/channel.
# You can use the /start command of this bot to see your chat id.
DEVELOPER_CHAT_ID = 00000
ALSO_ALLOWED = [00000]
LISTDE = {
    "HashOracle": "----",
    "PriceOracle": "----",
}

```


To start your first db

```
from codec.faucetcore import create_schema, oncedrop

create_schema()

oncedrop()

```