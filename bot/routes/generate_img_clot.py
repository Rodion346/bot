import requests
from aiogram import Router, F, Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import PRICE_CLOT

bot = Bot(token='6830235739:AAG0Bo5lnabU4hDVWlhPQmLtiMVePI2xRGg')
router = Router()

button_options = {
    'age': ['Возраст - 18', 'Возраст - 20', 'Возраст - 30', 'Возраст - 40', 'Возраст - 50'],
    'breastSize': ['Размер груди - маленькая', 'Размер груди - нормальная', 'Размер груди - большая'],
    'bodyType': ['Телосложение - маленькая', 'Телосложение - нормальная', 'Телосложение - большая'],
    'buttSize': ['Размер попы - маленькая', 'Размер попы - нормальная', 'Размер попы - большая'],
    'cloth': ['Одежда - без одежды', 'Одежда - бикини', 'Одежда - нижнее белье', 'Одежда - спортивная одежда',
              'Одежда - БДСМ', 'Одежда - латекс', 'Одежда - учительница', 'Одежда - школьница'],
    'pose': ['Поза - без позы', 'Поза - Missionary POV', 'Поза - Anal Fuck', 'Поза - Legs up presenting',
             'Поза - Spreading legs', 'Поза - Tit Fuck', 'Поза - TGirl', 'Поза - Tits On Glass']
}

body = {"маленькая": "small", "нормальная":"normal", "большая": "big"}
cloth = {"без одежды": "naked", "бикини": "bikini", "нижнее белье": "lingerie",
         "спортивная одежда": "sport wear", "БДСМ": "bdsm", "латекс": "latex", "учительница": "teacher", "школьница": "schoolgirl"}

selected_options = {}
sel = {}


async def save_temp_file(file_id: str):
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_bytes = await bot.download_file(file_path)
    return file_bytes

# Создаем инлайн клавиатуру
async def create_keyboard_clot():
    markup = InlineKeyboardBuilder()
    for button_name, options in button_options.items():
        current_text = options[0]
        button = InlineKeyboardButton(text=current_text, callback_data=f'option_{button_name}')
        markup.row(button)
    markup.row(InlineKeyboardButton(text="Отправить", callback_data='send'))
    return markup


# Обработчик нажатия на кнопку
@router.callback_query(lambda c: 'option_' in c.data)
async def process_callback_button(call: CallbackQuery):
    button_name = call.data.split('_')[1]
    options = button_options[button_name]

    for row in call.message.reply_markup.inline_keyboard:
        for button in row:
            if button.text in options:
                current_index = options.index(button.text)
                new_index = (current_index + 1) % len(options)

                if options[new_index] != button.text:
                    button.text = options[new_index]
                    await call.message.edit_reply_markup(reply_markup=call.message.reply_markup)
                    break

    await call.answer()


# Обработчик нажатия на кнопку "Отправить"
@router.callback_query(lambda c: c.data == 'send')
async def process_send(call: CallbackQuery):
    for button_name, options in button_options.items():
        for row in call.message.reply_markup.inline_keyboard:
            for button in row:
                if button.text in options:
                    ind = button.text.index("-") + len("-")
                    tx = button.text[ind:].strip()
                    if button_name == "breastSize" or button_name == "bodyType" or button_name == "buttSize":
                        selected_options[button_name] = body.get(tx)
                    elif button_name == "cloth":
                        selected_options[button_name] = cloth.get(tx)
                    else:
                        if tx == "без позы":
                            selected_options[button_name] = None
                        else:
                            selected_options[button_name] = tx

    await call.message.edit_reply_markup(reply_markup=None)
    sel[call.message.from_user.id] = selected_option
    print(sel)
    await call.message.answer(f"Вы выбрали: {selected_options}")

    await call.message.answer("Отправьте фото")




@router.message(F.photo)
async def handle_photo(message: types.Message):
    file_bytes = await save_temp_file(message.photo[-1].file_id)
    url = "https://public-api.clothoff.io/undress"

    files = {"image": (f"{message.from_user.id}", file_bytes)}
    payload = {
        "age": sel.get(f"{message.from_user.id}").get("age"),
        "breast_size": sel.get(f"{message.from_user.id}").get("breast_size"),
        "body_type": sel.get(f"{message.from_user.id}").get("body_type"),
        "butt_size": sel.get(f"{message.from_user.id}").get("butt_size"),
        "cloth": sel.get(f"{message.from_user.id}").get("cloth"),
        "pose": sel.get(f"{message.from_user.id}").get("pose"),
        "id_gen": f"{message.from_user.id}",
        "webhook": "https://rodion346-api-ai-bot-1eac.twc1.net/webhook"
    }
    headers = {
        "accept": "application/json",
        "x-api-key": "f5406795d2baab5be031ca82f3ebe1f50da871c3"
    }

    resp = requests.post(url, data=payload, files=files, headers=headers)
    print(resp.text)

@router.callback_query(F.data == "smart")
async def process_start_command(callback: types.CallbackQuery):
    kb = await create_keyboard_clot()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Задайте все параметры обработки:', reply_markup=kb.as_markup())