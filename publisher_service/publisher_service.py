import redis

def publish_messages():
    client = redis.Redis(host="redis", port=6379)
    messages = ["Mesaj 1", "Mesaj 2", "Mesaj 3"]  # Buraya sabit mesajlar ekliyoruz

    for message in messages:
        print(f"Mesaj yayınlanıyor: {message}")
        client.publish("mesaj_kanalı", message)

if __name__ == "__main__":
    publish_messages()
