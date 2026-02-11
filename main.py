import logging
import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# Вставь свой токен от BotFather
API_TOKEN = 'ТВОЙ_ТОКЕН_БОТА'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработка команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Кнопка для открытия твоего магазина (замени URL на свой)
    web_app_url = "https://ТВОЙ_НИК.github.io/ТВОЙ_РЕПОЗИТОРИЙ/"
    
    kb = [
        [types.KeyboardButton(text="открыть shop", web_app=types.WebAppInfo(url=web_app_url))]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        f"привет, {message.from_user.first_name}!\n\nнажми на кнопку ниже, чтобы перейти в магазин.",
        reply_markup=keyboard
    )

# Прием данных из Web App после нажатия "Я оплатил"
@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    # Распаковываем JSON данные из приложения
    data = json.loads(message.web_app_data.data)
    
    # Формируем сообщение для админа (тебя)
    admin_text = (
        "🔥 НОВЫЙ ЗАКАЗ!\n\n"
        f"📦 Товар: {data['item']}\n"
        f"💰 Сумма: {data['total']}\n\n"
        f"👤 Клиент: {data['customer']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"📍 Адрес: {data['address']}\n"
        f"📮 Индекс: {data['zip']}\n"
    )
    
    # Отправляем инфу админу (в данном случае тебе же)
    await message.answer("спасибо за заказ! ❤️\n\nмы получили ваши данные. пожалуйста, пришлите скриншот чека об оплате в этот чат для подтверждения.")
    
    # ТУТ МОЖНО ВСТАВИТЬ ID ТВОЕГО АККАУНТА, ЧТОБЫ ЗАКАЗЫ ПРИХОДИЛИ ТЕБЕ В ЛИЧКУ
    await bot.send_message(chat_id=message.from_user.id, text=admin_text)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())