from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command('help'))
async def send_help(message: types.Message):
    await message.answer('Команди бота:\n'
                                            '/start - запуск бота\n'
                                            '/help - подивитись усі команди\n'
                                            '/update - оновити нікнейм\n'
                                            '/delete - видалити свій нік з бази даних\n'
                                            '/info - отримати інформацію про гравця\n'
                                            '/friends - отримати список друзів\n'
                                            '/stats - отримати детальну статистику\n'
                                            '/global_raiting - отримати місце в глобальному рейтингу\n'
                                            '/country_raiting - отримати місце в рейтингу по країні\n'
                                            '/map_stats - отримати статистику по карті\n'
                                            '/weapon_stats - отримати статистику по виду зброї\n'
                                            '/whole_time_stat - отримати статистику за увесь час гри\n'
                                            '/get_match_stat - отримати статистику за конкретний матч')