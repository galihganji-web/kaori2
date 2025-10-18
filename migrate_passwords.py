import sqlite3
import bcrypt

def migrate_existing_passwords():
    """Convert plain text passwords ke hashed passwords"""
    conn = sqlite3.connect('pegawai.db')
    cursor = conn.cursor()
    
    # Ambil semua user dengan plain password
    cursor.execute("SELECT id, username, password FROM pegawai")
    users = cursor.fetchall()
    
    for user_id, username, password in users:
        # Cek apakah password sudah di-hash (bcrypt hash dimulai dengan $2b$)
        if isinstance(password, bytes) and password.startswith(b'$2b$'):
            print(f"User {username} sudah ter-hash, skip...")
            continue
        
        # Convert string password ke bytes jika perlu
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        # Hash password
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        
        # Update database
        cursor.execute("UPDATE pegawai SET password = ? WHERE id = ?", (hashed, user_id))
        print(f"Password untuk {username} berhasil di-hash!")
    
    conn.commit()
    conn.close()
    print("\n✅ Migrasi password selesai!")

if __name__ == "__main__":
    migrate_existing_passwords()