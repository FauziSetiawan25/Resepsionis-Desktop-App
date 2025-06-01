import sqlite3
import os

# Dapatkan path database berdasarkan nama rumah sakit
def get_db_path(hospital_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    db_filename = hospital_name.lower().replace(" ", "_") + ".db"
    return os.path.join(data_dir, db_filename)

# Koneksi ke database
def connect_db(hospital_name):
    db_path = get_db_path(hospital_name)
    print(f"[DEBUG] Terhubung ke DB: {db_path}")
    return sqlite3.connect(db_path)

# Inisialisasi DB dan tabel pasien
def init_db(hospital_name):
    conn = connect_db(hospital_name)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            nik TEXT,
            birth_date TEXT,
            gender TEXT,
            address TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

# Cek apakah pasien sudah ada
def is_patient_exist(patient_id, hospital_name):
    conn = connect_db(hospital_name)
    c = conn.cursor()
    c.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    data = c.fetchone()
    conn.close()
    return data is not None

# Simpan data pasien
def save_patient(data, hospital_name):
    conn = connect_db(hospital_name)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO patients (id, name, nik, birth_date, gender, address, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"],
        data["name"],
        data["nik"],
        data["birth_date"],
        data.get("gender", ""),
        data["address"],
        data.get("phone", "")
    ))
    conn.commit()
    conn.close()

# Update data pasien
def update_patient(data, hospital_name):
    conn = connect_db(hospital_name)
    c = conn.cursor()
    c.execute("""
        UPDATE patients
        SET name=?, nik=?, birth_date=?, gender=?, address=?, phone=?
        WHERE id=?
    """, (
        data["name"],
        data["nik"],
        data["birth_date"],
        data.get("gender", ""),
        data["address"],
        data.get("phone", ""),
        data["id"]
    ))
    conn.commit()
    conn.close()

# Ambil semua data pasien
def get_all_patients(hospital_name):
    conn = connect_db(hospital_name)
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    rows = c.fetchall()
    conn.close()
    return rows

# Hapus data pasien
def delete_patient(patient_id, hospital_name):
    conn = connect_db(hospital_name)
    c = conn.cursor()
    c.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()

# Print semua pasien (debug terminal)
def show_all_patients(hospital_name):
    patients = get_all_patients(hospital_name)
    if not patients:
        print("📭 Tidak ada data pasien.")
        return
    print("📋 Daftar Pasien:")
    print("-" * 60)
    for p in patients:
        print(f"🆔 ID       : {p[0]}")
        print(f"👤 Nama    : {p[1]}")
        print(f"🪪 NIK     : {p[2]}")
        print(f"🎂 Lahir   : {p[3]}")
        print(f"🚻 Gender  : {p[4]}")
        print(f"🏠 Alamat  : {p[5]}")
        print(f"📞 Telepon : {p[6]}")
        print("-" * 60)
