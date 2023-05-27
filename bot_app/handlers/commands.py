from aiogram import Router, types
import requests
from pydantic import parse_obj_as
from adddict import elo_dict
from models import Model, Player, Stats
from aiogram.filters import Command

router = Router()

@router.message(Command('info'))
async def get_info(message: types.Message):
    player = requests.get(f"https://csgo-fastapi.herokuapp.com/player_details_by_nickname/{message.from_user.id}")
    if player.status_code == 404:
        await message.answer('Ви ще не зареєструвалися, щоб зареєструватися, використайте команду /start')
        return
    else:
        players = parse_obj_as(Player, player.json())
        steamlink = f'http://steamcommunity.com/profiles/{players.steam_id_64}'
        faceitlink = f'https://www.faceit.com/{players.settings.language}/players/{players.nickname}'
        await message.answer_photo(f"{players.avatar}", caption=f'Cтатистика гравця: <b>{players.nickname}</b> (\U0001F50D{players.search_count})\n\n\n'
                                                                            f'<b>Загальне</b>\n\n'
                                                                            f'<pre>Faceit рівень: {players.games.csgo.skill_level}/10\n'
                                                                            f'Elo points: {players.games.csgo.faceit_elo}/{elo_dict[players.games.csgo.skill_level]}\n'
                                                                            f'Регіон: {players.games.csgo.region}\n'
                                                                            f'Країна: {players.country}\n'
                                                                            f'Підписка: {players.memberships[0]}\n'
                                                                            f'Нік Steam(на момент реєстрації акаунту Faceit): {players.games.csgo.game_player_name}\n'
                                                                            f'ID гравця в CSGO</pre>: <code>{players.games.csgo.game_player_id}</code>\n'
                                                                            f'<pre>ID гравця на платформі Faceit</pre>: <code>{players.player_id}\n\n\n</code>'
                                                                            f'<b>Платформи</b>\n'
                                                                            f'<a href="{steamlink}">Steam</a>\n'
                                                                            f'<a href="{faceitlink}">Faceit</a>\n',
                                                                                        parse_mode='html')
        
@router.message(Command('friends'))
async def list_of_friends(message: types.Message):
    message_gif= await message.answer_video('https://media.tenor.com/EzkCAO4YhPcAAAAC/bullets-gun-and-bullets.gif', caption='Це може зайняти деякий час, очікуйте...')
    friend = requests.get(f'https://csgo-fastapi.herokuapp.com/player_friendsids_by_nickname/{message.from_user.id}')
    if friend.status_code == 404:
        await message_gif.delete()
        await message.answer('Ви ще не зареєструвалися, щоб зареєструватися, використайте команду /start')
        return
    else:
        await message_gif.delete()
        await message.answer('Ваш список друзів:\n'+'\n'.join(friend.json()), parse_mode='html')
        

@router.message(Command('stats'))
async def get_stats(message: types.Message):
    stats = requests.get(f'https://csgo-fastapi.herokuapp.com/player_extended_csgo_stats/{message.from_user.id}')
    if stats.status_code == 404:
        await message.answer('Ви ще не зареєструвалися, щоб зареєструватися, використайте команду /start')
        return
    else:
        stats_of_player = parse_obj_as(Stats, stats.json())
        await message.answer_photo("https://corporate.faceit.com/wp-content/uploads/icon-pheasant-preview-2-268x151.png", 
                             caption= f'<b>Вінрейт</b>: {stats_of_player.lifetime.winrate}%\n'
                                    f'<b>Результати нещодавніх матчів</b>: {",".join(stats_of_player.lifetime.recent_results)}\n'
                                    f'<b>Кількість хєдшотів за увесь час</b>: {stats_of_player.lifetime.total_headshots}\n'
                                    f'<b>Середній к/д</b>: {stats_of_player.lifetime.average_kd_ratio}\n'
                                    f'<b>Найдовший вінстрік</b>: {stats_of_player.lifetime.longest_win_streak}\n'
                                    f'<b>Кількість перемог</b>: {stats_of_player.lifetime.wins}\n'
                                    f'<b>Середній відсоток хєдшотів</b>: {stats_of_player.lifetime.average_headshots}%\n'
                                    f'<b>Кількість матчів</b>: {stats_of_player.lifetime.matches}\n', 
                                            parse_mode='html')

