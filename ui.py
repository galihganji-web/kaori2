from tkinter import *
from tkinter import messagebox
import sqlite3
import os

def login():
    user = txt_username.get()
    pwd = txt_password.get()

    # check hardcoded admin first
    if user == "admin" and pwd == "password":
        messagebox.showinfo("Login Success", "Welcome, admin!")
        root.destroy()
        return

    # check credentials from SQLite database
    sukses = False
    try:
        # Use database path that is writable
        db_path = "pegawai.db"
        if not os.access(db_path, os.W_OK):
            db_path = os.path.join("/tmp", "pegawai.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM pegawai WHERE username=?", (user,))
        result = cursor.fetchone()
        conn.close()
        if result and result[1] == pwd:
            sukses = True
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")
        return

    if sukses:
        messagebox.showinfo("Login Success", "Welcome")
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

root = Tk()
root.title("Login Form")
root.geometry("300x150")
lbl_username = Label(root, text="Username:")
lbl_username.pack(pady=5)
txt_username = Entry(root)
txt_username.pack(pady=5)
lbl_password = Label(root, text="Password:")
lbl_password.pack(pady=5)
txt_password = Entry(root, show="*")
txt_password.pack(pady=5)
btn_login = Button(root, text="Login", command=login)
btn_login.pack(pady=10)
root.mainloop()


