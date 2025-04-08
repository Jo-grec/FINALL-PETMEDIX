import mariadb
import hashlib

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
            print("Database connection established.")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            self.conn = None
            self.cursor = None  # Ensure cursor is also None if connection fails

    def create_user(self, name, email, password, role):
        """Create a new user in the database."""
        if not self.cursor:
            print("Database connection not established. Cannot create user.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute(
                "INSERT INTO users (name, email, hashed_password, role) VALUES (?, ?, ?, ?)",
                (name, email, hashed_password, role)
            )
            self.conn.commit()
            print("User created successfully.")
        except mariadb.Error as e:
            print(f"Error creating user: {e}")

    def authenticate_user(self, email, password):
        """Authenticate a user by email and password."""
        if not self.cursor:
            print("Database connection not established. Cannot authenticate user.")
            return None

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute(
                "SELECT user_id, name, role FROM users WHERE email = ? AND hashed_password = ?",
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

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")