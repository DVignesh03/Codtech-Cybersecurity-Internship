# Task 1: File Integrity Checker

### Description:
This is a File Integrity Checker which has 2 operation modes. 

### File Structure

- **`integrity_checker.py`**: The script.
- **`requirements.txt`**: The file outlining the requirements to run this script.

### Operation Complexity

This script uses Python to perform it's tasks. The script connects to the DB (SQLite3) as soon as the script is executed. Select the mode to access the functions of the script. If the table needed doesn't exist the script automatically creates one.
First mode: Create/Update Baseline - In this mode the script scans a given folder and indexes the files in it into the DB.
Second mode: Monitor Integrity - In this mode the script scans the given folder and checks for changes in the folder. Changes made to the folder will be clearly outlined.

For intentional changes make sure to update the baseline to prevent confusion.

### How To Run

- Navigate to the directory of the script.
- Install the requirements.
- Initialize DB if needed.
- Run the script in Terminal using "Python integrity_checker.py".
