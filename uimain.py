from tkinter import *
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import subprocess
import sys
from main import fill_invitation
import time
from session import get_session, clear_session

# CEK SESSION - WAJIB LOGIN
session = get_session()
if not session:
    messagebox.showerror("Access Denied", "Anda harus login terlebih dahulu!")
    subprocess.Popen([sys.executable, 'login.py'])
    sys.exit()

# Ambil data user dari session
user_id = session['user_id']
user_name = session['nama']
user_jabatan = session['jabatan']
user_outlet = session['outlet']

# TEMA WARNA KAORI COFFEE
BG_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#1B5E7E"
SECONDARY_COLOR = "#2A7A9E"
TEXT_COLOR = "#1B5E7E"
BUTTON_HOVER = "#2A7A9E"

root = Tk()
root.title("Kaori Coffee - Main Application")
root.geometry("600x700")
root.configure(bg=BG_COLOR)

# Frame utama
main_frame = Frame(root, bg=BG_COLOR)
main_frame.pack(expand=True, fill=BOTH, padx=30, pady=20)

# Logo
try:
    logo_img = Image.open("kaori coffe logo.png")
    logo_img = logo_img.resize((120, 120), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = Label(main_frame, image=logo_photo, bg=BG_COLOR)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
except:
    Label(main_frame, text="KAORI COFFEE", font=("Arial", 16, "bold"), 
          fg=PRIMARY_COLOR, bg=BG_COLOR).pack(pady=10)

# Welcome message
lbl_welcome = Label(main_frame, text=f"Selamat Datang, {user_name}!", 
                   font=("Arial", 20, "bold"), fg=PRIMARY_COLOR, bg=BG_COLOR)
lbl_welcome.pack(pady=10)

lbl_info = Label(main_frame, text=f"Jabatan: {user_jabatan} | Outlet: {user_outlet}", 
                font=("Arial", 11), fg=TEXT_COLOR, bg=BG_COLOR)
lbl_info.pack(pady=5)

# Separator
Frame(main_frame, height=2, bg=PRIMARY_COLOR).pack(fill=X, pady=20)

def create_button(parent, text, command, icon=""):
    btn = Button(parent, text=f"{icon} {text}", command=command, 
                bg=PRIMARY_COLOR, fg="white", font=("Arial", 12, "bold"), 
                width=30, height=2, relief=FLAT, cursor="hand2",
                activebackground=BUTTON_HOVER, activeforeground="white")
    btn.pack(pady=10)
    return btn

def profile():
    profile_text = f"""
    PROFILE INFORMATION
    
    ID: {user_id}
    Nama: {user_name}
    Jabatan: {user_jabatan}
    Outlet: {user_outlet}
    """
    messagebox.showinfo("Profile", profile_text)

def pengajuan_cuti():
    cuti_window = Toplevel(root)
    cuti_window.title("Kaori Coffee - Pengajuan Cuti")
    cuti_window.geometry("450x600")
    cuti_window.configure(bg=BG_COLOR)
    
    Label(cuti_window, text="FORM PENGAJUAN CUTI", font=("Arial", 16, "bold"), 
          fg=PRIMARY_COLOR, bg=BG_COLOR).pack(pady=20)
    
    fields = [
        ("Jenis Cuti:", "Cuti Tahunan"),
        ("Tanggal Mulai:", "10 Januari 2025"),
        ("Tanggal Selesai:", "12 Januari 2025"),
        ("Jumlah Hari:", "3"),
        ("Alasan:", "Keperluan keluarga")
    ]
    
    entries = {}
    for label_text, default_val in fields:
        Label(cuti_window, text=label_text, font=("Arial", 11), 
              fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=(10, 5))
        entry = Entry(cuti_window, width=35, font=("Arial", 11), 
                     relief=SOLID, bd=2, highlightbackground=PRIMARY_COLOR)
        entry.insert(0, default_val)
        entry.pack(pady=5, ipady=5)
        entries[label_text] = entry
    
    def submit_cuti():
        data = {
            '[date]': time.strftime("%d %B %Y"),
            '[perihal]': 'Pengajuan Cuti',
            '[Nama_Panjang]': user_name,
            '[nama_panjang]': user_name,
            '[number]': user_id,
            '[cabang]': user_outlet,
            '[Posisi]': user_jabatan,
            '[start_date]': entries["Tanggal Mulai:"].get(),
            '[end_date]': entries["Tanggal Selesai:"].get(),
            '[hari]': entries["Jumlah Hari:"].get(),
            '[subjek]': entries["Jenis Cuti:"].get(),
            '[fill]': 'ttd'
        }
        
        try:
            template_path = 'template.docx'
            output_path = 'output.docx'
            final_path = fill_invitation(template_path, output_path, data)
            messagebox.showinfo("Success", f"Surat cuti berhasil dibuat!\nFile: {final_path}")
            cuti_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat surat: {str(e)}")
    
    Button(cuti_window, text="SUBMIT PENGAJUAN", command=submit_cuti, 
           bg=PRIMARY_COLOR, fg="white", font=("Arial", 12, "bold"), 
           width=25, height=2, relief=FLAT, cursor="hand2").pack(pady=30)

def logout():
    confirm = messagebox.askyesno("Logout", "Apakah Anda yakin ingin logout?")
    if confirm:
        clear_session()
        root.destroy()
        subprocess.Popen([sys.executable, 'login.py'])

# Menu Buttons
create_button(main_frame, "Profile Saya", profile, "👤")
create_button(main_frame, "Pengajuan Cuti", pengajuan_cuti, "📝")
create_button(main_frame, "Logout", logout, "🚪")

# Footer
Label(main_frame, text="© 2025 Kaori Coffee", font=("Arial", 9), 
      fg=SECONDARY_COLOR, bg=BG_COLOR).pack(side=BOTTOM, pady=20)

# Handle window close
def on_closing():
    logout()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
