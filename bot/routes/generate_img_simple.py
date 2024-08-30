import requests
from aiogram import Router, F, types

from bot.routes.generate_img_clot import save_temp_file
from config import PRICE_SIMPLE, BASE_URL_API

simple_router = Router()


@simple_router.callback_query(F.data == "simple")
async def process_start_command(callback: types.CallbackQuery):
    r = requests.get(f"{BASE_URL_API}/api/v1/user/{callback.from_user.id}")
    re = r.json()
    balance = re.get("balance")
    if int(balance) > int(PRICE_SIMPLE):
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer('Пришлите фото')
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer('Недостаточно средств')


@simple_router.message(F.photo)
async def handle_photo(message: types.Message):
    file_bytes = await save_temp_file(message.photo[-1].file_id)
    header = {'Authorization': 'Bearer zsWQ5mwIh7BvrcoNDbrjU6eU2EvqicvDJdIz8LmZ88225bcf', }
    task_id = requests.post(f"https://use.n8ked.app/api/deepnude", headers=header, data={"image": f"{file_bytes}"})
    task_id = task_id.json()
    payload = {"img_id": task_id.get("task_id")}
    r = requests.get(f"{BASE_URL_API}/api/v1/niked/{message.from_user.id}", json=payload)