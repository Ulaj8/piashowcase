import redis
import sqlite3

# SQLite veritabanına bağlan
def setup_database():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

# Redis'ten gelen mesajları dinleyip veritabanına kaydeder
def listen_for_messages():
    conn = setup_database()
    client = redis.Redis(host="redis", port=6379)
    pubsub = client.pubsub()
    pubsub.subscribe("mesaj_kanalı")

    print("Mesajlar dinleniyor ve kaydediliyor...")
    for message in pubsub.listen():
        if message['type'] == 'message':
            msg = message['data'].decode('utf-8')
            print(f"Yeni mesaj: {msg}")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (message) VALUES (?)", (msg,))
            conn.commit()

if __name__ == "__main__":
    listen_for_messages()
