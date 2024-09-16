from flask import Flask, jsonify, request  # Flask ve JSON işlemleri için gerekli kütüphaneler
import mysql.connector  # MySQL bağlantısı için gerekli kütüphane
import time

app = Flask(__name__)

# Veritabanı bağlantısı fonksiyonu
def connect_db():
    while True:
        try:
            # Veritabanı bağlantısı için gerekli bilgileri tanımlıyorum
            db = mysql.connector.connect(
                host="mysql",  # MySQL servisi adı (docker-compose ile container adı mysql)
                user="youruser",  # Daha önce oluşturduğun MySQL kullanıcı adı
                password="yourpassword",  # MySQL kullanıcı şifresi
                database="mydb"  # Bağlanacağın veritabanı
            )
            return db
        except mysql.connector.Error as err:
            print(f"Bağlanılamadı: {err}. 5 saniye sonra tekrar denenecek.")
            time.sleep(5)

db = connect_db()

# Ana sayfa endpoint'i
@app.route('/')
def ana_sayfa():
    return "Kullanıcı Servisine Hoş Geldiniz!"

# Tüm kullanıcıları listeleyen endpoint
@app.route('/kullanicilar', methods=['GET'])
def kullanicilari_getir():
    cursor = db.cursor(dictionary=True)  # Veritabanında sorgu yapabilmek için bir cursor oluşturuyorum
    cursor.execute("SELECT * FROM kullanicilar")  # Veritabanındaki tüm kullanıcıları çekiyorum
    kullanicilar = cursor.fetchall()  # Sonuçları alıyorum
    cursor.close()  # Cursor'u kapatıyorum
    return jsonify(kullanicilar), 200  # JSON formatında kullanıcıları döndürüyorum

# Yeni kullanıcı ekleme endpoint'i
@app.route('/kullanicilar', methods=['POST'])
def kullanici_ekle():
    yeni_kullanici = request.json  # İstekten gelen JSON verisini alıyorum
    cursor = db.cursor()  # Veritabanına veri eklemek için cursor oluşturuyorum
    cursor.execute(
        "INSERT INTO kullanicilar (isim, email) VALUES (%s, %s)",
        (yeni_kullanici['isim'], yeni_kullanici['email'])  # Kullanıcı bilgilerini veritabanına ekliyorum
    )
    db.commit()  # Değişiklikleri kaydediyorum
    yeni_kullanici['id'] = cursor.lastrowid  # Yeni kullanıcının id'sini alıyorum
    cursor.close()  # Cursor'u kapatıyorum
    return jsonify(yeni_kullanici), 201  # Başarılı ekleme yanıtı döndürüyorum

# Belirli bir kullanıcıyı ID'ye göre bulan endpoint
@app.route('/kullanicilar/<int:id>', methods=['GET'])
def kullanici_bul(id):
    cursor = db.cursor(dictionary=True)  # Kullanıcıyı bulmak için cursor oluşturuyorum
    cursor.execute("SELECT * FROM kullanicilar WHERE id = %s", (id,))  # ID'ye göre kullanıcıyı buluyorum
    kullanici = cursor.fetchone()  # Tek bir kullanıcı alıyorum
    cursor.close()  # Cursor'u kapatıyorum
    if kullanici is None:
        return jsonify({"hata": "Kullanıcı bulunamadı"}), 404  # Kullanıcı bulunmazsa hata döndürüyorum
    return jsonify(kullanici), 200  # Kullanıcıyı JSON formatında döndürüyorum

if __name__ == "__main__":  # Doğru if bloğu
    app.run(host="0.0.0.0", port=5001)  # Uygulama 5001 portunda çalışıyor
