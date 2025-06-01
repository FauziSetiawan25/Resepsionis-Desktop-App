import requests
from scanner import scan_qr_code
from db import init_db, is_patient_exist, save_patient

def get_patient_data(patient_id):
    url = f"http://localhost:8000/api/patients/{patient_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"[API] Error: {e}")
        return None

def main():
    print("📷 Aplikasi Scan QR Pasien")
    hospital_name = input("🏥 Masukkan nama rumah sakit: ")
    init_db(hospital_name)

    qr_data = scan_qr_code()

    if qr_data:
        print(f"✅ QR Code terbaca: {qr_data}")
        data = get_patient_data(qr_data)

        if data:
            print("🎉 Data pasien ditemukan:")
            print(data)

            if is_patient_exist(data["id"], hospital_name):
                print("ℹ️ Pasien sudah ada di database lokal.")
            else:
                save_patient(data, hospital_name)
                print("✅ Data pasien disimpan ke database lokal.")
        else:
            print("❌ Data tidak ditemukan di server.")
    else:
        print("⚠️ Tidak ada QR yang terbaca.")

if __name__ == "__main__":
    main()
