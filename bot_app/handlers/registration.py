from aiogram import Router, types
from keyboards.keyboards import cancel_keyboard, yes_or_no_keyboard
from fsm_class import Nickname
import requests
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text, Command

router = Router()

@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Бота запущено, введіть свій нік Faceit для реєстрації', reply_markup=cancel_keyboard())
    await state.set_state(Nickname.get_player)

@router.message(Nickname.get_player)
async def get(message: types.Message, state: FSMContext):
    players =  requests.post(f"https://csgo-fastapi.herokuapp.com/account/{message.text}", json={"faceit_nickname": f"{message.text}","telegram_id": f"{message.from_user.id}"})
    if players.status_code == 404:
        await message.answer('Гравця з таким ніком не існує, введіть нік ще раз', reply_markup=cancel_keyboard())
        return
    elif players.status_code == 302:
        await message.answer('Ви вже зареєстровані, якщо бажаєте перереєструватися, використовуйте команду /update')
        await state.clear()
    else:
        await message.answer('Акаунт успішно створено')
        await state.clear()

@router.message(Command('update'))
async def update_nick(message: types.Message, state: FSMContext):
    await message.answer('Введіть новий нік', reply_markup=cancel_keyboard())
    await state.set_state(Nickname.update_player)

@router.message(Nickname.update_player)
async def update(message: types.Message, state: FSMContext):
    new_nick = requests.put(f"https://csgo-fastapi.herokuapp.com/update_nickname/{message.from_user.id}/{message.text}", json={"faceit_nickname": f"{message.text}","telegram_id": f"{message.from_user.id}","search_count": 0})
    if new_nick.status_code == 404:
        await message.answer('Гравця з таким ніком не існує, або ви хочете оновити профіль, не зареєструвавшись, введіть нік ще раз, або використайте команду /start', 
                               reply_markup=cancel_keyboard())
        return
    elif new_nick.status_code == 302:
        await message.answer('Ви намагаєтесь змінити на теперішній нікнейм', reply_markup=cancel_keyboard())
        return
    else:
        await message.answer('Нікнейм успішно змінено')
        await state.clear()

@router.message(Command('delete'))
async def delete_account(message: types.Message):
    check = requests.get(f'https://csgo-fastapi.herokuapp.com/global_position/{message.from_user.id}')
    if check.status_code == 404:
        await message.answer('Ви ще не зареєструвалися, щоб зареєструватися, використайте команду /start')
        return
    else:
        await message.answer('Ви впевнені, що хочете видалити акаунт', reply_markup=yes_or_no_keyboard())

@router.callback_query(Text(startswith='ch_'))
async def deletion_choose(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == 'Yes':
        requests.delete(f"https://csgo-fastapi.herokuapp.com/delete_account/{callback.from_user.id}")
        await callback.message.answer('Акаунт було видалено')
        await callback.answer()
    if action == 'No':
        await callback.answer('Ви вийшли з процесу')

@router.callback_query(Text('cancel'), Nickname())
async def cancel_method(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Ви вийшли з процесу')