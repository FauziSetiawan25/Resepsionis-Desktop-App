import tkinter as tk
from tkinter import messagebox
from desktop_app import ReceptionistApp
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.auth_db import check_credentials, init_auth_db

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Login Resepsionis")
        self.root.geometry("400x250")
        self.root.configure(bg="#f0f0f0")

        # Inisialisasi auth_db jika belum ada
        init_auth_db()

        tk.Label(root, text="👤 Username:", bg="#f0f0f0").pack(pady=10)
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack()

        tk.Label(root, text="🔑 Password:", bg="#f0f0f0").pack(pady=10)
        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login, bg="#4CAF50", fg="white", width=20).pack(pady=20)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        hospital = check_credentials(username, password)
        if hospital:
            self.root.withdraw()  # Sembunyikan jendela login
            main_window = tk.Toplevel(self.root)
            main_window.state("zoomed")
            ReceptionistApp(main_window, login_root=self.root, hospital_name=hospital)
        else:
            messagebox.showerror("Login Gagal", "❌ Username atau password salah.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
