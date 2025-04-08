from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from modules.database import Database  # Import the Database class
from modules.signup import SignUpWindow  
from modules.home import HomePage

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PetMedix - Login")

        with open("styles/login.qss", "r") as file: 
            self.setStyleSheet(file.read())

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(50, 0, 50, 0)
        main_layout.setSpacing(30)

        self.logo_label = QLabel(self)
        self.logo_label.setObjectName("logologin")
        pixmap = QPixmap("assets/logologin.png")
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setAlignment(Qt.AlignCenter)

        self.welcome_label = QLabel("Welcome!", self)
        self.welcome_label.setObjectName("WelcomeLabel")
        self.welcome_label.setAlignment(Qt.AlignLeft)

        self.subwelcome_label = QLabel(
            "Keep Pets Healthy with Paws-itively Reliable Record-Keeping!", self)
        self.subwelcome_label.setObjectName("SubwelcomeLabel")
        self.subwelcome_label.setAlignment(Qt.AlignLeft)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Email")
        self.username_input.setFixedWidth(400)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(400)

        self.goto_signup_button = QPushButton("Forgot Password?", self)
        self.goto_signup_button.setFlat(True)
        self.goto_signup_button.setObjectName("forgotPasswordButton")
        self.goto_signup_button.setFixedWidth(50)
        self.goto_signup_button.setCursor(Qt.PointingHandCursor)

        password_layout = QVBoxLayout()
        password_layout.addWidget(self.password_input)

        link_layout = QHBoxLayout()
        link_layout.addStretch() 
        link_layout.addWidget(self.goto_signup_button)
        password_layout.addLayout(link_layout)

        self.login_button = QPushButton("Login", self)
        self.login_button.setObjectName("loginButton")
        self.login_button.setFixedWidth(150)
        self.login_button.clicked.connect(self.login_user)  # Connect to the login_user method

        form_container.setMaximumWidth(600)

        form_layout.addWidget(self.welcome_label)
        form_layout.addWidget(self.subwelcome_label)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.username_input)
        form_layout.addSpacing(20)
        form_layout.addLayout(password_layout) 
        form_layout.addSpacing(20)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.login_button)
        form_layout.addLayout(button_layout)
        
        signup_prompt_layout = QHBoxLayout()
        signup_prompt_layout.setAlignment(Qt.AlignCenter)

        self.new_here_label = QLabel("New here?", self)

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.setFlat(True)
        self.signup_button.setCursor(Qt.PointingHandCursor)
        self.signup_button.setObjectName("signupButton")

        signup_prompt_layout.addWidget(self.new_here_label)
        signup_prompt_layout.addWidget(self.signup_button)

        form_layout.addLayout(signup_prompt_layout)

        main_layout.addWidget(self.logo_label, stretch=1, alignment=Qt.AlignCenter)
        main_layout.addWidget(form_container, stretch=2, alignment=Qt.AlignCenter)

        self.main_widget.setLayout(main_layout)

        self.signup_button.clicked.connect(self.go_to_signup)

    def go_to_signup(self):
        print("Switching to signup page...")
        self.signup_window = SignUpWindow()  
        self.signup_window.showMaximized() 
        self.close() 

    def login_user(self):
        """Handle user login."""
        email = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not (email and password):
            QMessageBox.warning(self, "Input Error", "Email and password are required!")
            return

        # Connect to the database and authenticate the user
        db = Database()
        try:
            user = db.authenticate_user(email, password)
            if user:
                QMessageBox.information(self, "Success", f"Welcome {user['name']}!")
                
                # Redirect to HomePage
                self.home_page = HomePage()
                self.home_page.showMaximized()  # Ensure the HomePage is maximized
                self.close()  # Close the LoginWindow
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid email or password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to login: {e}")
        finally:
            db.close_connection()

    def go_to_signup(self):
        print("Switching to signup page...")
        self.signup_window = SignUpWindow()  
        self.signup_window.showMaximized() 
        self.close() 
