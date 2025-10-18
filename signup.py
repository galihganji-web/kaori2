from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import bcrypt
from encryption import encrypt_data, decrypt_data

# TEMA WARNA KAORI COFFEE
BG_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#1B5E7E"
SECONDARY_COLOR = "#2A7A9E"
TEXT_COLOR = "#1B5E7E"

root = Tk()
root.title("Kaori Coffee - Sign Up")
root.geometry("450x800")
root.configure(bg=BG_COLOR)

# Frame utama dengan scrollbar
canvas = Canvas(root, bg=BG_COLOR, highlightthickness=0)
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, bg=BG_COLOR)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Logo
try:
    logo_img = Image.open("kaori coffe logo.png")
    logo_img = logo_img.resize((150, 150), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = Label(scrollable_frame, image=logo_photo, bg=BG_COLOR)
    logo_label.image = logo_photo
    logo_label.pack(pady=15)
except:
    Label(scrollable_frame, text="KAORI COFFEE", font=("Arial", 16, "bold"), 
          fg=PRIMARY_COLOR, bg=BG_COLOR).pack(pady=15)

Label(scrollable_frame, text="REGISTRASI PEGAWAI", font=("Arial", 18, "bold"), 
      fg=PRIMARY_COLOR, bg=BG_COLOR).pack(pady=10)

# Form fields
fields = [
    ("Nama Panjang:", "e1"),
    ("Jabatan:", "e2"),
    ("Outlet:", "e3"),
    ("Username:", "e4"),
    ("Password:", "e5"),
    ("Nomor WA:", "e6")
]

entries = {}
for label_text, entry_name in fields:
    Label(scrollable_frame, text=label_text, font=("Arial", 11), 
          fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=(10, 5))
    
    if "Password" in label_text:
        entry = Entry(scrollable_frame, show="*", width=35, font=("Arial", 11), 
                     relief=SOLID, bd=2, highlightbackground=PRIMARY_COLOR)
    else:
        entry = Entry(scrollable_frame, width=35, font=("Arial", 11), 
                     relief=SOLID, bd=2, highlightbackground=PRIMARY_COLOR)
    
    entry.pack(pady=5, ipady=5)
    entries[entry_name] = entry

e1, e2, e3, e4, e5, e6 = entries['e1'], entries['e2'], entries['e3'], entries['e4'], entries['e5'], entries['e6']

def on_submit():
    nama_panjang = e1.get().strip()
    jabatan = e2.get().strip()
    outlet = e3.get().strip()
    username = e4.get().strip()
    password = e5.get().strip()
    nomor_wa = e6.get().strip()
    
    if not all([nama_panjang, jabatan, outlet, username, password, nomor_wa]):
        messagebox.showerror("Error", "Semua field harus diisi!")
        return
    
    if len(password) < 6:
        messagebox.showerror("Error", "Password minimal 6 karakter!")
        return
    
    try:
        conn = sqlite3.connect('pegawai.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM pegawai WHERE username = ?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username sudah digunakan!")
            conn.close()
            return
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        encrypted_nama = encrypt_data(nama_panjang)
        encrypted_jabatan = encrypt_data(jabatan)
        encrypted_outlet = encrypt_data(outlet)
        encrypted_nomor = encrypt_data(nomor_wa)
        
        cursor.execute("""
            INSERT INTO pegawai (nama_panjang, jabatan, outlet, username, password, nomor_hp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (encrypted_nama, encrypted_jabatan, encrypted_outlet, username, hashed_password, encrypted_nomor))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Data berhasil disimpan!\nNama: {nama_panjang}")
        
        for entry in entries.values():
            entry.delete(0, END)
        
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")

def on_delete():
    username = e4.get().strip()
    
    if not username:
        messagebox.showerror("Error", "Masukkan username yang akan dihapus!")
        return
    
    try:
        conn = sqlite3.connect('pegawai.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nama_panjang FROM pegawai WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if not result:
            messagebox.showerror("Error", f"Username '{username}' tidak ditemukan!")
            conn.close()
            return
        
        decrypted_nama = decrypt_data(result[1])
        
        confirm = messagebox.askyesno("Konfirmasi", 
                                      f"Hapus pegawai:\n{decrypted_nama} (username: {username})?")
        
        if confirm:
            cursor.execute("DELETE FROM pegawai WHERE username = ?", (username,))
            conn.commit()
            messagebox.showinfo("Success", f"Data '{decrypted_nama}' berhasil dihapus!")
            for entry in entries.values():
                entry.delete(0, END)
        
        conn.close()
        
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menghapus data: {str(e)}")

# Buttons
btn_submit = Button(scrollable_frame, text="DAFTAR", command=on_submit, 
                   bg=PRIMARY_COLOR, fg="white", font=("Arial", 12, "bold"), 
                   width=25, height=2, relief=FLAT, cursor="hand2")
btn_submit.pack(pady=15)

btn_delete = Button(scrollable_frame, text="HAPUS", command=on_delete, 
                   bg="#C0392B", fg="white", font=("Arial", 12, "bold"), 
                   width=25, height=2, relief=FLAT, cursor="hand2")
btn_delete.pack(pady=10)

Label(scrollable_frame, text="© 2025 Kaori Coffee", font=("Arial", 9), 
      fg=SECONDARY_COLOR, bg=BG_COLOR).pack(pady=20)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()