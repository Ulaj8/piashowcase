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

# Tüm stokları listeleyen endpoint
@app.route('/stoklar', methods=['GET'])
def stoklari_getir():
    conn = db_connection()  # Veritabanına bağlanıyoruz
    cursor = conn.cursor(dictionary=True)  # Sorgu sonucunu dictionary formatında almak için
    cursor.execute("SELECT * FROM stoklar")  # Tüm stokları sorguluyoruz
    stoklar = cursor.fetchall()  # Sorgu sonucunu alıyoruz
    cursor.close()  # Cursor'u kapatıyoruz
    conn.close()  # Veritabanı bağlantısını kapatıyoruz
    return jsonify(stoklar), 200  # JSON formatında stok listesini döndürüyoruz

# Yeni stok ekleyen endpoint
@app.route('/stoklar', methods=['POST'])
def stok_ekle():
    yeni_stok = request.json  # İstekle gelen JSON verisini alıyoruz
    conn = db_connection()  # Veritabanına bağlanıyoruz
    cursor = conn.cursor()  # Cursor oluşturuyoruz
    sql = "INSERT INTO stoklar (urun_id, miktar) VALUES (%s, %s)"  # Stok ekleme sorgusu
    cursor.execute(sql, (yeni_stok['urun_id'], yeni_stok['miktar']))  # Sorguyu çalıştırıyoruz
    conn.commit()  # Değişiklikleri kaydediyoruz
    cursor.close()  # Cursor'u kapatıyoruz
    conn.close()  # Veritabanı bağlantısını kapatıyoruz
    return jsonify({"mesaj": "Yeni stok eklendi."}), 201  # Başarılı ekleme mesajı döndürüyoruz

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)  # Flask uygulamasını başlatıyoruz, 5006 portunda dinliyor
