# 📋 Panduan Sistem Automasi Surat Cuti

## 🗄️ Database Structure

Database: `pegawai.db` (SQLite)

### Tabel: pegawai
```sql
id              INTEGER PRIMARY KEY AUTOINCREMENT
nama_panjang    TEXT NOT NULL
jabatan         TEXT
outlet          TEXT
username        TEXT UNIQUE
password        TEXT
nomor_hp        TEXT
created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

## 🚀 Cara Menggunakan

### 1. Setup Database (Jalankan sekali)
```bash
python3 setup_db.py
```

### 2. Registrasi Pegawai Baru
```bash
python3 signup.py
```
- Isi semua field (Nama, Jabatan, Outlet, Username, Password, Nomor WA)
- Klik tombol Submit
- Data akan tersimpan ke database `pegawai.db`

### 3. Generate Surat Cuti
```bash
python3 UI.py
```
- Masukkan Employee ID (contoh: 1, 2, dst)
- Klik "Generate Invitation"
- File surat akan tersimpan dengan format: `invitation_[ID]_[TIMESTAMP].docx`

### 4. Generate Surat Manual (via script)
```bash
python3 main.py
```

## 📂 File Structure

```
AKUMAUCUTI/
├── pegawai.db          # Database SQLite
├── pegawai.sql         # SQL Schema (referensi)
├── setup_db.py         # Setup database awal
├── signup.py           # Form registrasi pegawai
├── login.py            # Form login (jika ada)
├── UI.py               # Interface generate surat
├── main.py             # Fungsi core fill_invitation
├── database.py         # Fungsi query database
├── TEMPLATE.docx       # Template surat
└── output_*.docx       # Hasil generate surat
```

## 🔧 Troubleshooting

### Error: No module named 'tkinter'
```bash
brew install python-tk@3.14
```

### Error: Database tidak ditemukan
```bash
python3 setup_db.py
```

### Cek data di database
```bash
sqlite3 pegawai.db "SELECT * FROM pegawai;"
```

### Hapus semua data pegawai
```bash
sqlite3 pegawai.db "DELETE FROM pegawai;"
```

## 📝 Placeholder yang Tersedia di Template

- `[nama_panjang]` - Nama lengkap pegawai
- `[jabatan]` - Jabatan pegawai
- `[outlet]` - Nama outlet/cabang
- `[start_date]` - Tanggal mulai cuti
- `[end_date]` - Tanggal selesai cuti
- `[hari]` - Jumlah hari cuti
- `[date]` - Tanggal pembuatan surat
- `[fill]` - Placeholder tanda tangan

## 🎯 Fitur

- ✅ Case-insensitive replacement
- ✅ Mempertahankan formatting (bold, italic, warna)
- ✅ Support tabel, header, footer
- ✅ Timestamp otomatis
- ✅ Database integration
- ✅ Form validation
- ✅ Username unique constraint

## 📞 Support

Jika ada masalah, cek error message dan lihat bagian Troubleshooting.
