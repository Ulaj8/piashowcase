from flask import Flask, jsonify, request  # Flask, JSON yanıtları ve istekleri yönetmek için kullanılıyor.

app = Flask(__name__)

# Yorumları saklayan basit bir liste.
yorumlar = []

# Kök dizin ('/') için bir endpoint oluşturuyorum.
# Bu sayede uygulamaya istek gönderdiğimde çalıştığını görebileceğim.
@app.route('/')
def anasayfa():
    return "Merhaba! Yorum Servisi çalışıyor, burada yorumları yönetebilirim!"  # Basit bir yanıt döndürüyorum.

# Yorum ekleme endpoint'i
@app.route('/yorumlar', methods=['POST'])
def yorum_ekle():
    yorum = request.json  # İstekten gelen JSON verisini alıyoruz.
    print(f"Gelen Yorum: {yorum}")  # Gelen JSON verisini terminalde logluyoruz.
    
    # Basit hata kontrolü: eksik 'urun_id' veya 'yorum' durumunda hata döndür
    if 'urun_id' not in yorum or 'yorum' not in yorum:
        return jsonify({"hata": "Eksik bilgi, 'urun_id' ve 'yorum' gereklidir."}), 400
    
    yorumlar.append(yorum)  # Yorumları listeye ekliyoruz.
    return jsonify(yorum), 201  # Başarılı ekleme işlemi yanıtı döndürüyoruz.

# Tüm yorumları listeleyen endpoint
@app.route('/yorumlar', methods=['GET'])
def yorumlari_getir():
    if not yorumlar:
        return jsonify({"hata": "Henüz yorum bulunmamaktadır."}), 404  # Eğer yorum yoksa hata döndürüyoruz.
    return jsonify(yorumlar), 200  # Yorum listesini JSON formatında döndürüyoruz.

# Flask uygulamasını başlatıyorum. 5008 portunda çalışıyor.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)
