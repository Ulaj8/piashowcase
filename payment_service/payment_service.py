from flask import Flask, jsonify, request  # Flask ve JSON işlemleri için gerekli modüller.
import logging  # Loglama işlemleri için.

# Loglama ayarlarını yapıyorum
logging.basicConfig(level=logging.INFO)

# Flask uygulaması başlatılıyor
app = Flask(__name__)

# Ödeme işlemlerini saklamak için basit bir liste
payments = []

# Ödeme işlemi yapma endpoint'i
@app.route('/payments', methods=['POST'])
def process_payment():
    payment = request.json  # İstekten gelen JSON verisini alıyorum.
    
    # Basit hata kontrolü: Eksik 'order_id' veya 'amount' bilgisi varsa hata döndür
    if 'order_id' not in payment or 'amount' not in payment:
        return jsonify({"hata": "Eksik bilgi, 'order_id' ve 'amount' gereklidir."}), 400
    
    payment['status'] = 'success'  # Ödeme başarılı olduğu varsayılıyor.
    payments.append(payment)  # Ödemeyi listeye ekliyoruz.
    return jsonify(payment), 201  # Başarılı yanıt döndürüyoruz.

# Tüm ödemeleri listeleyen endpoint
@app.route('/payments', methods=['GET'])
def get_payments():
    if not payments:
        return jsonify({"hata": "Henüz ödeme işlemi bulunmamaktadır."}), 404  # Eğer ödeme yoksa hata döndürüyoruz.
    return jsonify(payments), 200  # Ödeme listesini JSON formatında döndürüyoruz.

# Flask uygulamasını başlatıyoruz. 5004 portunda çalışıyor.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
