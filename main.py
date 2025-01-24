import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode

from common.bot_cmds_list import keyboard_private_static
from handlers.privat import user_private

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ALLOWED_UPDATES = ["message","edited_message"]

bot = Bot(token = os.getenv("TOKEN"))

dp = Dispatcher()

dp.include_router(user_private)

async def main():
    await bot.delete_webhook(drop_pending_updates = True)
    await dp.start_polling(bot, allowed_updates = ALLOWED_UPDATES)
    await bot.set_my_commands(commands = keyboard_private_static, scope = types.BotCommandScopeAllPrivateChats())

asyncio.run(main()) 