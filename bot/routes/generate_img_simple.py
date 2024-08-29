import requests
from aiogram import Router, F, types

from config import PRICE_SIMPLE

simple_router = Router()

@simple_router.callback_query(F.data == "simple")
async def process_start_command(callback: types.CallbackQuery):
    r = requests.get(f"http://127.0.0.1:8000/api/v1/user/{callback.message.from_user.id}")
    re = r.json()
    balance = re.get("balance")
    if balance < PRICE_SIMPLE:
        await callback.message.answer("Недостаточно средств, пополните баланс!")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('В разработке')