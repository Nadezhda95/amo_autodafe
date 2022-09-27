#!/usr/bin/env python
import os
from amo_client import create_client
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ContentType
from aiogram.dispatcher.filters import filters

token = os.environ.get('BOT_TOKEN')
bot = Bot(token)
dp = Dispatcher(bot)

client = create_client()


@dp.message_handler(commands=['start'])
async def welcome(msg: types.Message):
    await msg.answer('Bot started')


@dp.message_handler(commands=['lead'])
async def get_lead(msg: types.Message):
    lead_id = msg.text.split(' ')[1]
    print(lead_id)
    buttons = {
        "b1": {
            "text": "Отправить комментарий",
            "callback_data": "post_note"
        }
    }

    keyboard_lead = InlineKeyboardMarkup().add(buttons["b1"])
    response = client.get_lead(lead_id)

    await msg.reply(response, reply_markup=keyboard_lead)


@dp.callback_query_handler(text=["post_note"])
async def create_note(call: types.CallbackQuery):
    msg = call.message
    lead_id = msg.text.split("{'id': ")[1].split(", 'name'")[0]
    print(lead_id)
    msg_to_send = f'Напишите комментарий к лиду с ид {lead_id}'
    force_reply = types.ForceReply.create('Комментарий')
    print(force_reply)
    await call.message.answer(text=msg_to_send, reply_markup=force_reply)


@dp.message_handler(is_reply=True)
async def post_note(msg: types.Message):
    client.post_note(lead_id=msg.reply_to_message.text.split('ид ')[1], note=msg.text)
    # client.create_entity_note('leads', msg.text, msg.reply_to_message.text.split('ид ')[1])
    await msg.answer('Комментарий публикован')


executor.start_polling(dp, skip_updates=True)
