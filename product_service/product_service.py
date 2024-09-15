from flask import Flask, jsonify, request
import mysql.connector  # MySQL veritabanı bağlantısı için gerekli kütüphane

app = Flask(__name__)

# Veritabanı bağlantısını sağlayan fonksiyon
def db_connection():
    return mysql.connector.connect(
        host="localhost",  # MySQL sunucusu yerel makinede çalışıyor
        user="youruser",  # MySQL kullanıcı adı
        password="yourpassword",  # MySQL kullanıcı şifresi
        database="mydb"  # Kullanılacak veritabanı
    )

# Tüm ürünleri listeleyen endpoint
@app.route('/urunler', methods=['GET'])
def urunleri_getir():
    conn = db_connection()  # Veritabanına bağlanıyoruz
    cursor = conn.cursor(dictionary=True)  # Sorgu sonucunu dictionary formatında almak için
    cursor.execute("SELECT * FROM urunler")  # Tüm ürünleri sorguluyoruz
    urunler = cursor.fetchall()  # Sorgu sonucunu alıyoruz
    cursor.close()  # Cursor'u kapatıyoruz
    conn.close()  # Veritabanı bağlantısını kapatıyoruz
    return jsonify(urunler), 200  # JSON formatında ürün listesini döndürüyoruz

# Yeni ürün ekleyen endpoint
@app.route('/urunler', methods=['POST'])
def urun_ekle():
    yeni_urun = request.json  # İstekle gelen JSON verisini alıyoruz
    conn = db_connection()  # Veritabanına bağlanıyoruz
    cursor = conn.cursor()  # Cursor oluşturuyoruz
    sql = "INSERT INTO urunler (isim, fiyat) VALUES (%s, %s)"  # Ürün ekleme sorgusu
    cursor.execute(sql, (yeni_urun['isim'], yeni_urun['fiyat']))  # Sorguyu çalıştırıyoruz
    conn.commit()  # Değişiklikleri kaydediyoruz
    cursor.close()  # Cursor'u kapatıyoruz
    conn.close()  # Veritabanı bağlantısını kapatıyoruz
    return jsonify({"mesaj": "Yeni ürün eklendi."}), 201  # Başarılı ekleme mesajı döndürüyoruz

# Belirli bir ürünü ID'ye göre getiren endpoint
@app.route('/urunler/<int:id>', methods=['GET'])
def urun_bul(id):
    conn = db_connection()  # Veritabanına bağlanıyoruz
    cursor = conn.cursor(dictionary=True)  # Sorgu sonucunu dictionary formatında almak için
    cursor.execute("SELECT * FROM urunler WHERE id = %s", (id,))  # Verilen ID'ye göre ürünü sorguluyoruz
    urun = cursor.fetchone()  # İlk bulduğu ürünü alıyoruz
    cursor.close()  # Cursor'u kapatıyoruz
    conn.close()  # Veritabanı bağlantısını kapatıyoruz
    if urun:
        return jsonify(urun), 200  # Ürün bulunduysa JSON formatında döndürüyoruz
    else:
        return jsonify({"mesaj": "Ürün bulunamadı."}), 404  # Ürün bulunamazsa hata mesajı döndürüyoruz

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)  # Flask uygulamasını başlatıyoruz, 5002 portunda dinliyor
