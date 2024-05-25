import asyncio
from fun import suggestion
from aiogram import Bot, Dispatcher
from tgbot.settings import *
from aiogram.fsm.storage.memory import MemoryStorage
# Доп. импорт для раздела про стратегии FSM
from aiogram.fsm.strategy import FSMStrategy

async def main():
    # Объект бота
    bot = Bot(token=BOT_TOKEN)
    # Диспетчер
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.GLOBAL_USER)
    dp.include_routers(suggestion.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("ты крутой")
    asyncio.run(main())
