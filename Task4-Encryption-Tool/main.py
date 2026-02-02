import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# --- CRYPTOGRAPHY LOGIC ---

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def process_file(file_path, password, mode='encrypt'):
    try:
        if mode == 'encrypt':
            salt = os.urandom(16)
            iv = os.urandom(16)
            key = derive_key(password, salt)
            
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Add Padding
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()
            
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            
            with open(file_path + ".enc", 'wb') as f:
                f.write(salt + iv + encrypted_data)
            return True, f"Encrypted: {os.path.basename(file_path)}.enc"

        elif mode == 'decrypt':
            with open(file_path, 'rb') as f:
                salt = f.read(16)
                iv = f.read(16)
                encrypted_data = f.read()
            
            key = derive_key(password, salt)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
            
            # Remove Padding
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()
            
            output_path = file_path.replace(".enc", "")
            if output_path == file_path: output_path += ".dec"
            
            with open(output_path, 'wb') as f:
                f.write(data)
            return True, f"Decrypted: {os.path.basename(output_path)}"

    except Exception as e:
        return False, str(e)

# --- GUI LOGIC ---

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CODTECH Advanced Encryption Tool")
        self.root.geometry("500x250")
        
        # File Selection
        tk.Label(root, text="Select File:").pack(pady=5)
        self.file_entry = tk.Entry(root, width=50)
        self.file_entry.pack(padx=20)
        tk.Button(root, text="Browse", command=self.browse_file).pack(pady=5)
        
        # Password
        tk.Label(root, text="Enter Password:").pack(pady=5)
        self.pass_entry = tk.Entry(root, width=30, show="*")
        self.pass_entry.pack()
        
        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Encrypt File", bg="#ffcccb", command=lambda: self.run('encrypt')).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Decrypt File", bg="#ccffcc", command=lambda: self.run('decrypt')).pack(side=tk.LEFT, padx=10)

    def browse_file(self):
        filename = filedialog.askopenfilename()
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, filename)

    def run(self, mode):
        file = self.file_entry.get()
        password = self.pass_entry.get()
        
        if not file or not password:
            messagebox.showwarning("Input Error", "Please select a file and enter a password.")
            return
            
        success, message = process_file(file, password, mode)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", f"Operation failed: {message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()