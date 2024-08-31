from aiogram import Router, F, Bot, types

from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests

from config import BASE_URL_API

start_router = Router()

user_state = {}

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
    buttons = ["🔞 Обработка фото", "💵 Купить обработки", "🤝 Реферальная программа", "👤 Профиль", "Реф ссылка"]
    keyboard = create_keyboard(buttons, columns=1)
    start_txt = ("❣️Привет, я - бот, который поможет тебе раздеть любую девушку с помощью ИИ. Ты сам решаешь какой будет результат - "
                 "обработать быстро или настроить все параметры по желанию. Нажми 'Обработать фото', чтобы начать!")
    await message.answer(start_txt, reply_markup=keyboard)



@start_router.message(F.text == "🔞 Обработка фото")
async def processing_image(message: types.Message):
    kb = InlineKeyboardBuilder()
    Button = InlineKeyboardButton(text='Умная', callback_data="smart")
    Button2 = InlineKeyboardButton(text='Простая', callback_data="simple")
    kb.row(Button)
    kb.row(Button2)
    obr_txt = ("👨‍💻 Умная обработка позволяет выбрать параметры тела (размер груди, возраст и тд.), одежду и различные "
               "позы.\n⚡️ Быстрая(будем называть это так) обработка - раздевание без дополнительных настроек. С отличным качеством и скоростью.")
    await message.answer('Выберите режим:', reply_markup=kb.as_markup())

@start_router.message(F.text == "👤 Профиль")
async def profile_info(message: types.Message):
    r = requests.get(f"{BASE_URL_API}/api/v1/user/{message.from_user.id}")
    re = r.json()
    id_user = re.get("id")
    balance = re.get("balance")
    await message.answer(f"ID: {id_user}\nБаланс: {balance}")


@start_router.message(F.text == "🤝 Реферальная программа")
async def referals_program(message: types.Message):
    buttons = ["⬅️ Назад", "🔗 Реф ссылка"]
    keyboard = create_keyboard(buttons, columns=1)
    await message.answer(f"Информация о реф программе", reply_markup=keyboard)

@start_router.message(F.text == "⬅️ Назад")
async def referals_program(message: types.Message):
    buttons = ["🔞 Обработка фото", "💵 Купить обработки", "🤝 Реферальная программа", "👤 Профиль", "🔗 Реф ссылка"]
    keyboard = create_keyboard(buttons, columns=1)
    await message.answer('Меню:', reply_markup=keyboard)

@start_router.message(F.text == "🔗 Реф ссылка")
async def get_invite_link(message: types.Message):
    await message.answer(f"https://t.me/SmartNudifyAI_bot?start={message.from_user.id}")


@start_router.message(F.text == "💵 Купить обработки" or F.data == "pay_photo")
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