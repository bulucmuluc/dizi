# Property of Kor.PiracyTeam - GNU General Public License v2.0

from helpers.guncelTarih import guncelTarih
from platform import python_version
from pyrogram import Client, __version__
import pkg_resources
from pyrogram.raw.all import layer
from info import ADMINS, SESSION, API_ID, API_HASH, BOT_TOKEN, bot_version, LOG
from utils import temp
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
from database.users_chats_db import db
from database.ia_filterdb import Media

def get_package_versions(file = 'requirements.txt'):
    diger = f"Python: {python_version()} - Pyrogram: {__version__} - Layer: {layer}" \
            f"\nBot Sürümü: {bot_version}"
    toret = []
    file1 = open(file, 'r')
    lines = file1.readlines()
    file1.close()
    
    for line in lines:
        try:
            v = pkg_resources.get_distribution(line.strip()).version
        except Exception as e:
            LOG.exception(e)
            continue
        toret.append(f"{line.strip()}=={v}")
    
    return f'\n{diger}\n\nPython Paketleri:\n\n' + '\n'.join(toret) + '\n'

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5
        )

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.MY_ID = me.id
        temp.MY_USERNAME = me.username
        temp.MY_NAME = me.first_name
        self.username = '@' + me.username
        temp.info_bot_str = f"{me.username} ({me.id}) {get_package_versions()}"
        LOG.info(f"Started: {temp.info_bot_str}")
        if len(ADMINS) != 0:
            try: await self.send_message(
                text=f"✅ Doğdum @{me.username} (`{me.id}`) \
                    \n\nTarih: {guncelTarih()}{get_package_versions()} \
                    \nTıkla: /start - /log",
                chat_id=ADMINS[0], reply_markup=ikm(temp.kapat_btn))
            except Exception as t: LOG.exception(str(t))

    async def stop(self, *args):
        if len(ADMINS) != 0:
            try: await self.send_message(
                text=f"❌ Öldüm @{temp.MY_USERNAME} (`{temp.MY_ID}`) \
                    \n\nTarih: {guncelTarih()} {get_package_versions()}",
                chat_id=ADMINS[0], reply_markup=ikm(temp.kapat_btn))
            except Exception as t: LOG.exception(str(t))
        await super().stop()
        LOG.info(f"Stopped: {temp.info_bot_str}")

app = Bot()
app.run()
