import base64

import requests
from aiogram import Router, F, types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.routes.bot import user_state
from bot.routes.generate_img_clot import save_temp_file, sel
from config import PRICE_SIMPLE, BASE_URL_API

simple_router = Router()


@simple_router.callback_query(F.data == "simple")
async def process_start_command(callback: types.CallbackQuery):
    user_state[callback.from_user.id] = "simple"
    r = requests.get(f"{BASE_URL_API}/api/v1/user/{callback.from_user.id}")
    re = r.json()
    balance = re.get("balance")
    if int(balance) > int(PRICE_SIMPLE):
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer('📷 Пришлите фото для обработки.')
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        kb = InlineKeyboardBuilder()
        Button = InlineKeyboardButton(text='💵 Купить обработки', callback_data="pay_photo")
        kb.row(Button)
        await callback.message.answer('💰 Пополните баланс, чтобы начать обработку', reply_markup=kb.as_markup())


@simple_router.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_state:
        await message.answer("Произошла ошибка: состояние не определено.")
        return

    if user_state[user_id] == 'simple':
        await handle_n8ked_photo(message)
        await message.answer("⌛️ Обработка займет примерно 10-15 секунд, после чего бот пришлет вам результат…")
    elif user_state[user_id] == 'smart':
        await handle_clothoff_photo(message)
        await message.answer("⌛️ Обработка займет примерно 10 секунд, после чего бот пришлет вам результат…")

    # Очищаем состояние после обработки
    del user_state[user_id]


async def handle_n8ked_photo(message: types.Message):
    file_bytes = await save_temp_file(message.photo[-1].file_id)
    fb = file_bytes.read()
    base64_encoded = base64.b64encode(fb)
    header = {'Authorization': 'Bearer zsWQ5mwIh7BvrcoNDbrjU6eU2EvqicvDJdIz8LmZ88225bcf'}
    task_id = requests.post(f"https://use.n8ked.app/api/deepnude", headers=header, data={"image": base64_encoded})
    task_id = task_id.json()
    payload = {"img_id": task_id.get("task_id"), "user_id": f"{message.from_user.id}"}
    r = requests.post(f"{BASE_URL_API}/api/v1/niked", params=payload)


async def handle_clothoff_photo(message: types.Message):
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
        "webhook": f"{BASE_URL_API}/webhook"
    }
    headers = {
        "accept": "application/json",
        "x-api-key": "f5406795d2baab5be031ca82f3ebe1f50da871c3"
    }

    resp = requests.post(url, data=payload, files=files, headers=headers)
    del sel[f"{message.from_user.id}"]