@router.message(Command('global_raiting'))
async def get_global_position(message: types.Message):
    position = requests.get(f'https://csgo-fastapi.herokuapp.com/global_position/{message.from_user.id}')
    if position.status_code == 404:
        await message.answer('Ви ще не зареєструвалися, щоб зареєструватися, використайте команду /start')
        return
    else:
        await message.answer(f'Ваша позиція: {position.json()[0]} в регіоні: {position.json()[1]}')
    
@router.message(Command('country_raiting'))
async def get_country_position(message: types.Message):
    position = requests.get(f'https://csgo-fastapi.herokuapp.com/country_position/{message.from_user.id}')
    if position.status_code == 404:
        await message.answer('Ви ще не зареєструвалися, щоб зареєструватися, використайте команду /start')
        return
    else:
        await message.answer(f'Ваша позиція: {position.json()[0]} в країні: {position.json()[1]}')

@router.message(Command('whole_time_stat'))
async def global_statistic(message: types.Message):
    global_stat = requests.get(f'https://csgo-fastapi.herokuapp.com/global_player_csgo_stats/{message.from_user.id}')
    if global_stat.status_code == 404:
        await message.answer('Ви ще не зареєструвалися, щоб зареєструватися, використайте команду /start')
        return
    elif global_stat.status_code == 451:
        await message.answer('Щоб використати даний метод потрібно мати відкритий Steam профіль')
        return
    else:
        stat = parse_obj_as(Model, global_stat.json())
        await message.answer_photo('https://i.blogs.es/a6ea54/counter-strike-2/1366_2000.jpeg', caption=f'<pre>Загальна кількість годин: {stat.timePlayed.displayValue}\n'
                                                                                                            f'Загальна кількість вбивств: {stat.kills.displayValue}\n'
                                                                                                            f'Загальна кількість смертей: {stat.deaths.displayValue}\n'
                                                                                                            f'K/D за увесь час гри: {stat.kd.displayValue}\n'
                                                                                                            f'Загальна кількість завданого урону: {stat.damage.displayValue}\n'
                                                                                                            f'Загальна кількість хедшотів: {stat.headshots.displayValue}\n'
                                                                                                            f'Загальний процент хедшотів: {stat.headshotPct.displayValue}'
                                                                                                            f'Загальна кількість пострілів: {stat.shotsFired.displayValue}\n'
                                                                                                            f'Загальна кількість влучень: {stat.shotsHit.displayValue}\n'
                                                                                                            f'Загальна точність: {stat.shotsAccuracy.displayValue}\n'
                                                                                                            f'Загальна кількість встановлених бомб: {stat.bombsPlanted.displayValue}\n'
                                                                                                            f'Загальна кількість знешкоджених бомб: {stat.bombsDefused.displayValue}\n'
                                                                                                            f'Загальна кількість зароблених грошей: {stat.moneyEarned.displayValue}\n'
                                                                                                            f'Загальна кількість врятованих заручників: {stat.hostagesRescued.displayValue}\n'
                                                                                                            f'Загальна кількість MVP: {stat.mvp.displayValue}\n'
                                                                                                            f'Загальна кількість матчів: {stat.matchesPlayed.displayValue}\n'
                                                                                                            f'Загальна кількість перемог: {stat.wins.displayValue}\n'
                                                                                                            f'Загальна кількість поразок: {stat.losses.displayValue}\n'
                                                                                                            f'Загальна кількість раундів: {stat.roundsPlayed.displayValue}\n'
                                                                                                            f'Загальна кількість виграшних раундів: {stat.roundsWon.displayValue}\n</pre>',
                                                                                                                    parse_mode='html')