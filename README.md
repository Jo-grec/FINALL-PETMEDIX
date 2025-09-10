# PetMedix - Veterinary Clinic Management System

A comprehensive veterinary clinic management system built with Python, PySide6, and MariaDB. PetMedix helps veterinary clinics manage their daily operations, from patient records to billing and medical reports.

## System Requirements

### Hardware Requirements
- Processor: Intel Core i3 or equivalent
- RAM: 4GB minimum (8GB recommended)
- Storage: 500MB free space
- Display: 1280x720 minimum resolution

### Software Requirements
- Operating System: Windows 10 or later
- MariaDB Server 10.6 or later
- Python 3.8 or later (for development only)
- Internet connection (for initial setup)

## Installation

### For End Users (Using the Packaged Application)

1. **Download and Extract**
   - Download the latest release ZIP file
   - Right-click the ZIP file and select "Extract All"
   - Choose a location (e.g., `C:\Program Files\PetMedix`)
   - Make sure to remember this location

2. **Install MariaDB Server**
   - Download MariaDB Server from [MariaDB Downloads](https://mariadb.org/download/)
   - Run the installer
   - During installation:
     - Set root password as: `joelmar123` (or change it in the database settings)
     - Keep the default port (3306)
     - Complete the installation

3. **Set Up the Database**
   - Open MariaDB Command Line Client (search in Windows Start menu)
   - Copy and paste these commands one by one:
     ```sql
     CREATE DATABASE petmedix;
     USE petmedix;
     source C:/path/to/your/extracted/folder/data.sql;
     ```
   - Replace `C:/path/to/your/extracted/folder/` with your actual extraction path
   - Wait for the database import to complete

4. **Run the Application**
   - Navigate to your extracted folder
   - Double-click `PetMedix.exe`
   - If Windows shows a security warning, click "More info" then "Run anyway"

### For Developers

1. **Set Up Development Environment**
   - Install Python 3.8 or later from [python.org](https://python.org)
   - Open Command Prompt as Administrator
   - Navigate to your project folder:
     ```bash
     cd path/to/PetMedix
     ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   - You should see `(venv)` at the start of your command prompt

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   - Wait for all packages to install
   - If you see any errors, make sure you have the latest pip:
     ```bash
     python -m pip install --upgrade pip
     ```

4. **Database Setup**
   - Follow the database setup steps from the End Users section
   - For development, you can use different database credentials by editing `modules/database.py`

5. **Run in Development Mode**
   ```bash
   python main.py
   ```

## Building from Source

### Prerequisites
- Python 3.8 or later
- All development dependencies installed
- MariaDB Server installed

### Build Steps

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build the Application**
   ```bash
   pyinstaller petmedix.spec
   ```
   - This process may take several minutes
   - The executable will be in the `dist` folder
   - A `build` folder will also be created (can be deleted)

3. **Test the Build**
   - Copy the `dist/PetMedix` folder to a new location
   - Make sure MariaDB is running
   - Run `PetMedix.exe`
   - Test all major features:
     - Login
     - Add/Edit clients
     - Add/Edit pets
     - Create medical records
     - Generate reports
     - Create invoices

## Database Configuration

### Default Settings
- Host: localhost
- Port: 3306
- User: root
- Password: joelmar123
- Database: petmedix

### Changing Database Settings
1. Open `modules/database.py` in a text editor
2. Find the `__init__` method
3. Modify the connection parameters:
   ```python
   def __init__(self, host="your_host", user="your_user", 
                password="your_password", database="petmedix"):
   ```

### Database Backup
- Regular backups are recommended
- Use MariaDB's backup tools:
  ```bash
  mysqldump -u root -p petmedix > backup.sql
  ```

## Features

### User Management
- Secure login system
- Role-based access (Admin, Veterinarian, Staff)
- Password recovery system
- User profile management

### Client Management
- Add/Edit client information
- Contact details
- Client history
- Multiple pets per client

### Pet Management
- Detailed pet profiles
- Medical history
- Treatment records
- Photo management
- Breed and species tracking

### Medical Records
- Consultation records
- Vaccination tracking
- Surgery records
- Deworming schedules
- Treatment history
- Medical notes

### Billing System
- Generate invoices
- Track payments
- Multiple payment methods
- Payment history
- PDF invoice generation

### Reporting
- Medical reports
- Treatment summaries
- Client reports
- Financial reports
- Export to PDF

## Troubleshooting

### Common Issues

1. **Application Won't Start**
   - Check if MariaDB is running
   - Verify database credentials
   - Ensure all files are in the correct folders

2. **Database Connection Error**
   - Verify MariaDB is running
   - Check database credentials
   - Ensure database exists
   - Check if port 3306 is available

3. **Missing Files**
   - Verify all folders (assets, styles, etc.) are present
   - Check file permissions
   - Re-extract the application if needed

- Built with PySide6 and MariaDB