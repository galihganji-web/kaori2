import sqlite3

# Buat database SQLite dari schema pegawai.sql
conn = sqlite3.connect('pegawai.db')
cursor = conn.cursor()

# Buat tabel pegawai dengan schema yang diperbaiki
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

# Insert data contoh
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

print("✅ Database pegawai.db berhasil dibuat!")
print("📊 Tabel pegawai dengan 2 data contoh sudah tersedia")
