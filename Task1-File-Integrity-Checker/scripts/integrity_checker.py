import sqlite3
import os
import hashlib
from datetime import datetime

# Logic to calculate the hash (from our previous step)
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

# Logic to create the baseline
def create_baseline(directory, db_connection):
    cursor = db_connection.cursor()
    print(f"[*] Creating baseline for: {directory}")
    
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            file_hash = calculate_sha256(file_path)
            
            if file_hash:
                # Store or update the file hash in the DB
                cursor.execute('''
                    INSERT OR REPLACE INTO file_hashes (file_path, file_hash, last_checked)
                    VALUES (?, ?, ?)
                ''', (file_path, file_hash, datetime.now()))
    
    db_connection.commit()
    print("[+] Baseline created and stored in database.")