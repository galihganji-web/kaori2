import json
import time
import os

SESSION_FILE = 'session.json'
SESSION_TIMEOUT = 3600  # 1 jam dalam detik

def create_session(user_id, username, nama, jabatan, outlet):
    """Buat session setelah login berhasil"""
    session_data = {
        'user_id': user_id,
        'username': username,
        'nama': nama,
        'jabatan': jabatan,
        'outlet': outlet,
        'login_time': time.time(),
        'is_active': True
    }
    
    with open(SESSION_FILE, 'w') as f:
        json.dump(session_data, f)
    
    return session_data

def get_session():
    """Ambil session yang aktif"""
    if not os.path.exists(SESSION_FILE):
        return None
    
    try:
        with open(SESSION_FILE, 'r') as f:
            session = json.load(f)
        
        # Cek apakah session masih aktif
        if not session.get('is_active'):
            return None
        
        # Cek timeout
        login_time = session.get('login_time', 0)
        if time.time() - login_time > SESSION_TIMEOUT:
            clear_session()
            return None
        
        return session
    except:
        return None

def clear_session():
    """Hapus session saat logout"""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def is_logged_in():
    """Cek apakah user sudah login"""
    session = get_session()
    return session is not None