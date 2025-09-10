from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QDialog, QFormLayout, QLineEdit, QComboBox, QTextEdit, QDateEdit, QHeaderView,
    QMessageBox, QTableWidgetItem, QFileDialog, QStackedWidget
)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QColor, QBrush, QIcon, QPixmap
from modules.database import Database
from datetime import datetime
from modules.utils import show_message, create_styled_message_box
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
        row1_layout.setSpacing(10)
        
        # Date field
        date_label = QLabel("Date")
        date_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px;")
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
                margin-top: 2px;
                font-family: Lato;
            }
        """)
        
        date_container = QVBoxLayout()
        date_container.setSpacing(0)
        date_container.addWidget(date_label)
        date_container.addWidget(self.date_edit)
        
        # Type field
        type_label = QLabel("Type")
        type_label.setStyleSheet("font-size: 16px;font-family: Lato; font-weight: bold; margin-bottom: 5px;")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Consultation", "Deworming", "Vaccination", "Surgery", "Grooming", "Other Treatments"])
        self.type_combo.setMinimumHeight(40)
        self.type_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 2px;
                font-family: Lato;
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
        pet_name_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px;")
        self.pet_name_combo = QComboBox()
        self.pet_name_combo.setMinimumHeight(40)
        self.pet_name_combo.setPlaceholderText("Select Pet")
        self.pet_name_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 2px;
                font-family: Lato;
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
        
        # Dynamic Fields Container
        self.dynamic_fields_container = QWidget()
        self.dynamic_fields_layout = QVBoxLayout(self.dynamic_fields_container)
        self.dynamic_fields_layout.setSpacing(0)
        form_scroll_layout.addWidget(self.dynamic_fields_container)
        
        # Create field widgets but don't add them yet
        self.field_widgets = {}
        
        # Consultation fields
        self.field_widgets["Consultation"] = {
            "risk_status": self.create_risk_status_field(),
            "reason": self.create_text_field("Reason for Consultation", "Reason for Consultation"),
            "diagnosis": self.create_text_field("Diagnosis", "Diagnosis"),
            "prescribed": self.create_text_field("Prescribed Treatment/Medication", "Prescribed Treatment/Medication")
        }
        
        # Deworming fields
        self.field_widgets["Deworming"] = {
            "medication": self.create_text_field("Deworming Medication", "Deworming Medication"),
            "dosage": self.create_text_field("Dosage Administered", "Dosage Administered"),
            "next_date": self.create_date_field("Next Scheduled Deworming")
        }
        
        # Vaccination fields
        self.field_widgets["Vaccination"] = {
            "vaccine": self.create_text_field("Vaccine Administered", "Vaccine Administered"),
            "dosage": self.create_text_field("Dosage Administered", "Dosage Administered"),
            "next_date": self.create_date_field("Next Scheduled Vaccination")
        }
        
        # Surgery fields
        self.field_widgets["Surgery"] = {
            "risk_status": self.create_risk_status_field(),
            "surgery_type": self.create_text_field("Type of Surgery", "Type of Surgery"),
            "anesthesia": self.create_text_field("Anesthesia Used", "Anesthesia Used"),
            "next_followup": self.create_date_field("Next Follow-up Date")
        }
        
        # Grooming fields
        self.field_widgets["Grooming"] = {
            "services": self.create_text_field("Grooming Service/s Availed", "Grooming Service/s Availed"),
            "notes": self.create_text_field("Notes", "Notes"),
            "next_date": self.create_date_field("Next Grooming Date")
        }
        
        # Other Treatments fields
        self.field_widgets["Other Treatments"] = {
            "type": self.create_text_field("Treatment Type", "Treatment Type"),
            "medication": self.create_text_field("Medication/Procedure Used", "Medication/Procedure Used"),
            "dosage": self.create_text_field("Dosage/Duration", "Dosage/Duration")
        }
        
        # Row 6: Veterinarian/Staff In Charge
        vet_label = QLabel("Veterinarian/Staff In Charge")
        vet_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px; margin-top: 5px;")
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
                font-family: Lato;
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
                font-family: Lato;
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
                font-family: Lato;
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
        
        # Connect type combo box to update fields
        self.type_combo.currentTextChanged.connect(self.update_form_fields)
        
        # Show initial fields
        self.update_form_fields(self.type_combo.currentText())

    def create_text_field(self, label_text, placeholder):
        """Create a text field with label and placeholder."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(0)
        label = QLabel(label_text)
        label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px;")
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(placeholder)
        text_edit.setFixedHeight(50)
        text_edit.setStyleSheet("""
            QTextEdit {
                padding: 3px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 15px;
                color: #000;
                margin-top: 8px;
                font-family: Lato;
            }
        """)
        layout.addWidget(label)
        layout.addWidget(text_edit)
        return container, text_edit

    def create_date_field(self, label_text):
        """Create a date field with label."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(0)
        label = QLabel(label_text)
        label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px;")
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        date_edit.setDisplayFormat("dd/MM/yyyy")
        date_edit.setMinimumHeight(40)
        date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
                font-family: Lato;
            }
        """)
        layout.addWidget(label)
        layout.addWidget(date_edit)
        return container, date_edit

    def create_risk_status_field(self):
        """Create a risk status field with a combo box."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(0)
        label = QLabel("Risk Status")
        label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px;")
        combo = QComboBox()
        combo.addItem("Select Risk Status")  # Add placeholder
        combo.addItems(["Low Risk", "Medium Risk", "High Risk"])
        combo.setMinimumHeight(40)
        combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
                font-family: Lato;
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
        layout.addWidget(label)
        layout.addWidget(combo)
        return container, combo

    def update_form_fields(self, treatment_type):
        """Update form fields based on selected treatment type."""
        # Remove all widgets from the dynamic fields layout
        while self.dynamic_fields_layout.count():
            item = self.dynamic_fields_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                layout = item.layout()
                while layout.count():
                    sub_item = layout.takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().setParent(None)
                        sub_item.widget().deleteLater()
                QWidget().setLayout(layout)

        # Add new fields based on treatment type
        if treatment_type in self.field_widgets:
            for field_widget, _ in self.field_widgets[treatment_type].values():
                self.dynamic_fields_layout.addWidget(field_widget)

        # Force update of the container to prevent stacking
        self.dynamic_fields_container.update()
        # Adjust the dialog size to fit the content
        self.adjustSize()

    def get_form_data(self):
        """Get all form data as a dictionary."""
        treatment_type = self.type_combo.currentText()
        data = {
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "type": treatment_type,
            "pet_name": self.pet_name_combo.currentText().strip(),
            "veterinarian": self.vet_combo.currentText().strip()
        }
        
        # Get dynamic field values based on treatment type
        if treatment_type in self.field_widgets:
            for field_name, (_, widget) in self.field_widgets[treatment_type].items():
                if isinstance(widget, QTextEdit):
                    if treatment_type == "Consultation":
                        data[field_name] = widget.toPlainText().strip()
                    elif treatment_type == "Deworming":
                        if field_name == "medication":
                            data["reason"] = widget.toPlainText().strip()
                        elif field_name == "dosage":
                            data["diagnosis"] = widget.toPlainText().strip()
                        elif field_name == "next_date":
                            data["prescribed"] = widget.toPlainText().strip()
                    elif treatment_type == "Vaccination":
                        if field_name == "vaccine":
                            data["reason"] = widget.toPlainText().strip()
                        elif field_name == "dosage":
                            data["diagnosis"] = widget.toPlainText().strip()
                        elif field_name == "next_date":
                            data["prescribed"] = widget.toPlainText().strip()
                    elif treatment_type == "Surgery":
                        if field_name == "surgery_type":
                            data["reason"] = widget.toPlainText().strip()
                        elif field_name == "anesthesia":
                            data["diagnosis"] = widget.toPlainText().strip()
                        elif field_name == "next_followup":
                            data["prescribed"] = widget.toPlainText().strip()
                    elif treatment_type == "Grooming":
                        if field_name == "services":
                            data["reason"] = widget.toPlainText().strip()
                        elif field_name == "notes":
                            data["diagnosis"] = widget.toPlainText().strip()
                        elif field_name == "next_date":
                            data["prescribed"] = widget.toPlainText().strip()
                    elif treatment_type == "Other Treatments":
                        if field_name == "type":
                            data["reason"] = widget.toPlainText().strip()
                        elif field_name == "medication":
                            data["diagnosis"] = widget.toPlainText().strip()
                        elif field_name == "dosage":
                            data["prescribed"] = widget.toPlainText().strip()
                elif isinstance(widget, QDateEdit):
                    if treatment_type == "Deworming" and field_name == "next_date":
                        data["prescribed"] = widget.date().toString("yyyy-MM-dd")
                    elif treatment_type == "Vaccination" and field_name == "next_date":
                        data["prescribed"] = widget.date().toString("yyyy-MM-dd")
                    elif treatment_type == "Surgery" and field_name == "next_followup":
                        data["prescribed"] = widget.date().toString("yyyy-MM-dd")
                    elif treatment_type == "Grooming" and field_name == "next_date":
                        data["prescribed"] = widget.date().toString("yyyy-MM-dd")
                elif isinstance(widget, QComboBox) and field_name == "risk_status":
                    data["risk_status"] = widget.currentText()
        
        return data

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
            """
            )
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

            # Store current selection
            current_vet = self.vet_combo.currentText()

            # Clear existing items first
            self.vet_combo.clear()

            # Add placeholder first
            self.vet_combo.addItem("Select Veterinarian")

            cursor.execute("""
                SELECT DISTINCT name
                FROM users
                WHERE role = 'Veterinarian'
                ORDER BY name ASC
            """)
            rows = cursor.fetchall()

            if not rows:
                self.vet_combo.addItem("No veterinarians found")
                return

            for row in rows:
                vet_name = row[0].strip()  # Remove any whitespace
                if vet_name:  # Only add if name is not empty
                    if not vet_name.startswith("Dr. "):
                        vet_name = f"Dr. {vet_name}"
                    self.vet_combo.addItem(vet_name)

            # Restore previous selection if it exists and is not the placeholder
            if current_vet and current_vet != "Select Veterinarian":
                index = self.vet_combo.findText(current_vet)
                if index >= 0:
                    self.vet_combo.setCurrentIndex(index)
                else:
                    # If not found in the list, add it and select it
                    # Only add Dr. prefix if it's not already there and not the placeholder
                    if not current_vet.startswith("Dr. ") and current_vet != "Select Veterinarian":
                        current_vet = f"Dr. {current_vet}"
                    self.vet_combo.addItem(current_vet)
                    self.vet_combo.setCurrentText(current_vet)

            db.close_connection()
        except Exception as e:
            print("Failed to load veterinarian names:", e)
            self.vet_combo.clear()
            self.vet_combo.addItem("Error loading veterinarians")

    def set_pet_name_for_edit(self, client_name, pet_name):
        """Set the pet_name_combo to a single, non-editable value for editing (pet name only)."""
        self.pet_name_combo.clear()
        self.pet_name_combo.addItem(pet_name)
        self.pet_name_combo.setCurrentIndex(0)
        self.pet_name_combo.setEnabled(False)

    def create_surgery_fields(self):
        """Create fields specific to surgery reports"""
        # Surgery Type
        surgery_type_label = QLabel("Type of Surgery:")
        self.surgery_type = QLineEdit()
        self.surgery_type.setPlaceholderText("Enter type of surgery")
        self.form_layout.addRow(surgery_type_label, self.surgery_type)
        
        # Risk Status
        risk_status_label = QLabel("Risk Status:")
        self.risk_status = QComboBox()
        self.risk_status.addItems(["Low Risk", "Medium Risk", "High Risk"])
        self.form_layout.addRow(risk_status_label, self.risk_status)
        
        # Anesthesia
        anesthesia_label = QLabel("Anesthesia Used:")
        self.anesthesia = QLineEdit()
        self.anesthesia.setPlaceholderText("Enter anesthesia details")
        self.form_layout.addRow(anesthesia_label, self.anesthesia)
        
        # Next Follow-up
        followup_label = QLabel("Next Follow-up:")
        self.followup = QDateEdit()
        self.followup.setCalendarPopup(True)
        self.followup.setDate(QDate.currentDate().addDays(7))
        self.form_layout.addRow(followup_label, self.followup)


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
        date_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px;")
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
                font-family: Lato;
            }
        """)
        
        date_container = QVBoxLayout()
        date_container.setSpacing(0)
        date_container.addWidget(date_label)
        date_container.addWidget(self.date_edit)
        
        # Type field
        type_label = QLabel("Type")
        type_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px;")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Consultation", "Deworming", "Vaccination", "Surgery", "Grooming", "Other Treatments"])
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
                font-family: Lato;
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
        pet_name_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px;")
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
                margin-top: 2px;
                font-family: Lato;
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
        
        # Dynamic Fields based on treatment type
        self.field1_label = QLabel()
        self.field1_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px;")
        self.field1_input = QTextEdit()
        self.field1_input.setReadOnly(True)
        self.field1_input.setFixedHeight(60)
        self.field1_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
                font-family: Lato;
            }
        """)
        
        field1_container = QVBoxLayout()
        field1_container.setSpacing(0)
        field1_container.addWidget(self.field1_label)
        field1_container.addWidget(self.field1_input)
        form_scroll_layout.addLayout(field1_container)
        
        self.field2_label = QLabel()
        self.field2_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px; margin-top: 5px;")
        self.field2_input = QTextEdit()
        self.field2_input.setReadOnly(True)
        self.field2_input.setFixedHeight(60)
        self.field2_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
                font-family: Lato;
            }
        """)
        
        field2_container = QVBoxLayout()
        field2_container.setSpacing(0)
        field2_container.addWidget(self.field2_label)
        field2_container.addWidget(self.field2_input)
        form_scroll_layout.addLayout(field2_container)
        
        self.field3_label = QLabel()
        self.field3_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px; margin-top: 5px;")
        self.field3_input = QTextEdit()
        self.field3_input.setReadOnly(True)
        self.field3_input.setFixedHeight(60)
        self.field3_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
                font-family: Lato;
            }
        """)
        
        field3_container = QVBoxLayout()
        field3_container.setSpacing(0)
        field3_container.addWidget(self.field3_label)
        field3_container.addWidget(self.field3_input)
        form_scroll_layout.addLayout(field3_container)
        
        # Add field4 for Risk Status
        self.field4_label = QLabel()
        self.field4_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px; margin-top: 5px;")
        self.field4_input = QTextEdit()
        self.field4_input.setReadOnly(True)
        self.field4_input.setFixedHeight(60)
        self.field4_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 8px;
                font-family: Lato;
            }
        """)
        
        field4_container = QVBoxLayout()
        field4_container.setSpacing(0)
        field4_container.addWidget(self.field4_label)
        field4_container.addWidget(self.field4_input)
        form_scroll_layout.addLayout(field4_container)
        
        # Row 6: Veterinarian/Staff In Charge
        vet_label = QLabel("Veterinarian/Staff In Charge")
        vet_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; margin-bottom: 5px; margin-top: 5px;")
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
                font-family: Lato;
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
                font-family: Lato;
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
            while len(data) < 8:  # Updated to match new data structure
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
                    
                    # Set field labels based on treatment type
                    if data[1] == "Consultation":
                        print("Debug - Setting Consultation Data:", data)  # Debug print
                        self.field1_label.setText("Risk Status")
                        self.field1_input.setPlainText(data[3] if len(data) > 3 else "Low Risk")
                        self.field2_label.setText("Reason for Consultation")
                        self.field2_input.setPlainText(data[4])
                        self.field3_label.setText("Diagnosis")
                        self.field3_input.setPlainText(data[5])
                        self.field4_label.setText("Prescribed Treatment/Medication")
                        self.field4_input.setPlainText(data[6])
                    elif data[1] == "Deworming":
                        self.field1_label.setText("Deworming Medication")
                        self.field1_input.setPlainText(data[4])
                        self.field2_label.setText("Dosage Administered")
                        self.field2_input.setPlainText(data[5])
                        self.field3_label.setText("Next Scheduled Deworming")
                        self.field3_input.setPlainText(data[6])
                        self.field4_label.hide()
                        self.field4_input.hide()
                    elif data[1] == "Vaccination":
                        self.field1_label.setText("Vaccine Administered")
                        self.field1_input.setPlainText(data[4])
                        self.field2_label.setText("Dosage Administered")
                        self.field2_input.setPlainText(data[5])
                        self.field3_label.setText("Next Scheduled Vaccination")
                        self.field3_input.setPlainText(data[6])
                        self.field4_label.hide()
                        self.field4_input.hide()
                    elif data[1] == "Surgery":
                        self.field1_label.setText("Risk Status")
                        self.field1_input.setPlainText(data[3] if len(data) > 3 else "Low Risk")
                        self.field2_label.setText("Type of Surgery")
                        self.field2_input.setPlainText(data[4])
                        self.field3_label.setText("Anesthesia Used")
                        self.field3_input.setPlainText(data[5])
                        self.field4_label.setText("Next Follow-up Date")
                        self.field4_input.setPlainText(data[6])
                        self.field4_label.show()
                        self.field4_input.show()
                    elif data[1] == "Grooming":
                        self.field1_label.setText("Grooming Service/s Availed")
                        self.field1_input.setPlainText(data[4])
                        self.field2_label.setText("Notes")
                        self.field2_input.setPlainText(data[5])
                        self.field3_label.setText("Next Grooming Date")
                        self.field3_input.setPlainText(data[6])
                        self.field4_label.hide()
                        self.field4_input.hide()
                    elif data[1] == "Other Treatments":
                        self.field1_label.setText("Treatment Type")
                        self.field1_input.setPlainText(data[4])
                        self.field2_label.setText("Medication/Procedure Used")
                        self.field2_input.setPlainText(data[5])
                        self.field3_label.setText("Dosage/Duration")
                        self.field3_input.setPlainText(data[6])
                        self.field4_label.hide()
                        self.field4_input.hide()
            
            # Set pet name
            if data[2]:  # Pet name is at index 2
                self.pet_name_combo.clear()  # Clear existing items
                self.pet_name_combo.addItem(data[2])  # Add only pet name
            
            # Set other fields
            if data[1] == "Consultation":
                print("Debug - Setting Consultation Data:", data)  # Debug print
                self.field1_label.setText("Risk Status")
                self.field1_input.setPlainText(data[3] if len(data) > 3 else "Low Risk")
                self.field2_label.setText("Reason for Consultation")
                self.field2_input.setPlainText(data[4])
                self.field3_label.setText("Diagnosis")
                self.field3_input.setPlainText(data[5])
                self.field4_label.setText("Prescribed Treatment/Medication")
                self.field4_input.setPlainText(data[6])
            elif data[1] == "Deworming":
                self.field1_label.setText("Deworming Medication")
                self.field1_input.setPlainText(data[4])
                self.field2_label.setText("Dosage Administered")
                self.field2_input.setPlainText(data[5])
                self.field3_label.setText("Next Scheduled Deworming")
                self.field3_input.setPlainText(data[6])
            elif data[1] == "Vaccination":
                self.field1_label.setText("Vaccine Administered")
                self.field1_input.setPlainText(data[4])
                self.field2_label.setText("Dosage Administered")
                self.field2_input.setPlainText(data[5])
                self.field3_label.setText("Next Scheduled Vaccination")
                self.field3_input.setPlainText(data[6])
            elif data[1] == "Surgery":
                self.field1_label.setText("Risk Status")
                self.field1_input.setPlainText(data[3] if len(data) > 3 else "Low Risk")
                self.field2_label.setText("Type of Surgery")
                self.field2_input.setPlainText(data[4])
                self.field3_label.setText("Anesthesia Used")
                self.field3_input.setPlainText(data[5])
                self.field4_label.setText("Next Follow-up Date")
                self.field4_input.setPlainText(data[6])
                self.field4_label.show()
                self.field4_input.show()
            elif data[1] == "Grooming":
                self.field1_label.setText("Grooming Service/s Availed")
                self.field1_input.setPlainText(data[4])
                self.field2_label.setText("Notes")
                self.field2_input.setPlainText(data[5])
                self.field3_label.setText("Next Grooming Date")
                self.field3_input.setPlainText(data[6])
                self.field4_label.hide()
                self.field4_input.hide()
            elif data[1] == "Other Treatments":
                self.field1_label.setText("Treatment Type")
                self.field2_label.setText("Medication/Procedure Used")
                self.field3_label.setText("Dosage/Duration")
            
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

def get_report_widget(user_role):
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
        "background-color: #F4F4F8; font-family: Lato; border: none; border-radius: 20px; margin-bottom: 5px;"
    )
    
    # Hide the Add Report button if the user is a receptionist
    if user_role.lower() == "receptionist":
        add_report_button.hide()

    # Save PDF Button
    save_pdf_button = QPushButton("Save PDF")
    save_pdf_button.setObjectName("SavePDFButton")
    save_pdf_button.setFixedSize(120, 40)
    save_pdf_button.setStyleSheet(
        "background-color: #F4F4F8; font-family: Lato; border: none; border-radius: 20px; margin-bottom: 5px;"
    )
    
    # Hide the button if the user is not a receptionist
    if user_role.lower() != "receptionist":
        save_pdf_button.hide()

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
            font-family: Lato;
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
            font-family: Lato;
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
        "Consultation",
        "Deworming",
        "Vaccination",
        "Surgery",
        "Grooming",
        "Other Treatments"
    ]

    treatment_widths = {
        "Consultation": 100,
        "Deworming": 100,
        "Vaccination": 100,
        "Surgery": 100,
        "Grooming": 100,
        "Other Treatments": 150
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
                min-width: """ + str(treatment_widths[treatment]) + """px;
            }
            QPushButton:hover {
                background-color: #FED766;
            }
            QPushButton[selected="true"] {
                background-color: #FED766;
                outline: none;
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
        if treatment == "Consultation":
            table.setColumnCount(9)  # Increased to 9 columns
            table.setHorizontalHeaderLabels([
                "Consultation Date", "Pet Name", "Owner/Client", "Risk Status",
                "Reason for Consultation", "Diagnosis", "Prescribed Treatment/Medication", "Veterinarian", "Action"
            ])
        elif treatment == "Deworming":
            table.setColumnCount(8)
            table.setHorizontalHeaderLabels([
                "Deworming Date", "Pet Name", "Owner/Client", "Deworming Medication",
                "Dosage Administered", "Next Scheduled Deworming", "Veterinarian", "Action"
            ])
        elif treatment == "Vaccination":
            table.setColumnCount(8)
            table.setHorizontalHeaderLabels([
                "Vaccination Date", "Pet Name", "Owner/Client", "Vaccine Administered",
                "Dosage Administered", "Next Scheduled Vaccination", "Veterinarian", "Action"
            ])
        elif treatment == "Surgery":
            table.setColumnCount(9)  # 9 columns: 8 data + 1 action
            table.setHorizontalHeaderLabels([
                "Surgery Date", "Pet Name", "Owner/Client", "Risk Status",
                "Type of Surgery", "Anesthesia Used", "Next Follow-up Date", "Veterinarian", "Action"
            ])
        elif treatment == "Grooming":
            table.setColumnCount(8)
            table.setHorizontalHeaderLabels([
                "Grooming Date", "Pet Name", "Owner/Client", "Grooming Service/s Availed",
                "Notes", "Next Grooming Date", "Veterinarian", "Action"
            ])
        elif treatment == "Other Treatments":
            table.setColumnCount(8)
            table.setHorizontalHeaderLabels([
                "Treatment Date", "Pet Name", "Owner/Client", "Treatment Type",
                "Medication/Procedure Used", "Dosage/Duration", "Veterinarian", "Action"
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
                padding: 5px;
                text-align: center;
                font-family: Lato;
            }
        """)
        table.verticalHeader().setVisible(False)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set column widths based on treatment type
        if treatment == "Consultation":
            # Column widths in order: Date, Pet Name, Owner/Client, Risk Status, Reason, Diagnosis, Prescribed, Vet, Action
            column_widths = [
                120,  # Consultation Date
                120,  # Pet Name
                150,  # Owner/Client
                100,  # Risk Status
                180,  # Reason for Consultation
                150,  # Diagnosis
                200,  # Prescribed Treatment/Medication
                100,  # Veterinarian
                140   # Action
            ]
            for i, width in enumerate(column_widths):
                table.setColumnWidth(i, width)
                # Center align the header
                header_item = table.horizontalHeaderItem(i)
                if header_item:
                    header_item.setTextAlignment(Qt.AlignCenter)
        elif treatment == "Deworming":
            for i, width in enumerate([150, 120, 150, 180, 150, 180, 150, 100]):
                table.setColumnWidth(i, width)
                header_item = table.horizontalHeaderItem(i)
                if header_item:
                    header_item.setTextAlignment(Qt.AlignCenter)
        elif treatment == "Vaccination":
            for i, width in enumerate([150, 120, 150, 180, 150, 180, 150, 100]):
                table.setColumnWidth(i, width)
                header_item = table.horizontalHeaderItem(i)
                if header_item:
                    header_item.setTextAlignment(Qt.AlignCenter)
        elif treatment == "Surgery":
            for i, width in enumerate([120, 120, 150, 100, 180, 180, 180, 100, 140]):
                table.setColumnWidth(i, width)
                header_item = table.horizontalHeaderItem(i)
                if header_item:
                    header_item.setTextAlignment(Qt.AlignCenter)
        elif treatment == "Grooming":
            for i, width in enumerate([150, 120, 150, 200, 180, 180, 150, 100]):
                table.setColumnWidth(i, width)
                header_item = table.horizontalHeaderItem(i)
                if header_item:
                    header_item.setTextAlignment(Qt.AlignCenter)
        elif treatment == "Other Treatments":
            for i, width in enumerate([150, 120, 150, 180, 200, 180, 150, 100]):
                table.setColumnWidth(i, width)
                header_item = table.horizontalHeaderItem(i)
                if header_item:
                    header_item.setTextAlignment(Qt.AlignCenter)

        tables[treatment] = table
        layout.addWidget(table)
        if treatment != "Consultation":
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
    tables["Consultation"].show()
    select_treatment(treatment_buttons["Consultation"])

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
                if treatment == "Consultation":
                    # Reorder the data to match the expected format
                    reordered_record = [
                        date,  # Date [0]
                        treatment,  # Type [1]
                        record[1] if len(record) > 1 else "",  # Pet Name [2]
                        record[3] if len(record) > 3 else "Low Risk",  # Risk Status [3]
                        record[4] if len(record) > 4 else "",  # Reason [4]
                        record[5] if len(record) > 5 else "",  # Diagnosis [5]
                        record[6] if len(record) > 6 else "",  # Prescribed [6]
                        record[7] if len(record) > 7 else ""   # Vet [7]
                    ]
                    
                    print("Debug - Reordered Record:", reordered_record)  # Debug print
                elif treatment == "Surgery":
                    # Final mapping for Surgery
                    reordered_record = [
                        date,  # Date [0]
                        treatment,  # Type [1]
                        record[1] if len(record) > 1 else "",  # Pet Name [2]
                        record[3] if len(record) > 3 else "Low Risk",  # Risk Status [3]
                        record[4] if len(record) > 4 else "",  # Type of Surgery [4]
                        record[5] if len(record) > 5 else "",  # Anesthesia Used [5]
                        record[6] if len(record) > 6 else "",  # Next Follow-up Date [6]
                        record[7] if len(record) > 7 else ""   # Veterinarian [7]
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
                        font-family: Lato;
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
                        font-family: Lato;
                    }
                """)
                header.setToolTip("")

    def open_report_form(treatment_type):
        """Open the report form dialog."""
        dialog = ReportFormDialog()
        if dialog.exec_() == QDialog.Accepted:
            # Get form data
            form_data = dialog.get_form_data()
            print("\n=== Debug: Form Data ===")
            print(f"Treatment Type: {treatment_type}")
            print(f"Form Data: {form_data}")
            
            # Extract pet name and client name
            pet_name_display = form_data["pet_name"]
            parts = pet_name_display.split(" - ")
            if len(parts) >= 2:
                client_name = parts[0].strip()
                pet_name = parts[-1].strip()
            else:
                pet_name = pet_name_display.strip()
                client_name = ""

            print(f"\n=== Debug: Extracted Names ===")
            print(f"Pet Name: {pet_name}")
            print(f"Client Name: {client_name}")

            # Validate data
            if not (pet_name and form_data["veterinarian"]):
                error_msg = create_styled_message_box(
                    QMessageBox.Warning,
                    "Error",
                    "Pet name and veterinarian are required!"
                )
                error_msg.setStandardButtons(QMessageBox.Ok)
                error_msg.exec()
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
                    error_msg = create_styled_message_box(
                        QMessageBox.Warning,
                        "Error",
                        f"Pet '{pet_name}' not found!"
                    )
                    error_msg.setStandardButtons(QMessageBox.Ok)
                    error_msg.exec()
                    return

                pet_id, client_id, client_name = result
                print(f"\n=== Debug: Database IDs ===")
                print(f"Pet ID: {pet_id}")
                print(f"Client ID: {client_id}")

                # Validate required fields based on treatment type
                missing_fields = []
                treatment_type = form_data["type"]
                
                if treatment_type == "Consultation":
                    if not form_data.get("reason", "").strip():
                        missing_fields.append("Reason for Consultation")
                    if not form_data.get("diagnosis", "").strip():
                        missing_fields.append("Diagnosis")
                    if not form_data.get("prescribed", "").strip():
                        missing_fields.append("Prescribed Treatment")
                elif treatment_type == "Deworming":
                    if not form_data.get("reason", "").strip():
                        missing_fields.append("Deworming Medication")
                    if not form_data.get("diagnosis", "").strip():
                        missing_fields.append("Dosage Administered")
                    if not form_data.get("prescribed", "").strip():
                        missing_fields.append("Next Scheduled Deworming")
                elif treatment_type == "Vaccination":
                    if not form_data.get("reason", "").strip():
                        missing_fields.append("Vaccine Administered")
                    if not form_data.get("diagnosis", "").strip():
                        missing_fields.append("Dosage Administered")
                    if not form_data.get("prescribed", "").strip():
                        missing_fields.append("Next Scheduled Vaccination")
                elif treatment_type == "Surgery":
                    if not form_data.get("reason", "").strip():
                        missing_fields.append("Type of Surgery")
                    if not form_data.get("diagnosis", "").strip():
                        missing_fields.append("Anesthesia Used")
                    if not form_data.get("prescribed", "").strip():
                        missing_fields.append("Next Follow-up Date")
                elif treatment_type == "Grooming":
                    if not form_data.get("reason", "").strip():
                        missing_fields.append("Grooming Services")
                    if not form_data.get("diagnosis", "").strip():
                        missing_fields.append("Notes")
                    if not form_data.get("prescribed", "").strip():
                        missing_fields.append("Next Grooming Date")
                elif treatment_type == "Other Treatments":
                    if not form_data.get("reason", "").strip():
                        missing_fields.append("Treatment Type")
                    if not form_data.get("diagnosis", "").strip():
                        missing_fields.append("Medication/Procedure")
                    if not form_data.get("prescribed", "").strip():
                        missing_fields.append("Dosage/Duration")

                if missing_fields:
                    error_msg = create_styled_message_box(
                        QMessageBox.Warning,
                        "Error",
                        f"Please fill in the following fields:\n{', '.join(missing_fields)}"
                    )
                    error_msg.setStandardButtons(QMessageBox.Ok)
                    error_msg.exec()
                    return

                # Save medical record
                if db.save_medical_record(
                    pet_id, client_id, form_data["date"], treatment_type, 
                    form_data.get("reason", ""), form_data.get("diagnosis", ""),
                    form_data.get("prescribed", ""), form_data["veterinarian"],
                    form_data.get("risk_status", "Low Risk")  # Add risk_status parameter
                ):
                    # Refresh all tables with new data
                    refresh_tables()
                    
                    # Show the appropriate table based on the report type
                    if treatment_type in tables:
                        show_table(tables[treatment_type])
                        select_treatment(treatment_buttons[treatment_type])
                    
                    success_msg = create_styled_message_box(
                        QMessageBox.Information,
                        "Success",
                        "Report added successfully!"
                    )
                    success_msg.setStandardButtons(QMessageBox.Ok)
                    success_msg.exec()
                else:
                    error_msg = create_styled_message_box(
                        QMessageBox.Critical,
                        "Error",
                        "Failed to save report!"
                    )
                    error_msg.setStandardButtons(QMessageBox.Ok)
                    error_msg.exec()
            except Exception as e:
                print(f"\n=== Debug: Error ===")
                print(f"Error: {e}")
                error_msg = create_styled_message_box(
                    QMessageBox.Critical,
                    "Error",
                    f"Failed to save report: {e}"
                )
                error_msg.setStandardButtons(QMessageBox.Ok)
                error_msg.exec()
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
                records = db.fetch_medical_records(treatment)
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
                        
                        # Add items to table with center alignment
                        if treatment == "Consultation":
                            # 9 columns, use record[8] for risk_status
                            for i, value in enumerate([
                                date, record[2], record[3], record[8], record[4], record[5], record[6], vet_name
                            ]):
                                item = QTableWidgetItem(str(value))
                                item.setTextAlignment(Qt.AlignCenter)
                                target_table.setItem(row_position, i, item)
                        elif treatment == "Surgery":
                            # 9 columns, use record[8] for risk_status
                            for i, value in enumerate([
                                date, record[2], record[3], record[8], record[4], record[5], record[6], vet_name
                            ]):
                                item = QTableWidgetItem(str(value))
                                item.setTextAlignment(Qt.AlignCenter)
                                target_table.setItem(row_position, i, item)
                        else:
                            # 8 columns, do NOT use record[8]
                            for i, value in enumerate([
                                date, record[2], record[3], record[4], record[5], record[6], vet_name
                            ]):
                                item = QTableWidgetItem(str(value))
                                item.setTextAlignment(Qt.AlignCenter)
                                target_table.setItem(row_position, i, item)

                        # Add action buttons
                        action_widget = QWidget()
                        action_layout = QHBoxLayout(action_widget)
                        action_layout.setContentsMargins(0, 0, 0, 0)
                        action_layout.setSpacing(5)
                        action_layout.setAlignment(Qt.AlignCenter)  # Center the buttons

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
                                font-family: Lato;
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
                                font-family: Lato;
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
                        
                        # Set the action buttons in the correct column based on treatment type
                        if treatment == "Consultation":
                            target_table.setCellWidget(row_position, 8, action_widget)  # Column 8 for Consultation
                        elif treatment == "Surgery":
                            target_table.setCellWidget(row_position, 8, action_widget)  # Column 8 for Surgery
                        else:
                            target_table.setCellWidget(row_position, 7, action_widget)  # Column 7 for other treatments

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
            print("Debug - Record array:", record)

            # Convert date back to yyyy-MM-dd format
            try:
                date = datetime.strptime(record[0], "%d/%m/%Y").strftime("%Y-%m-%d")
            except:
                date = datetime.now().strftime("%Y-%m-%d")
            record[0] = date

            # Show the edit dialog
            dialog = ReportFormDialog()
            
            # Disable type combo box and set the treatment type
            dialog.type_combo.setEnabled(False)
            dialog.type_combo.setCurrentText(treatment)
            
            # Get the original veterinarian name and ensure it has "Dr." prefix
            # Get veterinarian from the correct index based on treatment type
            if treatment == "Consultation":
                original_vet = record[7] if len(record) > 7 else ""  # Veterinarian is at index 7
            elif treatment == "Surgery":
                original_vet = record[7] if len(record) > 7 else ""  # Veterinarian is at index 7
            elif treatment == "Deworming":
                original_vet = record[6] if len(record) > 6 else ""  # Veterinarian is at index 6
            elif treatment == "Vaccination":
                original_vet = record[6] if len(record) > 6 else ""  # Veterinarian is at index 6
            elif treatment == "Grooming":
                original_vet = record[6] if len(record) > 6 else ""  # Veterinarian is at index 6
            elif treatment == "Other Treatments":
                original_vet = record[6] if len(record) > 6 else ""  # Veterinarian is at index 6
            else:
                original_vet = ""

            original_vet = original_vet.strip()  # Remove any whitespace
            if original_vet and original_vet != "Select Veterinarian" and not original_vet.startswith("Dr. "):
                original_vet = f"Dr. {original_vet}"
            
            # Set the veterinarian value before loading names
            if original_vet and original_vet != "Select Veterinarian":
                dialog.vet_combo.addItem(original_vet)
                dialog.vet_combo.setCurrentText(original_vet)
            
            # Load veterinarian names (which will now preserve the current selection)
            dialog.load_vet_names()
            
            # Find and set the correct veterinarian
            if original_vet:  # Only try to set if we have a valid name
                index = dialog.vet_combo.findText(original_vet)
                if index >= 0:
                    dialog.vet_combo.setCurrentIndex(index)
                else:
                    # If not found, add it to the list and select it
                    dialog.vet_combo.addItem(original_vet)
                    dialog.vet_combo.setCurrentText(original_vet)
            
            # Set the date first
            try:
                date_obj = QDate.fromString(date, "yyyy-MM-dd")
                dialog.date_edit.setDate(date_obj)
            except:
                dialog.date_edit.setDate(QDate.currentDate())
            
            # Set the form data based on correct indices for each treatment type
            if treatment == "Consultation":
                dialog.set_pet_name_for_edit(record[2].strip(), record[1].strip())
                dialog.update_form_fields(treatment)
                # Set risk status
                dialog.field_widgets[treatment]["risk_status"][1].setCurrentText(record[3])
                # Set other fields
                dialog.field_widgets[treatment]["reason"][1].setPlainText(record[4])
                dialog.field_widgets[treatment]["diagnosis"][1].setPlainText(record[5])
                dialog.field_widgets[treatment]["prescribed"][1].setPlainText(record[6])
            elif treatment == "Surgery":
                print("Debug - Setting Surgery Data:", record)
                dialog.set_pet_name_for_edit(record[2].strip(), record[1].strip())
                dialog.update_form_fields(treatment)
                # Set risk status
                dialog.field_widgets[treatment]["risk_status"][1].setCurrentText(record[3])
                # Set surgery type
                dialog.field_widgets[treatment]["surgery_type"][1].setPlainText(record[4])
                # Set anesthesia
                dialog.field_widgets[treatment]["anesthesia"][1].setPlainText(record[5])
                # Set next follow-up date
                if record[6]:
                    try:
                        # Try parsing the date in dd/mm/yyyy format
                        followup_date = datetime.strptime(record[6], "%d/%m/%Y")
                        dialog.field_widgets[treatment]["next_followup"][1].setDate(QDate(followup_date.year, followup_date.month, followup_date.day))
                    except:
                        try:
                            # Try parsing the date in yyyy-mm-dd format
                            followup_date = datetime.strptime(record[6], "%Y-%m-%d")
                            dialog.field_widgets[treatment]["next_followup"][1].setDate(QDate(followup_date.year, followup_date.month, followup_date.day))
                        except:
                            # If both formats fail, use the current date
                            dialog.field_widgets[treatment]["next_followup"][1].setDate(QDate.currentDate())
                else:
                    dialog.field_widgets[treatment]["next_followup"][1].setDate(QDate.currentDate())
            elif treatment == "Deworming":
                dialog.set_pet_name_for_edit(record[2].strip(), record[1].strip())
                dialog.update_form_fields(treatment)
                dialog.field_widgets[treatment]["medication"][1].setPlainText(record[3])
                dialog.field_widgets[treatment]["dosage"][1].setPlainText(record[4])
                if record[5]:
                    try:
                        # Try parsing the date in dd/mm/yyyy format
                        next_date = datetime.strptime(record[5], "%d/%m/%Y")
                        dialog.field_widgets[treatment]["next_date"][1].setDate(QDate(next_date.year, next_date.month, next_date.day))
                    except:
                        try:
                            # Try parsing the date in yyyy-mm-dd format
                            next_date = datetime.strptime(record[5], "%Y-%m-%d")
                            dialog.field_widgets[treatment]["next_date"][1].setDate(QDate(next_date.year, next_date.month, next_date.day))
                        except:
                            # If both formats fail, use the current date
                            dialog.field_widgets[treatment]["next_date"][1].setDate(QDate.currentDate())
                else:
                    dialog.field_widgets[treatment]["next_date"][1].setDate(QDate.currentDate())
            elif treatment == "Vaccination":
                dialog.set_pet_name_for_edit(record[2].strip(), record[1].strip())
                dialog.update_form_fields(treatment)
                dialog.field_widgets[treatment]["vaccine"][1].setPlainText(record[3])
                dialog.field_widgets[treatment]["dosage"][1].setPlainText(record[4])
                if record[5]:
                    try:
                        # Try parsing the date in dd/mm/yyyy format
                        next_date = datetime.strptime(record[5], "%d/%m/%Y")
                        dialog.field_widgets[treatment]["next_date"][1].setDate(QDate(next_date.year, next_date.month, next_date.day))
                    except:
                        try:
                            # Try parsing the date in yyyy-mm-dd format
                            next_date = datetime.strptime(record[5], "%Y-%m-%d")
                            dialog.field_widgets[treatment]["next_date"][1].setDate(QDate(next_date.year, next_date.month, next_date.day))
                        except:
                            # If both formats fail, use the current date
                            dialog.field_widgets[treatment]["next_date"][1].setDate(QDate.currentDate())
                else:
                    dialog.field_widgets[treatment]["next_date"][1].setDate(QDate.currentDate())
            elif treatment == "Grooming":
                dialog.set_pet_name_for_edit(record[2].strip(), record[1].strip())
                dialog.update_form_fields(treatment)
                dialog.field_widgets[treatment]["services"][1].setPlainText(record[3])
                dialog.field_widgets[treatment]["notes"][1].setPlainText(record[4])
                if record[5]:
                    try:
                        # Try parsing the date in dd/mm/yyyy format
                        next_date = datetime.strptime(record[5], "%d/%m/%Y")
                        dialog.field_widgets[treatment]["next_date"][1].setDate(QDate(next_date.year, next_date.month, next_date.day))
                    except:
                        try:
                            # Try parsing the date in yyyy-mm-dd format
                            next_date = datetime.strptime(record[5], "%Y-%m-%d")
                            dialog.field_widgets[treatment]["next_date"][1].setDate(QDate(next_date.year, next_date.month, next_date.day))
                        except:
                            # If both formats fail, use the current date
                            dialog.field_widgets[treatment]["next_date"][1].setDate(QDate.currentDate())
                else:
                    dialog.field_widgets[treatment]["next_date"][1].setDate(QDate.currentDate())
            elif treatment == "Other Treatments":
                dialog.set_pet_name_for_edit(record[2].strip(), record[1].strip())
                dialog.update_form_fields(treatment)
                dialog.field_widgets[treatment]["type"][1].setPlainText(record[3])
                dialog.field_widgets[treatment]["medication"][1].setPlainText(record[4])
                dialog.field_widgets[treatment]["dosage"][1].setPlainText(record[5])

            if dialog.exec():
                form_data = dialog.get_form_data()
                # Keep the original treatment type
                form_data["type"] = treatment
                
                pet_name_display = form_data["pet_name"]
                parts = pet_name_display.split(" - ")
                if len(parts) >= 2:
                    client_name = parts[0].strip()
                    pet_name = parts[-1].strip()
                else:
                    pet_name = pet_name_display.strip()
                    client_name = ""

                db = Database()
                try:
                    # Get pet and client IDs
                    db.cursor.execute("""
                        SELECT p.pet_id, c.client_id
                        FROM pets p
                        JOIN clients c ON p.client_id = c.client_id
                        WHERE LOWER(p.name) = LOWER(?)
                    """, (pet_name,))
                    result = db.cursor.fetchone()
                    if not result:
                        error_msg = create_styled_message_box(
                            QMessageBox.Warning,
                            "Error",
                            f"Pet '{pet_name}' not found!"
                        )
                        error_msg.setStandardButtons(QMessageBox.Ok)
                        error_msg.exec()
                        return
                    pet_id, client_id = result

                    # Get the record ID first
                    record_id = None
                    if treatment == "Consultation":
                        db.cursor.execute("""
                            SELECT consultation_id FROM consultations 
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND reason = ? AND risk_status = ?
                        """, (pet_id, client_id, date, record[4], record[3]))
                        result = db.cursor.fetchone()
                        if result:
                            record_id = result[0]
                    elif treatment == "Surgery":
                        print(f"Debug - Updating surgery record: pet_id={pet_id}, client_id={client_id}, date={date}, surgery_type={record[4]}, risk_status={record[3]}")
                        db.cursor.execute("""
                            SELECT surgery_id FROM surgeries 
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND surgery_type = ? AND risk_status = ?
                        """, (pet_id, client_id, date, record[4], record[3]))
                        result = db.cursor.fetchone()
                        if result:
                            record_id = result[0]
                            print(f"Debug - Found surgery_id: {record_id}")
                            # Update the surgery record
                            db.cursor.execute("""
                                UPDATE surgeries 
                                SET date = ?, surgery_type = ?, anesthesia = ?, next_followup = ?, veterinarian = ?, risk_status = ?
                                WHERE surgery_id = ?
                            """, (form_data["date"], form_data["reason"], form_data["diagnosis"], 
                                 form_data["prescribed"], form_data["veterinarian"], form_data.get("risk_status", "Low Risk"), record_id))
                            db.conn.commit()
                            success_msg = create_styled_message_box(
                                QMessageBox.Information,
                                "Success",
                                "Surgery report updated successfully!"
                            )
                            success_msg.setStandardButtons(QMessageBox.Ok)
                            success_msg.exec()
                            refresh_tables()
                            return
                    elif treatment == "Deworming":
                        db.cursor.execute("""
                            SELECT deworming_id FROM deworming 
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND medication = ?
                        """, (pet_id, client_id, date, record[3]))
                        result = db.cursor.fetchone()
                        if result:
                            record_id = result[0]
                    elif treatment == "Vaccination":
                        db.cursor.execute("""
                            SELECT vaccination_id FROM vaccinations 
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND vaccine = ?
                        """, (pet_id, client_id, date, record[3]))
                        result = db.cursor.fetchone()
                        if result:
                            record_id = result[0]
                    elif treatment == "Grooming":
                        db.cursor.execute("""
                            SELECT grooming_id FROM grooming 
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND services = ?
                        """, (pet_id, client_id, date, record[3]))
                        result = db.cursor.fetchone()
                        if result:
                            record_id = result[0]
                    elif treatment == "Other Treatments":
                        db.cursor.execute("""
                            SELECT treatment_id FROM other_treatments 
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND treatment_type = ?
                        """, (pet_id, client_id, date, record[3]))
                        result = db.cursor.fetchone()
                        if result:
                            record_id = result[0]

                    if not record_id:
                        error_msg = create_styled_message_box(
                            QMessageBox.Warning,
                            "Error",
                            "Could not find the record to update!"
                        )
                        error_msg.setStandardButtons(QMessageBox.Ok)
                        error_msg.exec()
                        return

                    # Update the record based on treatment type
                    if treatment == "Consultation":
                        db.cursor.execute("""
                            UPDATE consultations 
                            SET date = ?, reason = ?, diagnosis = ?, prescribed_treatment = ?, veterinarian = ?, risk_status = ?
                            WHERE consultation_id = ?
                        """, (form_data["date"], form_data["reason"], form_data["diagnosis"], 
                             form_data["prescribed"], form_data["veterinarian"], form_data.get("risk_status", "Low Risk"), record_id))
                    elif treatment == "Deworming":
                        db.cursor.execute("""
                            UPDATE deworming 
                            SET date = ?, medication = ?, dosage = ?, next_scheduled = ?, veterinarian = ?
                            WHERE deworming_id = ?
                        """, (form_data["date"], form_data["reason"], form_data["diagnosis"], 
                             form_data["prescribed"], form_data["veterinarian"], record_id))
                    elif treatment == "Vaccination":
                        db.cursor.execute("""
                            UPDATE vaccinations 
                            SET date = ?, vaccine = ?, dosage = ?, next_scheduled = ?, veterinarian = ?
                            WHERE vaccination_id = ?
                        """, (form_data["date"], form_data["reason"], form_data["diagnosis"], 
                             form_data["prescribed"], form_data["veterinarian"], record_id))
                    elif treatment == "Grooming":
                        db.cursor.execute("""
                            UPDATE grooming 
                            SET date = ?, services = ?, notes = ?, next_scheduled = ?, veterinarian = ?
                            WHERE grooming_id = ?
                        """, (form_data["date"], form_data["reason"], form_data["diagnosis"], 
                             form_data["prescribed"], form_data["veterinarian"], record_id))
                    elif treatment == "Other Treatments":
                        db.cursor.execute("""
                            UPDATE other_treatments 
                            SET date = ?, treatment_type = ?, medication = ?, dosage = ?, veterinarian = ?
                            WHERE treatment_id = ?
                        """, (form_data["date"], form_data["reason"], form_data["diagnosis"], 
                             form_data["prescribed"], form_data["veterinarian"], record_id))
                    
                    db.conn.commit()
                    success_msg = create_styled_message_box(
                        QMessageBox.Information,
                        "Success",
                        "Report updated successfully!"
                    )
                    success_msg.setStandardButtons(QMessageBox.Ok)
                    success_msg.exec()
                    refresh_tables()
                except Exception as e:
                    db.conn.rollback()
                    print(f"Debug - Error updating record: {e}")
                    error_msg = create_styled_message_box(
                        QMessageBox.Critical,
                        "Error",
                        f"Failed to update report: {e}"
                    )
                    error_msg.setStandardButtons(QMessageBox.Ok)
                    error_msg.exec()
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
            
            # Create confirmation message box
            confirm = create_styled_message_box(
                QMessageBox.Question,
                "Delete Report",
                "Are you sure you want to delete this report?"
            )
            confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirm.setDefaultButton(QMessageBox.No)
            
            if confirm.exec() == QMessageBox.Yes:
                # Delete the report from the database
                db = Database()
                try:
                    # Get pet and client IDs first
                    db.cursor.execute("""
                        SELECT p.pet_id, c.client_id
                        FROM pets p
                        JOIN clients c ON p.client_id = c.client_id
                        WHERE p.name = ? AND c.name = ?
                    """, (record[1], record[2]))  # pet_name and client_name
                    result = db.cursor.fetchone()
                    
                    if not result:
                        show_message(None, "Could not find the pet and client records!", QMessageBox.Warning)
                        return
                        
                    pet_id, client_id = result
                    
                    # Delete from the appropriate table based on treatment type
                    if treatment == "Consultation":
                        db.cursor.execute("""
                            DELETE FROM consultations
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND reason = ? AND risk_status = ?
                        """, (pet_id, client_id, date, record[4], record[3]))
                    elif treatment == "Deworming":
                        db.cursor.execute("""
                            DELETE FROM deworming
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND medication = ?
                        """, (pet_id, client_id, date, record[3]))
                    elif treatment == "Vaccination":
                        db.cursor.execute("""
                            DELETE FROM vaccinations
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND vaccine = ?
                        """, (pet_id, client_id, date, record[3]))
                    elif treatment == "Surgery":
                        print(f"Debug - Deleting surgery record: pet_id={pet_id}, client_id={client_id}, date={date}, surgery_type={record[4]}, risk_status={record[3]}")
                        db.cursor.execute("""
                            DELETE FROM surgeries
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND surgery_type = ? AND risk_status = ?
                        """, (pet_id, client_id, date, record[4], record[3]))
                    elif treatment == "Grooming":
                        db.cursor.execute("""
                            DELETE FROM grooming
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND services = ?
                        """, (pet_id, client_id, date, record[3]))
                    elif treatment == "Other Treatments":
                        db.cursor.execute("""
                            DELETE FROM other_treatments
                            WHERE pet_id = ? AND client_id = ? AND date = ? AND treatment_type = ?
                        """, (pet_id, client_id, date, record[3]))
                    
                    db.conn.commit()
                    
                    # Show success message
                    success_msg = create_styled_message_box(
                        QMessageBox.Information,
                        "Success",
                        "Report deleted successfully!"
                    )
                    success_msg.setStandardButtons(QMessageBox.Ok)
                    success_msg.exec()

                    # Refresh the table
                    refresh_tables()
                except Exception as e:
                    db.conn.rollback()
                    print(f"Debug - Error deleting record: {e}")
                    error_msg = create_styled_message_box(
                        QMessageBox.Critical,
                        "Error",
                        f"Failed to delete report: {e}"
                    )
                    error_msg.setStandardButtons(QMessageBox.Ok)
                    error_msg.exec()
                finally:
                    db.close_connection()
                
        except Exception as e:
            print(f"Error deleting report: {e}")

    # Initial load of data
    refresh_tables()

    add_report_button.clicked.connect(lambda: open_report_form(treatment_buttons["Consultation"].text()))

    # Store the filter function in the content widget for external access
    content.filter_tables = filter_tables

    def save_pdf():
        # Detect which table is visible
        table = None
        table_type = "Consultation"
        for treatment, t in tables.items():
            if t.isVisible():
                table = t
                table_type = treatment
                break

        if not table:
            return

        # Define the output folder relative to the project
        folder_path = os.path.join(os.getcwd(), "pdf_reports", "reports")
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
        license_number = None
        try:
            clinic_info = db.get_clinic_info()
            # Get clinic license number
            db.cursor.execute("SELECT vet_license FROM clinic_info LIMIT 1")
            result = db.cursor.fetchone()
            if result and result[0]:
                license_number = result[0]
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
            
            # Draw license number if available
            if license_number:
                c.setFont("Helvetica", 10)
                c.drawString(x_margin + 60, height - y_margin - 35, f"License No: {license_number}")
            
            c.setFont("Helvetica", 12)
            c.drawString(x_margin + 60, height - y_margin - 50, clinic_info.get("address", ""))
            c.drawString(x_margin + 60, height - y_margin - 70, f"Contact: {clinic_info.get('contact_number', '')}")

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
        
        # Show success message
        success_msg = create_styled_message_box(
            QMessageBox.Information,
            "Success",
            f"PDF successfully saved to:\n{file_path}"
        )
        success_msg.setStandardButtons(QMessageBox.Ok)
        success_msg.exec()

    save_pdf_button.clicked.connect(save_pdf)

    return content