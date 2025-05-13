from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QDialog, QFormLayout, QLineEdit, QComboBox, QTextEdit, QDateEdit, QHeaderView,
    QMessageBox, QTableWidgetItem, QFileDialog, QStackedWidget
)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QColor, QBrush, QIcon, QPixmap
from modules.database import Database
from datetime import datetime
from modules.utils import show_message
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class ReportFormDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PetMedix - Reports")
        self.setFixedSize(800, 750)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 15, 20, 15)
        title_label = QLabel("Report Form")
        title_label.setObjectName("TitleLabel")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFF;")
        title_layout.addWidget(title_label)
        layout.addWidget(title_container)
        
        # Form Layout
        form_widget = QWidget()
        form_scroll_layout = QVBoxLayout(form_widget)
        form_scroll_layout.setContentsMargins(40, 20, 40, 20)
        form_scroll_layout.setSpacing(20)
        
        # Row 1: Date, Type
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(20)
        
        # Date field
        date_label = QLabel("Date")
        date_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setMinimumHeight(40)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
        """)
        
        date_container = QVBoxLayout()
        date_container.setSpacing(0)
        date_container.addWidget(date_label)
        date_container.addWidget(self.date_edit)
        
        # Type field
        type_label = QLabel("Type")
        type_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Consultation", "Deworming", "Vaccination", "Surgery", "Grooming", "Other"])
        self.type_combo.setMinimumHeight(40)
        self.type_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
            QComboBox::drop-down {
                width: 30px;
                border: none;
            }
            QComboBox::down-arrow {
                width: 15px;
                height: 15px;
            }
        """)
        
        type_container = QVBoxLayout()
        type_container.setSpacing(0)
        type_container.addWidget(type_label)
        type_container.addWidget(self.type_combo)
        
        row1_layout.addLayout(date_container, 1)
        row1_layout.addLayout(type_container, 1)
        form_scroll_layout.addLayout(row1_layout)
        
        # Row 2: Pet Name
        pet_name_label = QLabel("Pet Name")
        pet_name_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.pet_name_combo = QComboBox()
        self.pet_name_combo.setMinimumHeight(40)
        self.pet_name_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
            QComboBox::drop-down {
                width: 30px;
                border: none;
            }
            QComboBox::down-arrow {
                width: 15px;
                height: 15px;
            }
        """)
        
        self.load_pet_names()
        
        pet_name_container = QVBoxLayout()
        pet_name_container.setSpacing(0)
        pet_name_container.addWidget(pet_name_label)
        pet_name_container.addWidget(self.pet_name_combo)
        form_scroll_layout.addLayout(pet_name_container)
        
        # Row 3: Reason for Consultation
        reason_label = QLabel("Reason for Consultation")
        reason_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText("Reason for Consultation")
        self.reason_input.setFixedHeight(60)
        self.reason_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
        """)
        
        reason_container = QVBoxLayout()
        reason_container.setSpacing(0)
        reason_container.addWidget(reason_label)
        reason_container.addWidget(self.reason_input)
        form_scroll_layout.addLayout(reason_container)
        
        # Row 4: Diagnosis
        diagnosis_label = QLabel("Diagnosis")
        diagnosis_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px; margin-top: 12px;")
        self.diagnosis_input = QTextEdit()
        self.diagnosis_input.setPlaceholderText("Diagnosis")
        self.diagnosis_input.setFixedHeight(60)
        self.diagnosis_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
        """)
        
        diagnosis_container = QVBoxLayout()
        diagnosis_container.setSpacing(0)
        diagnosis_container.addWidget(diagnosis_label)
        diagnosis_container.addWidget(self.diagnosis_input)
        form_scroll_layout.addLayout(diagnosis_container)
        
        # Row 5: Prescribed Treatment/Medication
        prescribed_label = QLabel("Prescribed Treatment/Medication")
        prescribed_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px; margin-top: 12px;")
        self.prescribed_input = QTextEdit()
        self.prescribed_input.setPlaceholderText("Prescribed Treatment/Medication")
        self.prescribed_input.setFixedHeight(60)
        self.prescribed_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
        """)
        
        prescribed_container = QVBoxLayout()
        prescribed_container.setSpacing(0)
        prescribed_container.addWidget(prescribed_label)
        prescribed_container.addWidget(self.prescribed_input)
        form_scroll_layout.addLayout(prescribed_container)
        
        # Row 6: Veterinarian/Staff In Charge
        vet_label = QLabel("Veterinarian/Staff In Charge")
        vet_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px; margin-top: 12px;")
        self.vet_combo = QComboBox()
        self.vet_combo.setMinimumHeight(40)
        self.vet_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
            QComboBox::drop-down {
                width: 30px;
                border: none;
            }
            QComboBox::down-arrow {
                width: 15px;
                height: 15px;
            }
        """)
        
        self.load_vet_names()
        
        vet_container = QVBoxLayout()
        vet_container.setSpacing(0)
        vet_container.addWidget(vet_label)
        vet_container.addWidget(self.vet_combo)
        form_scroll_layout.addLayout(vet_container)
        
        layout.addWidget(form_widget)
        
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
        save_btn.setObjectName("SaveButton")
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
        button_layout.setContentsMargins(0, 10, 50, 10)
        
        layout.addLayout(button_layout)

    def load_pet_names(self):
        """Load pet names grouped by their owners into the pet_name_combo."""
        try:
            db = Database()
            cursor = db.cursor

            cursor.execute("""
                SELECT c.name AS client_name, p.name AS pet_name
                FROM clients c
                JOIN pets p ON c.client_id = p.client_id
                ORDER BY c.name ASC, p.name ASC
            """)
            rows = cursor.fetchall()

            if not rows:
                self.pet_name_combo.addItem("No pets found")
                return

            current_owner = None
            for client_name, pet_name in rows:
                if client_name != current_owner:
                    self.pet_name_combo.addItem(f"{client_name} - Owner")
                    index = self.pet_name_combo.count() - 1
                    self.pet_name_combo.model().item(index).setEnabled(False)
                    current_owner = client_name

                self.pet_name_combo.addItem(f"  {pet_name}")

            db.close_connection()
        except Exception as e:
            print("Failed to load pet names:", e)
            self.pet_name_combo.addItem("Error loading pets")
            
    def load_vet_names(self):
        """Load veterinarian names into the vet_combo."""
        try:
            db = Database()
            cursor = db.cursor

            cursor.execute("""
                SELECT name
                FROM users
                WHERE role = 'Veterinarian'
                ORDER BY name ASC
            """)
            rows = cursor.fetchall()

            if not rows:
                self.vet_combo.addItem("No veterinarians found")
                return

            for row in rows:
                self.vet_combo.addItem(row[0])

            db.close_connection()
        except Exception as e:
            print("Failed to load veterinarian names:", e)
            self.vet_combo.addItem("Error loading veterinarians")


class ViewReportDialog(QDialog):
    def __init__(self, report_data):
        super().__init__()
        self.setWindowTitle("PetMedix - Reports")
        self.setFixedSize(800, 750)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 15, 20, 15)
        
        # Extract pet name from the data
        pet_name = report_data[2]  # Pet name is at index 2
        title_label = QLabel(f"{pet_name}'s Report")
        title_label.setObjectName("TitleLabel")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFF;")
        title_layout.addWidget(title_label)
        layout.addWidget(title_container)
        
        # Form Layout
        form_widget = QWidget()
        form_scroll_layout = QVBoxLayout(form_widget)
        form_scroll_layout.setContentsMargins(40, 20, 40, 20)
        form_scroll_layout.setSpacing(20)
        
        # Row 1: Date, Type
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(20)
        
        # Date field
        date_label = QLabel("Date")
        date_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setMinimumHeight(40)
        self.date_edit.setReadOnly(True)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
        """)
        
        date_container = QVBoxLayout()
        date_container.setSpacing(0)
        date_container.addWidget(date_label)
        date_container.addWidget(self.date_edit)
        
        # Type field
        type_label = QLabel("Type")
        type_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Consultation", "Deworming", "Vaccination", "Surgery", "Grooming", "Other"])
        self.type_combo.setMinimumHeight(40)
        self.type_combo.setEnabled(False)
        self.type_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
            QComboBox::drop-down {
                width: 30px;
                border: none;
            }
            QComboBox::down-arrow {
                width: 15px;
                height: 15px;
            }
        """)
        
        type_container = QVBoxLayout()
        type_container.setSpacing(0)
        type_container.addWidget(type_label)
        type_container.addWidget(self.type_combo)
        
        row1_layout.addLayout(date_container, 1)
        row1_layout.addLayout(type_container, 1)
        form_scroll_layout.addLayout(row1_layout)
        
        # Row 2: Pet Name
        pet_name_label = QLabel("Pet Name")
        pet_name_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.pet_name_combo = QComboBox()
        self.pet_name_combo.setMinimumHeight(40)
        self.pet_name_combo.setEnabled(False)
        self.pet_name_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
            QComboBox::drop-down {
                width: 30px;
                border: none;
            }
            QComboBox::down-arrow {
                width: 15px;
                height: 15px;
            }
        """)
        
        pet_name_container = QVBoxLayout()
        pet_name_container.setSpacing(0)
        pet_name_container.addWidget(pet_name_label)
        pet_name_container.addWidget(self.pet_name_combo)
        form_scroll_layout.addLayout(pet_name_container)
        
        # Row 3: Reason for Consultation
        reason_label = QLabel("Reason for Consultation")
        reason_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        self.reason_input = QTextEdit()
        self.reason_input.setReadOnly(True)
        self.reason_input.setFixedHeight(60)
        self.reason_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
        """)
        
        reason_container = QVBoxLayout()
        reason_container.setSpacing(0)
        reason_container.addWidget(reason_label)
        reason_container.addWidget(self.reason_input)
        form_scroll_layout.addLayout(reason_container)
        
        # Row 4: Diagnosis
        diagnosis_label = QLabel("Diagnosis")
        diagnosis_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px; margin-top: 12px;")
        self.diagnosis_input = QTextEdit()
        self.diagnosis_input.setReadOnly(True)
        self.diagnosis_input.setFixedHeight(60)
        self.diagnosis_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
        """)
        
        diagnosis_container = QVBoxLayout()
        diagnosis_container.setSpacing(0)
        diagnosis_container.addWidget(diagnosis_label)
        diagnosis_container.addWidget(self.diagnosis_input)
        form_scroll_layout.addLayout(diagnosis_container)
        
        # Row 5: Prescribed Treatment/Medication
        prescribed_label = QLabel("Prescribed Treatment/Medication")
        prescribed_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px; margin-top: 12px;")
        self.prescribed_input = QTextEdit()
        self.prescribed_input.setReadOnly(True)
        self.prescribed_input.setFixedHeight(60)
        self.prescribed_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
        """)
        
        prescribed_container = QVBoxLayout()
        prescribed_container.setSpacing(0)
        prescribed_container.addWidget(prescribed_label)
        prescribed_container.addWidget(self.prescribed_input)
        form_scroll_layout.addLayout(prescribed_container)
        
        # Row 6: Veterinarian/Staff In Charge
        vet_label = QLabel("Veterinarian/Staff In Charge")
        vet_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px; margin-top: 12px;")
        self.vet_combo = QComboBox()
        self.vet_combo.setMinimumHeight(40)
        self.vet_combo.setEnabled(False)
        self.vet_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
            }
            QComboBox::drop-down {
                width: 30px;
                border: none;
            }
            QComboBox::down-arrow {
                width: 15px;
                height: 15px;
            }
        """)
        
        vet_container = QVBoxLayout()
        vet_container.setSpacing(0)
        vet_container.addWidget(vet_label)
        vet_container.addWidget(self.vet_combo)
        form_scroll_layout.addLayout(vet_container)
        
        layout.addWidget(form_widget)
        
        # Close Button
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 10, 0, 10)
        
        close_btn = QPushButton("Close")
        close_btn.setFixedSize(120, 50)
        close_btn.setStyleSheet("""
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
        close_btn.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        button_layout.addStretch()
        
        layout.addWidget(button_container)
        
        # Set the data
        self.set_report_data(report_data)
        
    def set_report_data(self, data):
        """Set the form data from the report."""
        try:
            # Ensure we have all required fields
            while len(data) < 8:
                data.append("")
            
            # Set date
            if data[0]:
                try:
                    date = datetime.strptime(data[0], "%Y-%m-%d")
                    self.date_edit.setDate(QDate(date.year, date.month, date.day))
                except:
                    self.date_edit.setDate(QDate.currentDate())
            
            # Set type
            if data[1]:
                index = self.type_combo.findText(data[1])
                if index >= 0:
                    self.type_combo.setCurrentIndex(index)
            
            # Set pet name
            if data[2] and data[3]:
                self.pet_name_combo.clear()  # Clear existing items
                self.pet_name_combo.addItem(f"{data[3]} - {data[2]}")  # Client - Pet
            
            # Set other fields
            if data[4]:
                self.reason_input.setText(data[4])
            if data[5]:
                self.diagnosis_input.setText(data[5])
            if data[6]:
                self.prescribed_input.setText(data[6])
            
            # Set veterinarian name
            if data[7]:
                vet_name = data[7]
                if not vet_name.startswith("Dr. "):
                    vet_name = f"Dr. {vet_name}"
                self.vet_combo.clear()  # Clear existing items
                self.vet_combo.addItem(vet_name)
                self.vet_combo.setCurrentText(vet_name)
            else:
                self.vet_combo.clear()
                self.vet_combo.addItem("No veterinarian assigned")
            
        except Exception as e:
            print(f"Error setting report data: {e}")

def get_report_widget():
    content = QWidget()
    layout = QVBoxLayout(content)
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 30)

    # Store current search text
    current_search = ""

    # Header setup
    header = QWidget()
    header.setFixedHeight(50)
    header.setStyleSheet("background-color: #102547;")
    header_layout = QHBoxLayout()
    header_layout.setContentsMargins(0, 0, 0, 0)
    header_layout.setSpacing(10)

    # Report Label
    report_label = QLabel("Report")
    report_label.setObjectName("ReportLabel")
    report_label.setAlignment(Qt.AlignVCenter)

    # Add Report Button
    add_report_button = QPushButton("Add Report")
    add_report_button.setObjectName("AddReportButton")
    add_report_button.setFixedSize(120, 40)
    add_report_button.setStyleSheet(
        "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px;"
    )

    # Save PDF Button
    save_pdf_button = QPushButton("Save PDF")
    save_pdf_button.setObjectName("SavePDFButton")
    save_pdf_button.setFixedSize(120, 40)
    save_pdf_button.setStyleSheet(
        "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px;"
    )

    # Edit Button
    edit_button = QPushButton()
    edit_button.setObjectName("EditButton")
    edit_button.setFixedSize(40, 40)  # Make it square for round shape
    edit_button.setIcon(QIcon("assets/edit client button.png"))
    edit_button.setIconSize(QSize(20, 20))
    edit_button.setStyleSheet("""
        QPushButton {
            background-color: #FED766;
            border: none;
            border-radius: 20px;
            margin-bottom: 5px;
        }
        QPushButton:hover {
            background-color: #FFC107;
        }
    """)
    edit_button.hide()  # Initially hidden

    # Delete Button
    delete_button = QPushButton()
    delete_button.setObjectName("DeleteButton")
    delete_button.setFixedSize(40, 40)  # Make it square for round shape
    delete_button.setIcon(QIcon("assets/trash-can.png"))
    delete_button.setIconSize(QSize(20, 20))
    delete_button.setStyleSheet("""
        QPushButton {
            background-color: #FF6F61;
            border: none;
            border-radius: 20px;
            margin-bottom: 5px;
        }
        QPushButton:hover {
            background-color: #E53935;
        }
    """)
    delete_button.hide()  # Initially hidden

    # Create a container widget for the action buttons
    action_buttons_container = QWidget()
    action_buttons_layout = QHBoxLayout(action_buttons_container)
    action_buttons_layout.setContentsMargins(0, 0, 0, 0)
    action_buttons_layout.setSpacing(10)
    action_buttons_layout.setAlignment(Qt.AlignLeft)  # Align buttons to the left
    action_buttons_layout.addWidget(edit_button)
    action_buttons_layout.addWidget(delete_button)

    header_layout.addWidget(report_label)
    header_layout.addWidget(add_report_button)
    header_layout.addWidget(save_pdf_button)
    header_layout.addWidget(action_buttons_container)

    # Treatment Buttons
    treatment_buttons_widget = QWidget()
    treatment_layout = QHBoxLayout()
    treatment_layout.setContentsMargins(0, 0, 50, 0)
    treatment_layout.setSpacing(0)

    treatment_buttons = {}

    # Define treatments and create tables
    treatments = [
        "All",
        "Consultation",
        "Deworming",
        "Vaccination",
        "Surgery",
        "Grooming",
        "Other"
    ]

    treatment_widths = {
        "All": 70,
        "Consultation": 100,
        "Deworming": 100,
        "Vaccination": 100,
        "Surgery": 100,
        "Grooming": 100,
        "Other": 100
    }

    for treatment in treatments:
        button = QPushButton(treatment)
        button.setFixedSize(treatment_widths[treatment], 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #F4F4F8;
                font-family: Poppins;
                font-style: normal;
                font-weight: 300;
                line-height: normal;
                border: none;
                font-size: 15px;
                padding-left: 10px;
                padding-right: 10px;
            }
            QPushButton:hover {
                background-color: #FED766;
            }
            QPushButton[selected="true"] {
                background-color: #FED766;
            }
        """)
        treatment_layout.addWidget(button)
        treatment_buttons[treatment] = button

    treatment_buttons_widget.setLayout(treatment_layout)
    header_layout.addStretch()
    header_layout.addWidget(treatment_buttons_widget)
    header.setLayout(header_layout)
    layout.addWidget(header)

    # Create tables for each treatment type
    tables = {}
    for treatment in treatments:
        table = QTableWidget()
        if treatment == "All":
            table.setColumnCount(8)  # Removed Action column
            table.setHorizontalHeaderLabels([
                "Date", "Type", "Pet Name", "Owner/Client", "Reason",
                "Diagnosis", "Prescribed Treatment", "Veterinarian"
            ])
        else:
            table.setColumnCount(8)
            table.setHorizontalHeaderLabels([
                "Date", "Pet Name", "Owner/Client", "Reason",
                "Diagnosis", "Prescribed Treatment", "Veterinarian", "Action"
            ])
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #000;
            }
            QHeaderView::section {
                background-color: #FED766;
                color: #000;
                font-weight: bold;
                height: 40px;
            }
        """)
        table.verticalHeader().setVisible(False)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set column widths
        if treatment == "All":
            for i, width in enumerate([150, 120, 120, 150, 200, 180, 200, 150]):
                table.setColumnWidth(i, width)
        else:
            for i, width in enumerate([150, 120, 150, 200, 180, 200, 150, 100]):
                table.setColumnWidth(i, width)

        tables[treatment] = table
        layout.addWidget(table)
        if treatment != "All":
            table.hide()

    def show_table(table_to_show):
        for table in tables.values():
            table.hide()
        table_to_show.show()
        # Reapply current search filter when switching tables
        if current_search:
            filter_tables(current_search)

    def select_treatment(selected_button):
        for button in treatment_buttons.values():
            button.setProperty('selected', False)
            button.style().unpolish(button)
            button.style().polish(button)

        selected_button.setProperty('selected', True)
        selected_button.style().unpolish(selected_button)
        selected_button.style().polish(selected_button)

    # Connect treatment buttons
    for treatment, button in treatment_buttons.items():
        button.clicked.connect(lambda checked, t=treatment: [
            show_table(tables[t]),
            select_treatment(treatment_buttons[t])
        ])

    # Show All table by default
    tables["All"].show()
    select_treatment(treatment_buttons["All"])

    def handle_row_selection():
        """Handle row selection and show/hide action buttons accordingly."""
        table = None
        for t in tables.values():
            if t.isVisible():
                table = t
                break
        
        if not table:
            return

        selected_rows = table.selectionModel().selectedRows()
        
        if selected_rows:
            edit_button.show()
            delete_button.show()
        else:
            edit_button.hide()
            delete_button.hide()

    # Connect the selection change signal for all tables
    for table in tables.values():
        table.selectionModel().selectionChanged.connect(handle_row_selection)

    def handle_cell_click(row, col, table):
        """Handle cell click event to show report details."""
        # Skip if clicking on action buttons
        if col == 7:  # Action column
            return
            
        try:
            record = []
            
            # Get all data from the row
            for i in range(table.columnCount() - 1):  # Exclude action column
                item = table.item(row, i)
                if item:
                    record.append(item.text())
                else:
                    record.append("")
            
            # Ensure we have enough data
            if len(record) < 7:
                print(f"Warning: Not enough data in row {row}")
                return
            
            # Convert date back to yyyy-MM-dd format
            try:
                date = datetime.strptime(record[0], "%d/%m/%Y").strftime("%Y-%m-%d")
            except:
                date = datetime.now().strftime("%Y-%m-%d")
            record[0] = date
            
            # Get the treatment type from the table
            treatment = None
            for t, tab in tables.items():
                if tab == table:
                    treatment = t
                    break
            
            if not treatment:
                print("Warning: Could not determine treatment type")
                return
            
            # Ensure the data is in the correct order for the view dialog
            try:
                if treatment == "All":
                    # Reorder the data to match the expected format
                    reordered_record = [
                        date,  # Date
                        record[1] if len(record) > 1 else "",  # Type
                        record[2] if len(record) > 2 else "",  # Pet Name
                        record[3] if len(record) > 3 else "",  # Client Name
                        record[4] if len(record) > 4 else "",  # Reason
                        record[5] if len(record) > 5 else "",  # Diagnosis
                        record[6] if len(record) > 6 else "",  # Prescribed
                        record[7] if len(record) > 7 else ""   # Vet
                    ]
                else:
                    # Reorder the data to match the expected format
                    reordered_record = [
                        date,  # Date
                        treatment,  # Type
                        record[1] if len(record) > 1 else "",  # Pet Name
                        record[2] if len(record) > 2 else "",  # Client Name
                        record[3] if len(record) > 3 else "",  # Reason
                        record[4] if len(record) > 4 else "",  # Diagnosis
                        record[5] if len(record) > 5 else "",  # Prescribed
                        record[6] if len(record) > 6 else ""   # Vet
                    ]
                
                # Ensure we have all required fields
                while len(reordered_record) < 8:
                    reordered_record.append("")
                
                # Show the view dialog
                dialog = ViewReportDialog(reordered_record)
                dialog.exec()
                
            except Exception as e:
                print(f"Error processing report data: {e}")
                return
            
        except Exception as e:
            print(f"Error showing report details: {e}")

    # Connect cell click event for all tables
    for table in tables.values():
        table.cellClicked.connect(lambda row, col, t=table: handle_cell_click(row, col, t))

    def filter_tables(search_text):
        """Filter all tables based on search text."""
        nonlocal current_search
        current_search = search_text.lower()
        
        visible_rows = 0
        for table in tables.values():
            for row in range(table.rowCount()):
                show_row = False
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item and current_search in item.text().lower():
                        show_row = True
                        break
                table.setRowHidden(row, not show_row)
                if show_row:
                    visible_rows += 1

        # Update table headers to show search status
        for table in tables.values():
            header = table.horizontalHeader()
            if current_search:
                header.setStyleSheet("""
                    QHeaderView::section {
                        background-color: #FED766;
                        color: #000;
                        font-weight: bold;
                        height: 40px;
                    }
                """)
                # Add search indicator to header
                if visible_rows > 0:
                    header.setToolTip(f"Showing {visible_rows} results for '{current_search}'")
                else:
                    header.setToolTip(f"No results found for '{current_search}'")
            else:
                header.setStyleSheet("""
                    QHeaderView::section {
                        background-color: #FED766;
                        color: #000;
                        font-weight: bold;
                        height: 40px;
                    }
                """)
                header.setToolTip("")

    def open_report_form():
        dialog = ReportFormDialog()
        if dialog.exec():
            # Get form data
            date = dialog.date_edit.date().toString("yyyy-MM-dd")
            report_type = dialog.type_combo.currentText()
            pet_name_display = dialog.pet_name_combo.currentText().strip()
            reason = dialog.reason_input.toPlainText().strip()
            diagnosis = dialog.diagnosis_input.toPlainText().strip()
            prescribed = dialog.prescribed_input.toPlainText().strip()
            veterinarian = dialog.vet_combo.currentText().strip()

            # Extract actual pet name and client name
            parts = pet_name_display.split(" - ")
            if len(parts) >= 2:
                client_name = parts[0].strip()
                pet_name = parts[-1].strip()
            else:
                pet_name = pet_name_display.strip()
                client_name = ""

            # Validate data
            if not (pet_name and reason and veterinarian):
                show_message(dialog, "All fields are required!", QMessageBox.Warning)
                return

            # Save to database
            db = Database()
            try:
                # Get pet and client IDs
                db.cursor.execute("""
                    SELECT p.pet_id, c.client_id, c.name AS client_name
                    FROM pets p
                    JOIN clients c ON p.client_id = c.client_id
                    WHERE LOWER(p.name) = LOWER(?)
                """, (pet_name,))
                result = db.cursor.fetchone()

                if not result:
                    show_message(dialog, f"Pet '{pet_name}' not found!", QMessageBox.Warning)
                    return

                pet_id, client_id, client_name = result

                # Save medical record
                if db.save_medical_record(
                    pet_id, client_id, date, report_type, reason, diagnosis,
                    prescribed, veterinarian
                ):
                    # Refresh all tables with new data
                    refresh_tables()
                    
                    # Show the appropriate table based on the report type
                    if report_type in tables:
                        show_table(tables[report_type])
                        select_treatment(treatment_buttons[report_type])
                    else:
                        show_table(tables["All"])
                        select_treatment(treatment_buttons["All"])
                    
                    show_message(dialog, "Report added successfully!")
                else:
                    show_message(dialog, "Failed to save report!", QMessageBox.Critical)
            except Exception as e:
                show_message(dialog, f"Failed to save report: {e}", QMessageBox.Critical)
            finally:
                db.close_connection()
        else:
            print("Report creation cancelled")

    def refresh_tables():
        """Refresh all tables with data from the database."""
        db = Database()
        try:
            # Clear all tables
            for table in tables.values():
                table.setRowCount(0)

            # Fetch and populate data for each treatment type
            for treatment in treatments:
                records = db.fetch_medical_records(treatment if treatment != "All" else None)
                target_table = tables[treatment]
                
                for record in records:
                    row_position = target_table.rowCount()
                    target_table.insertRow(row_position)
                    
                    try:
                        # Format date to dd/MM/yyyy
                        date = datetime.strptime(record[0], "%Y-%m-%d").strftime("%d/%m/%Y")
                        
                        # Ensure veterinarian name has Dr. prefix
                        vet_name = record[7]
                        if not vet_name.startswith("Dr. "):
                            vet_name = f"Dr. {vet_name}"
                        
                        # Add items to table
                        target_table.setItem(row_position, 0, QTableWidgetItem(date))  # Date
                        if treatment == "All":
                            target_table.setItem(row_position, 1, QTableWidgetItem(record[1]))  # Type
                            target_table.setItem(row_position, 2, QTableWidgetItem(record[2]))  # Pet Name
                            target_table.setItem(row_position, 3, QTableWidgetItem(record[3]))  # Client Name
                            target_table.setItem(row_position, 4, QTableWidgetItem(record[4]))  # Reason
                            target_table.setItem(row_position, 5, QTableWidgetItem(record[5]))  # Diagnosis
                            target_table.setItem(row_position, 6, QTableWidgetItem(record[6]))  # Prescribed
                            target_table.setItem(row_position, 7, QTableWidgetItem(vet_name))  # Vet
                        else:
                            target_table.setItem(row_position, 0, QTableWidgetItem(date))  # Date
                            target_table.setItem(row_position, 1, QTableWidgetItem(record[2]))  # Pet Name
                            target_table.setItem(row_position, 2, QTableWidgetItem(record[3]))  # Client Name
                            target_table.setItem(row_position, 3, QTableWidgetItem(record[4]))  # Reason
                            target_table.setItem(row_position, 4, QTableWidgetItem(record[5]))  # Diagnosis
                            target_table.setItem(row_position, 5, QTableWidgetItem(record[6]))  # Prescribed
                            target_table.setItem(row_position, 6, QTableWidgetItem(vet_name))  # Vet

                            # Add action buttons for non-All tables
                            action_widget = QWidget()
                            action_layout = QHBoxLayout(action_widget)
                            action_layout.setContentsMargins(0, 0, 0, 0)
                            action_layout.setSpacing(5)

                            edit_button = QPushButton("Edit")
                            edit_button.setFixedWidth(70)
                            edit_button.setStyleSheet("""
                                QPushButton {
                                    background-color: #FED766;
                                    border: none;
                                    border-radius: 5px;
                                    font-size: 10px;
                                    padding: 2px 8px;
                                    min-height: 10px;
                                    min-width: 30px;
                                }
                                QPushButton:hover {
                                    background-color: #FFC107;
                                }
                            """)

                            delete_button = QPushButton("Delete")
                            delete_button.setFixedWidth(70)
                            delete_button.setStyleSheet("""
                                QPushButton {
                                    background-color: #FF6F61;
                                    border: none;
                                    border-radius: 5px;
                                    font-size: 10px;
                                    color: white;
                                    padding: 2px 8px;
                                    min-height: 10px;
                                    min-width: 30px;
                                }
                                QPushButton:hover {
                                    background-color: #E53935;
                                }
                            """)

                            # Connect button signals
                            edit_button.clicked.connect(lambda checked, r=row_position, t=treatment: handle_edit_action(r, t))
                            delete_button.clicked.connect(lambda checked, r=row_position, t=treatment: handle_delete_action(r, t))

                            action_layout.addWidget(edit_button)
                            action_layout.addWidget(delete_button)
                            action_widget.setLayout(action_layout)
                            target_table.setCellWidget(row_position, 7, action_widget)

                    except Exception as e:
                        print(f"Error adding row to table: {e}")
        except Exception as e:
            print(f"Error refreshing tables: {e}")
        finally:
            db.close_connection()
            
        # Reapply current search filter after refresh
        if current_search:
            filter_tables(current_search)

    def handle_edit_action(row, treatment):
        """Handle edit button click in the action buttons."""
        try:
            table = tables[treatment]
            record = []
            
            # Get all data from the row
            for i in range(table.columnCount() - 1):  # Exclude action column
                item = table.item(row, i)
                if item:
                    record.append(item.text())
                else:
                    record.append("")
            
            # Convert date back to yyyy-MM-dd format
            date = datetime.strptime(record[0], "%d/%m/%Y").strftime("%Y-%m-%d")
            record[0] = date
            
            # Show the edit dialog
            dialog = ReportFormDialog()
            
            # Set the form data
            dialog.date_edit.setDate(QDate.fromString(record[0], "yyyy-MM-dd"))
            dialog.type_combo.setCurrentText(record[1])
            dialog.pet_name_combo.setCurrentText(f"{record[3]} - {record[2]}")
            dialog.reason_input.setPlainText(record[4])
            dialog.diagnosis_input.setPlainText(record[5])
            dialog.prescribed_input.setPlainText(record[6])
            dialog.vet_combo.setCurrentText(record[7])
            
            if dialog.exec():
                # Save changes to the database
                db = Database()
                try:
                    db.cursor.execute("""
                        UPDATE medical_records
                        SET date = ?, type = ?, reason = ?, diagnosis = ?, prescribed = ?, veterinarian = ?
                        WHERE date = ? AND reason = ?
                    """, (
                        dialog.date_edit.date().toString("yyyy-MM-dd"),
                        dialog.type_combo.currentText(),
                        dialog.reason_input.toPlainText().strip(),
                        dialog.diagnosis_input.toPlainText().strip(),
                        dialog.prescribed_input.toPlainText().strip(),
                        dialog.vet_combo.currentText().strip(),
                        record[0],  # Original date
                        record[4]   # Original reason
                    ))
                    db.conn.commit()
                    QMessageBox.information(None, "Success", "Report updated successfully!")

                    # Refresh the table
                    refresh_tables()
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"Failed to update report: {e}")
                finally:
                    db.close_connection()
                
        except Exception as e:
            print(f"Error editing report: {e}")

    def handle_delete_action(row, treatment):
        """Handle delete button click in the action buttons."""
        try:
            table = tables[treatment]
            record = []
            
            # Get all data from the row
            for i in range(table.columnCount() - 1):  # Exclude action column
                item = table.item(row, i)
                if item:
                    record.append(item.text())
                else:
                    record.append("")
            
            # Convert date back to yyyy-MM-dd format
            date = datetime.strptime(record[0], "%d/%m/%Y").strftime("%Y-%m-%d")
            
            confirmation = QMessageBox.question(
                None,
                "Delete Confirmation",
                "Are you sure you want to delete this report?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirmation == QMessageBox.Yes:
                # Delete the report from the database
                db = Database()
                try:
                    db.cursor.execute("""
                        DELETE FROM medical_records
                        WHERE date = ? AND reason = ?
                    """, (date, record[4]))
                    db.conn.commit()
                    QMessageBox.information(None, "Success", "Report deleted successfully!")

                    # Refresh the table
                    refresh_tables()
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"Failed to delete report: {e}")
                finally:
                    db.close_connection()
                
        except Exception as e:
            print(f"Error deleting report: {e}")

    # Initial load of data
    refresh_tables()

    add_report_button.clicked.connect(open_report_form)

    # Store the filter function in the content widget for external access
    content.filter_tables = filter_tables

    def save_pdf():
        # Detect which table is visible
        table = None
        table_type = "All"
        for treatment, t in tables.items():
            if t.isVisible():
                table = t
                table_type = treatment
                break

        if not table:
            return

        # Define the output folder relative to the project
        folder_path = os.path.join(os.getcwd(), "pdf_reports")
        os.makedirs(folder_path, exist_ok=True)  # Create folder if not exists

        # Create file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{table_type}_Reports_{timestamp}.pdf"
        file_path = os.path.join(folder_path, file_name)

        # Create PDF in landscape mode
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        # Swap width and height for landscape
        width, height = height, width
        c.setPageSize((width, height))

        # Get clinic information from database
        db = Database()
        clinic_info = None
        try:
            clinic_info = db.get_clinic_info()
        except Exception as e:
            print(f"Error fetching clinic info: {e}")
        finally:
            db.close_connection()

        # Set up margins and spacing
        x_margin = 50
        y_margin = 50
        row_height = 25
        header_height = 100

        # Draw header
        # Clinic Logo (if available)
        logo_path = "assets/logologin.png"
        if os.path.exists(logo_path):
            c.drawImage(logo_path, x_margin, height - y_margin - 50, width=50, height=50)

        # Clinic Information
        if clinic_info:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(x_margin + 60, height - y_margin - 20, clinic_info.get("name", "PetMedix Animal Clinic"))
            c.setFont("Helvetica", 12)
            c.drawString(x_margin + 60, height - y_margin - 40, clinic_info.get("address", ""))
            c.drawString(x_margin + 60, height - y_margin - 60, f"Contact: {clinic_info.get('contact_number', '')}")

        # Report Title and Date
        c.setFont("Helvetica-Bold", 14)
        c.drawString(width - 250, height - y_margin - 20, f"{table_type} Reports")
        c.setFont("Helvetica", 12)
        c.drawString(width - 250, height - y_margin - 40, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # Draw a line under the header
        c.setStrokeColorRGB(0.003922, 0.145098, 0.278431)  # #012547 in RGB
        c.line(x_margin, height - y_margin - header_height, width - x_margin, height - y_margin - header_height)

        # Table headers - exclude action column
        y_start = height - y_margin - header_height - 30
        headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount() - 1)]  # Exclude action column
        
        # Calculate column widths based on content
        col_widths = []
        total_width = width - (2 * x_margin)
        for i in range(table.columnCount() - 1):  # Exclude action column
            # Get the maximum width needed for this column
            header_width = len(headers[i]) * 7  # Approximate width for header text
            content_width = 0
            for row in range(table.rowCount()):
                item = table.item(row, i)
                if item:
                    content_width = max(content_width, len(item.text()) * 7)
            col_widths.append(max(header_width, content_width) + 10)  # Add padding

        # Adjust column widths to fit page
        total_col_width = sum(col_widths)
        if total_col_width > total_width:
            ratio = total_width / total_col_width
            col_widths = [w * ratio for w in col_widths]

        # Draw table headers
        x_pos = x_margin
        c.setFont("Helvetica-Bold", 10)
        for i, header in enumerate(headers):
            c.drawString(x_pos + 5, y_start, header)
            x_pos += col_widths[i]

        # Draw table content
        c.setFont("Helvetica", 10)
        y_pos = y_start - row_height
        for row in range(table.rowCount()):
            # Check if we need a new page
            if y_pos < y_margin + row_height:
                c.showPage()
                # Redraw header on new page
                c.setFont("Helvetica-Bold", 16)
                c.drawString(x_margin + 60, height - y_margin - 20, clinic_info.get("name", "PetMedix Animal Clinic"))
                c.setFont("Helvetica-Bold", 14)
                c.drawString(width - 250, height - y_margin - 20, f"{table_type} Reports (continued)")
                c.setFont("Helvetica", 10)
                y_pos = height - y_margin - header_height - 30

            x_pos = x_margin
            for col in range(table.columnCount() - 1):  # Exclude action column
                item = table.item(row, col)
                if item:
                    # Draw text
                    c.drawString(x_pos + 5, y_pos, item.text())
                x_pos += col_widths[col]
            y_pos -= row_height

        # Add footer
        c.setFont("Helvetica", 8)
        c.drawString(x_margin, y_margin, f"Generated by PetMedix System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(width - x_margin - 100, y_margin, f"Page 1")

        c.save()
        QMessageBox.information(None, "PDF Saved", f"PDF successfully saved to:\n{file_path}")

    save_pdf_button.clicked.connect(save_pdf)

    return content