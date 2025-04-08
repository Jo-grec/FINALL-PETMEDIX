from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PetMedix - Home")

        # Apply styles from external QSS file
        with open("styles/login.qss", "r") as file:
            self.setStyleSheet(file.read())

        # Main layout (horizontal layout with left navbar and right content)
        main_layout = QVBoxLayout(self)

        # Create the header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header.setObjectName("Header")
        header_layout.setContentsMargins(20, 10, 50, 10)  # Padding
        header_layout.setSpacing(10)

        # Logo on the left
        self.logo_label = QLabel()
        pixmap = QPixmap("assets/petmedix.png")  # Path to your PetMedix logo
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setFixedHeight(50)  # Adjust if needed
        self.logo_label.setScaledContents(True)

        # Username label
        self.username_label = QLabel("Hello, Dr. Smith")
        self.username_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.username_label.setObjectName("UsernameLabel")

        # User icon
        self.user_icon_label = QLabel()
        user_pixmap = QPixmap("assets/userlogo.png")  # 👉 Path to your user icon
        self.user_icon_label.setPixmap(user_pixmap)
        self.user_icon_label.setFixedSize(40, 40)
        self.user_icon_label.setScaledContents(True)

        # Mini layout for username + user icon
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.username_label)
        user_layout.addWidget(self.user_icon_label)
        user_layout.setSpacing(8)

        user_widget = QWidget()
        user_widget.setLayout(user_layout)

        # Add to the header layout
        header_layout.addWidget(self.logo_label, alignment=Qt.AlignLeft)
        header_layout.addStretch() 
        header_layout.addWidget(user_widget, alignment=Qt.AlignRight)

        # Add header to the main layout
        main_layout.addWidget(header)

        # Create the body layout (horizontal layout with navbar on the left and content on the right)
        body_layout = QHBoxLayout()

        # Create the left navigation bar (narrow)
        navbar = QWidget()
        navbar_layout = QVBoxLayout(navbar)
        navbar.setObjectName("NavBar")
        navbar_layout.setContentsMargins(10, 10, 10, 10)  # Padding for the navbar
        navbar_layout.setSpacing(10)

        navbar_logo = QLabel()
        navbar_logo_pixmap = QPixmap("assets/logo.png")  # Path to your navigation logo
        navbar_logo.setPixmap(navbar_logo_pixmap)
        navbar_logo.setObjectName("Navbarlogo")
        navbar_logo.setFixedHeight(240) 
        navbar_logo.setAlignment(Qt.AlignCenter)
        navbar_logo.setScaledContents(True)

        # Add navbar logo to the navbar layout
        navbar_layout.addWidget(navbar_logo)
        
        clinic_name_label = QLabel("PetMedix<br> Animal Clinic")
        clinic_name_label.setAlignment(Qt.AlignCenter)
        clinic_name_label.setObjectName("ClinicNameLabel")
        navbar_layout.addWidget(clinic_name_label)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # Set the shape of the frame to a horizontal line
        line.setFrameShadow(QFrame.Sunken)  # Make the line appear sunken (optional)
        navbar_layout.addWidget(line)

        # Example navigation buttons
        button1 = QPushButton("Home")
        button2 = QPushButton("Client")
        button3 = QPushButton("Reports")
        button4 = QPushButton("Appointments")
        button5 = QPushButton("Billings")
        button6 = QPushButton("Settings")
        
        navbar_layout.addWidget(button1)
        navbar_layout.addWidget(button2)
        navbar_layout.addWidget(button3)
        navbar_layout.addWidget(button4)
        navbar_layout.addWidget(button5)
        navbar_layout.addWidget(button6)
        
        button1.setFlat(True)
        button2.setFlat(True)
        button3.setFlat(True)
        button4.setFlat(True)
        button5.setFlat(True)
        button6.setFlat(True)

        # Add a stretch to move the buttons to the top
        navbar_layout.addStretch()  # This ensures the buttons are at the top

        # Set fixed width for the navbar (narrow width, e.g., 150px)
        navbar.setFixedWidth(260)

        # Add the navbar to the left side of the body layout
        body_layout.addWidget(navbar)

        # Create the right content area (takes the remaining space)
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_area.setStyleSheet("background-color: #fff;")  # Optional: background color for content area

        # Add content area to the right side of the body layout
        body_layout.addWidget(content_area)

        # Add the body layout (navbar + content) to the main layout
        main_layout.addLayout(body_layout)

        # Set the main layout for the window
        self.setLayout(main_layout)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication([])

    window = HomePage()
    window.showMaximized()
    app.exec()
