from pyexpat.errors import messages

import requests
from aiogram import Router
from aiogram.types import CallbackQuery

router_balance = Router()



@router_balance.callback_query(lambda p: 'sum_' in p.data)
async def process_callback_button(call: CallbackQuery):
    credit = call.data.split('_')[1]
    await call.message.answer(credit)