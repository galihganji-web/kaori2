import sqlite3
import os

def fetch_employee_data(emp_id):
    """Ambil data karyawan dari database berdasarkan ID"""
    db_path = 'pegawai.db'
    
    # Cek apakah database ada
    if not os.path.exists(db_path):
        print("Database tidak ditemukan. Jalankan setup_db.py terlebih dahulu!")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nama_panjang, jabatan, outlet, nomor_hp
            FROM pegawai 
            WHERE id = ?
        """, (emp_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'nama_panjang': row[0],
                'jabatan': row[1],
                'outlet': row[2],
                'nomor_pegawai': row[3]
            }
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def create_database():
    """Buat database dan tabel jika belum ada"""
    conn = sqlite3.connect('pegawai.db')
    cursor = conn.cursor()
    
    # Buat tabel pegawai
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pegawai (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_panjang TEXT NOT NULL,
        jabatan TEXT,
        outlet TEXT,
        username TEXT UNIQUE,
        password TEXT,
        nomor_hp TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Insert contoh data jika belum ada
    cursor.execute("SELECT COUNT(*) FROM pegawai")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO pegawai (nama_panjang, jabatan, outlet, username, password, nomor_hp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('Siti Aminah', 'Manajer Operasional', 'Outlet Jakarta', 'siti', 'pass123', '081234567890'))
        
        cursor.execute("""
            INSERT INTO pegawai (nama_panjang, jabatan, outlet, username, password, nomor_hp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('Budi Santoso', 'Staff Administrasi', 'Outlet Bandung', 'budi', 'pass456', '081987654321'))
    
    conn.commit()
    conn.close()
    print("Database berhasil dibuat dengan data contoh!")

if __name__ == "__main__":
    # Jalankan file ini sekali untuk membuat database
    create_database()
    print("Setup database selesai!")
