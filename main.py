import telebot

# Твой токен
TOKEN = '8515886958:AAHWLWjmGtFj9BsUleOSsqZCaoN7NxdBHf4'
# Твой личный ID (цифрами). Если не знаешь, напиши /id любому боту-инфо
ADMIN_ID = 123456789  # ВСТАВЬ СЮДА СВОЙ ID

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "привет! я саппорт mister snich. напиши свой вопрос, и менеджер ответит тебе здесь.")

# Пересылка сообщения от клиента админу
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def forward_to_admin(message):
    client_username = f"@{message.from_user.username}" if message.from_user.username else "скрыт"
    log_msg = f"📩 сообщение от клиента!\nID: {message.chat.id}\nUser: {client_username}\n\nТекст: {message.text}"
    
    # Отправляем админу инфо и само сообщение для возможности Reply
    bot.send_message(ADMIN_ID, log_msg)
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, "--- используй 'ответить' на пересланное сообщение выше ---")

# Ответ админа клиенту через Reply
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message)
def reply_to_client(message):
    try:
        # Пытаемся достать ID из пересланного сообщения
        if message.reply_to_message.forward_from:
            target_id = message.reply_to_message.forward_from.id
        else:
            # Если пересылка скрыта, админу придется вручную копировать ID из лога выше
            # (Но обычно forward_message для админа работает)
            bot.send_message(ADMIN_ID, "не удалось найти ID клиента автоматически. проверь логи выше.")
            return

        bot.send_message(target_id, f"ответ менеджера:\n\n{message.text}")
        bot.send_message(ADMIN_ID, "✅ отправлено!")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"ошибка: {e}")

if __name__ == '__main__':
    print("Саппорт-бот mister snich запущен...")
    bot.infinity_polling()
