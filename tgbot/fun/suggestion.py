import json

from aiogram.filters.command import Command
from aiogram.filters import StateFilter, BaseFilter
from aiogram import Router, F, Bot
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, IS_MEMBER
from aiogram import types
import sqlite3
import os
import requests

from tgbot.settings import *
from tgbot.keyboard import *


channel = []
admin_ch = {}
router = Router()
imge = {}

# router.message.filter(F.chat.type == "channel")


class Post(StatesGroup):
    text = State()
    img = State()
    ok = State()


@router.my_chat_member(ChatMemberUpdatedFilter((IS_NOT_MEMBER|IS_MEMBER) >> ADMINISTRATOR))
async def admin_bot_mes(event:ChatMemberUpdated, bot:Bot):
    channel = {"id": event.chat.id, "name":event.chat.title, "admin":json.dumps([i.user.id for i in await bot.get_chat_administrators(event.chat.id)])}
    r = requests.post(url + "/new_channel", data=channel)
    if r.status_code == 201:
        msg = await event.answer(
            text=f"Меню предложки", reply_markup=get_menu_keyboard(event.chat.id).as_markup()
        )
        await bot.send_message(event.from_user.id, "Вы сделали все правельно, я готов к работе")
        await bot.pin_chat_message(event.chat.id, message_id=msg.message_id)
    else:
        await bot.send_message(event.from_user.id, "Что-то пошло не так, попробуйте позже")


@router.my_chat_member(ChatMemberUpdatedFilter(ADMINISTRATOR>>IS_NOT_MEMBER))
async def member_bot_mes(event:ChatMemberUpdated, bot:Bot):
    r = requests.post(url+"/delete_ch", data={"id":event.chat.id})
    if r.status_code == 201:
        await bot.send_message(event.from_user.id, f"Вы удалили меня из канала {event.chat.title}\nЕсли вам что-то не понравилось напишите @{nickname} ")


@router.message(Command("start"))
async def start(meg: Message):
    await meg.answer(
        text=f"Меню предложки", reply_markup=get_menu_keyboard(event.chat.id).as_markup()
    )


@router.callback_query(F.data.startswith("sug"))
async def post1(callback: CallbackQuery, state: FSMContext, bot:Bot, imge: dict):
    await state.clear()
    await state.set_state(Post.text)
    await state.update_data(chanel_id=callback.data.split('_')[1])
    imge[callback.from_user.id] = []
    await bot.send_message(callback.from_user.id, "Напишите пост")
    await callback.answer()


@router.message(Post.text)
async def process_name(message: Message, state: FSMContext):
    print(await state.get_state())
    await state.update_data(post_text=message.text)
    await message.answer("теперь скрины")
    await state.set_state(Post.img)


@router.message(Post.img, F.photo)
async def img_post(meg: Message, state: FSMContext, bot: Bot, imge: dict):

    await bot.download(meg.photo[-1], os.path.join("imge_post", f"{meg.photo[-1].file_unique_id}.jpg"))
    imge[meg.from_user.id].append(os.path.join("imge_post", f"{meg.photo[-1].file_unique_id}.jpg"))
    await state.update_data(images=imge[meg.from_user.id])
    await state.set_state(Post.ok)
    await meg.answer("Для подтверждения выберете да, а для отклона нет", reply_markup=yes_or_no().as_markup())


@router.message(Post.ok, F.text.lower() == "да")
async def post_ok(meg:Message, state:FSMContext):
    data = await state.get_data()
    await state.clear()
    data["id"] = meg.from_user.id
    data["user"] = meg.from_user.username
    print(data)
    r = requests.post(url + "/add_post", data=data)
    if r.status_code == 201:
        await meg.answer("Пост отправлен на проверку")


@router.message(Post.ok, F.text.lower() == "нет")
async def post_no(meg:Message, state:FSMContext):
    await state.clear()
    await meg.answer("Хорошо")


