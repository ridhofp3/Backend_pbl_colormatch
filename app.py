from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import json
from mysql.connector import Error

# Inisialisasi Flask app
app = Flask(__name__)
CORS(app)  # Mengizinkan cross-origin

# Konfigurasi koneksi MySQL
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",  # Ganti dengan username MySQL kamu
        password="root",  # Ganti dengan password MySQL kamu
        database="scan_history"  # Ganti dengan nama database yang kamu gunakan
    )
    
    if db.is_connected():
        print("Berhasil terhubung ke database MySQL!")
except Error as e:
    print(f"Gagal terhubung ke database MySQL: {e}")
    db = None  # Jika koneksi gagal, set db ke None untuk mencegah aplikasi berjalan

# Endpoint untuk mendapatkan data
@app.route('/data', methods=['GET'])
def get_data():
    if db is None or not db.is_connected():
        return jsonify({"message": "Tidak dapat terhubung ke database"}), 500

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_history")  # Ganti dengan nama tabel yang sesuai
    result = cursor.fetchall()
    cursor.close()
    return jsonify(result)  # Mengembalikan data dalam format JSON

# Endpoint untuk menambah data
@app.route('/data', methods=['POST'])
def add_data():
    if db is None or not db.is_connected():
        return jsonify({"message": "Tidak dapat terhubung ke database"}), 500

    data = request.json  # Mengambil data JSON yang dikirimkan
    cursor = db.cursor()
    sql = """
    INSERT INTO user_history (UUID, scan_date, recommendation, skin_tone) 
    VALUES (%s, %s, %s, %s)
    """
    
    # Menyusun nilai untuk dimasukkan ke dalam query
    val = (
        data['UUID'], 
        data['scan_date'], 
        json.dumps(data.get('recommendation', None)),  # Mengonversi recommendation ke JSON string
        data.get('skin_tone', None)
    )
    
    cursor.execute(sql, val)
    db.commit()  # Menyimpan perubahan ke database
    cursor.close()
    return jsonify({"message": "Data added successfully"}), 201  # Mengembalikan pesan sukses

# Endpoint untuk memeriksa status koneksi database
@app.route('/check_connection', methods=['GET'])
def check_connection():
    if db is None or not db.is_connected():
        return jsonify({"message": "Tidak terhubung ke database MySQL"}), 500
    return jsonify({"message": "Berhasil terhubung ke database MySQL!"})

# Endpoint testing, untuk memastikan API berjalan dengan baik
@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({"message": "API bekerja dengan baik"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
