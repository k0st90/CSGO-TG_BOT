from aiogram import Router, types
import requests
from keyboards.keyboards import get_keyboard_for_map, weapon_keyboard, map_keyboard
from pydantic import parse_obj_as
from aiogram.filters import Text, Command
from models import Map, Model_Weapon, MapPlayerStats

router = Router()

@router.message(Command('map_stats'))
async def get_map_statistic(message: types.Message):
    await message.answer_photo('https://gumlet.assettype.com/afkgaming%2F2022-07%2F76d8de2d-8d7e-4141-b75c-6e8780b00b44%2FCover_Image___Most_Popular_CSGO_Maps_In_2022__Jan_June_.jpg?compress=true&dpr=1&w=1200', 
                         caption='Оберіть карту',
                         reply_markup=get_keyboard_for_map())
    
@router.callback_query(Text(startswith='de_'))
async def get_map_stats(callback: types.CallbackQuery):
    nmap = requests.get(f'https://csgo-fastapi.herokuapp.com/player_map_csgo_stats/{callback.data}/{callback.from_user.id}')
    if nmap.status_code == 404:
        await callback.answer()
        await callback.message.answer('Ви ще не зареєструвалися, щоб зареєструватися, використайте команду /start')
    else:
        nmap = parse_obj_as(Map, nmap.json())
        await callback.answer()
        await callback.message.answer_photo(nmap.img_regular, caption=f'Карта: <b>{callback.data}</b>\n\n\n'
                                                                    f'<b>Загальна статистика</b>:\n'
                                                                    f'<pre>Кількість перемог: {nmap.stats.Wins}\n'
                                                                    f'Кількість раундів: {nmap.stats.Rounds}\n'
                                                                    f'Кількість матчів: {nmap.stats.Matches}\n'
                                                                    f'Вінрейт: {nmap.stats.winrate}%\n'
                                                                    f'Кількість вбивств: {nmap.stats.Kills}\n'
                                                                    f'Кількість смертей: {nmap.stats.Deaths}\n'
                                                                    f'Кількість асистів: {nmap.stats.Assists}\n'
                                                                    f'Кількість хедшотів: {nmap.stats.total_headshots}\n'
                                                                    f'Кількість вбивств хедшотом: {nmap.stats.Headshots}\n'
                                                                    f'Кількість MVP: {nmap.stats.MVPs}\n'
                                                                    f'Кількість потрійних вбивств: {nmap.stats.triple_kills}\n'
                                                                    f'Кількість четверних вбивств: {nmap.stats.quadro_kills}\n'
                                                                    f'Кількість ейсів: {nmap.stats.penta_kills}</pre>\n\n'
                                                                    f'<b>Середні показники за матч</b>:\n\n'
                                                                    f'<pre>Середня кількість вбивств: {nmap.stats.average_kills}\n'
                                                                    f'Середня кількість смертей: {nmap.stats.average_deaths}\n'
                                                                    f'Середня кількість асистів: {nmap.stats.average_assists}\n'
                                                                    f'Середній процент хедшотів: {nmap.stats.average_headsots}%\n'
                                                                    f'Середній K/D: {nmap.stats.average_kd_ratio}\n'
                                                                    f'Середня кількість MVP: {nmap.stats.average_mvps}\n'
                                                                    f'Середня кількість вбивств за раунд: {nmap.stats.average_kr_ratio}\n'
                                                                    f'Середня кількість хедшотів за матч: {nmap.stats.headshots_per_match}\n'
                                                                    f'Середня кількість потрійних вбивств: {nmap.stats.average_triple_kills}\n'
                                                                    f'Середня кількість четверних вбивств: {nmap.stats.average_qadro_kills}\n'
                                                                    f'Середня кількість ейсів: {nmap.stats.average_penta_kills}</pre>', 
                                                                    parse_mode='html')

@router.message(Command('weapon_stats'))
async def choose_weapon(message: types.Message):
    await message.answer_animation('https://mir-s3-cdn-cf.behance.net/project_modules/disp/b42a8498338197.5ed9c5c78052d.gif', 
                         caption='Оберіть вид зброї',
                         reply_markup=weapon_keyboard())

@router.callback_query(Text(startswith='wp_'))
async def get_weapon(callback: types.CallbackQuery):
    weapon = callback.data.split("_")[1]
    weapon_stats = requests.get(f'https://csgo-fastapi.herokuapp.com/player_csgo_stats_weapon/{callback.from_user.id}/{weapon}')
    if weapon_stats.status_code == 404: 
        await callback.answer()
        await callback.message.answer('Ви ще не зареєструвалися, щоб зареєструватися, використайте команду /start')
    elif weapon_stats.status_code == 451:
        await callback.answer()
        await callback.message.answer('Щоб використати даний метод потрібно мати відкритий Steam профіль')
    else:
        nweapon=parse_obj_as(Model_Weapon, weapon_stats.json())
        await callback.message.answer_photo(nweapon.metadata.imageUrl, caption=f'<pre>Назва зброї: {nweapon.metadata.name}\n'
                                                                                f'Категорія: {nweapon.metadata.category}\n' 
                                                                                f'Кількість вбивств з цієї зброї: {nweapon.stats.kills.displayValue}\n'
                                                                                f'Кількість зроблених пострілів: {nweapon.stats.shotsFired.displayValue}\n'
                                                                                f'Кількість влучень: {nweapon.stats.shotsHit.displayValue}\n'
                                                                                f'Точність: {nweapon.stats.shotsAccuracy.displayValue}\n</pre>',
                                                                                            parse_mode='html')
        await callback.answer()

@router.message(Command('get_match_stat'))
async def last_20_games(message: types.Message):
    last20 = requests.get(f'https://csgo-fastapi.herokuapp.com/last_20_games_stats/{message.from_user.id}')
    if last20.status_code == 404:
        await message.answer_photo('Ви ще не зареєструвалися, щоб зареєструватися, використайте команду /start')
    else:
        await message.answer_animation('https://media.tenor.com/EdzTFfUhLrwAAAAC/clock-ticktock.gif' ,caption='Останні 20 матчів:', reply_markup=map_keyboard(last20.json()))

@router.callback_query(Text(startswith='mp_'))
async def get_match_stat(callback: types.CallbackQuery):
    match_id = callback.data.split("_")[1]
    stats = parse_obj_as(MapPlayerStats, requests.get(f'https://csgo-fastapi.herokuapp.com/match_statistic/{callback.from_user.id}/{match_id}').json())
    await callback.message.answer_photo(f'{stats.map_url}', 
                                            caption=f'<b>Результати</b>:\n'
                                                f'<pre>Карта: {stats.mapname}\n'
                                                f'Рахунок: {stats.score}</pre>\n\n'
                                                f'<b>Ваша статистика</b>:\n'
                                                f'<pre>Кількість вбивств: {stats.Kills}\n'
                                                f'Кількість смертей: {stats.Deaths}\n' 
                                                f'Кількість асистів: {stats.Assists}\n'
                                                f'K/D:{stats.kd_ratio}\n'
                                                f'Кількість MVP: {stats.MVPs}\n'
                                                f'Середня кількість вбивств за раунд: {stats.kr_ratio}\n'
                                                f'Кількість хедшотів: {stats.Headshots}\n'
                                                f'Відсоток хедшотів: {stats.headshots_percentage}%\n'
                                                f'Кількість потрійних вбивств: {stats.triple_kills}\n'
                                                f'Кількість четверних вбивств: {stats.Quadro_kills}\n'
                                                f'Кількість ейсів: {stats.penta_kills}\n</pre>',
                                                    parse_mode='html')
    await callback.answer()