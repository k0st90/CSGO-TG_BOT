from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_keyboard_for_map():
    buttons = [
        [InlineKeyboardButton(text='de_dust2', callback_data='de_dust2')],
        [InlineKeyboardButton(text='de_nuke', callback_data='de_nuke')],
        [InlineKeyboardButton(text='de_vertigo', callback_data='de_vertigo')],
        [InlineKeyboardButton(text='de_ancient', callback_data='de_ancient')],
        [InlineKeyboardButton(text='de_anubis', callback_data='de_anubis')],
        [InlineKeyboardButton(text='de_mirage', callback_data='de_mirage')],
        [InlineKeyboardButton(text='de_cache', callback_data='de_cache')],
        [InlineKeyboardButton(text='de_train', callback_data='de_train')],
        [InlineKeyboardButton(text='de_inferno', callback_data='de_inferno')],
        [InlineKeyboardButton(text='de_overpass', callback_data='de_overpass')]
    ]

    keyboard_map = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard_map

def cancel_keyboard():
    button = [
        [InlineKeyboardButton(text='cancel', callback_data='cancel')]
    ]
    keyboard_map = InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard_map

def yes_or_no_keyboard():
    buttons =[
        [InlineKeyboardButton(text='Так', callback_data='ch_Yes')],
        [InlineKeyboardButton(text='Ні', callback_data='ch_No')]
    ]
    keyboard_map = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard_map

def weapon_keyboard():
    buttons = [
        [InlineKeyboardButton(text='AK-47', callback_data='wp_AK')],
        [InlineKeyboardButton(text='AUG', callback_data='wp_AUG')],
        [InlineKeyboardButton(text='AWP', callback_data='wp_AWP')],
        [InlineKeyboardButton(text='bizon', callback_data='wp_bizon')],
        [InlineKeyboardButton(text='deagle', callback_data='wp_deagle')],
        [InlineKeyboardButton(text='dualberettas', callback_data='wp_dualberettas')],
        [InlineKeyboardButton(text='famas', callback_data='wp_famas')],
        [InlineKeyboardButton(text='fiveseven', callback_data='wp_fiveseven')],
        [InlineKeyboardButton(text='G3SG1', callback_data='wp_G3SG1')],
        [InlineKeyboardButton(text='galil', callback_data='wp_galil')],
        [InlineKeyboardButton(text='glock', callback_data='wp_glock')],
        [InlineKeyboardButton(text='P2000', callback_data='wp_P2000')],
        [InlineKeyboardButton(text='M249', callback_data='wp_M249')],
        [InlineKeyboardButton(text='m4a4', callback_data='wp_m4a4')],
        [InlineKeyboardButton(text='MAC-10', callback_data='wp_MAC-10')],
        [InlineKeyboardButton(text='MAG-7', callback_data='wp_MAG-7')],
        [InlineKeyboardButton(text='MP7', callback_data='wp_MP7')],
        [InlineKeyboardButton(text='MP9', callback_data='wp_MP9')],
        [InlineKeyboardButton(text='Negev', callback_data='wp_Negev')],
        [InlineKeyboardButton(text='Nova', callback_data='wp_Nova')],
        [InlineKeyboardButton(text='P250', callback_data='wp_P250')],
        [InlineKeyboardButton(text='P90', callback_data='wp_P90')],
        [InlineKeyboardButton(text='Sawedoff', callback_data='wp_Sawedoff')],
        [InlineKeyboardButton(text='Scar-20', callback_data='wp_Scar-20')],
        [InlineKeyboardButton(text='SG553', callback_data='wp_SG553')],
        [InlineKeyboardButton(text='SSG08', callback_data='wp_SSG08')],
        [InlineKeyboardButton(text='Zeusx27', callback_data='wp_Zeusx27')],
        [InlineKeyboardButton(text='Tec-9', callback_data='wp_Tec-9')],
        [InlineKeyboardButton(text='ump-45', callback_data='wp_ump-45')],
        [InlineKeyboardButton(text='xm1014', callback_data='wp_xm1014')]
    ]
    keyboard_map = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard_map

def map_keyboard(match_time):
    builder = InlineKeyboardBuilder()
    for keys, values in match_time.items():
        builder.button(text=f'{keys}', callback_data=f'mp_{values}')
    builder.adjust(2)
    return builder.as_markup()