import sqlite3
from encryption import encrypt_data, decrypt_data

def migrate_to_encrypted():
    """Enkripsi data yang sudah ada di database"""
    conn = sqlite3.connect('pegawai.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nama_panjang, jabatan, outlet, nomor_hp FROM pegawai")
    users = cursor.fetchall()
    
    for user_id, nama, jabatan, outlet, nomor in users:
        # Cek apakah sudah terenkripsi (coba dekripsi)
        try:
            if isinstance(nama, bytes):
                decrypt_data(nama)
                print(f"User ID {user_id} sudah terenkripsi, skip...")
                continue
        except:
            pass
        
        # Enkripsi data
        encrypted_nama = encrypt_data(nama) if nama else b""
        encrypted_jabatan = encrypt_data(jabatan) if jabatan else b""
        encrypted_outlet = encrypt_data(outlet) if outlet else b""
        encrypted_nomor = encrypt_data(nomor) if nomor else b""
        
        cursor.execute("""
            UPDATE pegawai 
            SET nama_panjang = ?, jabatan = ?, outlet = ?, nomor_hp = ? 
            WHERE id = ?
        """, (encrypted_nama, encrypted_jabatan, encrypted_outlet, encrypted_nomor, user_id))
        
        print(f"✅ User ID {user_id} berhasil dienkripsi!")
    
    conn.commit()
    conn.close()
    print("\n✅ Migrasi enkripsi selesai!")

if __name__ == "__main__":
    migrate_to_encrypted()