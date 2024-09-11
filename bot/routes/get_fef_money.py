import requests
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from config import BASE_URL_API

router_get_money = Router()

class OrderTask(StatesGroup):
    waiting_amount = State()
    waiting_address = State()

@router_get_money.message(F.text == "💰 Вывод средств")
async def process_callback_button(message: Message, state: FSMContext):
    response = requests.get(f"{BASE_URL_API}/api/v1/user/{message.from_user.id}").json()
    if int(response.get("referal_balance")) < 10:
        await message.answer("Недостаточно монет для вывода")
        await state.clear()
    else:
        await message.answer("Введите сумму")
        await state.set_state(OrderTask.waiting_amount)

@router_get_money.message(OrderTask.waiting_amount)
async def process_amount(message: Message, state: FSMContext):
    response = requests.get(f"{BASE_URL_API}/api/v1/user/{message.from_user.id}").json()
    await message.answer("Введите адрес кошелька")
    await state.update_data(waiting_amount=message.text)
    if int(message.text) <= int(response.get("referal_balance")):
        await state.update_data(waiting_amount=message.text)
        await state.set_state(OrderTask.waiting_address)
    else:
        await message.answer("Недостаточно средств для вывода")
        await state.clear()

@router_get_money.message(OrderTask.waiting_address)
async def process_bank(message: Message, state: FSMContext):
    await state.update_data(waiting_address=message.text)
    user_data = await state.get_data()
    payload = {
        "id": f"{message.from_user.id}",
        "amount": int(user_data['waiting_amount']),
        "to_address": user_data['waiting_address'],
    }
    response = requests.post(f"{BASE_URL_API}/api/v1/application", json=payload)
    if response.status_code == 200:
        await message.answer("Заявка создана!")
        response = requests.get(f"{BASE_URL_API}/api/v1/user/{message.from_user.id}").json()
        payload = {"id": f"{message.from_user.id}", "new_balance": -int(response.get("referal_balance")), "type_balance": 0}
        requests.post(f"{BASE_URL_API}/api/v1/user/{message.from_user.id}", params=payload).json()
    else:
        await message.answer("Произошла ошибка при отправке запроса.")
    await state.clear()