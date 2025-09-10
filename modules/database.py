import mariadb
import hashlib
from datetime import datetime

class Database:
    def __init__(self, host="localhost", user="root", password="", database="petmedix"):
        try:
            self.conn = mariadb.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            print("✅ Database connection established.")
            self.create_tables()
        except mariadb.Error as e:
            print(f"❌ Error connecting to MariaDB: {e}")
            self.conn = None
            self.cursor = None

    def create_tables(self):
        """Create all necessary tables if they don't exist."""
        try:
            # Users Table (No foreign key dependencies)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100),
                email VARCHAR(100) NOT NULL UNIQUE,
                hashed_password VARCHAR(64) NOT NULL,
                role VARCHAR(50) NOT NULL,
                status VARCHAR(20) DEFAULT 'Pending',
                license_number VARCHAR(50),
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Check if license_number column exists in users table
            self.cursor.execute("SHOW COLUMNS FROM users LIKE 'license_number'")
            if not self.cursor.fetchone():
                print("Adding license_number column to users table...")
                self.cursor.execute("ALTER TABLE users ADD COLUMN license_number VARCHAR(50)")
                self.conn.commit()
                print("✅ license_number column added to users table")
                
                # Generate license numbers for existing veterinarians
                self.generate_license_numbers()
            else:
                # Update any old format license numbers
                self.update_old_license_numbers()

            # Check if risk_status column exists in consultations table
            self.cursor.execute("SHOW COLUMNS FROM consultations LIKE 'risk_status'")
            if not self.cursor.fetchone():
                print("Adding risk_status column to consultations table...")
                self.cursor.execute("ALTER TABLE consultations ADD COLUMN risk_status ENUM('Low Risk', 'Medium Risk', 'High Risk') DEFAULT 'Low Risk'")
                self.conn.commit()
                print("✅ risk_status column added to consultations table")

            # Check if control_number column exists in clients table
            self.cursor.execute("SHOW COLUMNS FROM clients LIKE 'control_number'")
            if not self.cursor.fetchone():
                print("Adding control_number column to clients table...")
                self.cursor.execute("ALTER TABLE clients ADD COLUMN control_number VARCHAR(20) UNIQUE")
                self.conn.commit()
                print("✅ control_number column added to clients table")

            # Check if time column exists in appointments table
            self.cursor.execute("SHOW COLUMNS FROM appointments LIKE 'time'")
            if not self.cursor.fetchone():
                print("Adding time column to appointments table...")
                self.cursor.execute("ALTER TABLE appointments ADD COLUMN time TIME NOT NULL AFTER date")
                self.conn.commit()
                print("✅ Time column added to appointments table")

            # Clients Table (No foreign key dependencies)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address VARCHAR(255),
                contact_number VARCHAR(15),
                email VARCHAR(100) UNIQUE,
                control_number VARCHAR(20) UNIQUE
            );
            """)

            # Pets Table (Depends on clients)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                pet_id INT AUTO_INCREMENT PRIMARY KEY,
                client_id INT NOT NULL,
                name VARCHAR(100) NOT NULL,
                gender ENUM('Male', 'Female'),
                species VARCHAR(50),
                breed VARCHAR(50),
                color VARCHAR(50),
                birthdate DATE,
                age INT,
                weight DECIMAL(10,2),
                height DECIMAL(10,2),
                photo_path VARCHAR(255),
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Billing Table (Depends on clients and pets)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS billing (
                billing_id INT AUTO_INCREMENT PRIMARY KEY,
                invoice_no VARCHAR(50),
                client_id INT NOT NULL,
                pet_id INT NOT NULL,
                date_issued DATE NOT NULL,
                subtotal DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                vat DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                total_amount DECIMAL(10, 2) NOT NULL,
                payment_status ENUM('PAID', 'UNPAID', 'PARTIAL') NOT NULL,
                partial_amount DECIMAL(10, 2) DEFAULT 0.00,
                payment_method ENUM('CASH', 'CREDIT CARD', 'GCASH', 'BANK TRANSFER'),
                received_by VARCHAR(100),
                reason VARCHAR(200),
                veterinarian VARCHAR(100),
                notes TEXT,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE,
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE
            );
            """)
            
            # Billing Services Table (Depends on billing)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS billing_services (
                service_id INT AUTO_INCREMENT PRIMARY KEY,
                billing_id INT NOT NULL,
                service_description VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10, 2) NOT NULL,
                line_total DECIMAL(10, 2) NOT NULL,
                service_date DATE,
                FOREIGN KEY (billing_id) REFERENCES billing(billing_id) ON DELETE CASCADE
            );
            """)

            # Clinic Information Table (No foreign key dependencies)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clinic_info (
                clinic_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address VARCHAR(255),
                contact_number VARCHAR(15),
                email VARCHAR(100),
                employees_count INT,
                photo_path VARCHAR(255),
                logo_path VARCHAR(255),
                vet_license VARCHAR(20)
            );
            """)

            # Check if vet_license column exists in clinic_info table
            self.cursor.execute("SHOW COLUMNS FROM clinic_info LIKE 'vet_license'")
            if not self.cursor.fetchone():
                print("Adding vet_license column to clinic_info table...")
                self.cursor.execute("ALTER TABLE clinic_info ADD COLUMN vet_license VARCHAR(20)")
                self.conn.commit()
                print("✅ vet_license column added to clinic_info table")

            # User Profiles Table (Depends on users)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                profile_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(10) NOT NULL,
                contact_number VARCHAR(15),
                address VARCHAR(255),
                gender VARCHAR(20),
                birthdate DATE,
                photo_path VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            """)

            # Security Questions Table (Depends on users)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_questions (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(10) NOT NULL,
                question_one VARCHAR(255) NOT NULL,
                answer_one VARCHAR(255) NOT NULL,
                question_two VARCHAR(255) NOT NULL,
                answer_two VARCHAR(255) NOT NULL,
                question_three VARCHAR(255) NOT NULL,
                answer_three VARCHAR(255) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            """)

            # Password History Table (Depends on users)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_history (
                history_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(10) NOT NULL,
                hashed_password VARCHAR(64) NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            """)

            # Consultations Table (Depends on pets and clients)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                consultation_id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                client_id INT NOT NULL,
                date DATE NOT NULL,
                reason TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                prescribed_treatment TEXT NOT NULL,
                veterinarian VARCHAR(100) NOT NULL,
                risk_status ENUM('Low Risk', 'Medium Risk', 'High Risk') DEFAULT 'Low Risk',
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Deworming Table (Depends on pets and clients)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS deworming (
                deworming_id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                client_id INT NOT NULL,
                date DATE NOT NULL,
                medication TEXT NOT NULL,
                dosage TEXT NOT NULL,
                next_scheduled DATE NOT NULL,
                veterinarian VARCHAR(100) NOT NULL,
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Vaccination Table (Depends on pets and clients)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vaccinations (
                vaccination_id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                client_id INT NOT NULL,
                date DATE NOT NULL,
                vaccine TEXT NOT NULL,
                dosage TEXT NOT NULL,
                next_scheduled DATE NOT NULL,
                veterinarian VARCHAR(100) NOT NULL,
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Surgery Table (Depends on pets and clients)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS surgeries (
                surgery_id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                client_id INT NOT NULL,
                date DATE NOT NULL,
                surgery_type TEXT NOT NULL,
                anesthesia TEXT NOT NULL,
                next_followup DATE NOT NULL,
                veterinarian VARCHAR(100) NOT NULL,
                risk_status VARCHAR(20) DEFAULT 'Low Risk',
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Grooming Table (Depends on pets and clients)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS grooming (
                grooming_id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                client_id INT NOT NULL,
                date DATE NOT NULL,
                services TEXT NOT NULL,
                notes TEXT NOT NULL,
                next_scheduled DATE NOT NULL,
                veterinarian VARCHAR(100) NOT NULL,
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Other Treatments Table (Depends on pets and clients)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS other_treatments (
                treatment_id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                client_id INT NOT NULL,
                date DATE NOT NULL,
                treatment_type TEXT NOT NULL,
                medication TEXT NOT NULL,
                dosage TEXT NOT NULL,
                veterinarian VARCHAR(100) NOT NULL,
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Pet Notes Table (Depends on pets)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pet_notes (
                note_id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                note_type VARCHAR(20) NOT NULL CHECK (note_type IN ('past_illnesses', 'medical_history')),
                notes TEXT,
                last_updated TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY pet_note_type (pet_id, note_type),
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE
            );
            """)

            # Create indexes for pet_notes
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_pet_notes_pet_id ON pet_notes(pet_id);")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_pet_notes_type ON pet_notes(note_type);")

            # Appointments Table (Depends on pets and clients)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                client_id INT NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                status ENUM('Scheduled', 'Completed', 'Cancelled', 'No-Show', 'Rescheduled', 'Urgent') NOT NULL,
                payment_status ENUM('Pending', 'Paid', 'Unpaid') NOT NULL,
                reason TEXT,
                veterinarian VARCHAR(100),
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Ensure the status column exists in users table
            try:
                self.cursor.execute("SHOW COLUMNS FROM users LIKE 'status'")
                if not self.cursor.fetchone():
                    self.cursor.execute("ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'Pending'")
                    print("✅ 'status' column added to users table")
            except mariadb.Error as e:
                print(f"❌ Error checking/adding 'status' column: {e}")

            # Create default admin account if it doesn't exist
            self.cursor.execute("SELECT 1 FROM users WHERE role = 'Admin'")
            if not self.cursor.fetchone():
                admin_id = "2025A0001"
                name = "Admin"
                email = "admin@petmedix.com"
                password = "admin123"
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                
                try:
                    self.cursor.execute("""
                        INSERT INTO users (user_id, name, email, hashed_password, role, status, created_date)
                        VALUES (?, ?, ?, ?, 'Admin', 'Verified', NOW())
                    """, (admin_id, name, email, hashed_password))
                    self.conn.commit()
                    print("✅ Default admin account created")
                except mariadb.Error as e:
                    print(f"❌ Error creating admin account: {e}")
                    # If the error is due to duplicate entry, try to update the existing admin
                    if "Duplicate entry" in str(e):
                        self.cursor.execute("""
                            UPDATE users 
                            SET hashed_password = ?, status = 'Verified'
                            WHERE role = 'Admin'
                        """, (hashed_password,))
                        self.conn.commit()
                        print("✅ Admin account updated")

            self.conn.commit()
            print("✅ Tables created successfully.")
        except mariadb.Error as e:
            print(f"❌ Error creating tables: {e}")

    def _ensure_billing_columns(self):
        """Make sure the billing table has all required columns."""
        try:
            # Check if columns exist and add them if they don't
            self.cursor.execute("SHOW COLUMNS FROM billing LIKE 'invoice_no'")
            if not self.cursor.fetchone():
                self.cursor.execute("ALTER TABLE billing ADD COLUMN invoice_no VARCHAR(50)")
                
            self.cursor.execute("SHOW COLUMNS FROM billing LIKE 'reason'")
            if not self.cursor.fetchone():
                self.cursor.execute("ALTER TABLE billing ADD COLUMN reason TEXT")
                
            self.cursor.execute("SHOW COLUMNS FROM billing LIKE 'veterinarian'")
            if not self.cursor.fetchone():
                self.cursor.execute("ALTER TABLE billing ADD COLUMN veterinarian VARCHAR(100)")
                
            self.conn.commit()
            print("✅ Billing table columns verified.")
        except mariadb.Error as e:
            print(f"❌ Error ensuring billing columns: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed.")

    def generate_user_id(self, role):
        """Generate a new USER_ID based on role (2025R0001 for Receptionist, 2025V0001 for Veterinarian)."""
        year = datetime.now().year
        prefix = f"{year}{'R' if role == 'Receptionist' else 'V'}"
        try:
            self.cursor.execute(
                "SELECT USER_ID FROM users WHERE USER_ID LIKE ? ORDER BY USER_ID DESC LIMIT 1",
                (prefix + '%',)
            )
            last_id = self.cursor.fetchone()
            if last_id:
                last_number = int(last_id[0][-4:])
                next_number = last_number + 1
            else:
                next_number = 1
            return f"{prefix}{str(next_number).zfill(4)}"
        except mariadb.Error as e:
            print(f"❌ Error generating USER_ID: {e}")
            return None

    def create_user(self, name, last_name, email, password, role, status='Pending', license_number=None):
        """Insert a user with a generated USER_ID. Status can be set (default 'Pending')."""
        if not self.cursor:
            print("❌ Database not connected.")
            return None

        user_id = self.generate_user_id(role)
        if not user_id:
            print("❌ Could not generate USER_ID.")
            return None

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute(
                "INSERT INTO users (USER_ID, NAME, LAST_NAME, EMAIL, HASHED_PASSWORD, ROLE, STATUS, LICENSE_NUMBER) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, name, last_name, email, hashed_password, role, status, license_number)
            )
            self.conn.commit()
            print(f"✅ User created with USER_ID: {user_id}")
            return user_id  # Return the generated USER_ID
        except Exception as e:
            print(f"❌ Error inserting user: {e}")
            return None
            
    def authenticate_user(self, identifier, password):
        """Authenticate a user by email or user_id and password."""
        if not self.cursor:
            print("❌ Database connection not established. Cannot authenticate user.")
            return None

        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash the input password
        try:
            # First check if it's an admin login
            self.cursor.execute(
                """
                SELECT user_id, name, last_name, role, status
                FROM users 
                WHERE (email = ? OR user_id = ?) AND hashed_password = ? AND role = 'Admin'
                """,
                (identifier, identifier, hashed_password)
            )
            user = self.cursor.fetchone()
            
            if user:
                return {
                    "user_id": user[0],
                    "name": user[1],
                    "last_name": user[2],
                    "role": user[3],
                    "status": user[4]
                }
            
            # If not admin, check for regular user
            self.cursor.execute(
                """
                SELECT user_id, name, last_name, role, status
                FROM users 
                WHERE (email = ? OR user_id = ?) AND hashed_password = ?
                """,
                (identifier, identifier, hashed_password)
            )
            user = self.cursor.fetchone()
            
            if user:
                return {
                    "user_id": user[0],
                    "name": user[1],
                    "last_name": user[2],
                    "role": user[3],
                    "status": user[4]
                }
            else:
                print(f"❌ No user found with identifier: {identifier}")
                return None
        except Exception as e:
            print(f"❌ Error authenticating user: {e}")
            return None

    def user_exists(self, email):
        """Check if a user already exists by email."""
        if not self.cursor:
            print("Database connection not established. Cannot check user existence.")
            return False

        try:
            self.cursor.execute("SELECT 1 FROM users WHERE EMAIL = ?", (email,))
            return self.cursor.fetchone() is not None
        except mariadb.Error as e:
            print(f"Error checking user existence: {e}")
            return False
        
    def fetch_counts(self):
        """Fetch counts for clients, medical records, and appointments from the database."""
        if not self.cursor:
            print("❌ Database not connected.")
            return 0, 0, 0  # Default counts

        try:
            # Count clients
            self.cursor.execute("SELECT COUNT(*) FROM clients")
            clients_count = self.cursor.fetchone()[0]

            # Count medical records from all treatment tables
            total_medical_records = 0
            
            # Count consultations
            self.cursor.execute("SELECT COUNT(*) FROM consultations")
            total_medical_records += self.cursor.fetchone()[0]
            
            # Count deworming records
            self.cursor.execute("SELECT COUNT(*) FROM deworming")
            total_medical_records += self.cursor.fetchone()[0]
            
            # Count vaccination records
            self.cursor.execute("SELECT COUNT(*) FROM vaccinations")
            total_medical_records += self.cursor.fetchone()[0]
            
            # Count surgery records
            self.cursor.execute("SELECT COUNT(*) FROM surgeries")
            total_medical_records += self.cursor.fetchone()[0]
            
            # Count grooming records
            self.cursor.execute("SELECT COUNT(*) FROM grooming")
            total_medical_records += self.cursor.fetchone()[0]
            
            # Count other treatments records
            self.cursor.execute("SELECT COUNT(*) FROM other_treatments")
            total_medical_records += self.cursor.fetchone()[0]

            # Count appointments
            self.cursor.execute("SELECT COUNT(*) FROM appointments")
            appointments_count = self.cursor.fetchone()[0]

            return clients_count, total_medical_records, appointments_count
        except mariadb.Error as e:
            print(f"❌ Error fetching counts: {e}")
            return 0, 0, 0  # Default counts in case of an error
        
    def save_client(self, name, address, contact_number, email):
        """Save or update a client in the database."""
        if not self.cursor:
            print("❌ Database not connected.")
            return False

        try:
            # Check if the client already exists by email
            self.cursor.execute("SELECT client_id FROM clients WHERE email = ?", (email,))
            result = self.cursor.fetchone()

            # Generate control number based on address and client_id
            if result:
                client_id = result[0]
                control_number = f"CN-{address[:3].upper()}-{client_id:04d}"
                # Update existing client
                self.cursor.execute("""
                    UPDATE clients
                    SET name = ?, address = ?, contact_number = ?, control_number = ?
                    WHERE client_id = ?
                """, (name, address, contact_number, control_number, client_id))
            else:
                # Insert new client
                self.cursor.execute("""
                    INSERT INTO clients (name, address, contact_number, email)
                    VALUES (?, ?, ?, ?)
                """, (name, address, contact_number, email))
                
                # Get the new client_id and update control_number
                client_id = self.cursor.lastrowid
                control_number = f"CN-{address[:3].upper()}-{client_id:04d}"
                self.cursor.execute("""
                    UPDATE clients
                    SET control_number = ?
                    WHERE client_id = ?
                """, (control_number, client_id))

            self.conn.commit()
            print("✅ Client saved successfully.")
            return True
        except mariadb.Error as e:
            print(f"❌ Error saving client: {e}")
            return False

    def get_client_info(self, email):
        """Fetch client information by email."""
        if not self.cursor:
            print("❌ Database not connected.")
            return None

        try:
            self.cursor.execute("""
                SELECT name, control_number, address, contact_number, email
                FROM clients
                WHERE email = ?
            """, (email,))
            return self.cursor.fetchone()
        except mariadb.Error as e:
            print(f"❌ Error fetching client info: {e}")
            return None
            
    def save_appointment(self, pet_id, client_id, date, status, payment_status, reason, veterinarian):
        """Save an appointment to the database."""
        try:
            self.cursor.execute("""
                INSERT INTO appointments (pet_id, client_id, date, status, payment_status, reason, veterinarian)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (pet_id, client_id, date, status, payment_status, reason, veterinarian))
            self.conn.commit()  # Ensure the transaction is committed
            print("✅ Appointment saved successfully.")
        except Exception as e:
            print(f"❌ Error saving appointment: {e}")
            raise
        
    def fetch_appointments(self):
        """Fetch all appointments with pet and client information."""
        try:
            self.cursor.execute("""
                SELECT 
                    DATE_FORMAT(a.date, '%Y-%m-%d') as date,
                    TIME_FORMAT(a.time, '%H:%i:%s') as time,
                    p.name, c.name, a.reason, a.status, 
                    a.payment_status, a.veterinarian
                FROM appointments a
                JOIN pets p ON a.pet_id = p.pet_id
                JOIN clients c ON a.client_id = c.client_id
                ORDER BY a.date DESC, a.time DESC
            """)
            return self.cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error fetching appointments: {e}")
            return []
        
    def save_billing(self, client_id, pet_id, date_issued, total_amount, payment_status, 
                    payment_method, received_by, invoice_no, reason, veterinarian, notes,
                    subtotal=0.00, vat=0.00, partial_amount=0.00):
        """Save billing information to database."""
        try:
            print(f"\n=== Debug: Saving Billing ===")
            print(f"client_id: {client_id}")
            print(f"pet_id: {pet_id}")
            print(f"date_issued: {date_issued}")
            print(f"total_amount: {total_amount}")
            print(f"payment_status: {payment_status}")
            print(f"payment_method: {payment_method}")
            print(f"received_by: {received_by}")
            print(f"invoice_no: {invoice_no}")
            print(f"reason: {reason}")
            print(f"veterinarian: {veterinarian}")
            print(f"notes: {notes}")
            print(f"subtotal: {subtotal}")
            print(f"vat: {vat}")
            print(f"partial_amount: {partial_amount}")

            # Validate required fields
            if not client_id or not pet_id or not date_issued or not total_amount or not payment_status:
                print("❌ Missing required fields")
                return None

            # Check if client_id exists
            self.cursor.execute("SELECT 1 FROM clients WHERE client_id = ?", (client_id,))
            if not self.cursor.fetchone():
                print(f"❌ Client ID {client_id} does not exist")
                return None

            # Check if pet_id exists
            self.cursor.execute("SELECT 1 FROM pets WHERE pet_id = ?", (pet_id,))
            if not self.cursor.fetchone():
                print(f"❌ Pet ID {pet_id} does not exist")
                return None

            # Print the SQL query for debugging
            query = """
                INSERT INTO billing (
                    client_id, pet_id, date_issued, total_amount, payment_status, 
                    payment_method, received_by, invoice_no, reason, veterinarian, notes,
                    subtotal, vat, partial_amount
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            print(f"\nExecuting query:\n{query}")
            print(f"With values: {client_id}, {pet_id}, {date_issued}, {total_amount}, {payment_status}, {payment_method}, {received_by}, {invoice_no}, {reason}, {veterinarian}, {notes}, {subtotal}, {vat}, {partial_amount}")

            # Start transaction
            print("\nStarting transaction...")
            self.conn.begin()

            try:
                self.cursor.execute(query, (
                    client_id, pet_id, date_issued, total_amount, payment_status,
                    payment_method, received_by, invoice_no, reason, veterinarian, notes,
                    subtotal, vat, partial_amount
                ))
                
                # Get the inserted ID
                billing_id = self.cursor.lastrowid
                print(f"\nInserted billing_id: {billing_id}")
                
                # Verify the record was actually inserted
                self.cursor.execute("SELECT * FROM billing WHERE billing_id = ?", (billing_id,))
                inserted_record = self.cursor.fetchone()
                if inserted_record:
                    print(f"✅ Verified record in database: {inserted_record}")
                else:
                    print("❌ Record not found in database after insert!")
                
                # Commit the transaction
                print("\nCommitting transaction...")
                self.conn.commit()
                print("✅ Transaction committed successfully")
                
                print(f"✅ Billing saved successfully with ID: {billing_id}")
                return billing_id
                
            except Exception as e:
                print(f"❌ Error during transaction: {e}")
                print("Rolling back transaction...")
                self.conn.rollback()
                raise e
                
        except Exception as e:
            print(f"❌ Database error saving billing: {e}")
            import traceback
            traceback.print_exc()
            return None
        
    def generate_invoice_no(self):
        """Generate a unique invoice number like INV-2025-0001."""
        year = datetime.now().year
        prefix = f"INV-{year}"
        try:
            self.cursor.execute(
                "SELECT invoice_no FROM billing WHERE invoice_no LIKE ? ORDER BY invoice_no DESC LIMIT 1",
                (f"{prefix}-%",)
            )
            last_invoice = self.cursor.fetchone()
            if last_invoice:
                last_number = int(last_invoice[0].split('-')[-1])
                next_number = last_number + 1
            else:
                next_number = 1
            return f"{prefix}-{str(next_number).zfill(4)}"
        except Exception as e:
            print(f"❌ Error generating invoice number: {e}")
            return f"{prefix}-0001"

    def fetch_billing_data(self):
        """Fetch all billing data to display in the table."""
        if not self.cursor:
            print("❌ Database not connected.")
            return []

        try:
            self.cursor.execute("""
                SELECT b.billing_id, b.invoice_no, b.date_issued, c.name as client_name, 
                    p.name as pet_name, b.total_amount, b.payment_method, b.payment_status
                FROM billing b
                JOIN clients c ON b.client_id = c.client_id
                JOIN pets p ON b.pet_id = p.pet_id
                ORDER BY b.invoice_no DESC
            """)
            return self.cursor.fetchall()
        except mariadb.Error as e:
            print(f"❌ Error fetching billing data: {e}")
            return []

    def delete_invoice(self, billing_id):
        """Delete an invoice and its associated services from the database."""
        if not self.cursor:
            print("❌ Database not connected.")
            return False

        try:
            # First delete associated services due to foreign key constraint
            self.cursor.execute("DELETE FROM billing_services WHERE billing_id = ?", (billing_id,))
            
            # Then delete the invoice
            self.cursor.execute("DELETE FROM billing WHERE billing_id = ?", (billing_id,))
            
            self.conn.commit()
            print(f"✅ Invoice {billing_id} deleted successfully.")
            return True
        except mariadb.Error as e:
            print(f"❌ Error deleting invoice: {e}")
            return False

    def get_client_id_by_name(self, client_name):
        """Get client ID by name."""
        if not self.cursor:
            print("❌ Database not connected.")
            return None

        try:
            self.cursor.execute("SELECT client_id FROM clients WHERE name = ?", (client_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except mariadb.Error as e:
            print(f"❌ Error getting client ID: {e}")
            return None

    def get_pet_id_by_name_and_client(self, pet_name, client_id):
        """Get pet ID by name and client ID."""
        if not self.cursor:
            print("❌ Database not connected.")
            return None

        try:
            self.cursor.execute("SELECT pet_id FROM pets WHERE name = ? AND client_id = ?", 
                            (pet_name, client_id))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except mariadb.Error as e:
            print(f"❌ Error getting pet ID: {e}")
            return None
        
        
    def save_user_profile(self, user_id, contact_number, address, gender, birthdate, photo_path=None):
        """Save or update a user profile in the database."""
        if not self.cursor:
            print("❌ Database not connected.")
            return False

        try:
            # Check if profile already exists
            self.cursor.execute("SELECT profile_id FROM user_profiles WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()

            if result:
                # Update existing profile
                if photo_path:
                    self.cursor.execute("""
                        UPDATE user_profiles
                        SET contact_number = ?, address = ?, gender = ?, birthdate = ?, photo_path = ?
                        WHERE user_id = ?
                    """, (contact_number, address, gender, birthdate, photo_path, user_id))
                else:
                    self.cursor.execute("""
                        UPDATE user_profiles
                        SET contact_number = ?, address = ?, gender = ?, birthdate = ?
                        WHERE user_id = ?
                    """, (contact_number, address, gender, birthdate, user_id))
            else:
                # Insert new profile
                self.cursor.execute("""
                    INSERT INTO user_profiles (user_id, contact_number, address, gender, birthdate, photo_path)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, contact_number, address, gender, birthdate, photo_path))

            self.conn.commit()
            print("✅ User profile saved successfully.")
            return True
        except mariadb.Error as e:
            print(f"❌ Error saving user profile: {e}")
            return False

    def save_security_questions(self, user_id, question_one, answer_one, question_two, answer_two, question_three, answer_three):
        """Save security questions and answers for a user."""
        if not self.cursor:
            print("❌ Database not connected.")
            return False

        try:
            # Hash the answers for security
            hashed_answer_one = hashlib.sha256(answer_one.lower().strip().encode()).hexdigest()
            hashed_answer_two = hashlib.sha256(answer_two.lower().strip().encode()).hexdigest()
            hashed_answer_three = hashlib.sha256(answer_three.lower().strip().encode()).hexdigest()

            self.cursor.execute("""
                INSERT INTO security_questions 
                (user_id, question_one, answer_one, question_two, answer_two, question_three, answer_three)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, question_one, hashed_answer_one, question_two, hashed_answer_two, question_three, hashed_answer_three))
            
            self.conn.commit()
            print("✅ Security questions saved successfully.")
            return True
        except mariadb.Error as e:
            print(f"❌ Error saving security questions: {e}")
            return False

    def verify_security_answers(self, user_id, answer_one, answer_two, answer_three):
        """Verify security answers for password reset."""
        if not self.cursor:
            print("❌ Database not connected.")
            return False

        try:
            # Hash the provided answers
            hashed_answer_one = hashlib.sha256(answer_one.lower().strip().encode()).hexdigest()
            hashed_answer_two = hashlib.sha256(answer_two.lower().strip().encode()).hexdigest()
            hashed_answer_three = hashlib.sha256(answer_three.lower().strip().encode()).hexdigest()

            self.cursor.execute("""
                SELECT 1 FROM security_questions 
                WHERE user_id = ? 
                AND answer_one = ? 
                AND answer_two = ? 
                AND answer_three = ?
            """, (user_id, hashed_answer_one, hashed_answer_two, hashed_answer_three))
            
            return self.cursor.fetchone() is not None
        except mariadb.Error as e:
            print(f"❌ Error verifying security answers: {e}")
            return False

    def save_clinic_info(self, name, address, contact_number, email, employees_count, logo_path=None, vet_license=None):
        try:
            self.cursor.execute("SELECT clinic_id FROM clinic_info LIMIT 1")
            existing = self.cursor.fetchone()

            if existing:
                if logo_path:
                    self.cursor.execute("""
                        UPDATE clinic_info
                        SET name = ?, address = ?, contact_number = ?, email = ?, employees_count = ?, logo_path = ?, vet_license = ?
                        WHERE clinic_id = ?
                    """, (name, address, contact_number, email, employees_count, logo_path, vet_license, existing[0]))
                else:
                    self.cursor.execute("""
                        UPDATE clinic_info
                        SET name = ?, address = ?, contact_number = ?, email = ?, employees_count = ?, vet_license = ?
                        WHERE clinic_id = ?
                    """, (name, address, contact_number, email, employees_count, vet_license, existing[0]))
            else:
                self.cursor.execute("""
                    INSERT INTO clinic_info (name, address, contact_number, email, employees_count, logo_path, vet_license)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name, address, contact_number, email, employees_count, logo_path, vet_license))

            self.conn.commit()
            print("✅ Clinic info saved.")
            return True
        except Exception as e:
            print(f"❌ Error saving clinic info: {e}")
            return False
        
    def get_clinic_info(self):
        """Return the clinic information as a dictionary."""
        try:
            self.cursor.execute("SELECT name, address, contact_number, email FROM clinic_info LIMIT 1")
            row = self.cursor.fetchone()
            if row:
                return {
                    "name": row[0],
                    "address": row[1],
                    "contact_number": row[2],
                    "email": row[3]
                }
        except Exception as e:
            print(f"❌ Error fetching clinic info: {e}")
        return None

    def save_medical_record(self, pet_id, client_id, date, type, reason, diagnosis, prescribed_treatment, veterinarian, risk_status=None):
        """Save a medical record to the appropriate table based on type."""
        try:
            print(f"\n=== Debug: Saving {type} Record ===")
            print(f"Pet ID: {pet_id}")
            print(f"Client ID: {client_id}")
            print(f"Date: {date}")
            print(f"Type: {type}")
            print(f"Reason: {reason}")
            print(f"Diagnosis: {diagnosis}")
            print(f"Prescribed: {prescribed_treatment}")
            print(f"Veterinarian: {veterinarian}")
            if type == "Consultation":
                print(f"Risk Status: {risk_status}")

            # Convert empty strings to None for date fields
            if not date or date.strip() == "":
                date = datetime.now().strftime("%Y-%m-%d")
            if not prescribed_treatment or prescribed_treatment.strip() == "":
                prescribed_treatment = datetime.now().strftime("%Y-%m-%d")

            if type == "Consultation":
                self.cursor.execute("""
                    INSERT INTO consultations (
                        pet_id, client_id, date, reason, diagnosis, 
                        prescribed_treatment, veterinarian, risk_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (pet_id, client_id, date, reason, diagnosis, prescribed_treatment, veterinarian, risk_status))
            
            elif type == "Deworming":
                self.cursor.execute("""
                    INSERT INTO deworming (
                        pet_id, client_id, date, medication, dosage, 
                        next_scheduled, veterinarian
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (pet_id, client_id, date, reason, diagnosis, prescribed_treatment, veterinarian))
            
            elif type == "Vaccination":
                self.cursor.execute("""
                    INSERT INTO vaccinations (
                        pet_id, client_id, date, vaccine, dosage, 
                        next_scheduled, veterinarian
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (pet_id, client_id, date, reason, diagnosis, prescribed_treatment, veterinarian))
            
            elif type == "Surgery":
                print("\n=== Debug: Inserting into surgeries table ===")
                try:
                    self.cursor.execute("""
                        INSERT INTO surgeries (
                            pet_id, client_id, date, surgery_type, anesthesia, 
                            next_followup, veterinarian, risk_status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (pet_id, client_id, date, reason, diagnosis, prescribed_treatment, veterinarian, risk_status))
                    print("✅ Surgery record inserted successfully")
                except Exception as e:
                    print(f"❌ Error inserting surgery record: {e}")
                    raise e
            
            elif type == "Grooming":
                self.cursor.execute("""
                    INSERT INTO grooming (
                        pet_id, client_id, date, services, notes, 
                        next_scheduled, veterinarian
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (pet_id, client_id, date, reason, diagnosis, prescribed_treatment, veterinarian))
            
            elif type == "Other Treatments":
                print("\n=== Debug: Saving Other Treatments Record ===")
                print(f"Inserting into other_treatments table:")
                print(f"pet_id: {pet_id}")
                print(f"client_id: {client_id}")
                print(f"date: {date}")
                print(f"treatment_type: {reason}")
                print(f"medication: {diagnosis}")
                print(f"dosage: {prescribed_treatment}")
                print(f"veterinarian: {veterinarian}")
                self.cursor.execute("""
                    INSERT INTO other_treatments (
                        pet_id, client_id, date, treatment_type, medication, 
                        dosage, veterinarian
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (pet_id, client_id, date, reason, diagnosis, prescribed_treatment, veterinarian))
                print("✅ Other Treatments record inserted successfully")

            self.conn.commit()
            print("✅ Medical record saved successfully.")
            return True
        except Exception as e:
            print(f"❌ Error saving medical record: {e}")
            return False

    def fetch_medical_records(self, record_type=None):
        """Fetch medical records from the appropriate table based on type."""
        try:
            if record_type == "Consultation":
                self.cursor.execute("""
                    SELECT 
                        DATE_FORMAT(c.date, '%Y-%m-%d') as date,
                        'Consultation' as type,
                        p.name AS pet_name,
                        cl.name AS client_name,
                        c.reason,
                        c.diagnosis,
                        c.prescribed_treatment,
                        c.veterinarian,
                        c.risk_status
                    FROM consultations c
                    JOIN pets p ON c.pet_id = p.pet_id
                    JOIN clients cl ON c.client_id = cl.client_id
                    ORDER BY c.date DESC
                """)
            elif record_type == "Deworming":
                self.cursor.execute("""
                    SELECT 
                        DATE_FORMAT(d.date, '%Y-%m-%d') as date,
                        'Deworming' as type,
                        p.name AS pet_name,
                        cl.name AS client_name,
                        d.medication as reason,
                        d.dosage as diagnosis,
                        d.next_scheduled as prescribed_treatment,
                        d.veterinarian
                    FROM deworming d
                    JOIN pets p ON d.pet_id = p.pet_id
                    JOIN clients cl ON d.client_id = cl.client_id
                    ORDER BY d.date DESC
                """)
            elif record_type == "Vaccination":
                self.cursor.execute("""
                    SELECT 
                        DATE_FORMAT(v.date, '%Y-%m-%d') as date,
                        'Vaccination' as type,
                        p.name AS pet_name,
                        cl.name AS client_name,
                        v.vaccine as reason,
                        v.dosage as diagnosis,
                        v.next_scheduled as prescribed_treatment,
                        v.veterinarian
                    FROM vaccinations v
                    JOIN pets p ON v.pet_id = p.pet_id
                    JOIN clients cl ON v.client_id = cl.client_id
                    ORDER BY v.date DESC
                """)
            elif record_type == "Surgery":
                self.cursor.execute("""
                    SELECT 
                        DATE_FORMAT(s.date, '%Y-%m-%d') as date,
                        'Surgery' as type,
                        p.name AS pet_name,
                        cl.name AS client_name,
                        s.surgery_type as reason,
                        s.anesthesia as diagnosis,
                        s.next_followup as prescribed_treatment,
                        s.veterinarian,
                        s.risk_status
                    FROM surgeries s
                    JOIN pets p ON s.pet_id = p.pet_id
                    JOIN clients cl ON s.client_id = cl.client_id
                    ORDER BY s.date DESC
                """)
            elif record_type == "Grooming":
                self.cursor.execute("""
                    SELECT 
                        DATE_FORMAT(g.date, '%Y-%m-%d') as date,
                        'Grooming' as type,
                        p.name AS pet_name,
                        cl.name AS client_name,
                        g.services as reason,
                        g.notes as diagnosis,
                        g.next_scheduled as prescribed_treatment,
                        g.veterinarian
                    FROM grooming g
                    JOIN pets p ON g.pet_id = p.pet_id
                    JOIN clients cl ON g.client_id = cl.client_id
                    ORDER BY g.date DESC
                """)
            elif record_type == "Other Treatments":
                self.cursor.execute("""
                    SELECT 
                        DATE_FORMAT(ot.date, '%Y-%m-%d') as date,
                        'Other Treatments' as type,
                        p.name AS pet_name,
                        cl.name AS client_name,
                        ot.treatment_type as reason,
                        ot.medication as diagnosis,
                        ot.dosage as prescribed_treatment,
                        ot.veterinarian
                    FROM other_treatments ot
                    JOIN pets p ON ot.pet_id = p.pet_id
                    JOIN clients cl ON ot.client_id = cl.client_id
                    ORDER BY ot.date DESC
                """)
            
            records = self.cursor.fetchall()
            print(f"Fetched {len(records)} records from database")
            return records
        except Exception as e:
            print(f"❌ Error fetching medical records: {e}")
            return []

    def check_password_history(self, user_id, new_password):
        """Check if the new password has been used before."""
        if not self.cursor:
            print("❌ Database not connected.")
            return False

        try:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            
            # Check current password
            self.cursor.execute("""
                SELECT 1 FROM users 
                WHERE user_id = ? AND hashed_password = ?
            """, (user_id, hashed_password))
            
            if self.cursor.fetchone():
                return True  # Password is the same as current password
            
            # Check password history (last 3 passwords)
            self.cursor.execute("""
                SELECT 1 FROM password_history 
                WHERE user_id = ? AND hashed_password = ?
                ORDER BY created_date DESC LIMIT 3
            """, (user_id, hashed_password))
            
            return self.cursor.fetchone() is not None
        except mariadb.Error as e:
            print(f"❌ Error checking password history: {e}")
            return False

    def add_to_password_history(self, user_id, hashed_password):
        """Add a password to the history."""
        if not self.cursor:
            print("❌ Database not connected.")
            return False

        try:
            self.cursor.execute("""
                INSERT INTO password_history (user_id, hashed_password)
                VALUES (?, ?)
            """, (user_id, hashed_password))
            self.conn.commit()
            return True
        except mariadb.Error as e:
            print(f"❌ Error adding to password history: {e}")
            return False

    def update_password(self, user_id, new_password):
        """Update user password and add to history."""
        if not self.cursor:
            print("❌ Database not connected.")
            return False

        try:
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            
            # Get current password before updating
            self.cursor.execute("""
                SELECT hashed_password FROM users 
                WHERE user_id = ?
            """, (user_id,))
            current_password = self.cursor.fetchone()
            
            if current_password:
                # Add current password to history
                self.add_to_password_history(user_id, current_password[0])
            
            # Update password
            self.cursor.execute("""
                UPDATE users 
                SET hashed_password = ? 
                WHERE user_id = ?
            """, (hashed_password, user_id))
            
            self.conn.commit()
            return True
        except mariadb.Error as e:
            print(f"❌ Error updating password: {e}")
            return False

    def migrate_medical_records(self):
        """Migrate records from medical_records table to their respective treatment tables."""
        try:
            print("\n=== Starting Medical Records Migration ===")
            
            # Get all records from medical_records
            self.cursor.execute("""
                SELECT pet_id, client_id, date, type, reason, diagnosis, 
                       prescribed_treatment, veterinarian
                FROM medical_records
            """)
            records = self.cursor.fetchall()
            
            print(f"Found {len(records)} records to migrate")
            
            # Migrate each record to its respective table
            for record in records:
                pet_id, client_id, date, type, reason, diagnosis, prescribed, veterinarian = record
                
                try:
                    if type == "Consultation":
                        self.cursor.execute("""
                            INSERT INTO consultations (
                                pet_id, client_id, date, reason, diagnosis, 
                                prescribed_treatment, veterinarian
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (pet_id, client_id, date, reason, diagnosis, prescribed, veterinarian))
                    
                    elif type == "Deworming":
                        self.cursor.execute("""
                            INSERT INTO deworming (
                                pet_id, client_id, date, medication, dosage, 
                                next_scheduled, veterinarian
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (pet_id, client_id, date, reason, diagnosis, prescribed, veterinarian))
                    
                    elif type == "Vaccination":
                        self.cursor.execute("""
                            INSERT INTO vaccinations (
                                pet_id, client_id, date, vaccine, dosage, 
                                next_scheduled, veterinarian
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (pet_id, client_id, date, reason, diagnosis, prescribed, veterinarian))
                    
                    elif type == "Surgery":
                        self.cursor.execute("""
                            INSERT INTO surgeries (
                                pet_id, client_id, date, surgery_type, anesthesia, 
                                next_followup, veterinarian
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (pet_id, client_id, date, reason, diagnosis, prescribed, veterinarian))
                    
                    elif type == "Grooming":
                        self.cursor.execute("""
                            INSERT INTO grooming (
                                pet_id, client_id, date, services, notes, 
                                next_scheduled, veterinarian
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (pet_id, client_id, date, reason, diagnosis, prescribed, veterinarian))
                    
                    elif type == "Other Treatments":
                        self.cursor.execute("""
                            INSERT INTO other_treatments (
                                pet_id, client_id, date, treatment_type, medication, 
                                dosage, veterinarian
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (pet_id, client_id, date, reason, diagnosis, prescribed, veterinarian))
                    
                    self.conn.commit()
                    print(f"✅ Migrated record: {type} for pet_id {pet_id}")
                    
                except Exception as e:
                    print(f"❌ Error migrating record: {e}")
                    self.conn.rollback()
            
            # Drop the medical_records table
            self.cursor.execute("DROP TABLE IF EXISTS medical_records")
            self.conn.commit()
            print("✅ Dropped medical_records table")
            
            print("=== Migration Complete ===")
            return True
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            return False

    def has_security_questions(self, user_id):
        """Check if a user has already set up security questions."""
        if not self.cursor:
            print("❌ Database not connected.")
            return False

        try:
            self.cursor.execute("""
                SELECT 1 FROM security_questions 
                WHERE user_id = ?
            """, (user_id,))
            
            return self.cursor.fetchone() is not None
        except mariadb.Error as e:
            print(f"❌ Error checking security questions: {e}")
            return False

    def fetch_vet_appointments(self, veterinarian, filter_type='all'):
        """Fetch appointments for a specific veterinarian with filtering options."""
        try:
            base_query = """
                SELECT a.date, p.name AS pet_name, c.name AS client_name, 
                       a.reason, a.status, a.payment_status
                FROM appointments a
                JOIN pets p ON a.pet_id = p.pet_id
                JOIN clients c ON a.client_id = c.client_id
                WHERE a.veterinarian = ?
            """
            
            if filter_type == 'today':
                base_query += " AND DATE(a.date) = CURDATE()"
            elif filter_type == 'upcoming':
                base_query += " AND DATE(a.date) >= CURDATE()"
            
            base_query += " ORDER BY a.date ASC"
            
            self.cursor.execute(base_query, (veterinarian,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching vet appointments: {e}")
            return []

    def fetch_unpaid_reports(self, filter_type='all'):
        """Fetch reports that haven't been billed yet."""
        try:
            base_query = """
                SELECT 
                    COALESCE(c.date, d.date, v.date, s.date, g.date, o.date) as treatment_date,
                    p.name AS pet_name,
                    cl.name AS client_name,
                    CASE
                        WHEN c.consultation_id IS NOT NULL THEN 'Consultation'
                        WHEN d.deworming_id IS NOT NULL THEN 'Deworming'
                        WHEN v.vaccination_id IS NOT NULL THEN 'Vaccination'
                        WHEN s.surgery_id IS NOT NULL THEN 'Surgery'
                        WHEN g.grooming_id IS NOT NULL THEN 'Grooming'
                        WHEN o.treatment_id IS NOT NULL THEN 'Other Treatment'
                    END as treatment_type,
                    COALESCE(c.veterinarian, d.veterinarian, v.veterinarian, s.veterinarian, g.veterinarian, o.veterinarian) as veterinarian
                FROM pets p
                JOIN clients cl ON p.client_id = cl.client_id
                LEFT JOIN consultations c ON p.pet_id = c.pet_id
                LEFT JOIN deworming d ON p.pet_id = d.pet_id
                LEFT JOIN vaccinations v ON p.pet_id = v.pet_id
                LEFT JOIN surgeries s ON p.pet_id = s.pet_id
                LEFT JOIN grooming g ON p.pet_id = g.pet_id
                LEFT JOIN other_treatments o ON p.pet_id = o.pet_id
                LEFT JOIN billing b ON (
                    p.pet_id = b.pet_id AND 
                    (
                        DATE(c.date) = b.date_issued OR
                        DATE(d.date) = b.date_issued OR
                        DATE(v.date) = b.date_issued OR
                        DATE(s.date) = b.date_issued OR
                        DATE(g.date) = b.date_issued OR
                        DATE(o.date) = b.date_issued
                    )
                )
                WHERE b.billing_id IS NULL
            """
            
            if filter_type == 'today':
                base_query += " AND DATE(COALESCE(c.date, d.date, v.date, s.date, g.date, o.date)) = CURDATE()"
            elif filter_type == 'upcoming':
                base_query += " AND DATE(COALESCE(c.date, d.date, v.date, s.date, g.date, o.date)) >= CURDATE()"
            
            base_query += " ORDER BY treatment_date DESC"
            
            self.cursor.execute(base_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching unpaid reports: {e}")
            return []

    def fetch_recent_reports(self, filter_type='all'):
        """Fetch recent reports from all treatment tables."""
        try:
            base_query = """
                SELECT 
                    COALESCE(c.date, d.date, v.date, s.date, g.date, o.date) as treatment_date,
                    p.name AS pet_name,
                    cl.name AS client_name,
                    CASE
                        WHEN c.consultation_id IS NOT NULL THEN 'Consultation'
                        WHEN d.deworming_id IS NOT NULL THEN 'Deworming'
                        WHEN v.vaccination_id IS NOT NULL THEN 'Vaccination'
                        WHEN s.surgery_id IS NOT NULL THEN 'Surgery'
                        WHEN g.grooming_id IS NOT NULL THEN 'Grooming'
                        WHEN o.treatment_id IS NOT NULL THEN 'Other Treatment'
                    END as treatment_type,
                    COALESCE(c.veterinarian, d.veterinarian, v.veterinarian, s.veterinarian, g.veterinarian, o.veterinarian) as veterinarian
                FROM pets p
                JOIN clients cl ON p.client_id = cl.client_id
                LEFT JOIN consultations c ON p.pet_id = c.pet_id
                LEFT JOIN deworming d ON p.pet_id = d.pet_id
                LEFT JOIN vaccinations v ON p.pet_id = v.pet_id
                LEFT JOIN surgeries s ON p.pet_id = s.pet_id
                LEFT JOIN grooming g ON p.pet_id = g.pet_id
                LEFT JOIN other_treatments o ON p.pet_id = o.pet_id
                WHERE COALESCE(c.date, d.date, v.date, s.date, g.date, o.date) IS NOT NULL
            """
            
            if filter_type == 'today':
                base_query += " AND DATE(COALESCE(c.date, d.date, v.date, s.date, g.date, o.date)) = CURDATE()"
            elif filter_type == 'upcoming':
                base_query += " AND DATE(COALESCE(c.date, d.date, v.date, s.date, g.date, o.date)) >= CURDATE()"
            
            base_query += " ORDER BY treatment_date DESC LIMIT 50"  # Show only the 50 most recent reports
            
            self.cursor.execute(base_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching recent reports: {e}")
            return []

    def fetch_recent_reports_summary(self, user_role=None):
        """Fetch recent reports with only consultation date, pet name, owner name, and veterinarian."""
        try:
            print("\n=== Debug: Starting fetch_recent_reports_summary ===")
            # Union query to combine all treatment types
            query = """
                SELECT * FROM (
                    SELECT date, 'Consultation' as type, p.name as pet_name, cl.name as client_name, 
                           CASE 
                               WHEN veterinarian LIKE 'Dr. %' THEN veterinarian
                               ELSE CONCAT('Dr. ', veterinarian)
                           END as veterinarian
                    FROM consultations c
                    JOIN pets p ON c.pet_id = p.pet_id
                    JOIN clients cl ON c.client_id = cl.client_id
                    UNION ALL
                    SELECT date, 'Deworming' as type, p.name as pet_name, cl.name as client_name, 
                           CASE 
                               WHEN veterinarian LIKE 'Dr. %' THEN veterinarian
                               ELSE CONCAT('Dr. ', veterinarian)
                           END as veterinarian
                    FROM deworming d
                    JOIN pets p ON d.pet_id = p.pet_id
                    JOIN clients cl ON d.client_id = cl.client_id
                    UNION ALL
                    SELECT date, 'Vaccination' as type, p.name as pet_name, cl.name as client_name, 
                           CASE 
                               WHEN veterinarian LIKE 'Dr. %' THEN veterinarian
                               ELSE CONCAT('Dr. ', veterinarian)
                           END as veterinarian
                    FROM vaccinations v
                    JOIN pets p ON v.pet_id = p.pet_id
                    JOIN clients cl ON v.client_id = cl.client_id
                    UNION ALL
                    SELECT date, 'Surgery' as type, p.name as pet_name, cl.name as client_name, 
                           CASE 
                               WHEN veterinarian LIKE 'Dr. %' THEN veterinarian
                               ELSE CONCAT('Dr. ', veterinarian)
                           END as veterinarian
                    FROM surgeries s
                    JOIN pets p ON s.pet_id = p.pet_id
                    JOIN clients cl ON s.client_id = cl.client_id
                    UNION ALL
                    SELECT date, 'Grooming' as type, p.name as pet_name, cl.name as client_name, 
                           CASE 
                               WHEN veterinarian LIKE 'Dr. %' THEN veterinarian
                               ELSE CONCAT('Dr. ', veterinarian)
                           END as veterinarian
                    FROM grooming g
                    JOIN pets p ON g.pet_id = p.pet_id
                    JOIN clients cl ON g.client_id = cl.client_id
                    UNION ALL
                    SELECT date, 'Other Treatment' as type, p.name as pet_name, cl.name as client_name, 
                           CASE 
                               WHEN veterinarian LIKE 'Dr. %' THEN veterinarian
                               ELSE CONCAT('Dr. ', veterinarian)
                           END as veterinarian
                    FROM other_treatments o
                    JOIN pets p ON o.pet_id = p.pet_id
                    JOIN clients cl ON o.client_id = cl.client_id
                ) AS combined_reports
            """
            
            # Add WHERE clause for receptionists to show only this week's reports
            if user_role == "Receptionist":
                query += " WHERE YEARWEEK(date) = YEARWEEK(CURDATE())"
            
            query += """
                ORDER BY date DESC
                LIMIT 20;
            """
            
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching recent reports summary: {e}")
            return []

    def fetch_recent_appointments_summary(self, user_role=None):
        """Fetch recent appointments for the home page."""
        try:
            base_query = """
                SELECT 
                    DATE_FORMAT(a.date, '%Y-%m-%d') as date,
                    TIME_FORMAT(a.time, '%H:%i:%s') as time,
                    p.name as pet_name,
                    a.reason,
                    c.name as owner,
                    a.status,
                    a.veterinarian
                FROM appointments a
                JOIN pets p ON a.pet_id = p.pet_id
                JOIN clients c ON a.client_id = c.client_id
            """
            
            # Add WHERE clause for veterinarians to show only this week's appointments
            if user_role == "Veterinarian":
                base_query += """
                WHERE YEARWEEK(a.date) = YEARWEEK(CURDATE())
                """
            
            base_query += """
                ORDER BY a.date DESC, a.time DESC
                LIMIT 10
            """
            
            self.cursor.execute(base_query)
            appointments = self.cursor.fetchall()
            return appointments
        except mariadb.Error as e:
            print(f"Error fetching recent appointments: {e}")
            return []

    def generate_license_numbers(self):
        """Generate license numbers for existing veterinarians who don't have one."""
        try:
            # Get all veterinarians without license numbers
            self.cursor.execute("""
                SELECT user_id, name 
                FROM users 
                WHERE role = 'Veterinarian' 
                AND (license_number IS NULL OR license_number = '')
            """)
            vets = self.cursor.fetchall()
            
            for vet in vets:
                # Extract the number from the user_id (e.g., 2025V0007 -> 0007)
                vet_number = vet[0][-4:]
                # Generate license number: PRC0007
                license_number = f"PRC{vet_number}"
                
                # Update the veterinarian's record
                self.cursor.execute("""
                    UPDATE users 
                    SET license_number = ? 
                    WHERE user_id = ?
                """, (license_number, vet[0]))
            
            self.conn.commit()
            print(f"✅ Generated license numbers for {len(vets)} veterinarians")
            return True
        except Exception as e:
            print(f"❌ Error generating license numbers: {e}")
            return False

    def update_old_license_numbers(self):
        """Update veterinarians with old format license numbers to new PRC format."""
        try:
            # Get all veterinarians with old format license numbers
            self.cursor.execute("""
                SELECT user_id, license_number 
                FROM users 
                WHERE role = 'Veterinarian' 
                AND (license_number LIKE 'VET-%' OR license_number LIKE 'PRC No. %')
            """)
            vets = self.cursor.fetchall()
            
            for vet in vets:
                # Extract the number from the user_id (e.g., 2025V0007 -> 0007)
                vet_number = vet[0][-4:]
                # Generate new PRC format license number
                new_license = f"PRC{vet_number}"
                
                # Update the veterinarian's record
                self.cursor.execute("""
                    UPDATE users 
                    SET license_number = ? 
                    WHERE user_id = ?
                """, (new_license, vet[0]))
                
                print(f"Updated license number for {vet[0]} from {vet[1]} to {new_license}")
            
            self.conn.commit()
            print(f"✅ Updated license numbers for {len(vets)} veterinarians")
            return True
        except Exception as e:
            print(f"❌ Error updating license numbers: {e}")
            return False

    def get_vet_license_number(self, veterinarian_name):
        """Get the license number for a veterinarian by their name."""
        try:
            self.cursor.execute("""
                SELECT license_number 
                FROM users 
                WHERE role = 'Veterinarian' 
                AND (name = ? OR CONCAT(name, ' ', last_name) = ?)
            """, (veterinarian_name, veterinarian_name))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"❌ Error getting veterinarian license number: {e}")
            return None