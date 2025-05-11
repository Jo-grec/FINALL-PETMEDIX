from PySide6.QtWidgets import (
    QWidget, QDialog, QLabel, QHBoxLayout, QVBoxLayout, QPushButton,
    QLineEdit, QFrame, QGridLayout, QScrollArea, QComboBox, QDateEdit, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPainterPath
import os
from shutil import copyfile
import re

from modules.database import Database
from modules.utils import show_message

class UpdateInfoDialog(QDialog):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data or {}
        self.setWindowTitle("Update Profile Information")
        self.setFixedSize(650, 620)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 10, 20, 10)
        title_label = QLabel("Personal Information")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFF;")
        title_layout.addWidget(title_label)
        layout.addWidget(title_container)
        
        # Form content
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(40, 30, 40, 30)
        form_layout.setSpacing(20)
        
        # First row: First Name, Last Name
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(20)
        
        # First Name
        fname_label = QLabel("First Name")
        fname_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.fname_input = QLineEdit()
        # Extract first and last name from full name
        name_parts = self.user_data["name"].split()
        if len(name_parts) > 1:
            self.fname_input.setText(name_parts[0])
            self.lname_input_text = " ".join(name_parts[1:])
        else:
            self.fname_input.setText(self.user_data["name"])
            self.lname_input_text = ""
        
        self.fname_input.setMinimumHeight(40)
        self.fname_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        fname_container = QVBoxLayout()
        fname_container.addWidget(fname_label)
        fname_container.addWidget(self.fname_input)
        
        # Last Name
        lname_label = QLabel("Last Name")
        lname_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.lname_input = QLineEdit()
        self.lname_input.setText(self.lname_input_text)
        self.lname_input.setMinimumHeight(40)
        self.lname_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        lname_container = QVBoxLayout()
        lname_container.addWidget(lname_label)
        lname_container.addWidget(self.lname_input)
        
        row1_layout.addLayout(fname_container)
        row1_layout.addLayout(lname_container)
        form_layout.addLayout(row1_layout)
        
        # Address
        address_label = QLabel("Address")
        address_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.address_input = QLineEdit()
        self.address_input.setText(self.user_data["address"])
        self.address_input.setMinimumHeight(40)
        self.address_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        address_container = QVBoxLayout()
        address_container.addWidget(address_label)
        address_container.addWidget(self.address_input)
        form_layout.addLayout(address_container)
        
        # Email and Role
        row3_layout = QHBoxLayout()
        row3_layout.setSpacing(20)
        
        # Email
        email_label = QLabel("Email Address")
        email_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.email_input = QLineEdit()
        self.email_input.setText(self.user_data["email"])
        self.email_input.setMinimumHeight(40)
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        email_container = QVBoxLayout()
        email_container.addWidget(email_label)
        email_container.addWidget(self.email_input)
        
        # Role
        role_label = QLabel("Role")
        role_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Veterinarian", "Veterinary Technician", "Receptionist", "Practice Manager", "Animal Care Assistant"])
        self.role_combo.setCurrentText(self.user_data["role"])
        self.role_combo.setMinimumHeight(40)
        self.role_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                width: 30px;
                border: none;
            }
        """)
        
        role_container = QVBoxLayout()
        role_container.addWidget(role_label)
        role_container.addWidget(self.role_combo)
        
        row3_layout.addLayout(email_container)
        row3_layout.addLayout(role_container)
        form_layout.addLayout(row3_layout)
        
        # Contact Number and Gender
        row4_layout = QHBoxLayout()
        row4_layout.setSpacing(20)
        
        # Contact Number
        contact_label = QLabel("Contact Number")
        contact_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.contact_input = QLineEdit()
        self.contact_input.setText(self.user_data["contact"])
        self.contact_input.setMinimumHeight(40)
        self.contact_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        contact_container = QVBoxLayout()
        contact_container.addWidget(contact_label)
        contact_container.addWidget(self.contact_input)
        
        # Gender
        gender_label = QLabel("Gender")
        gender_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        self.gender_combo.setCurrentText(self.user_data["gender"])
        self.gender_combo.setMinimumHeight(40)
        self.gender_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                width: 30px;
                border: none;
            }
        """)
        
        gender_container = QVBoxLayout()
        gender_container.addWidget(gender_label)
        gender_container.addWidget(self.gender_combo)
        
        row4_layout.addLayout(contact_container)
        row4_layout.addLayout(gender_container)
        form_layout.addLayout(row4_layout)
        
        # Birthdate and Change Password
        row5_layout = QHBoxLayout()
        row5_layout.setSpacing(20)
        
        # Birthdate
        birthdate_label = QLabel("Birthdate")
        birthdate_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True)
        
        # Parse birthdate from string (DD/MM/YYYY)
        if "birthdate" in self.user_data:
            try:
                day, month, year = self.user_data["birthdate"].split('/')
                self.birthdate_input.setDate(QDate(int(year), int(month), int(day)))
            except (ValueError, IndexError):
                self.birthdate_input.setDate(QDate.currentDate())
        else:
            self.birthdate_input.setDate(QDate.currentDate())
            
        self.birthdate_input.setDisplayFormat("dd/MM/yyyy")
        self.birthdate_input.setMinimumHeight(40)
        self.birthdate_input.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        birthdate_container = QVBoxLayout()
        birthdate_container.addWidget(birthdate_label)
        birthdate_container.addWidget(self.birthdate_input)
        
        row5_layout.addLayout(birthdate_container)
        form_layout.addLayout(row5_layout)
        
        layout.addWidget(form_container)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(120, 50)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save")
        save_btn.setFixedSize(120, 50)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #01315d;
            }
        """)
        save_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        button_layout.setContentsMargins(0, 0, 50, 0)
        
        layout.addLayout(button_layout)
    
    def get_updated_data(self):
        """Return the updated user data as a dictionary"""
        return {
            "name": f"{self.fname_input.text()} {self.lname_input.text()}",
            "id": self.user_data["id"],  # ID typically doesn't change
            "role": self.role_combo.currentText(),
            "contact": self.contact_input.text(),
            "address": self.address_input.text(),
            "email": self.email_input.text(),
            "gender": self.gender_combo.currentText(),
            "birthdate": self.birthdate_input.date().toString("dd/MM/yyyy")
        }
        
class UpdateClinicInfoDialog(QDialog):
    def __init__(self, clinic_data=None):
        super().__init__()
        self.setWindowTitle("Update Clinic Information")
        self.setFixedSize(650, 500)
        
        self.clinic_data = clinic_data
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 10, 20, 10)
        title_label = QLabel("Veterinary Clinic Information")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFF;")
        title_layout.addWidget(title_label)
        layout.addWidget(title_container)
        
        # Form content
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(40, 30, 40, 30)
        form_layout.setSpacing(20)
        
        # Clinic Name
        name_label = QLabel("Clinic Name")
        name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.name_input = QLineEdit()
        self.name_input.setText(self.clinic_data["name"])
        self.name_input.setMinimumHeight(40)
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        name_container = QVBoxLayout()
        name_container.addWidget(name_label)
        name_container.addWidget(self.name_input)
        form_layout.addLayout(name_container)
        
        # Address
        address_label = QLabel("Address")
        address_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.address_input = QLineEdit()
        self.address_input.setText(self.clinic_data["address"])
        self.address_input.setMinimumHeight(40)
        self.address_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        address_container = QVBoxLayout()
        address_container.addWidget(address_label)
        address_container.addWidget(self.address_input)
        form_layout.addLayout(address_container)
        
        # Email Address
        email_label = QLabel("Email Address")
        email_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.email_input = QLineEdit()
        self.email_input.setText(self.clinic_data["email"])
        self.email_input.setMinimumHeight(40)
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        email_container = QVBoxLayout()
        email_container.addWidget(email_label)
        email_container.addWidget(self.email_input)
        form_layout.addLayout(email_container)
        
        # Contact Number and Employees row
        row_layout = QHBoxLayout()
        row_layout.setSpacing(20)
        
        # Contact Number
        contact_label = QLabel("Contact Number")
        contact_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.contact_input = QLineEdit()
        self.contact_input.setText(self.clinic_data["contact"])
        self.contact_input.setMinimumHeight(40)
        self.contact_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        contact_container = QVBoxLayout()
        contact_container.addWidget(contact_label)
        contact_container.addWidget(self.contact_input)
        
        # Number of Employees
        employees_label = QLabel("No. of Employees")
        employees_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.employees_input = QLineEdit()
        self.employees_input.setText(self.clinic_data["employees"])
        self.employees_input.setMinimumHeight(40)
        self.employees_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        employees_container = QVBoxLayout()
        employees_container.addWidget(employees_label)
        employees_container.addWidget(self.employees_input)
        
        row_layout.addLayout(contact_container)
        row_layout.addLayout(employees_container)
        form_layout.addLayout(row_layout)
        
        layout.addWidget(form_container)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(120, 50)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save")
        save_btn.setFixedSize(120, 50)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #01315d;
            }
        """)
        save_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        button_layout.setContentsMargins(0, 0, 50, 0)
        
        layout.addLayout(button_layout)
    
    def get_updated_data(self):
        """Return the updated clinic data as a dictionary"""
        return {
            "name": self.name_input.text(),
            "email": self.email_input.text(),
            "address": self.address_input.text(),
            "contact": self.contact_input.text(),
            "employees": self.employees_input.text()
        }

