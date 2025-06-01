from db import init_db, get_all_patients

def show_all_patients():
    hospital = input("🏥 Masukkan nama rumah sakit: ")
    init_db(hospital)  # inisialisasi DB jika belum ada
    patients = get_all_patients(hospital)
    
    if not patients:
        print("📭 Tidak ada data pasien.")
        return

    print(f"📋 Daftar Pasien dari {hospital}:")
    print("-" * 60)
    for p in patients:
        print(f"🆔 ID       : {p[0]}")
        print(f"👤 Nama    : {p[1]}")
        print(f"🪪 NIK     : {p[2]}")
        print(f"🎂 Lahir   : {p[3]}")
        print(f"🏠 Alamat  : {p[4]}")
        print("-" * 60)

if __name__ == "__main__":
    show_all_patients()
