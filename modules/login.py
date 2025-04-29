from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from modules.database import Database  # Import the Database class
from modules.petmedix import PetMedix
from modules.utils import create_styled_message_box

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PetMedix - Login")

        with open("styles/login.qss", "r") as file: 
            self.setStyleSheet(file.read())

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(100, 0, 50, 0)
        main_layout.setSpacing(10)

        self.logo_label = QLabel(self)
        self.logo_label.setObjectName("logologin")
        pixmap = QPixmap("assets/loginlogo.png")
        resized_pixmap = pixmap.scaled(350, 470, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(resized_pixmap)
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

        # Username field with icon
        username_container = QWidget()
        username_container.setObjectName("Container")
        username_layout = QHBoxLayout(username_container)
        username_layout.setContentsMargins(15, 0, 15, 0)
        username_layout.setSpacing(10)

        # User icon
        user_icon_pixmap = QPixmap("assets/authentication 1.png")
        user_icon_label = QLabel()
        user_icon_label.setFixedSize(24, 24)
        if not user_icon_pixmap.isNull():
            user_icon_label.setPixmap(user_icon_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            user_icon_label.setText("👤")
            user_icon_label.setStyleSheet("background: transparent;")

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Email")
        self.username_input.setFixedWidth(500)

        # password field with icon and toggle visibility
        password_container = QWidget()
        password_container.setObjectName("Container")
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(15, 0, 15, 0)
        password_layout.setSpacing(10)

        password_icon_pixmap = QPixmap("assets/key 1.png")
        eye_closed_pixmap = QPixmap("assets/visible 1.png")
        eye_open_pixmap = QPixmap("assets/eye open.png")

        # password icon
        password_icon_label = QLabel()
        password_icon_label.setFixedSize(24, 24)
        if not  password_icon_pixmap.isNull():
            password_icon_label.setPixmap( password_icon_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            password_icon_label.setText("🔑")
            password_icon_label.setStyleSheet("background: transparent;")
        
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(550)

        #toggle visibility
        eye_icon_label = QLabel()
        eye_icon_label.setFixedSize(24, 24)
        if not eye_closed_pixmap.isNull():
            eye_icon_label.setPixmap(eye_closed_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            eye_icon_label.setText("👁️")
        eye_icon_label.setStyleSheet("background: transparent;")
        eye_icon_label.setCursor(Qt.PointingHandCursor)

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

        self.goto_signup_button = QPushButton("Forgot Password?", self)
        self.goto_signup_button.setFlat(True)
        self.goto_signup_button.setObjectName("forgotPasswordButton")
        self.goto_signup_button.setFixedWidth(100)
        self.goto_signup_button.setCursor(Qt.PointingHandCursor)

        forgot_password_layout = QHBoxLayout()
        forgot_password_layout.addStretch()
        forgot_password_layout.addWidget(self.goto_signup_button)
        forgot_password_layout.setContentsMargins(0, 0, 20, 0)

      
        username_layout.addWidget(user_icon_label)
        username_layout.addWidget(self.username_input, 1)

        password_layout.addWidget(password_icon_label)
        password_layout.addWidget(self.password_input, 1)
        password_layout.addWidget(eye_icon_label)

        link_layout = QHBoxLayout()
        link_layout.addStretch() 
        link_layout.addWidget(self.goto_signup_button)

        self.login_button = QPushButton("Login", self)
        self.login_button.setObjectName("loginButton")
        self.login_button.setFixedWidth(150)
        self.login_button.clicked.connect(self.login_user)  # Connect to the login_user method

        form_container.setMaximumWidth(600)

        form_layout.addWidget(self.welcome_label)
        form_layout.addWidget(self.subwelcome_label)
        form_layout.addSpacing(20)
        form_layout.addWidget(username_container)
        form_layout.addSpacing(20)
        form_layout.addWidget(password_container) 
        form_layout.addSpacing(5)  
        form_layout.addLayout(forgot_password_layout)  
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
        signup_prompt_layout.setSpacing(0)
        signup_prompt_layout.setContentsMargins(30, 0, 0, 0)

        form_layout.addLayout(signup_prompt_layout)

        main_layout.addWidget(self.logo_label, stretch= 1, alignment=Qt.AlignRight)
        main_layout.addWidget(form_container, stretch=2, alignment=Qt.AlignCenter)

        self.main_widget.setLayout(main_layout)

        self.signup_button.clicked.connect(self.go_to_signup)

    def go_to_signup(self):
        print("Switching to signup page...")
        from modules.signup import SignUpWindow
        self.signup_window = SignUpWindow()  
        self.signup_window.showMaximized() 
        self.close() 

    def login_user(self):
        """Handle user login."""
        identifier = self.username_input.text().strip()  # Can be email or USER_ID
        password = self.password_input.text().strip()

        if not (identifier and password):
            QMessageBox.warning(self, "Input Error", "Email/User ID and password are required!")
            return

        # Connect to the database and authenticate the user
        db = Database()
        try:
            user = db.authenticate_user(identifier, password)
            if user:
                message_box = create_styled_message_box(
                    QMessageBox.Information, 
                    "Success", 
                    f"Welcome {user['name']}!"
                )
                message_box.exec()
                
                # Redirect to HomePage
                self.home_page = PetMedix()
                self.home_page.showMaximized()  # Ensure the HomePage is maximized
                self.close()  # Close the LoginWindow
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid email/User ID or password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to login: {e}")
        finally:
            db.close_connection()

