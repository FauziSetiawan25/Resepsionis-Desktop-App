import tkinter as tk
import requests
from datetime import date
from tkinter import ttk, messagebox
import tkinter.simpledialog as simpledialog
from scanner import scan_qr_code
from db import *

class ReceptionistApp:
    def __init__(self, root, login_root=None, hospital_name=""):
        self.hospital_name = hospital_name
        self.root = root
        self.login_root = login_root
        self.root.title("🏥 Sistem Resepsionis Rumah Sakit")
        self.root.geometry("800x500")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("default")

        # Gaya tabel Treeview
        style.configure("Treeview",
            background="#ffffff",
            foreground="#333",
            rowheight=30,
            fieldbackground="#ffffff",
            font=("Segoe UI", 10)
        )
        style.configure("Treeview.Heading",
            background="#4CAF50",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )
        style.map("Treeview", background=[("selected", "#cce5ff")])


        # Gaya tombol umum
        button_style = {
            "font": ("Segoe UI", 10, "bold"),
            "padx": 20,
            "pady": 5,
            "bd": 0,
            "relief": "flat",
            "activeforeground": "white"
        }

        self.title_label = tk.Label(root, text="📋 Daftar Pasien", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=5)

        self.hospital_label = tk.Label(root, text=self.hospital_name, font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.hospital_label.pack(pady=5)


        # Tabel daftar pasien
        self.tree = ttk.Treeview(root, columns=("id",  "name", "nik", "birth_date", "gender", "address", "phone"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=130)

        self.tree.pack(pady=10, fill="both", expand=True)

        self.tree.bind("<Double-1>", self.show_patient_details)

        # Tombol
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        self.scan_btn = tk.Button(
        button_frame,
        text="📷 Scan QR",
        command=self.scan_qr,
        bg="#4CAF50",
        fg="white",
        activebackground="#45a049",
        **button_style
        )
        self.scan_btn.pack(side="left", padx=10)

        # self.refresh_btn = tk.Button(
        #     button_frame,
        #     text="🔄 Refresh",
        #     command=self.refresh_table,
        #     bg="#2196F3",
        #     fg="white",
        #     activebackground="#1e88e5",
        #     **button_style
        # )
        # self.refresh_btn.pack(side="left", padx=10)

        # self.edit_btn = tk.Button(
        # button_frame,
        # text="✏️ Edit",
        # command=self.edit_selected,
        # bg="#FFC107",
        # fg="black",
        # activebackground="#e0a800",
        # **button_style
        # )
        # self.edit_btn.pack(side="left", padx=10)

        self.delete_btn = tk.Button(
            button_frame,
            text="🗑️ Hapus",
            command=self.delete_selected,
            bg="#f44336",
            fg="white",
            activebackground="#d32f2f",
            **button_style
        )
        self.delete_btn.pack(side="left", padx=10)

        self.logout_btn = tk.Button(
        self.root,
        text="🏃🚪",
        command=self.logout,
        bg="#f44336",
        fg="white",
        activebackground="#d32f2f",
        **button_style
        )
        self.logout_btn.place(x=10, y=10)


        # Inisialisasi DB untuk RS sesuai login
        init_db(self.hospital_name)
        self.refresh_table()


    def refresh_table(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)
            for patient in get_all_patients(self.hospital_name):
                self.tree.insert("", "end", values=patient)
        except Exception as e:
            print(f"[Error refresh_table] {e}")

    def scan_qr(self):
        try:
            qr_data = scan_qr_code()
            if qr_data:
                print(f"✅ QR Code terbaca: {qr_data}")
                url = f"http://localhost:8000/api/patients/{qr_data}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if is_patient_exist(data["id"], self.hospital_name):
                        messagebox.showinfo("Info", "ℹ️ Pasien sudah ada di database.")
                    else:
                        save_patient(data, self.hospital_name)
                        messagebox.showinfo("Sukses", "✅ Data pasien berhasil ditambahkan!")
                    self.refresh_table()
                else:
                    messagebox.showwarning("Tidak ditemukan", "❌ Data tidak ditemukan di server.")
            else:
                messagebox.showwarning("Tidak terbaca", "⚠️ Tidak ada QR yang terbaca.")
        except Exception as e:
            messagebox.showerror("Gagal", f"❌ Terjadi kesalahan saat scan: {e}")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "❗ Pilih pasien yang ingin dihapus.")
            return

        confirm = messagebox.askyesno("Konfirmasi", "Apakah kamu yakin ingin menghapus data ini?")
        if not confirm:
            return

        for item in selected:
            patient_id = self.tree.item(item)["values"][0]  # kolom pertama adalah ID
            delete_patient(patient_id, self.hospital_name)
            self.tree.delete(item)

        messagebox.showinfo("Berhasil", "✅ Data berhasil dihapus.")
    def show_patient_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item)["values"]
        patient_id = values[0]

        # Ambil data dari API
        try:
            url = f"http://localhost:8000/api/patients/{patient_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
            else:
                messagebox.showwarning("Gagal", "⚠️ Tidak bisa ambil data dari server.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"❌ Gagal mengambil detail pasien: {e}")
            return

        detail_win = tk.Toplevel(self.root)
        detail_win.state("zoomed")
        detail_win.title("📋 Detail Pasien")
        detail_win.geometry("480x500")
        detail_win.configure(bg="#f0f0f0")

        info_text = f"""
        🆔 ID: {data.get("id")}
        👤 Nama: {data.get("name")}
        🆔 NIK: {data.get("nik")}
        🎂 Tempat, Tanggal Lahir: {data.get("birth_place")}, {data.get("birth_date")}
        🚻 Jenis Kelamin: {data.get("gender")}
        🏠 Alamat: {data.get("address")}
        📞 No. HP: {data.get("phone")}
        ❤️ Status Pernikahan: {data.get("marital_status")}
        💼 Pekerjaan: {data.get("job")}
        🌏 Kewarganegaraan: {data.get("citizenship")}
        🛐 Agama: {data.get("religion")}

        🩺 Riwayat Penyakit: {data.get("medical_history")}
        ⚠️ Alergi: {data.get("allergies")}
        🩸 Golongan Darah: {data.get("blood_type")}
        🆔 No. BPJS: {data.get("bpjs")}

        📞 Kontak Darurat:
            Nama: {data.get("emergency_contact", {}).get("name")}
            Hubungan: {data.get("emergency_contact", {}).get("relation")}
            No. HP: {data.get("emergency_contact", {}).get("phone")}
        """


        tk.Label(detail_win, text=info_text, justify="left", bg="#f0f0f0", font=("Segoe UI", 10)).pack(padx=10, pady=10, anchor="w")

        # Label riwayat
        tk.Label(detail_win, text="📚 Riwayat Berobat:", font=("Segoe UI", 10, "bold"), bg="#f0f0f0").pack(anchor="w", padx=10)

        # Scrollable Text
        text_frame = tk.Frame(detail_win, bg="#f0f0f0")
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)

        text_widget = tk.Text(text_frame, height=10, wrap="word", font=("Segoe UI", 10))
        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def load_riwayat():
            riwayat = data.get("riwayat_berobat", [])
            text_widget.configure(state="normal")
            text_widget.delete("1.0", "end")
            if not riwayat:
                text_widget.insert("1.0", "Belum ada riwayat berobat.")
            else:
                for entry in riwayat:
                    text_widget.insert("end", f"📍 {entry['rumah_sakit']} - {entry['tanggal']}\n📝 {entry['keterangan']}\n\n")
            text_widget.configure(state="disabled")

        load_riwayat()

        def tambah_riwayat():
            keterangan = simpledialog.askstring("Keterangan", "Masukkan keterangan pemeriksaan:")
            if not keterangan:
                return

            new_entry = {
                "rumah_sakit": self.hospital_name,
                "keterangan": keterangan,
                "tanggal": str(date.today())
            }

            # Tambahkan ke riwayat lokal
            riwayat = data.get("riwayat_berobat") or []
            riwayat.append(new_entry)
            data["riwayat_berobat"] = riwayat

            try:
                patient_id = data.get("id")  # atau NIK
                if not patient_id:
                    raise ValueError("ID pasien tidak ditemukan.")

                # Kirim PUT request ke API
                response = requests.put(
                    f"http://localhost:8000/api/patients/{patient_id}",
                    json=data
                )

                if response.status_code == 200:
                    messagebox.showinfo("Sukses", "✅ Riwayat berhasil ditambahkan.")
                    load_riwayat()
                else:
                    messagebox.showerror("Gagal", f"❌ Gagal menyimpan riwayat. Status: {response.status_code}")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Gagal update data: {e}")


        # Tombol tambah
        tk.Button(detail_win, text="➕ Tambah Riwayat", command=tambah_riwayat,
                bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold")).pack(pady=10)



    # def edit_selected(self):
    #     selected = self.tree.selection()
    #     if not selected:
    #         messagebox.showwarning("Peringatan", "❗ Pilih pasien yang ingin diedit.")
    #         return

    #     values = self.tree.item(selected)["values"]
    #     edit_win = tk.Toplevel(self.root)
    #     edit_win.title("✏️ Edit Data Pasien")

    #     labels = ["Nama", "NIK", "Tanggal Lahir", "Alamat"]
    #     fields = []

    #     for i, label in enumerate(labels):
    #         tk.Label(edit_win, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
    #         entry = tk.Entry(edit_win, width=40)
    #         entry.grid(row=i, column=1, padx=10, pady=5)
    #         entry.insert(0, values[i+1])  # +1 karena kolom pertama ID
    #         fields.append(entry)

    #     def save_changes():
    #         new_data = {
    #             "id": values[0],
    #             "name": fields[0].get(),
    #             "nik": fields[1].get(),
    #             "birth_date": fields[2].get(),
    #             "address": fields[3].get()
    #         }

    #         # Simpan ke lokal
    #         update_patient(new_data, self.hospital_name)
            
    #         # Kirim ke API (kalau mau sinkron)
    #         try:
    #             response = requests.post("http://localhost:8000/api/patients", json=new_data)
    #             if response.status_code == 200:
    #                 messagebox.showinfo("Berhasil", "✅ Data berhasil disimpan dan dikirim ke server.")
    #             else:
    #                 messagebox.showwarning("Server", "⚠️ Data lokal disimpan, tapi gagal kirim ke server.")
    #         except:
    #             messagebox.showwarning("Server", "⚠️ Tidak dapat terhubung ke server.")

    #         self.refresh_table()
    #         edit_win.destroy() 

    #     tk.Button(edit_win, text="💾 Simpan", command=save_changes, bg="#4CAF50", fg="white", padx=10).grid(row=5, columnspan=2, pady=10)


    def logout(self):
        if self.login_root:
            self.login_root.deiconify() 
        self.root.destroy()

    def add_history(self, patient_id, parent_win=None):
            form = tk.Toplevel(self.root)
            form.title("Tambah Riwayat Berobat")
            form.geometry("400x300")

            tk.Label(form, text="🏥 Rumah Sakit").pack(pady=5)
            hospital_entry = tk.Entry(form, width=40)
            hospital_entry.insert(0, self.hospital_name)
            hospital_entry.pack()

            tk.Label(form, text="📝 Keterangan").pack(pady=5)
            note_entry = tk.Entry(form, width=40)
            note_entry.pack()

            tk.Label(form, text="📅 Tanggal (YYYY-MM-DD)").pack(pady=5)
            date_entry = tk.Entry(form, width=40)
            date_entry.pack()

            def submit():
                try:
                    # Fetch data dari server
                    url = f"http://localhost:8000/api/patients/{patient_id}"
                    response = requests.get(url)
                    if response.status_code != 200:
                        raise Exception("Pasien tidak ditemukan di server.")

                    data = response.json()
                    history = data.get("riwayat_berobat", []) or []

                    # Tambahkan entry baru
                    history.append({
                        "rumah_sakit": hospital_entry.get(),
                        "keterangan": note_entry.get(),
                        "tanggal": date_entry.get()
                    })

                    data["riwayat_berobat"] = history

                    # Kirim balik ke server
                    save = requests.post("http://localhost:8000/api/patients", json=data)
                    if save.status_code == 200:
                        messagebox.showinfo("Berhasil", "✅ Riwayat ditambahkan.")
                        form.destroy()
                        if parent_win: parent_win.destroy()
                    else:
                        raise Exception("Gagal menyimpan ke server.")
                except Exception as e:
                    messagebox.showerror("Gagal", f"❌ {e}")

            tk.Button(form, text="💾 Simpan", command=submit, bg="#4CAF50", fg="white", padx=10).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceptionistApp(root)
    root.mainloop()

