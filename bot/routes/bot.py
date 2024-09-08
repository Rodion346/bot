from aiogram import Router, F, Bot, types

from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests

from config import BASE_URL_API

start_router = Router()

user_state = {}

prices = [
    ("📸 3 фото", 200),
    ("📸 5 фото", 300),
    ("📸 10 фото", 450),
    ("📸 25 фото", 900),
    ("📸 50 фото", 1400),
]

def create_service_keyboard(services_with_prices):
    keyboard = InlineKeyboardBuilder()
    for service, price in services_with_prices:
        service_button = InlineKeyboardButton(text=service, callback_data=f"sum_{price}_{service}")
        price_button = InlineKeyboardButton(text=f"{price} ₽", callback_data=f"sum_{price}_{service}")
        keyboard.row(service_button, price_button)

    return keyboard


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
    requests.post(f"{BASE_URL_API}/api/v1/user", json=payload)
    buttons = ["🔞 Обработка фото", "💵 Купить обработки", "🤝 Реферальная программа", "👤 Профиль"]
    keyboard = create_keyboard(buttons, columns=1)
    start_txt = ("❣️Привет, я - бот, который поможет тебе раздеть любую девушку с помощью ИИ. Ты сам решаешь какой будет результат - "
                 "обработать быстро или настроить все параметры по желанию. Нажми 'Обработать фото', чтобы начать!")
    await message.answer(start_txt, reply_markup=keyboard)



@start_router.message(F.text == "🔞 Обработка фото")
async def processing_image(message: types.Message):
    kb = InlineKeyboardBuilder()
    Button = InlineKeyboardButton(text='👨‍💻 Умная', callback_data="smart")
    Button2 = InlineKeyboardButton(text='⚡️ Быстрая', callback_data="simple")
    kb.row(Button)
    kb.row(Button2)
    obr_txt = ("👨‍💻 Умная обработка позволяет выбрать параметры тела (размер груди, возраст и тд.), одежду и различные "
               "позы.\n⚡️ Быстрая(будем называть это так) обработка - раздевание без дополнительных настроек. С отличным качеством и скоростью.")
    await message.answer(obr_txt, reply_markup=kb.as_markup())

@start_router.message(F.text == "👤 Профиль")
async def profile_info(message: types.Message):
    response = requests.get(f"{BASE_URL_API}/api/v1/user/{message.from_user.id}").json()
    id_user = response.get("id")
    processing_balance = response.get("processing_balance")
    referal_balance = response.get("referal_balance")
    await message.answer(f"ID: {id_user}\nОбработки: {processing_balance}\nБаланс: {referal_balance}")


@start_router.message(F.text == "🤝 Реферальная программа")
async def referals_program(message: types.Message):
    buttons = ["⬅️ Назад", "🔗 Получить реферальную ссылку", "💰 Вывод средств"]
    keyboard = create_keyboard(buttons, columns=1)
    response = requests.get(f"{BASE_URL_API}/api/v1/user/{message.from_user.id}").json()
    referal_balance = response.get("referal_balance")
    await message.answer(f"Ваш реферальный баланс: {referal_balance}\nЕсли вы еще не получили реферальную ссылку - нажмите на кнопку\n🔗 Получить реферальную ссылку", reply_markup=keyboard)

@start_router.message(F.text == "⬅️ Назад")
async def back_menu(message: types.Message):
    buttons = ["🔞 Обработка фото", "💵 Купить обработки", "🤝 Реферальная программа", "👤 Профиль"]
    keyboard = create_keyboard(buttons, columns=1)
    await message.answer(' ', reply_markup=keyboard)

@start_router.message(F.text == "🔗 Получить реферальную ссылку")
async def get_invite_link(message: types.Message):
    await message.answer("Ваша реферальная ссылка готова. Вы можете делиться ей с друзьями, публиковать в различных соцсетях (Tiktok, Reels, Shorts) или форумах. Вы будете получать 30% от сумму пополнений ваших рефералов на свой счет. Всю эту суммы вы можете получить выплатой в USDT Trc20 на свой кошелек (минимальный размер вывода 10USDT).")
    await message.answer(f"https://t.me/SmartNudifyAI_bot?start={message.from_user.id}")


@start_router.message(F.text == "💵 Купить обработки")
async def top_balance(message: types.Message):
    kb = create_service_keyboard(prices)
    await message.answer("Выберите количество обработок:", reply_markup=kb.as_markup())
    await message.edit_reply_markup(reply_markup=None)

@start_router.callback_query(F.data == "pay_photo")
async def top_balance(call: CallbackQuery):
    kb = create_service_keyboard(prices)
    await call.message.answer("Выберите количество обработок:", reply_markup=kb.as_markup())
    await call.message.edit_reply_markup(reply_markup=None)