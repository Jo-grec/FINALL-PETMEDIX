from PySide6.QtWidgets import QWidget, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QHBoxLayout, QMessageBox, QComboBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QIcon
from modules.database import Database  # Import the Database class
from modules.utils import create_styled_message_box
import re

class SignUpWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PetMedix - Sign Up")

        with open("styles/login.qss", "r") as file:
            self.setStyleSheet(file.read())

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(200, 130, 200, 130)
        layout.setSpacing(10)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)
        header_layout.setObjectName("signupHeader")

        self.title_label = QLabel("Get Started with PetMedix!", self)
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)

        login_prompt_layout = QHBoxLayout()
        login_prompt_layout.setAlignment(Qt.AlignCenter)

        self.have_account_label = QLabel("Already have an account?", self)
        self.have_account_label.setObjectName("HaveaccountLabel")

        self.login_button = QPushButton("Log in", self)
        self.login_button.setFlat(True)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setObjectName("LoginButton")

        login_prompt_layout.addWidget(self.have_account_label)
        login_prompt_layout.addWidget(self.login_button)
        login_prompt_layout.setSpacing(5)
        login_prompt_layout.setContentsMargins(30, 0, 0, 0)

        header_layout.addWidget(self.title_label)
        header_layout.addLayout(login_prompt_layout)

        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(20)

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

        # password field w/. toggle visibility
        password_container = QWidget()
        password_container.setObjectName("SignupPasswordContainer")
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 15, 0)
        password_layout.setSpacing(10)

        eye_closed_pixmap = QPixmap("assets/visible 1.png")
        eye_open_pixmap = QPixmap("assets/eye open.png")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        #toggle visibility
        eye_icon_label = QLabel()
        eye_icon_label.setFixedSize(24, 24)
        if not eye_closed_pixmap.isNull():
            eye_icon_label.setPixmap(eye_closed_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            eye_icon_label.setText("👁️")
        eye_icon_label.setStyleSheet("background: transparent;")
        eye_icon_label.setCursor(Qt.PointingHandCursor)

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(eye_icon_label)

        # Function to toggle password visibility
        def toggle_password_visibility():
            if self.password_input.echoMode() == QLineEdit.Password:
                self.password_input.setEchoMode(QLineEdit.Normal)
                if not eye_open_pixmap.isNull():
                    eye_icon_label.setPixmap(eye_open_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    eye_icon_label.setText("👁️‍🗨️")
            else:
                self.password_input.setEchoMode(QLineEdit.Password)
                if not eye_closed_pixmap.isNull():
                    eye_icon_label.setPixmap(eye_closed_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    eye_icon_label.setText("👁️")

        # Connect click event to toggle function
        eye_icon_label.mousePressEvent = lambda event: toggle_password_visibility()

        self.first_name_input.setObjectName("FormInput")
        self.last_name_input.setObjectName("FormInput")
        self.email_input.setObjectName("FormInput")
        self.password_input.setObjectName("PasswordFormInput")

        grid_layout.addWidget(self.first_name_input, 0, 0)
        grid_layout.addWidget(self.last_name_input, 0, 1)
        grid_layout.addWidget(self.email_input, 1, 0)
        grid_layout.addWidget(self.role_input, 1, 1)
        grid_layout.addWidget(password_container, 2, 0, 1, 2)

        self.signup_button = QPushButton("Create Account")
        self.signup_button.setObjectName("create")
        self.signup_button.setFixedWidth(400)
        self.signup_button.clicked.connect(self.create_account)  # Connect to the create_account method

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.signup_button)

        layout.addLayout(header_layout)  # Add the header layout instead of separate widgets
        layout.addSpacing(30)  # Space between header and form
        layout.addLayout(grid_layout)
        layout.addSpacing(20)
        layout.addLayout(button_layout)

        self.main_widget.setLayout(layout)

        self.login_button.clicked.connect(self.go_to_login)

    def go_to_login(self):
        print("Switching to login page...")
        from modules.login import LoginWindow
        self.login_window = LoginWindow() 
        self.login_window.showMaximized() 
        self.close() 

    def create_account(self):
        """Handle user signup."""
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_input.currentText().strip()
        password = self.password_input.text().strip()

        if not (first_name and last_name and email and password) or role == "Select Role":
            message_box = create_styled_message_box(
                QMessageBox.Warning, 
                "Input Error", 
                "All fields are required!"
            )
            message_box.exec()
            return

        if not email.endswith("@petmedix.med"):
            QMessageBox.warning(self, "Invalid Email", "Email must end with @petmedix.med")
            return

        if not re.fullmatch(r"[A-Za-z0-9]{6,20}", password):
            QMessageBox.warning(self, "Invalid Password",
                "Password must be alphanumeric and 6-20 characters long.")
            return

        full_name = f"{first_name} {last_name}"

        db = Database()
        try:
            # Check if user already exists
            if db.user_exists(email):
                QMessageBox.warning(self, "Account Exists", "An account with this email already exists.")
                return

            # Create user and retrieve the generated USER_ID
            user_id = db.create_user(full_name, email, password, role)
            if user_id:
                QMessageBox.information(self, "Success", f"Account created successfully! Your username is: {user_id}")

                redirect_label = QLabel("Redirecting to login page...", self)
                redirect_label.setAlignment(Qt.AlignCenter)
                redirect_label.setStyleSheet("font-size: 16px; color: green;")
                self.layout().addWidget(redirect_label)

                QTimer.singleShot(2000, self.redirect_to_login)
            else:
                QMessageBox.critical(self, "Error", "Failed to generate a username. Please try again.")
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