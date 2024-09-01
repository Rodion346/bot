from pyexpat.errors import messages

import requests
from aiogram import Router
from aiogram.types import CallbackQuery

from bot.routes.generate_img_clot import bot
from config import BASE_URL_API

router_balance = Router()



@router_balance.callback_query(lambda p: 'sum_' in p.data)
async def process_callback_button(call: CallbackQuery):
    cal_data = call.data
    credit = cal_data.split("_")[2].split(" ")[1].strip()
    payload = {"id": f"{call.from_user.id}", "new_balance": int(credit), "type_balance": 1}
    requests.post(f"{BASE_URL_API}/api/v1/user/{call.from_user.id}", params=payload).json()
    response = requests.get(f"{BASE_URL_API}/api/v1/user/{call.from_user.id}").json()
    id_user_bonus = response.get("referer_id")
    if id_user_bonus != "0":
        payload_bonus = {"id": id_user_bonus, "new_balance": int(int(credit) / 2), "type_balance": 0}
        requests.post(f"{BASE_URL_API}/api/v1/user/{call.from_user.id}", json=payload_bonus).json()
        await bot.send_message(id_user_bonus, f"Вам начислен бонус {int(int(credit) / 2)} за пополнение реферала")
        await call.message.answer(f"Баланс пополнен на {credit} обработок")
    await call.message.edit_reply_markup(reply_markup=None)