# Task 2: Web Application Vulnerability Scanner

#### Description

This is a web application vulnerability scanner. It scans for common vulnerabilities like XSS and SQL injection. It is for security purpose only, and it works in that way only.

### File Structure

 - **`web_scanner.py`**: The Python script for scanning vulnerabilties.
 - **`requirements.txt`**: The text file listing the requirements for the script to run.

### Operation Complexity

This script uses Python modules like requests and BeautifulSoup to find and test forms in a web application. After testing it lists the findings with a final scan report. The script does not perform any active probing. All actions performed by the script are completely passive scanning and safe.

### How To Run

- Navigate to the directory of the script.
- Install the requirements.
- Run the script in Terminal using "python web_scanner.py"