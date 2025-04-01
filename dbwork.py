import sqlite3

conn = sqlite3.connect('topics_hrefs.db', check_same_thread=False)
c = conn.cursor()


def get_chapter(table):
    topics = list(c.execute(f"""SELECT Chapter FROM {table} """))
    for i in range(1, len(topics) + 1):
        for top in list(c.execute(f"""SELECT Chapter FROM {table} WHERE No={i} """)):
            yield top


def get_topic(table):
    topics = list(c.execute(f"""SELECT topic FROM {table} """))
    for i in range(1, len(topics)+1):
        for top in list(c.execute(f"""SELECT topic FROM {table} WHERE No={i} """)):
            yield top


def get_data(table, what, nom):
    for top in list(c.execute(f"""SELECT {what} FROM {table} WHERE No={nom} """)):
        yield list(top)


def get_href(table, topic):
    hrefs = list(c.execute(f"""SELECT href FROM {table} WHERE short_topic='{topic}' """))
    return hrefs[0][0]


def get_noms(nom):
    topics = list(c.execute(f"""SELECT Nos FROM PythonChapters WHERE short_chapter = '{nom}'"""))
    return topics[0][0]


def get_db_connection():
    connection = sqlite3.connect('topics_hrefs.db')
    connection.row_factory = sqlite3.Row
    return connection


# Сохранение ID сообщений в базу данных
def save_message_ids(topic_id, message_ids):
    connection = get_db_connection()
    for msg_id in message_ids:
        connection.execute('INSERT INTO messages (topic_id, message_id) VALUES (?, ?)', (topic_id, msg_id))
    connection.commit()
    connection.close()


# Получение ID сообщений по теме
def get_message_ids(topic_id):
    connection = get_db_connection()
    cursor = connection.execute('SELECT message_id FROM messages WHERE topic_id = ?', (topic_id,))
    message_ids = [row['message_id'] for row in cursor.fetchall()]
    connection.close()
    return message_ids


# Удаление ID сообщений по теме
def delete_topic_messages(topic_id):
    connection = get_db_connection()
    connection.execute('DELETE FROM messages WHERE topic_id = ?', (topic_id,))
    connection.commit()
    connection.close()
