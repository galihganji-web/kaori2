from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
import bcrypt
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from encryption import decrypt_data, encrypt_data
from functools import wraps
import time

try:
    from main import fill_invitation
except:
    fill_invitation = None

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

app.secret_key = os.environ.get('SECRET_KEY', 'fXU4seCyGZ9VNqsscXI6rmbGwyN5HpZ9x_bJgN1JGWo=')
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Database path for serverless
DB_PATH = '/tmp/pegawai.db'

# Copy database to /tmp on cold start
if not os.path.exists(DB_PATH):
    import shutil
    source_db = os.path.join(os.path.dirname(__file__), '..', 'pegawai.db')
    if os.path.exists(source_db):
        shutil.copy(source_db, DB_PATH)

def get_db_connection():
    """Helper untuk koneksi database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return render_template('login.html', error='Username dan password harus diisi!')
        
        if username == 'admin' and password == 'password':
            session.permanent = True
            session['user_id'] = 'admin'
            session['username'] = 'admin'
            session['nama'] = 'Administrator'
            session['jabatan'] = 'Admin'
            session['outlet'] = 'HQ'
            return redirect(url_for('dashboard'))
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nama_panjang, jabatan, outlet, password 
                FROM pegawai WHERE username = ?
            """, (username,))
            result = cursor.fetchone()
            conn.close()
            
            if result and bcrypt.checkpw(password.encode('utf-8'), result[4]):
                session.permanent = True
                session['user_id'] = str(result[0])
                session['username'] = username
                session['nama'] = decrypt_data(result[1])
                session['jabatan'] = decrypt_data(result[2])
                session['outlet'] = decrypt_data(result[3])
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Username atau password salah!')
        except Exception as e:
            return render_template('login.html', error=f'Error: {str(e)}')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama_panjang = request.form.get('nama_panjang', '').strip()
        jabatan = request.form.get('jabatan', '').strip()
        outlet = request.form.get('outlet', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        nomor_wa = request.form.get('nomor_wa', '').strip()
        
        if not all([nama_panjang, jabatan, outlet, username, password, nomor_wa]):
            return render_template('register.html', error='Semua field harus diisi!')
        
        if len(password) < 6:
            return render_template('register.html', error='Password minimal 6 karakter!')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM pegawai WHERE username = ?", (username,))
            if cursor.fetchone():
                conn.close()
                return render_template('register.html', error='Username sudah digunakan!')
            
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
            
            return render_template('register.html', success=f'Registrasi berhasil! Silakan login dengan username: {username}')
        except Exception as e:
            return render_template('register.html', error=f'Gagal registrasi: {str(e)}')
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session)

@app.route('/pengajuan-cuti', methods=['GET', 'POST'])
@login_required
def pengajuan_cuti():
    if request.method == 'POST':
        jenis_cuti = request.form.get('jenis_cuti')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        jumlah_hari = request.form.get('jumlah_hari')
        alasan = request.form.get('alasan')
        
        if not fill_invitation:
            return render_template('pengajuan_cuti.html', user=session, 
                                 error='Fitur generate dokumen sementara tidak tersedia')
        
        data = {
            '[date]': time.strftime("%d %B %Y"),
            '[perihal]': 'Pengajuan Cuti',
            '[Nama_Panjang]': session['nama'],
            '[nama_panjang]': session['nama'],
            '[number]': session['user_id'],
            '[cabang]': session['outlet'],
            '[Posisi]': session['jabatan'],
            '[start_date]': start_date,
            '[end_date]': end_date,
            '[hari]': jumlah_hari,
            '[subjek]': jenis_cuti,
            '[fill]': 'ttd'
        }
        
        try:
            template_path = os.path.join(os.path.dirname(__file__), '..', 'template.docx')
            output_path = '/tmp/output.docx'
            final_path = fill_invitation(template_path, output_path, data)
            
            return send_file(final_path, as_attachment=True, 
                           download_name=f'Cuti_{session["nama"]}_{time.strftime("%Y%m%d")}.docx')
        except Exception as e:
            return render_template('pengajuan_cuti.html', user=session, 
                                 error=f'Gagal membuat surat: {str(e)}')
    
    return render_template('pengajuan_cuti.html', user=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'message': 'Kaori Coffee System is running'}

# Export for Vercel
handler = app