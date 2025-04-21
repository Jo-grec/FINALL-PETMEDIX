from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QHBoxLayout, QMessageBox, QComboBox
from PySide6.QtCore import Qt, QTimer
from modules.database import Database  # Import the Database class
import re

class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PetMedix - Sign Up")

        with open("styles/login.qss", "r") as file:
            self.setStyleSheet(file.read())

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(200, 10, 200, 10)

        self.title_label = QLabel("Get Started with PetMedix!", self)
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        grid_layout = QGridLayout()

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.role_input = QComboBox()
        self.role_input.setEditable(True)
        self.role_input.addItem("Select Role")
        self.role_input.addItems(["Receptionist", "Veterinarian"])
        self.role_input.setCurrentIndex(0)
        self.role_input.lineEdit().setReadOnly(True)
        self.role_input.lineEdit().setPlaceholderText("Role")
        self.role_input.setObjectName("RoleComboBox")  # For styling

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        grid_layout.addWidget(self.first_name_input, 0, 0)
        grid_layout.addWidget(self.last_name_input, 0, 1)
        grid_layout.addWidget(self.email_input, 1, 0)
        grid_layout.addWidget(self.role_input, 1, 1)
        grid_layout.addWidget(self.password_input, 2, 0, 1, 2)

        self.signup_button = QPushButton("Create Account")
        self.signup_button.setObjectName("create")
        self.signup_button.setFixedWidth(250)
        self.signup_button.clicked.connect(self.create_account)  # Connect to the create_account method

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.signup_button)

        layout.addWidget(self.title_label)
        layout.addSpacing(20)
        layout.addLayout(grid_layout)
        layout.addSpacing(20)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def create_account(self):
        """Handle user signup."""
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_input.text().strip()
        password = self.password_input.text().strip()

        if not (first_name and last_name and email and password) or role == "Select Role":
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        if not email.endswith("@petmedix.med"):
            QMessageBox.warning(self, "Invalid Email", "Email must end with @petmedix.med")
            return

        if not re.fullmatch(r"[A-Za-z0-9]+", password):
            QMessageBox.warning(self, "Invalid Password", "Password must be alphanumeric (letters and numbers only).")
            return

        full_name = f"{first_name} {last_name}"

        db = Database()
        try:
            # Check if user already exists
            if db.user_exists(email):
                QMessageBox.warning(self, "Account Exists", "An account with this email already exists.")
                return

            db.create_user(full_name, email, password, role)
            QMessageBox.information(self, "Success", "Account created successfully!")

            redirect_label = QLabel("Redirecting to login page...", self)
            redirect_label.setAlignment(Qt.AlignCenter)
            redirect_label.setStyleSheet("font-size: 16px; color: green;")
            self.layout().addWidget(redirect_label)

            QTimer.singleShot(2000, self.redirect_to_login)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create account: {e}")
        finally:
            db.close_connection()

    def redirect_to_login(self):
        """Redirect to the login page."""
        from modules.login import LoginWindow  # Import here to avoid circular imports
        self.login_window = LoginWindow()
        self.login_window.showMaximized()  
        self.close()