def get_setting_widget(user_id=None):
    
    db = Database()
    
    user_data = {
        "id": "",
        "name": "",
        "role": "",
        "email": "",
        "contact": "",
        "address": "",
        "gender": "",
        "birthdate": "",
        "photo_path": ""
    }

    
    widget = QWidget()
    main_layout = QVBoxLayout(widget)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(5)

    # Title
    settings_label = QLabel("Settings")
    settings_label.setObjectName("SettingsLabel")
    settings_label.setStyleSheet("font-size: 24px; font-weight: bold;")
    settings_label.setAlignment(Qt.AlignLeft)
    main_layout.addWidget(settings_label)

    # ---------- Profile Information Section ----------
    profile_section = QFrame()
    profile_section.setStyleSheet("background-color: white; border-radius: 5px;")
    profile_layout = QVBoxLayout(profile_section)
    profile_layout.setContentsMargins(10, 10, 10, 10)
    profile_layout.setSpacing(0)
    
    # Section Header
    profile_header = QLabel("PROFILE INFORMATION")
    profile_header.setStyleSheet("font-weight: bold; font-size: 16px;")
    profile_layout.addWidget(profile_header)
    
    # Content layout
    profile_content = QHBoxLayout()
    profile_content.setSpacing(25)
    
    # Left side - User picture
    picture_column = QVBoxLayout()
    picture_column.setAlignment(Qt.AlignTop | Qt.AlignCenter)
    
    user_picture = QLabel()
    user_picture.setFixedSize(200, 200)
    user_picture.setAlignment(Qt.AlignCenter)
    user_picture.setText("User\nPicture")
    
    upload_btn = QPushButton("Upload Photo")
    upload_btn.setStyleSheet("""
            background-color: #dfe4ea;
            color: #000;
            font-size: 12px;
            padding: 3px;
            border-radius: 3px;
            margin-left:50px;
        """)
    upload_btn.setFixedWidth(100)
        
    def upload_photo():
        file_path, _ = QFileDialog.getOpenFileName("Select Profile Picture", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            # Save image to profile_photos
            photo_dir = os.path.join("assets", "profile_photos")
            os.makedirs(photo_dir, exist_ok=True)
            filename = f"{user_id}.jpg"
            new_path = os.path.join(photo_dir, filename)
            copyfile(file_path, new_path)

            # Save new path in DB
            db.save_user_profile(
                user_id,
                user_data["contact"],
                user_data["address"],
                user_data["gender"],
                user_data["birthdate"],
                photo_path=new_path
            )
            db.conn.commit()

            original_pixmap = QPixmap(new_path)
            size = clinic_logo.size()
            
            rounded_pixmap = QPixmap(size)
            rounded_pixmap.fill(Qt.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, size.width(), size.height())
            painter.setClipPath(path)
            
            scaled_pixmap = original_pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            user_picture.setPixmap(rounded_pixmap)
            user_picture.setText("")

            user_data["photo_path"] = new_path  # ensure future calls use correct path

    upload_btn.clicked.connect(upload_photo)
    
    picture_column.addWidget(user_picture)
    picture_column.setSpacing(0) 
    picture_column.addWidget(upload_btn)
    picture_column.addStretch()
    
    # Right side - User info
    info_column = QGridLayout()
    info_column.setVerticalSpacing(10)
    info_column.setHorizontalSpacing(10)
    
    # Create info label pairs and store them in a dictionary for easy update later
    info_labels = {}
    info_fields = [
        ("Name", "name"),
        ("ID", "id"),
        ("Role", "role"),
        ("Contact Number", "contact"),
        ("Address", "address"),
        ("Email Address", "email"),
        ("Gender", "gender"),
        ("Birthdate", "birthdate")
    ]
    
    # Fetch user data if user_id is provided
    if user_id:
        try:
            db.cursor.execute("""
                SELECT user_id, name, last_name, email, role FROM users 
                WHERE user_id = ?
            """, (user_id,))
            user_db_data = db.cursor.fetchone()
                
            if user_db_data:
                # Create user data dictionary from database result
                user_data["id"] = user_db_data[0]
                full_name = f"{user_db_data[1]} {user_db_data[2]}" if user_db_data[2] else user_db_data[1]
                user_data["name"] = full_name
                user_data["role"] = user_db_data[4]
                user_data["email"] = user_db_data[3]
                    
                # Try to get additional profile information if available
                db.cursor.execute("""
                    SELECT contact_number, address, gender, birthdate, photo_path FROM user_profiles 
                    WHERE user_id = ?
                """, (user_id,))
                profile_data = db.cursor.fetchone()
                    
                if profile_data:
                    user_data["contact"] = profile_data[0] or ""
                    user_data["address"] = profile_data[1] or ""
                    user_data["gender"] = profile_data[2] or ""
                    # Format the birthdate if it exists
                    if profile_data[3]:
                        if isinstance(profile_data[3], str):
                            user_data["birthdate"] = profile_data[3]
                        else:
                            # Format date object to string
                            user_data["birthdate"] = profile_data[3].strftime("%d/%m/%Y")

                    else:
                        user_data["birthdate"] = ""   
                    user_data["photo_path"] = profile_data[4] or ""
        except Exception as e:
            print(f"Error fetching user data: {e}")
            
        if user_data.get("photo_path") and os.path.exists(user_data["photo_path"]):
            original_pixmap = QPixmap(user_data["photo_path"])
            size = user_picture.size()
            rounded_pixmap = QPixmap(size)
            rounded_pixmap.fill(Qt.transparent)

            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, size.width(), size.height())
            painter.setClipPath(path)

            scaled_pixmap = original_pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()

            user_picture.setPixmap(rounded_pixmap)
            user_picture.setText("")
    
    # Create and populate the info fields
    row = 0
    for label_text, data_key in info_fields:
        # Create the label key (left column)
        label_key = QLabel(f"{label_text}:")
        label_key.setStyleSheet("font-weight: bold; color: #222f3e;")
        
        # Create the label value (right column)
        label_value = QLabel(user_data[data_key])
        label_value.setStyleSheet("color: #222f3e;")
        
        # Add to grid layout
        info_column.addWidget(label_key, row, 0)
        info_column.addWidget(label_value, row, 1)
        
        # Store reference to value label for updates
        info_labels[label_text] = label_value
        
        row += 1
    
    # Action buttons on the right
    button_column = QVBoxLayout()
    button_column.setAlignment(Qt.AlignTop)
    
    update_btn = QPushButton("Update Info")
    update_btn.setIcon(QIcon("edit_icon.png"))
    update_btn.setIconSize(QSize(10, 10))
    update_btn.setStyleSheet("""
        background-color: #012547;
        color: #fff;
        font-size: 12px;
        padding: 8px;
        border-radius: 20px;
        text-align: center;
    """)
    update_btn.setFixedWidth(120)
    
    permission_btn = QPushButton("See Permission")
    permission_btn.setIcon(QIcon("permission_icon.png"))
    permission_btn.setIconSize(QSize(10, 10))
    permission_btn.setStyleSheet("""
        background-color: #012547;
        color: #fff;
        font-size: 12px;
        padding: 8px;
        border-radius: 20;
        text-align: center;
    """)
    permission_btn.setFixedWidth(120)
    
    # Connect the update button to open the dialog
    def open_update_info_dialog():
        dialog = UpdateInfoDialog(user_data)
        if dialog.exec():
            # Get updated data from the dialog
            updated_data = dialog.get_updated_data()

            # Convert birthdate to SQL-friendly format (yyyy-MM-dd)
            qt_date = dialog.birthdate_input.date()
            birthdate_sql = qt_date.toString("yyyy-MM-dd")

            # Update the labels
            info_labels["Name"].setText(updated_data["name"])
            info_labels["ID"].setText(updated_data["id"])
            info_labels["Role"].setText(updated_data["role"])
            info_labels["Contact Number"].setText(updated_data["contact"])
            info_labels["Address"].setText(updated_data["address"])
            info_labels["Email Address"].setText(updated_data["email"])
            info_labels["Gender"].setText(updated_data["gender"])
            info_labels["Birthdate"].setText(updated_data["birthdate"])

            # Update the user_data dictionary
            for key, value in updated_data.items():
                user_data[key] = value

            if user_id:
                try:
                    # Split name for DB update
                    name_parts = updated_data["name"].split(" ", 1)
                    first_name = name_parts[0]
                    last_name = name_parts[1] if len(name_parts) > 1 else ""

                    # Update user table
                    db.cursor.execute("""
                        UPDATE users SET name = ?, last_name = ?, email = ?
                        WHERE user_id = ?
                    """, (first_name, last_name, updated_data["email"], user_id))

                    # Update or insert profile info
                    db.save_user_profile(
                        user_id,
                        updated_data["contact"],
                        updated_data["address"],
                        updated_data["gender"],
                        birthdate_sql,
                        photo_path=user_data.get("photo_path")
                    )

                    db.conn.commit()
                    print("✅ User information updated and saved to database.")
                except Exception as e:
                    print(f"❌ Error updating user info in database: {e}")
        else:
            print("Update cancelled")
    
    update_btn.clicked.connect(open_update_info_dialog)
    
    button_column.addWidget(update_btn)
    button_column.addWidget(permission_btn)
    button_column.addStretch()
    
    # Add all columns to the profile content
    profile_content.addLayout(picture_column)
    profile_content.addSpacing(40)
    profile_content.addLayout(info_column, 1)  # Give it stretch factor
    profile_content.addLayout(button_column)
    
    profile_layout.addLayout(profile_content)
    main_layout.addWidget(profile_section)

    # ---------- Clinic Information Section ----------
    clinic_section = QFrame()
    clinic_section.setStyleSheet("background-color: white; border-radius: 5px;")
    clinic_layout = QVBoxLayout(clinic_section)
    clinic_layout.setContentsMargins(10, 10, 10, 10)
    clinic_layout.setSpacing(25)
    
    # Section Header
    clinic_header = QLabel("VET CLINIC INFORMATION")
    clinic_header.setStyleSheet("font-weight: bold; font-size: 16px;")
    clinic_layout.addWidget(clinic_header)
    
    # Content layout
    clinic_content = QHBoxLayout()
    clinic_content.setSpacing(25)
    
    clinic_data = {
    "name": "",
    "address": "",
    "contact": "",
    "email": "",
    "employees": "",
    "logo_path": ""
    }

    # Left side - Clinic logo
    clinic_picture_column = QVBoxLayout()
    clinic_picture_column.setAlignment(Qt.AlignTop | Qt.AlignCenter)

    clinic_logo = QLabel()
    clinic_logo.setFixedSize(200, 200)
    clinic_logo.setAlignment(Qt.AlignCenter)
    clinic_logo.setText("Clinic\nLogo")

    clinic_upload_btn = QPushButton("Upload Photo")
    clinic_upload_btn.setStyleSheet("""
        background-color: #dfe4ea;
        color: #000;
        font-size: 12px;
        padding: 3px;
        border-radius: 3px;
        margin-left:50px;
    """)
    clinic_upload_btn.setFixedWidth(100)
    
    def upload_logo():
        file_path, _ = QFileDialog.getOpenFileName("Select Clinic Logo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            logo_dir = os.path.join("assets", "clinic_logos")
            os.makedirs(logo_dir, exist_ok=True)

            filename = "clinic_logo.jpg"
            new_path = os.path.join(logo_dir, filename)
            copyfile(file_path, new_path)

            original_pixmap = QPixmap(new_path)
            size = clinic_logo.size()

            # Resize and round the image
            rounded_pixmap = QPixmap(size)
            rounded_pixmap.fill(Qt.transparent)

            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, size.width(), size.height())
            painter.setClipPath(path)

            scaled_pixmap = original_pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()

            clinic_logo.setPixmap(rounded_pixmap)
            clinic_logo.setText("")  # remove placeholder

            # Save path to DB
            db.save_clinic_info(
                clinic_data["name"],
                clinic_data["address"],
                clinic_data["contact"],
                clinic_data["email"],
                clinic_data["employees"],
                logo_path=new_path
            )
            clinic_data["logo_path"] = new_path

    clinic_upload_btn.clicked.connect(upload_logo)

    clinic_picture_column.addWidget(clinic_logo)
    clinic_picture_column.addWidget(clinic_upload_btn)
    clinic_picture_column.addStretch()
    
    # Right side - Clinic info
    clinic_info_column = QGridLayout()
    clinic_info_column.setVerticalSpacing(10)
    clinic_info_column.setHorizontalSpacing(10)
    
    # Load clinic info from database
    try:
        db.cursor.execute("SELECT name, address, contact_number, email, employees_count, logo_path FROM clinic_info LIMIT 1")
        clinic_row = db.cursor.fetchone()
        if clinic_row:
            clinic_data = {
                "name": clinic_row[0],
                "address": clinic_row[1],
                "contact": clinic_row[2],
                "email": clinic_row[3],
                "employees": str(clinic_row[4]),
                "logo_path": clinic_row[5] or ""
            }
        else:
            clinic_data = {
                "name": "VetGuard Animal Clinic",
                "email": "vetguardclinic@gmail.com",
                "address": "Jaro, Iloilo City",
                "contact": "09430434443",
                "employees": "21"
            }
    except Exception as e:
        print(f"❌ Error loading clinic data: {e}")
        
    if clinic_data.get("logo_path") and os.path.exists(clinic_data["logo_path"]):
        original_pixmap = QPixmap(clinic_data["logo_path"])
        size = clinic_logo.size()
        rounded_pixmap = QPixmap(size)
        rounded_pixmap.fill(Qt.transparent)

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size.width(), size.height())
        painter.setClipPath(path)

        scaled_pixmap = original_pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        clinic_logo.setPixmap(rounded_pixmap)
        clinic_logo.setText("")
            

    # ✅ Now define clinic_fields using the loaded clinic_data
    clinic_fields = {
        "Name:": clinic_data["name"],
        "Email Address:": clinic_data["email"],
        "Address:": clinic_data["address"],
        "Contact Number:": clinic_data["contact"],
        "No. of Employees:": clinic_data["employees"]
    }
  
    # Create a dictionary to store the clinic QLabel widgets
    clinic_labels = {}
    
    row = 0
    for label_text, value_text in clinic_fields.items():
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; color: #222f3e;")
        
        value = QLabel(value_text)
        value.setStyleSheet("color: #222f3e;")
        
        clinic_info_column.addWidget(label, row, 0)
        clinic_info_column.addWidget(value, row, 1)
        clinic_labels[label_text.replace(":", "")] = value
        row += 1
        
    # Clinic update button
    clinic_button_column = QVBoxLayout()
    clinic_button_column.setAlignment(Qt.AlignTop)
    
    update_clinic_btn = QPushButton("Update Info")
    update_clinic_btn.setIcon(QIcon("edit_icon.png"))
    update_clinic_btn.setIconSize(QSize(10, 10))
    update_clinic_btn.setStyleSheet("""
        background-color: #012547;
        color: #fff;
        font-size: 12px;
        padding: 8px;
        border-radius: 20px;
        text-align: center;
    """)
    update_clinic_btn.setFixedWidth(120)
    
        # Connect the clinic update button to open the clinic update dialog
    def open_update_clinic_dialog():
        dialog = UpdateClinicInfoDialog(clinic_data)
        if dialog.exec():
            # Get updated data from the dialog first
            updated_data = dialog.get_updated_data()
            
            db.save_clinic_info(
                updated_data["name"],
                updated_data["address"],
                updated_data["contact"],
                updated_data["email"],
                int(updated_data["employees"]),
                logo_path=clinic_data.get("logo_path")  # preserve existing logo
            )

            # Update the labels
            clinic_labels["Name"].setText(updated_data["name"])
            clinic_labels["Email Address"].setText(updated_data["email"])
            clinic_labels["Address"].setText(updated_data["address"])
            clinic_labels["Contact Number"].setText(updated_data["contact"])
            clinic_labels["No. of Employees"].setText(updated_data["employees"])
            
            # Update the clinic_data dictionary
            for key, value in updated_data.items():
                clinic_data[key] = value
                
            print("Clinic information updated successfully")
        else:
            print("Clinic update cancelled")

    update_clinic_btn.clicked.connect(open_update_clinic_dialog)
    
    clinic_button_column.addWidget(update_clinic_btn)
    clinic_button_column.addStretch()
    
    # Add all columns to the clinic content
    clinic_content.addLayout(clinic_picture_column)
    clinic_content.addSpacing(40)
    clinic_content.addLayout(clinic_info_column, 1)  # Give it stretch factor
    clinic_content.addLayout(clinic_button_column)
    
    clinic_layout.addLayout(clinic_content)
    main_layout.addWidget(clinic_section)
    
    return widget

