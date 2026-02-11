import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import BotCommand, WebAppInfo

# Твой токен
API_TOKEN = '8515886958:AAHWLWjmGtFj9BsUleOSsqZCaoN7NxdBHf4'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def init_db():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                     (id INTEGER PRIMARY KEY, user TEXT, item TEXT, size TEXT)''')
    conn.commit()
    conn.close()

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='главное меню'),
        BotCommand(command='/catalog', description='каталог'),
    ]
    await bot.set_my_commands(main_menu_commands)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    # Твоя рабочая ссылка с GitHub
    builder.button(
        text="открыть магазин", 
        web_app=WebAppInfo(url="https://olisher2015pro100.github.io/my-shop-app/") 
    )
    builder.button(text="текстовый каталог", callback_data="open_catalog")
    builder.adjust(1)
    await message.answer(
        f"привет, {message.from_user.first_name}.\nвыбирай способ заказа:", 
        reply_markup=builder.as_markup()
    )

# Исправленная функция с правильными отступами
@dp.message(F.web_app_data)
async def web_app_receive(message: types.Message):
    item = message.web_app_data.data
    await message.answer(f"отличный выбор! ты выбрал: {item}.\nтеперь выбери размер в каталоге.")

@dp.message(Command("catalog"))
@dp.callback_query(F.data == "open_catalog")
async def show_catalog(event: types.Message | types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="zip-hoode", callback_data="cat_zip-hoode")
    builder.button(text="t-shirt", callback_data="cat_t-shirt")
    builder.button(text="long sleeve", callback_data="cat_long sleeve")
    builder.adjust(1)
    text = "каталог:"
    if isinstance(event, types.Message):
        await event.answer(text, reply_markup=builder.as_markup())
    else:
        await event.message.edit_text(text, reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("cat_"))
async def choose_size(callback: types.CallbackQuery):
    item_name = callback.data.split("_")[1]
    builder = InlineKeyboardBuilder()
    if item_name == "zip-hoode":
        builder.button(text="baby-size", callback_data=f"order_{item_name}_baby-size")
        builder.button(text="big-size", callback_data=f"order_{item_name}_big-size")
    else:
        builder.button(text="s-m", callback_data=f"order_{item_name}_s-m")
        builder.button(text="m-l", callback_data=f"order_{item_name}_m-l")
        builder.button(text="l-xl", callback_data=f"order_{item_name}_l-xl")
    builder.button(text="назад", callback_data="open_catalog")
    builder.adjust(1)
    await callback.message.edit_text(f"выберите размер для {item_name}:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("order_"))
async def start_payment(callback: types.CallbackQuery):
    _, item, size = callback.data.split("_")
    builder = InlineKeyboardBuilder()
    builder.button(text="оплатить заказ", callback_data=f"pay_confirm_{item}_{size}")
    builder.button(text="отмена", callback_data="open_catalog")
    builder.adjust(1)
    await callback.message.edit_text(
        f"заказ: {item} ({size})\n\nнажмите кнопку для получения реквизитов.",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("pay_confirm_"))
async def show_payment_info(callback: types.CallbackQuery):
    data = callback.data.split("_")
    item, size = data[2], data[3]
    user = callback.from_user.username or callback.from_user.first_name
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user, item, size) VALUES (?, ?, ?)", (user, item, size))
    conn.commit()
    conn.close()
    await callback.message.answer(
        f"счет для {user}:\nтовар: {item} ({size})\n\nреквизиты сбп: +79990000000\nотправьте чек менеджеру."
    )
    await callback.answer()

async def main():
    init_db()
    await set_main_menu(bot)
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())