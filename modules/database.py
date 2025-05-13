import mariadb
import hashlib
from datetime import datetime

class Database:
    def __init__(self, host="localhost", user="root", password="joelmar123", database="petmedix"):
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
            # Users Table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100),
                email VARCHAR(100) NOT NULL UNIQUE,
                hashed_password VARCHAR(64) NOT NULL,
                role VARCHAR(50) NOT NULL,
                status VARCHAR(20) DEFAULT 'Pending',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Ensure the status column exists
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

            # Clients Table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address VARCHAR(255),
                contact_number VARCHAR(15),
                email VARCHAR(100) UNIQUE
            );
            """)

            # Pets Table
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
                photo_path VARCHAR(255),
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Appointments Table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                client_id INT NOT NULL,
                date DATE NOT NULL,
                status ENUM('Scheduled', 'Completed', 'Cancelled', 'No-Show', 'Rescheduled', 'Urgent') NOT NULL,
                payment_status ENUM('Pending', 'Paid', 'Unpaid') NOT NULL,
                reason TEXT,
                veterinarian VARCHAR(100),
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Medical Records Table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_records (
                record_id INT AUTO_INCREMENT PRIMARY KEY,
                pet_id INT NOT NULL,
                client_id INT NOT NULL,
                date DATE NOT NULL,
                type ENUM('Consultation', 'Deworming', 'Vaccination', 'Surgical Operation', 'Grooming', 'Other Treatments') NOT NULL,
                reason TEXT,
                diagnosis TEXT,
                prescribed_treatment TEXT,
                veterinarian VARCHAR(100),
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            );
            """)

            # Billing Table - UPDATED: Using a single definition with all required columns
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS billing (
                billing_id INT AUTO_INCREMENT PRIMARY KEY,
                invoice_no VARCHAR(50),
                client_id INT NOT NULL,
                pet_id INT NOT NULL,
                date_issued DATE NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                payment_status ENUM('Paid', 'Unpaid', 'Partial') NOT NULL,
                payment_method ENUM('Cash', 'Credit Card', 'GCash', 'Bank Transfer'),
                received_by VARCHAR(100),
                reason VARCHAR(200),
                veterinarian VARCHAR(100),
                notes VARCHAR(200),
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE,
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE
            );
            """)
            
            # Drop and recreate billing_services table to ensure correct structure
            self.cursor.execute("DROP TABLE IF EXISTS billing_services")
            self.cursor.execute("""
            CREATE TABLE billing_services (
                service_id INT AUTO_INCREMENT PRIMARY KEY,
                billing_id INT NOT NULL,
                service_description VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10, 2) NOT NULL,
                line_total DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (billing_id) REFERENCES billing(billing_id) ON DELETE CASCADE
            );
            """)

            # Clinic Information Table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clinic_info (
                clinic_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address VARCHAR(255),
                contact_number VARCHAR(15),
                email VARCHAR(100),
                employees_count INT,
                photo_path VARCHAR(255)
            );
            """)
            
            try:
                self.cursor.execute("SHOW COLUMNS FROM clinic_info LIKE 'logo_path'")
                if not self.cursor.fetchone():
                    self.cursor.execute("ALTER TABLE clinic_info ADD COLUMN logo_path VARCHAR(255)")
                    print("✅ 'logo_path' column added to clinic_info.")
            except mariadb.Error as e:
                print(f"❌ Error checking/adding 'logo_path' column: {e}")

            
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
            
            try:
                self.cursor.execute("SHOW COLUMNS FROM user_profiles LIKE 'photo_path'")
                if not self.cursor.fetchone():
                    self.cursor.execute("ALTER TABLE user_profiles ADD COLUMN photo_path VARCHAR(255)")
                    print("✅ 'photo_path' column added to user_profiles.")
            except mariadb.Error as e:
                print(f"❌ Error checking/adding 'photo_path' column: {e}")
            
            # Security Questions Table
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

            # Password History Table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_history (
                history_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(10) NOT NULL,
                hashed_password VARCHAR(64) NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            """)
            
            # Ensure the billing table has all required columns
            self._ensure_billing_columns()
            
            self.conn.commit()
            print("✅ Tables created successfully.")
        except mariadb.Error as e:
            print(f"❌ Error creating tables: {e}")
            
            # Ensure 'logo_path' column exists in clinic_info
            try:
                self.cursor.execute("SHOW COLUMNS FROM clinic_info LIKE 'logo_path'")
                if not self.cursor.fetchone():
                    self.cursor.execute("ALTER TABLE clinic_info ADD COLUMN logo_path VARCHAR(255)")
                    print("✅ 'logo_path' column added to clinic_info.")
            except mariadb.Error as e:
                print(f"❌ Error adding 'logo_path' column: {e}")
            
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

    def create_user(self, name, last_name, email, password, role):
        """Insert a user with a generated USER_ID."""
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
                "INSERT INTO users (USER_ID, NAME, LAST_NAME, EMAIL, HASHED_PASSWORD, ROLE) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, name, last_name, email, hashed_password, role)
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

            # Count medical records
            self.cursor.execute("SELECT COUNT(*) FROM medical_records")
            medical_records_count = self.cursor.fetchone()[0]

            # Count appointments
            self.cursor.execute("SELECT COUNT(*) FROM appointments")
            appointments_count = self.cursor.fetchone()[0]

            return clients_count, medical_records_count, appointments_count
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

            if result:
                # Update existing client
                client_id = result[0]
                self.cursor.execute("""
                    UPDATE clients
                    SET name = ?, address = ?, contact_number = ?
                    WHERE client_id = ?
                """, (name, address, contact_number, client_id))
            else:
                # Insert new client
                self.cursor.execute("""
                    INSERT INTO clients (name, address, contact_number, email)
                    VALUES (?, ?, ?, ?)
                """, (name, address, contact_number, email))

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
                SELECT name, address, contact_number, email
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
        """Fetch all appointments from the database."""
        try:
            self.cursor.execute("""
                SELECT a.date, p.name AS pet_name, c.name AS client_name, a.reason, a.status, 
                    a.payment_status, a.veterinarian
                FROM appointments a
                JOIN pets p ON a.pet_id = p.pet_id
                JOIN clients c ON a.client_id = c.client_id
                ORDER BY a.date DESC
            """)
            return self.cursor.fetchall()  # Return all rows
        except Exception as e:
            print(f"❌ Error fetching appointments: {e}")
            return []
        
    def save_billing(self, client_id, pet_id, date_issued, total_amount, payment_status, 
                    payment_method, received_by, invoice_no, reason, veterinarian, notes):
        """Save billing information to database."""
        try:
            self.cursor.execute("""
                INSERT INTO billing (
                    client_id, pet_id, date_issued, total_amount, payment_status, 
                    payment_method, received_by, invoice_no, reason, veterinarian, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                client_id, pet_id, date_issued, total_amount, payment_status,
                payment_method, received_by, invoice_no, reason, veterinarian, notes
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"❌ Database error saving billing: {e}")
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
                ORDER BY b.date_issued DESC
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

    def save_clinic_info(self, name, address, contact_number, email, employees_count, logo_path=None):
        try:
            self.cursor.execute("SELECT clinic_id FROM clinic_info LIMIT 1")
            existing = self.cursor.fetchone()

            if existing:
                if logo_path:
                    self.cursor.execute("""
                        UPDATE clinic_info
                        SET name = ?, address = ?, contact_number = ?, email = ?, employees_count = ?, logo_path = ?
                        WHERE clinic_id = ?
                    """, (name, address, contact_number, email, employees_count, logo_path, existing[0]))
                else:
                    self.cursor.execute("""
                        UPDATE clinic_info
                        SET name = ?, address = ?, contact_number = ?, email = ?, employees_count = ?
                        WHERE clinic_id = ?
                    """, (name, address, contact_number, email, employees_count, existing[0]))
            else:
                self.cursor.execute("""
                    INSERT INTO clinic_info (name, address, contact_number, email, employees_count, logo_path)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, address, contact_number, email, employees_count, logo_path))

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

    def save_medical_record(self, pet_id, client_id, date, type, reason, diagnosis, prescribed_treatment, veterinarian):
        """Save a medical record to the database."""
        try:
            self.cursor.execute("""
                INSERT INTO medical_records (
                    pet_id, client_id, date, type, reason, diagnosis,
                    prescribed_treatment, veterinarian
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pet_id, client_id, date, type, reason, diagnosis,
                prescribed_treatment, veterinarian
            ))
            self.conn.commit()
            print("✅ Medical record saved successfully.")
            return True
        except Exception as e:
            print(f"❌ Error saving medical record: {e}")
            return False

    def fetch_medical_records(self, record_type=None):
        """Fetch medical records from the database, optionally filtered by type."""
        try:
            if record_type and record_type != "All":
                self.cursor.execute("""
                    SELECT 
                        DATE_FORMAT(mr.date, '%Y-%m-%d') as date,
                        mr.type,
                        p.name AS pet_name,
                        c.name AS client_name,
                        mr.reason,
                        mr.diagnosis,
                        mr.prescribed_treatment,
                        mr.veterinarian
                    FROM medical_records mr
                    JOIN pets p ON mr.pet_id = p.pet_id
                    JOIN clients c ON mr.client_id = c.client_id
                    WHERE mr.type = ?
                    ORDER BY mr.date DESC
                """, (record_type,))
            else:
                self.cursor.execute("""
                    SELECT 
                        DATE_FORMAT(mr.date, '%Y-%m-%d') as date,
                        mr.type,
                        p.name AS pet_name,
                        c.name AS client_name,
                        mr.reason,
                        mr.diagnosis,
                        mr.prescribed_treatment,
                        mr.veterinarian
                    FROM medical_records mr
                    JOIN pets p ON mr.pet_id = p.pet_id
                    JOIN clients c ON mr.client_id = c.client_id
                    ORDER BY mr.date DESC
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