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
                email VARCHAR(100) NOT NULL UNIQUE,
                hashed_password VARCHAR(64) NOT NULL,
                role VARCHAR(50) NOT NULL
            );
            """)

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

            # Billing Table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS billing (
                billing_id INT AUTO_INCREMENT PRIMARY KEY,
                client_id INT NOT NULL,
                pet_id INT NOT NULL,
                date_issued DATE NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                payment_status ENUM('Paid', 'Unpaid', 'Partial') NOT NULL,
                payment_method ENUM('Cash', 'Credit Card', 'GCash', 'Bank Transfer'),
                received_by VARCHAR(100),
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE,
                FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE
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
                employees_count INT
            );
            """)

            self.conn.commit()
            print("✅ Tables created successfully.")
        except mariadb.Error as e:
            print(f"❌ Error creating tables: {e}")

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("✅ Database connection closed.")

    def generate_user_id(self):
        """Generate a new USER_ID like 2025V0001."""
        year = datetime.now().year
        prefix = f"{year}V"
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

    def create_user(self, name, email, password, role):
        """Insert a user with a generated USER_ID."""
        if not self.cursor:
            print("❌ Database not connected.")
            return None

        user_id = self.generate_user_id()
        if not user_id:
            print("❌ Could not generate USER_ID.")
            return None

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute(
                "INSERT INTO users (USER_ID, NAME, EMAIL, HASHED_PASSWORD, ROLE) VALUES (?, ?, ?, ?, ?)",
                (user_id, name, email, hashed_password, role)
            )
            self.conn.commit()
            print(f"✅ User created with USER_ID: {user_id}")
            return user_id  # Return the generated USER_ID
        except mariadb.Error as e:
            print(f"❌ Error inserting user: {e}")
            return None
            
    def authenticate_user(self, identifier, password):
        """Authenticate a user by email or user_id and password."""
        if not self.cursor:
            print("Database connection not established. Cannot authenticate user.")
            return None

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute(
                """
                SELECT USER_ID, NAME, ROLE 
                FROM users 
                WHERE (EMAIL = ? OR USER_ID = ?) AND HASHED_PASSWORD = ?
                """,
                (identifier, identifier, hashed_password)
            )
            user = self.cursor.fetchone()
            if user:
                return {"user_id": user[0], "name": user[1], "role": user[2]}
            else:
                return None
        except mariadb.Error as e:
            print(f"Error authenticating user: {e}")
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
        
        # home dynamic countings
        
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


    # fetching client info to display
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

