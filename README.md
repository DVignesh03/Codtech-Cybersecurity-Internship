# Cybersecurity & Ethical Hacking Internship - Codtech IT Solutions

This repository contains the deliverables for a one-month virtual internship. The projects focus on building functional security tools using Python, emphasizing automation, cryptography, and vulnerability assessment.

## 🛠️ Projects Overview

### 1. File Integrity Checker
- **`Purpose`:** Monitors directory changes to detect unauthorized file modifications.
- **`Tech Stack`:** Python, `hashlib` (SHA-256), `sqlite3`.
- **`Key Feature`:** Uses a local database to store file "baselines" for persistence across scans.

### 2. Web Application Vulnerability Scanner
- **`Purpose`:** Probes web forms for common weaknesses such as SQL Injection (SQLi) and Cross-Site Scripting (XSS).
- **`Tech Stack`:** `requests`, `BeautifulSoup4`.
- **`Key Feature`:** Implements accuracy-focused detection by searching for specific database error signatures.

### 3. Modular Penetration Testing Toolkit
- **`Purpose`:** A unified suite for network reconnaissance and auditing.
- **`Modules`:** * **TCP Port Scanner:** Identifies open services on a target.
    - **`Banner Grabber`:** Discovers service versions for vulnerability research.
    - **`SSH Brute-Forcer`:** Audits credential strength using `paramiko`.
    - **`Subdomain Finder`:** Maps out an organization's attack surface.

### 4. Advanced Encryption Tool
- **`Purpose`:** Secure file encryption and decryption utility.
- **`Tech Stack`:** `cryptography` library, `Tkinter` (GUI).
- **`Key Feature`:** Implements AES-256 in CBC mode with PBKDF2 key derivation (100,000 iterations) for robust protection.

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)

2. Install dependencies:
   ```bash
   pip install -r requirements.txt