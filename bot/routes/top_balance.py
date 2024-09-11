import requests
from typing import Optional, List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import HTTPException
from pydantic import BaseModel
from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton

from bot.routes.generate_img_clot import bot
from config import BASE_URL_API

router_balance = Router()



BASE_URL = "https://api.cashinout.io"

AUTHORIZATION_TOKEN = "f843547c258654dc7f22d668a19f4da5"

# Модель для создания одноразового счёта
class OneTimeInvoiceRequest(BaseModel):
    amount: str
    currency: int = 0
    currencies: List[int]
    durationSeconds: Optional[int] = 86400
    callbackUrl: Optional[str] = None
    redirectUrl: Optional[str] = None
    externalText: Optional[str] = None




async def create_one_time_invoice(invoice: OneTimeInvoiceRequest):
    headers = {
        "Authorization": AUTHORIZATION_TOKEN,
    }

    body = invoice.dict()

    response = requests.post(f"{BASE_URL}/merchant/createOneTimeInvoice", json=body, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)



"""@router_balance.callback_query(lambda p: 'sum_' in p.data)
async def process_callback_button(call: CallbackQuery):
    cal_data = call.data
    credit = cal_data.split("_")[2].split(" ")[1].strip()
    payload = {"id": f"{call.from_user.id}", "new_balance": int(credit), "type_balance": 1}
    requests.post(f"{BASE_URL_API}/api/v1/user/{call.from_user.id}", params=payload).json()
    response = requests.get(f"{BASE_URL_API}/api/v1/user/{call.from_user.id}").json()
    id_user_bonus = response.get("referer_id")
    if id_user_bonus != "0":
        payload_bonus = {"id": id_user_bonus, "new_balance": int(int(credit) / 2), "type_balance": 0}
        requests.post(f"{BASE_URL_API}/api/v1/user/{id_user_bonus}", params=payload_bonus).json()
        await bot.send_message(id_user_bonus, f"Вам начислен бонус {int(int(credit) / 2)} за пополнение реферала")
        await call.message.answer(f"Баланс пополнен на {credit} обработок")
    await call.message.edit_reply_markup(reply_markup=None)"""


@router_balance.callback_query(lambda p: 'sum_' in p.data)
async def process_callback_button(call: CallbackQuery):
    cal_data = call.data
    credit = cal_data.split("_")[2].split(" ")[1].strip()
    amount = cal_data.split("_")[1]
    data = {
    "amount": f"{amount}",
    "currency": 0,
    "currencies": [0],
    "durationSeconds": 86400,
    "callbackUrl": f"{BASE_URL_API}/merchant/callback",
    "redirectUrl": "",
    "externalText": f"{call.from_user.id}_{credit}"
    }
    inv = OneTimeInvoiceRequest(**data)
    link_pay = await create_one_time_invoice(inv)
    kb = InlineKeyboardBuilder()
    Button = InlineKeyboardButton(text='Оплатить', url=f"{BASE_URL}/{link_pay}")
    kb.row(Button)
    await call.message.edit_reply_markup(reply_markup=kb.as_markup())