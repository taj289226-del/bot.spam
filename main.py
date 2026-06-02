import telebot
import config
import time
bot = telebot.TeleBot(config.telebot)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """
Hi there, I am bot.antispam.
""")



@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(commands=['ban_2'])
def temp_ban(message):
    # Проверяем, что команда отправлена в ответ на сообщение человека
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        
        # Вычисляем время разблокировки: текущее время + 10 минут (600 секунд)
        ban_duration = 20  
        unban_time = int(time.time()) + ban_duration
        
        try:
            # Баним пользователя на заданное время
            bot.ban_chat_member(chat_id=chat_id, user_id=user_id, until_date=unban_time)
            bot.reply_to(message, f"Пользователь забанен на 10 минут.")
            
        except Exception as e:
            bot.reply_to(message, f"Ошибка при блокировке: {e}")
    else:
        bot.reply_to(message, "Эта команда должна быть ответом на сообщение нарушителя.")

bot.infinity_polling()


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.infinity_polling(none_stop=True)