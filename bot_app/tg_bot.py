import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from settings import config
from handlers import commands, help_command, inline_commands, registration

async def main():
    bot = Bot(f'{config.bot_token.get_secret_value()}')
    dp = Dispatcher(storage=MemoryStorage())
    

    dp.include_routers(commands.router, help_command.router, inline_commands.router, registration.router)

    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    






