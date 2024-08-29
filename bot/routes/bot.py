from aiogram import Router, F, Bot, types

from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests
start_router = Router()


def create_keyboard(buttons, columns=2):
    keyboard_buttons = []
    for i in range(0, len(buttons), columns):
        row = [types.KeyboardButton(text=button) for button in buttons[i:i + columns]]
        keyboard_buttons.append(row)
    return types.ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True)

@start_router.message(Command('start'))
async def process_start_command(message: types.Message):
    referer_id = str(message.text[7:]) if len(message.text) > 7 else "0"
    payload = {"id": f"{message.from_user.id}", "referer_id": referer_id}
    requests.post("http://127.0.0.1:8000/api/v1/user", json=payload)
    buttons = ["Обработка фото", "Пополнить баланс", "Реферальная программа", "Профиль"]
    keyboard = create_keyboard(buttons, columns=1)
    await message.answer('Привет!', reply_markup=keyboard)


@start_router.message(F.text == "Обработка фото")
async def processing_image(message: types.Message):
    kb = InlineKeyboardBuilder()
    Button = InlineKeyboardButton(text='Умная', callback_data="smart")
    Button2 = InlineKeyboardButton(text='Простая', callback_data="simple")
    kb.row(Button)
    kb.row(Button2)
    await message.answer('Выберите режим:', reply_markup=kb.as_markup())

@start_router.message(F.text == "Профиль")
async def profile_info(message: types.Message):
    r = requests.get(f"http://127.0.0.1:8000/api/v1/user/{message.from_user.id}")
    re = r.json()
    id_user = re.get("id")
    balance = re.get("balance")
    await message.answer(f"ID: {id_user}\nБаланс: {balance}")


@start_router.message(F.text == "Реферальная программа")
async def referals_program(message: types.Message):
    await message.answer(f"Информация о реф программе")


@start_router.message(F.text == "Пополнить баланс")
async def top_balance(message: types.Message):
    button1 = InlineKeyboardButton(text="100", callback_data="sum_100")
    button2 = InlineKeyboardButton(text="200", callback_data="sum_200")
    button3 = InlineKeyboardButton(text="300", callback_data="sum_300")
    button4 = InlineKeyboardButton(text="400", callback_data="sum_400")
    button5 = InlineKeyboardButton(text="500", callback_data="sum_500")
    button6 = InlineKeyboardButton(text="600", callback_data="sum_600")

    keyboard = InlineKeyboardBuilder()

    keyboard.row(button1, button2, button3, button4, button5, button6, width=2)
    await message.answer("Выберите сумму:", reply_markup=keyboard.as_markup())