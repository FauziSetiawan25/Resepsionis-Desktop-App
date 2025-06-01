from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS jika perlu akses frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy data lengkap
dummy_data = {
    "101": {
        "id": 101,
        "name": "Andi Wijaya",
        "nik": "1234567890123456",
        "birth_place": "Bandung",
        "birth_date": "1993-05-01",
        "gender": "Laki-laki",
        "address": "Jl. Merdeka No. 10, Bandung",
        "phone": "081234567890",
        "marital_status": "Menikah",
        "job": "Karyawan Swasta",
        "citizenship": "WNI",
        "religion": "Islam",
        "emergency_contact": {
            "name": "Ahmad Rahma",
            "phone": "081298765432",
            "relation": "Suami"
        },
        "bpjs": "1234567890",
        "medical_history": "Hipertensi",
        "allergies": "Debu",
        "blood_type": "O",
        "riwayat_berobat": [
            {
                "rumah_sakit": "RS Harapan Bunda",
                "keterangan": "Pemeriksaan awal dan registrasi ulang.",
                "tanggal": "2025-04-01"
            },
            {
                "rumah_sakit": "RS Kasih Ibu",
                "keterangan": "Kontrol lanjutan pasca operasi.",
                "tanggal": "2025-04-12"
            }
        ]
    },
    "102": {
        "id": 102,
        "name": "Siti Rahma",
        "nik": "9876543210987654",
        "birth_place": "Jakarta",
        "birth_date": "1996-08-12",
        "gender": "Perempuan",
        "address": "Jl. Diponegoro No. 5, Jakarta",
        "phone": "082112345678",
        "marital_status": "Menikah",
        "occupation": "Ibu Rumah Tangga",
        "nationality": "WNI",
        "religion": "Islam",
        "emergency_contact": {
            "name": "Dedi Saputra",
            "phone": "085712345678",
            "relation": "Suami"
        },
        "bpjs": "9876543210987",
        "medical_history": "",
        "allergy": "Seafood",
        "blood_type": "A",
        "riwayat_berobat": None
    }
}

# Endpoint ambil data pasien
@app.get("/api/patients/{patient_id}")
def get_patient(patient_id: str):
    patient = dummy_data.get(patient_id)
    if patient:
        return patient
    return {"detail": "Not found"}

# Endpoint tambah / update pasien
@app.post("/api/patients/")
async def add_or_update_patient(patient: Request):
    data = await patient.json()
    patient_id = str(data.get("id"))

    # Default value untuk semua field
    default_fields = {
        "name": "",
        "nik": "",
        "birth_place": "",
        "birth_date": "",
        "gender": "",
        "address": "",
        "phone": "",
        "marital_status": "",
        "job": "",
        "citizenship": "",
        "religion": "",
        "emergency_contact": {
            "name": "",
            "phone": "",
            "relation": ""
        },
        "bpjs": "",
        "medical_history": "",
        "allergies": "",
        "blood_type": "",
        "riwayat_berobat": None
    }

    # Pastikan semua field ada
    for field, default_value in default_fields.items():
        if field not in data:
            data[field] = default_value
        elif field == "emergency_contact":
            # Jaga-jaga kalau cuma sebagian isian kontak darurat yang dikirim
            for sub_field in ["name", "phone", "relation"]:
                data[field].setdefault(sub_field, "")

    dummy_data[patient_id] = data
    return {"message": "Patient data saved successfully"}
