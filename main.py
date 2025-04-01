import telebot
import dbwork
import parsework

TOKEN = 'My Token'
bot = telebot.TeleBot(TOKEN)
msg = telebot.types.Message

markup = telebot.types.InlineKeyboardMarkup()
python = telebot.types.InlineKeyboardButton(text="Python", callback_data="python")
markup.add(python)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! "
                                      "Я могу помочь тебе в изучении языка программирования!"
                                      "\n\nПросто выбери, какой язык изучать:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # python topics
    global msg
    python_topics = dbwork.get_topic("Python")
    python_topics_0 = []
    python_topics_true = []

    for tuptop in python_topics:
        python_topics_0.append(tuptop[0])

    for topic in python_topics_0:
        if len(topic) >= 33:
            topic = f"{topic[:33]}"
        else:
            topic = f"{topic}"
        python_topics_true.append(topic)

    # python chapters
    python_chapters = dbwork.get_chapter("PythonChapters")
    python_chapters_0 = []
    python_chapters_true = []

    for tuptop in python_chapters:
        python_chapters_0.append(tuptop[0])

    for chap in python_chapters_0:
        if len(chap) >= 33:
            chap = f"{chap[:33]}"
        else:
            chap = f"{chap}"
        python_chapters_true.append(chap)

    # Обработка кнопки "Удалить все"
    if call.data.startswith("delete_all_"):
        # Получаем ID темы из callback_data
        topic_id = call.data.replace("delete_all_", "")
        # Получаем список ID сообщений из базы данных
        message_ids = dbwork.get_message_ids(topic_id)
        # Удаляем все сообщения
        for msg_id in message_ids:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=msg_id)
            except Exception as e:
                print(f"Не удалось удалить сообщение {msg_id}: {e}")
        # Удаляем запись из базы данных
        dbwork.delete_topic_messages(topic_id)
        return

    # calls
    if call.data == "python":
        python_markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        counter_chapters = 0

        for chapter in python_chapters_true:
            counter_chapters += 1
            if len(chapter) >= 33:
                chapter_true = f"{chapter[:33]}"
                chapter = chapter_true
                chapter_true = f"{chapter_true}.."
            else:
                chapter_true = f"{chapter}"
            button = telebot.types.InlineKeyboardButton(chapter_true,
                                                        callback_data=chapter)
            python_markup.add(button)

        bot.edit_message_text("Выбери главу, с которой хочешь начать:",
                              chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=python_markup)

    if call.data in python_topics_true:
        href = dbwork.get_href("Python", call.data)
        text = parsework.get_text(href)
        message_ids = []  # Список для хранения ID сообщений

        for page in text:
            if "https://metanit.com/python/tutorial/pics" in page:
                # Отправляем изображение
                msg = bot.send_photo(chat_id=call.message.chat.id, photo=page)
                message_ids.append(msg.message_id)  # Сохраняем ID сообщения
            else:
                # Отправляем текст
                msg = bot.send_message(call.message.chat.id, page, parse_mode='HTML')
                message_ids.append(msg.message_id)  # Сохраняем ID сообщения

        # Сохраняем ID сообщений в базе данных
        dbwork.save_message_ids(call.data, message_ids)

        # Добавляем Inline Keyboard с кнопкой "Удалить все" на последнее сообщение
        delete_markup = telebot.types.InlineKeyboardMarkup()
        delete_button = telebot.types.InlineKeyboardButton(
            "Удалить все", callback_data=f"delete_all_{call.data}"
        )
        delete_markup.add(delete_button)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                      message_id=msg.message_id,
                                      reply_markup=delete_markup)

    if call.data in python_chapters_true:
        chapter_topics_noms = dbwork.get_noms(call.data)
        text = chapter_topics_noms.replace("[", "").replace("]", "")
        nums = text.split(', ')

        python_markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        for num in nums:
            button = telebot.types.InlineKeyboardButton(list(dbwork.get_data("Python",
                                                                             "topic",
                                                                             num))[0][0],
                                                        callback_data=list(dbwork.get_data("Python",
                                                                                           "short_topic",
                                                                                           num))[0][0])
            python_markup.add(button)
        button_back = telebot.types.InlineKeyboardButton("Назад", callback_data="python")
        python_markup.add(button_back)
        bot.edit_message_text("Хорошо! Выбери тему, которую хочешь изучить:",
                              chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=python_markup)


# Запуск бота
bot.polling()
