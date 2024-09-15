from flask import Flask, jsonify, request
import mysql.connector  # MySQL entegrasyonu için

app = Flask(__name__)

# Veritabanı bağlantısını sağlayan fonksiyon
def db_connection():
    return mysql.connector.connect(
        host="localhost",  # MySQL sunucusu yerel makinede çalışıyor
        user="youruser",  # MySQL kullanıcı adı
        password="yourpassword",  # MySQL kullanıcı şifresi
        database="mydb"  # Kullanılacak veritabanı
    )

# Tüm siparişleri listeleyen endpoint
@app.route('/siparisler', methods=['GET'])
def siparisleri_getir():
    conn = db_connection()  # Veritabanına bağlanıyoruz
    cursor = conn.cursor(dictionary=True)  # Sorgu sonucunu dictionary formatında almak için
    cursor.execute("SELECT * FROM siparisler")  # Tüm siparişleri sorguluyoruz
    siparisler = cursor.fetchall()  # Sorgu sonucunu alıyoruz
    cursor.close()  # Cursor'u kapatıyoruz
    conn.close()  # Veritabanı bağlantısını kapatıyoruz
    return jsonify(siparisler), 200  # JSON formatında sipariş listesini döndürüyoruz

# Yeni sipariş ekleyen endpoint
@app.route('/siparisler', methods=['POST'])
def siparis_ekle():
    yeni_siparis = request.json  # İstekle gelen JSON verisini alıyoruz
    conn = db_connection()  # Veritabanına bağlanıyoruz
    cursor = conn.cursor()  # Cursor oluşturuyoruz
    sql = "INSERT INTO siparisler (urun_id, miktar, toplam_fiyat) VALUES (%s, %s, %s)"  # Sipariş ekleme sorgusu
    cursor.execute(sql, (yeni_siparis['urun_id'], yeni_siparis['miktar'], yeni_siparis['toplam_fiyat']))  # Sorguyu çalıştırıyoruz
    conn.commit()  # Değişiklikleri kaydediyoruz
    cursor.close()  # Cursor'u kapatıyoruz
    conn.close()  # Veritabanı bağlantısını kapatıyoruz
    return jsonify({"mesaj": "Yeni sipariş eklendi."}), 201  # Başarılı ekleme mesajı döndürüyoruz

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)  # Flask uygulamasını başlatıyoruz, 5003 portunda dinliyor