def save_settings(self):
    """Save the settings to the database."""
    # Get values from form
    clinic_name = self.clinic_name_input.text().strip()
    email = self.email_input.text().strip()
    phone = self.phone_input.text().strip()
    address = self.address_input.toPlainText().strip()
    vat_rate = self.vat_rate_input.text().strip()

    # Validate required fields
    if not (clinic_name and email and phone):
        show_message(self, "Clinic name, email, and phone are required!", QMessageBox.Warning)
        return

    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        show_message(self, "Please enter a valid email address!", QMessageBox.Warning)
        return

    # Validate VAT rate
    try:
        vat_rate = float(vat_rate)
        if vat_rate < 0 or vat_rate > 100:
            show_message(self, "VAT rate must be between 0 and 100!", QMessageBox.Warning)
            return
    except ValueError:
        show_message(self, "Please enter a valid VAT rate!", QMessageBox.Warning)
        return

    # Save to database
    db = Database()
    try:
        # Save settings
        if db.save_settings(clinic_name, email, phone, address, vat_rate):
            show_message(self, "Settings saved successfully!")
            self.accept()
        else:
            show_message(self, "Failed to save settings!", QMessageBox.Critical)
    except Exception as e:
        show_message(self, f"Failed to save settings: {e}", QMessageBox.Critical)
    finally:
        db.close_connection()

def reset_settings(self):
    """Reset settings to default values."""
    # Confirm reset
    confirmation = QMessageBox()
    confirmation.setIcon(QMessageBox.Question)
    confirmation.setText("Are you sure you want to reset all settings to default values?")
    confirmation.setWindowTitle("")
    confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    
    if confirmation.exec() == QMessageBox.Yes:
        # Reset to default values
        self.clinic_name_input.setText("PetMedix Veterinary Clinic")
        self.email_input.setText("")
        self.phone_input.setText("")
        self.address_input.setPlainText("")
        self.vat_rate_input.setText("12")

        # Save to database
        db = Database()
        try:
            if db.save_settings(
                "PetMedix Veterinary Clinic",
                "",
                "",
                "",
                12
            ):
                show_message(self, "Settings reset successfully!")
            else:
                show_message(self, "Failed to reset settings!", QMessageBox.Critical)
        except Exception as e:
            show_message(self, f"Failed to reset settings: {e}", QMessageBox.Critical)
        finally:
            db.close_connection()


