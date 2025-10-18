from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess
import sys
import bcrypt
import os
from encryption import decrypt_data
from session import create_session, is_logged_in, clear_session

def login():
    user = txt_username.get().strip()
    pwd = txt_password.get().strip()

    if not user or not pwd:
        messagebox.showerror("Error", "Username dan password harus diisi!")
        return

    if user == "admin" and pwd == "password":
        create_session('admin', 'admin', 'Administrator', 'Admin', 'HQ')
        messagebox.showinfo("Login Success", "Welcome, Admin!")
        root.destroy()
        subprocess.Popen([sys.executable, 'uimain.py'])
        return

    try:
        conn = sqlite3.connect('pegawai.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, nama_panjang, jabatan, outlet, password 
            FROM pegawai 
            WHERE username = ?
        """, (user,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            employee_id, encrypted_nama, encrypted_jabatan, encrypted_outlet, hashed_password = result
            
            if bcrypt.checkpw(pwd.encode('utf-8'), hashed_password):
                nama = decrypt_data(encrypted_nama)
                jabatan = decrypt_data(encrypted_jabatan)
                outlet = decrypt_data(encrypted_outlet)
                
                create_session(str(employee_id), user, nama, jabatan, outlet)
                
                messagebox.showinfo("Login Success", 
                                  f"Selamat datang, {nama}!\n"
                                  f"Jabatan: {jabatan}\n"
                                  f"Outlet: {outlet}")
                root.destroy()
                subprocess.Popen([sys.executable, 'uimain.py'])
            else:
                messagebox.showerror("Login Failed", "Username atau password salah!")
                txt_password.delete(0, END)
        else:
            messagebox.showerror("Login Failed", "Username atau password salah!")
            txt_password.delete(0, END)
            
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

def open_signup():
    """Buka window signup"""
    subprocess.Popen([sys.executable, 'signup.py'])

if is_logged_in():
    subprocess.Popen([sys.executable, 'uimain.py'])
    sys.exit()

# TEMA WARNA KAORI COFFEE
BG_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#1B5E7E"
SECONDARY_COLOR = "#2A7A9E"
TEXT_COLOR = "#1B5E7E"

root = Tk()
root.title("Kaori Coffee - Login")
root.geometry("400x600")  # Naikkan tinggi untuk tombol signup
root.configure(bg=BG_COLOR)

# Frame utama
main_frame = Frame(root, bg=BG_COLOR)
main_frame.pack(expand=True, fill=BOTH, padx=30, pady=20)

# Logo
try:
    logo_img = Image.open("kaori coffe logo.png")
    logo_img = logo_img.resize((200, 200), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = Label(main_frame, image=logo_photo, bg=BG_COLOR)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
except:
    Label(main_frame, text="KAORI COFFEE", font=("Arial", 20, "bold"), 
          fg=PRIMARY_COLOR, bg=BG_COLOR).pack(pady=10)

# Header
Label(main_frame, text="LOGIN SYSTEM", font=("Arial", 18, "bold"), 
      fg=PRIMARY_COLOR, bg=BG_COLOR).pack(pady=10)

# Username
lbl_username = Label(main_frame, text="Username:", font=("Arial", 11), 
                     fg=TEXT_COLOR, bg=BG_COLOR)
lbl_username.pack(pady=(15, 5))
txt_username = Entry(main_frame, width=30, font=("Arial", 11), 
                     relief=SOLID, bd=2, highlightbackground=PRIMARY_COLOR, 
                     highlightcolor=PRIMARY_COLOR, highlightthickness=1)
txt_username.pack(pady=5, ipady=5)

# Password
lbl_password = Label(main_frame, text="Password:", font=("Arial", 11), 
                     fg=TEXT_COLOR, bg=BG_COLOR)
lbl_password.pack(pady=(10, 5))
txt_password = Entry(main_frame, show="*", width=30, font=("Arial", 11), 
                     relief=SOLID, bd=2, highlightbackground=PRIMARY_COLOR, 
                     highlightcolor=PRIMARY_COLOR, highlightthickness=1)
txt_password.pack(pady=5, ipady=5)

# Show password checkbox
show_password_var = BooleanVar()
def toggle_password():
    if show_password_var.get():
        txt_password.config(show="")
    else:
        txt_password.config(show="*")

chk_show = Checkbutton(main_frame, text="Tampilkan Password", variable=show_password_var, 
                       command=toggle_password, bg=BG_COLOR, fg=TEXT_COLOR, 
                       selectcolor=BG_COLOR, activebackground=BG_COLOR)
chk_show.pack(pady=5)

txt_password.bind('<Return>', lambda event: login())

# Button Login
btn_login = Button(main_frame, text="LOGIN", command=login, 
                   bg=PRIMARY_COLOR, fg="white", font=("Arial", 12, "bold"), 
                   width=20, height=2, relief=FLAT, cursor="hand2")
btn_login.pack(pady=15)

# Separator atau text
Label(main_frame, text="Belum punya akun?", font=("Arial", 9), 
      fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=(5, 5))

# Button Signup - INI YANG DITAMBAHKAN!
btn_signup = Button(main_frame, text="REGISTER PEGAWAI", command=open_signup,
                    bg=SECONDARY_COLOR, fg="white", font=("Arial", 10, "bold"),
                    width=20, height=1, relief=FLAT, cursor="hand2")
btn_signup.pack(pady=5)  # ← INI YANG KURANG!

# Footer
Label(main_frame, text="© 2025 Kaori Coffee", font=("Arial", 9), 
      fg=SECONDARY_COLOR, bg=BG_COLOR).pack(side=BOTTOM, pady=10)

root.mainloop()


