from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QDialog
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from modules.database import Database  # Import the Database class
from modules.petmedix import PetMedix
from modules.utils import create_styled_message_box, show_message
import re
import hashlib

class ForgotPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reset Password")
        self.setFixedSize(500, 500)  # Increased width to 500
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Step 1: Security Questions
        self.security_widget = QWidget()
        security_layout = QVBoxLayout(self.security_widget)
        security_layout.setSpacing(15)
        security_layout.setAlignment(Qt.AlignCenter)  # Center the content

        # Title for Step 1
        step1_title = QLabel("Step 1: Verify Your Identity")
        step1_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        step1_title.setAlignment(Qt.AlignCenter)

        # Container for inputs
        input_container = QWidget()
        input_container.setFixedWidth(400)  # Fixed width for input container
        input_layout = QVBoxLayout(input_container)
        input_layout.setSpacing(15)

        # User ID input
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("Enter your User ID")
        self.user_id_input.setObjectName("FormInput")
        self.user_id_input.setFixedHeight(35)

        # Security questions
        self.answer_one = QLineEdit()
        self.answer_one.setPlaceholderText("What is your mother's maiden name?")
        self.answer_one.setObjectName("FormInput")
        self.answer_one.setFixedHeight(35)

        self.answer_two = QLineEdit()
        self.answer_two.setPlaceholderText("What was the name of your first pet?")
        self.answer_two.setObjectName("FormInput")
        self.answer_two.setFixedHeight(35)

        self.answer_three = QLineEdit()
        self.answer_three.setPlaceholderText("What is the name of the street you grew up on?")
        self.answer_three.setObjectName("FormInput")
        self.answer_three.setFixedHeight(35)

        # Verify button
        self.verify_button = QPushButton("Verify Answers")
        self.verify_button.setObjectName("create")
        self.verify_button.setFixedHeight(40)
        self.verify_button.setFixedWidth(200)  # Fixed width for button
        self.verify_button.clicked.connect(self.verify_answers)

        # Add widgets to input container
        input_layout.addWidget(QLabel("Enter your User ID and answer security questions:"))
        input_layout.addWidget(self.user_id_input)
        input_layout.addWidget(self.answer_one)
        input_layout.addWidget(self.answer_two)
        input_layout.addWidget(self.answer_three)
        input_layout.addWidget(self.verify_button, alignment=Qt.AlignCenter)

        # Add title and container to security layout
        security_layout.addWidget(step1_title)
        security_layout.addWidget(input_container)
        security_layout.addStretch()

        # Step 2: New Password
        self.password_widget = QWidget()
        password_layout = QVBoxLayout(self.password_widget)
        password_layout.setSpacing(15)
        password_layout.setAlignment(Qt.AlignCenter)  # Center the content

        # Title for Step 2
        step2_title = QLabel("Step 2: Set New Password")
        step2_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        step2_title.setAlignment(Qt.AlignCenter)

        # Container for password inputs
        password_container = QWidget()
        password_container.setFixedWidth(400)  # Fixed width for password container
        password_input_layout = QVBoxLayout(password_container)
        password_input_layout.setSpacing(15)

        # New password
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Enter new password")
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setObjectName("FormInput")
        self.new_password.setFixedHeight(35)

        # Confirm password
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm new password")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setObjectName("FormInput")
        self.confirm_password.setFixedHeight(35)

        # Submit button
        self.submit_button = QPushButton("Reset Password")
        self.submit_button.setObjectName("create")
        self.submit_button.setFixedHeight(40)
        self.submit_button.setFixedWidth(200)  # Fixed width for button
        self.submit_button.clicked.connect(self.reset_password)

        # Add widgets to password container
        password_input_layout.addWidget(QLabel("Enter your new password:"))
        password_input_layout.addWidget(self.new_password)
        password_input_layout.addWidget(self.confirm_password)
        password_input_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        # Add title and container to password layout
        password_layout.addWidget(step2_title)
        password_layout.addWidget(password_container)
        password_layout.addStretch()

        # Initially hide the password widget
        self.password_widget.hide()

        # Add both widgets to main layout
        self.main_layout.addWidget(self.security_widget)
        self.main_layout.addWidget(self.password_widget)

        self.setLayout(self.main_layout)

    def verify_answers(self):
        user_id = self.user_id_input.text().strip()
        answer_one = self.answer_one.text().strip()
        answer_two = self.answer_two.text().strip()
        answer_three = self.answer_three.text().strip()

        if not all([user_id, answer_one, answer_two, answer_three]):
            show_message(self, "Please fill in all fields!", QMessageBox.Warning)
            return

        db = Database()
        try:
            if db.verify_security_answers(user_id, answer_one, answer_two, answer_three):
                # Store user_id for password reset
                self.verified_user_id = user_id
                # Show password reset form
                self.security_widget.hide()
                self.password_widget.show()
                # Update window title
                self.setWindowTitle("Set New Password")
            else:
                show_message(self, "Invalid security answers!", QMessageBox.Warning)
        except Exception as e:
            show_message(self, f"Error verifying answers: {e}", QMessageBox.Critical)
        finally:
            db.close_connection()

    def reset_password(self):
        if not hasattr(self, 'verified_user_id'):
            show_message(self, "Please verify your identity first!", QMessageBox.Warning)
            return

        new_password = self.new_password.text().strip()
        confirm_password = self.confirm_password.text().strip()

        if not all([new_password, confirm_password]):
            show_message(self, "Please fill in all password fields!", QMessageBox.Warning)
            return

        if new_password != confirm_password:
            show_message(self, "Passwords do not match!", QMessageBox.Warning)
            return

        if not re.fullmatch(r"[A-Za-z0-9]{6,20}", new_password):
            show_message(self, "Password must be alphanumeric and 6-20 characters long.", QMessageBox.Warning)
            return

        db = Database()
        try:
            # Check if password has been used before
            if db.check_password_history(self.verified_user_id, new_password):
                show_message(self, "You cannot use a password that you have used in the last 3 password changes or your current password.", QMessageBox.Warning)
                return

            # Update password
            if db.update_password(self.verified_user_id, new_password):
                show_message(self, "Password reset successful!", QMessageBox.Information)
                self.accept()
            else:
                show_message(self, "Failed to update password. Please try again.", QMessageBox.Critical)
        except Exception as e:
            show_message(self, f"Error resetting password: {e}", QMessageBox.Critical)
        finally:
            db.close_connection()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PetMedix - Login")
        self.setWindowIcon(QIcon("assets/logo.ico"))
        self.setup_ui()

    def setup_ui(self):
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
        self.goto_signup_button.clicked.connect(self.show_forgot_password_dialog)

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
        email = self.username_input.text().strip()  # Can be email or USER_ID
        password = self.password_input.text().strip()

        # Validate input
        if not (email and password):
            show_message(self, "Email/User ID and password are required!", QMessageBox.Warning)
            return

        # Connect to the database and authenticate the user
        db = Database()
        try:
            user = db.authenticate_user(email, password)
            if user:
                user_id = user.get('user_id', 'Unknown ID')
                role = user.get('role', 'Unknown Role')
                last_name = user.get('last_name', 'Unknown')
                status = user.get('status', 'Unknown')
                
                print(f"Login successful - User ID: {user_id}, Role: {role}, Status: {status}")
                
                # Check if user is admin
                if role == 'Admin':
                    print("Admin login detected, launching admin dashboard...")
                    from modules.admin_dashboard import AdminDashboard
                    self.admin_dashboard = AdminDashboard()
                    self.admin_dashboard.showMaximized()
                    self.close()
                else:
                    # For non-admin users, check if they are verified
                    if status != 'Verified':
                        show_message(self, "Your account is pending verification. Please contact the administrator.", QMessageBox.Warning)
                        return
                        
                    message_box = create_styled_message_box(
                        QMessageBox.Information, 
                        "Success", 
                        f"Welcome {user['name']} {last_name}!"
                    )
                    message_box.exec()
                    
                    # Redirect to HomePage with role and last_name
                    self.home_page = PetMedix(user_id=user_id, role=role, last_name=last_name)
                    self.home_page.showMaximized()
                    self.close()
            else:
                show_message(self, "Invalid email/User ID or password.", QMessageBox.Warning)
        except Exception as e:
            print(f"Login error: {str(e)}")
            show_message(self, f"Failed to login: {e}", QMessageBox.Critical)
        finally:
            db.close_connection()

    def show_forgot_password_dialog(self):
        dialog = ForgotPasswordDialog(self)
        dialog.exec()
