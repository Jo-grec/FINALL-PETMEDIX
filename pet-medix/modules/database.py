import mariadb
import hashlib
from datetime import datetime

class Database:
    def __init__(self, host="localhost", user="root", password="axeljohn123", database="petmedix"):
        try:
            self.conn = mariadb.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            print("✅ Database connection established.")
            self.create_users_table()
        except mariadb.Error as e:
            print(f"❌ Error connecting to MariaDB: {e}")
            self.conn = None
            self.cursor = None

    def create_users_table(self):
        """Create the users table if it doesn't exist."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    USER_ID VARCHAR(10) PRIMARY KEY,
                    NAME VARCHAR(100) NOT NULL,
                    EMAIL VARCHAR(100) NOT NULL UNIQUE,
                    HASHED_PASSWORD VARCHAR(64) NOT NULL,
                    ROLE VARCHAR(50) NOT NULL
                )
            """)
            self.conn.commit()
            print("✅ Table 'users' ready.")
        except mariadb.Error as e:
            print(f"❌ Error creating table: {e}")

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
            return

        user_id = self.generate_user_id()
        if not user_id:
            print("❌ Could not generate USER_ID.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute(
                "INSERT INTO users (USER_ID, NAME, EMAIL, HASHED_PASSWORD, ROLE) VALUES (?, ?, ?, ?, ?)",
                (user_id, name, email, hashed_password, role)
            )
            self.conn.commit()
            print(f"✅ User created with USER_ID: {user_id}")
        except mariadb.Error as e:
            print(f"❌ Error inserting user: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("🔒 Database connection closed.")
            
    def authenticate_user(self, email, password):
        """Authenticate a user by email and password."""
        if not self.cursor:
            print("Database connection not established. Cannot authenticate user.")
            return None

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute(
                "SELECT USER_ID, NAME, ROLE FROM users WHERE EMAIL = ? AND HASHED_PASSWORD = ?",
                (email, hashed_password)
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

