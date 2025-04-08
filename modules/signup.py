from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QHBoxLayout
from PySide6.QtCore import Qt

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
        
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Role")
        
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

        button_layout = QHBoxLayout()
        button_layout.addStretch() 
        button_layout.addWidget(self.signup_button)

        layout.addWidget(self.title_label)
        layout.addSpacing(20)
        layout.addLayout(grid_layout)  
        layout.addSpacing(20)
        layout.addLayout(button_layout)  

        self.setLayout(layout)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication([])

    window = SignUpWindow()
    window.showMaximized()  

    app.exec()
