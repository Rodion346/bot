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
    waiting_bank = State()

@router_get_money.message(F.text == "💰 Вывод средств")
async def process_callback_button(message: Message, state: FSMContext):
    await message.answer("Введите сумму")
    await state.set_state(OrderTask.waiting_amount)

@router_get_money.message(OrderTask.waiting_amount)
async def process_amount(message: Message, state: FSMContext):
    await message.answer("Введите номер карты/телефон")
    await state.update_data(waiting_amount=message.text)
    await state.set_state(OrderTask.waiting_address)

@router_get_money.message(OrderTask.waiting_address)
async def process_address(message: Message, state: FSMContext):
    await message.answer("Введите банк получения платежа")
    await state.update_data(waiting_address=message.text)
    await state.set_state(OrderTask.waiting_bank)

@router_get_money.message(OrderTask.waiting_bank)
async def process_bank(message: Message, state: FSMContext):
    await state.update_data(waiting_bank=message.text)
    user_data = await state.get_data()
    payload = {
        "id": f"{message.from_user.id}",
        "amount": int(user_data['waiting_amount']),
        "to_address": user_data['waiting_address'],
        "bank": user_data['waiting_bank']
    }
    response = requests.post(f"{BASE_URL_API}/api/v1/application", json=payload)
    if response.status_code == 200:
        await message.answer("Заявка создана!")
    else:
        await message.answer("Произошла ошибка при отправке запроса.")
    await state.clear()