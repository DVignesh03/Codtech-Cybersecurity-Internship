import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- 1. RECONNAISSANCE: FINDING ENTRY POINTS ---

def get_all_forms(url):
    """Fetches the page and returns all found form tags."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find_all("form")
    except Exception as e:
        print(f"[!] Error accessing {url}: {e}")
        return []

def get_form_details(form):
    """Extracts action, method, and input fields from a form."""
    details = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

# --- 2. DETECTION LOGIC: PROBING FOR WEAKNESSES ---

def submit_form(url, details, value):
    """Submits a form with a specific payload value."""
    target_url = urljoin(url, details["action"])
    data = {}
    for input_tag in details["inputs"]:
        if input_tag["type"] == "text" or input_tag["type"] == "search":
            data[input_tag["name"]] = value
        else:
            data[input_tag["name"]] = "test_value"

    try:
        if details["method"] == "post":
            return requests.post(target_url, data=data, timeout=10)
        else:
            return requests.get(target_url, params=data, timeout=10)
    except Exception as e:
        print(f"[!] Submission error: {e}")
        return None

def check_sql_injection(response_text):
    """Scans response for common database error messages."""
    SQL_ERRORS = [
        "you have an error in your sql syntax;",
        "warning: mysql_fetch_array()",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
        "sqlite3.operationalerror",
        "oracle error",
    ]
    for error in SQL_ERRORS:
        if error in response_text.lower():
            return True, error
    return False, None

# --- 3. MAIN SCANNER ENGINE ---

def run_scanner(url):
    print(f"\n[*] Target: {url}")
    forms = get_all_forms(url)
    print(f"[*] Found {len(forms)} forms. Initializing scan...\n")
    
    findings = []

    for i, form in enumerate(forms, 1):
        details = get_form_details(form)
        print(f"[*] Testing Form #{i} [Action: {details['action']}]")

        # Test 1: SQL Injection
        for payload in ["'", "1' OR '1'='1"]:
            response = submit_form(url, details, payload)
            if response:
                is_vulnerable, error_type = check_sql_injection(response.text)
                if is_vulnerable:
                    msg = f"[!] SQLi detected in Form #{i} via error: {error_type}"
                    findings.append(msg)
                    print(msg)
                    break

        # Test 2: XSS (Reflected)
        xss_payload = "<script>alert('XSS')</script>"
        response = submit_form(url, details, xss_payload)
        if response and xss_payload in response.text:
            msg = f"[!] XSS detected in Form #{i} (Payload reflected in HTML)"
            findings.append(msg)
            print(msg)

    return findings

if __name__ == "__main__":
    print("=== CODTECH Web Vulnerability Scanner ===")
    target_url = input("Enter the URL to scan (include http/https): ").strip()
    
    if target_url:
        results = run_scanner(target_url)
        
        print("\n" + "="*30)
        print("FINAL SCAN REPORT")
        print("="*30)
        if results:
            for report in results:
                print(report)
        else:
            print("No common vulnerabilities detected in the tested forms.")
    else:
        print("[!] No URL provided.")