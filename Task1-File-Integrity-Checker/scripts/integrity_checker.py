import hashlib
import sqlite3
import os
from datetime import datetime

# 1. Initialize the Database
def init_db():
    conn = sqlite3.connect('hash.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS save_hash (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            file_hash TEXT,
            last_checked TEXT
        )
    ''')
    conn.commit()
    return conn

# 2. Calculate SHA-256 Fingerprint
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"[!] Could not read {file_path}: {e}")
        return None

# 3. Baseline Mode
def create_baseline(directory, conn):
    cursor = conn.cursor()
    print(f"\n[*] Creating/Updating baseline for: {directory}")
    
    file_count = 0
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.normpath(os.path.join(root, name))
            file_hash = calculate_sha256(file_path)
            
            if file_hash:
                # Using .isoformat() to avoid the DeprecationWarning
                cursor.execute('''
                    INSERT OR REPLACE INTO save_hash (file_path, file_hash, last_checked)
                    VALUES (?, ?, ?)
                ''', (file_path, file_hash, datetime.now().isoformat()))
                file_count += 1
    
    conn.commit()
    print(f"[SUCCESS] Baseline saved for {file_count} files.")

# 4. Monitoring Mode
def monitor_integrity(directory, conn):
    cursor = conn.cursor()
    print(f"\n[*] Monitoring started for: {directory}")
    
    cursor.execute('SELECT file_path, file_hash FROM save_hash')
    stored_data = dict(cursor.fetchall())
    
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.normpath(os.path.join(root, name))
            current_hash = calculate_sha256(file_path)
            
            if file_path in stored_data:
                if current_hash != stored_data[file_path]:
                    print(f"[!] ALERT: File Modified! -> {file_path}")
                del stored_data[file_path]
            else:
                print(f"[+] NEW FILE detected: {file_path}")

    for deleted_file in stored_data:
        print(f"[-] DELETED FILE detected: {deleted_file}")

# 5. Main Execution
if __name__ == "__main__":
    db_conn = init_db()
    
    print("\n=== CODTECH File Integrity Checker ===")
    print("1. Create/Update Baseline (Scan folder and save hashes)")
    print("2. Monitor Integrity (Compare current files to baseline)")
    choice = input("Select an option (1/2): ")

    raw_path = input("Enter the full path of the folder: ")
    target_folder = raw_path.strip().replace('"', '').replace("'", "")
    
    if os.path.isdir(target_folder):
        if choice == '1':
            create_baseline(target_folder, db_conn)
        elif choice == '2':
            monitor_integrity(target_folder, db_conn)
        else:
            print("[!] Invalid choice.")
    else:
        print("[ERROR] Path not found.")
    
    db_conn.close()