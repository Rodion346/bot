from pyexpat.errors import messages

import requests
from aiogram import Router, F, Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from generate_img_clot import bot

router_balance = Router()



@router_balance.callback_query(lambda c: 'sum_' in c.data)
async def process_callback_button(call: CallbackQuery):
    credit = int(call.data.split('_')[1])
    await call.message.answer(f"{credit}")