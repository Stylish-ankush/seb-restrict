#Github.com/Vasusen-code

from pyrogram import Client

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from decouple import config
import logging, time, sys

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = config("6435225", default=None, cast=int)
API_HASH = config("4e984ea35f854762dcde906dce426c2d", default=None)
BOT_TOKEN = config("6813489985:AAHZPCBlcgIDoB3tk3OAWZz54yCqYSkctWU", default=None)
SESSION = config("BQEqxgYAeX7NZr87yxLntrWNXtSjQarvL7G2ylxO0VKP7ugk5g_KvcoNlBFHHizBjYv_JLKFJ03gs9Hli1xkaw8_Z7WhXfUpvNwMQnJYDW0U7sj86Cm6vYSlVPwd7jUEdxS0IIEE0hHsJKNxOumWgrISf_OEMXl700bhYKHC47gX5njS1UvwCu_WSlcD_nVcIvuDIRT9lRxNQQCXQ_zn4Sdwd9EN2gakD5DOcLu-maROqiiW9812xj5vnchinFY_ixh3OX_FOlUQkY5OUsW02BlhgZjpQqsgVktlXsecPsCCP5cghAbsSyXZyFGB5IE-JcDZxr7IMrjP2R_pXftAslsj9pvD2QAAAAF8HBVkAA", default=None)
FORCESUB = config("Insane_updates", default=None)
AUTH = config("6178003527", default=None, cast=int)

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 

userbot = Client("saverestricted", session_string=SESSION, api_hash=API_HASH, api_id=API_ID) 

try:
    userbot.start()
except BaseException:
    print("Userbot Error ! Have you added SESSION while deploying??")
    sys.exit(1)

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)    

try:
    Bot.start()
except Exception as e:
    print(e)
    sys.exit(1)
