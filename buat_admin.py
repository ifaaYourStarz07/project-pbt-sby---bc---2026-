"""
buat_admin.py - Script Otomatis Nambahkeun Akun Admin SHA256
Aplikasi Business Center SMKN 13 Bandung
"""

import hashlib
from db import execute_query

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def input_admin_otomatis():
    username_anyar = "admin13"
    password_asli  = "admin123"
    role_user      = "admin" # Sangkan role-na otomatis jadi admin
    
    # Prosés enkripsi password nganggo SHA256 sakumaha dina login_admin.py
    password_hashed = hash_password(password_asli)

    print("🔄 Sedang ngasupkeun akun admin ka database...")
    
    try:
        
        # Kolom disaluyukeun sareng QUERY SELECT dina login_admin.py (username, password, role)
        execute_query(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username_anyar, password_hashed, role_user),
            fetch=False
        )
        
        print("\n🔥 MANTAP! Akun admin dibuat.")
        print("─" * 50)
        print(f" Username : {username_anyar}")
        print(f" Password : {password_asli}")
        print(f" Role     : {role_user}")
        print(f" Hash DB  : {password_hashed}")
        print("─" * 50)
        print("Sok tés !")

    except Exception as e:
        print(f"\n❌ Waduh gagal mang, cek database: {e}")

if __name__ == "__main__":
    input_admin_otomatis()