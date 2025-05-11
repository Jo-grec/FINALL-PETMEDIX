from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QDialog, QFormLayout, QLineEdit, QComboBox, QTextEdit, QDateEdit, QHeaderView,
    QMessageBox, QTableWidgetItem
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor, QBrush, QIcon
from modules.database import Database
from datetime import datetime
from modules.utils import show_message


class ReportFormDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PetMedix - Reports")
        self.setFixedSize(800, 600)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 10, 20, 10)
        title_label = QLabel("Report Form")
        title_label.setObjectName("TitleLabel")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFF;")
        title_layout.addWidget(title_label)
        layout.addWidget(title_container)
        
        # Form Layout
        form_widget = QWidget()
        form_scroll_layout = QVBoxLayout(form_widget)
        form_scroll_layout.setContentsMargins(40, 20, 40, 10)
        form_scroll_layout.setSpacing(0)
        
        # Row 1: Date, Type
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)
        
        # Date field
        date_label = QLabel("Date")
        date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
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
            }
        """)
        
        date_container = QVBoxLayout()
        date_container.addWidget(date_label)
        date_container.addWidget(self.date_edit)
        
        # Type field
        type_label = QLabel("Type")
        type_label.setStyleSheet("font-size: 16px; font-weight: bold;")
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
        type_container.addWidget(type_label)
        type_container.addWidget(self.type_combo)
        
        row1_layout.addLayout(date_container, 1)
        row1_layout.addLayout(type_container, 1)
        form_scroll_layout.addLayout(row1_layout)
        
        # Row 2: Pet Name
        pet_name_label = QLabel("Pet Name")
        pet_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.pet_name_combo = QComboBox()
        self.pet_name_combo.setMinimumHeight(40)
        self.pet_name_combo.setStyleSheet("""
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
            QComboBox::down-arrow {
                width: 15px;
                height: 15px;
            }
        """)
        
        self.load_pet_names()
        
        form_scroll_layout.addWidget(pet_name_label)
        form_scroll_layout.addWidget(self.pet_name_combo)
        
        # Row 3: Reason for Consultation
        reason_label = QLabel("Reason for Consultation")
        reason_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText("Reason for Consultation")
        self.reason_input.setFixedHeight(80)
        self.reason_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        form_scroll_layout.addWidget(reason_label)
        form_scroll_layout.addWidget(self.reason_input)
        
        # Row 4: Diagnosis
        diagnosis_label = QLabel("Diagnosis")
        diagnosis_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.diagnosis_input = QTextEdit()
        self.diagnosis_input.setPlaceholderText("Diagnosis")
        self.diagnosis_input.setFixedHeight(80)
        self.diagnosis_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        form_scroll_layout.addWidget(diagnosis_label)
        form_scroll_layout.addWidget(self.diagnosis_input)
        
        # Row 5: Prescribed Treatment/Medication
        prescribed_label = QLabel("Prescribed Treatment/Medication")
        prescribed_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.prescribed_input = QTextEdit()
        self.prescribed_input.setPlaceholderText("Prescribed Treatment/Medication")
        self.prescribed_input.setFixedHeight(80)
        self.prescribed_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        form_scroll_layout.addWidget(prescribed_label)
        form_scroll_layout.addWidget(self.prescribed_input)
        
        # Row 6: Veterinarian/Staff In Charge
        vet_label = QLabel("Veterinarian/Staff In Charge")
        vet_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.vet_combo = QComboBox()
        self.vet_combo.setMinimumHeight(40)
        self.vet_combo.setStyleSheet("""
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
            QComboBox::down-arrow {
                width: 15px;
                height: 15px;
            }
        """)
        
        self.load_vet_names()
        
        form_scroll_layout.addWidget(vet_label)
        form_scroll_layout.addWidget(self.vet_combo)
        
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
        button_layout.setContentsMargins(0, 0, 50, 0)
        
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
        self.setWindowTitle("View Report")
        self.setFixedSize(800, 600)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 10, 20, 10)
        title_label = QLabel("View Report")
        title_label.setObjectName("TitleLabel")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFF;")
        title_layout.addWidget(title_label)
        layout.addWidget(title_container)
        
        # Form Layout
        form_widget = QWidget()
        form_scroll_layout = QVBoxLayout(form_widget)
        form_scroll_layout.setContentsMargins(40, 20, 40, 10)
        form_scroll_layout.setSpacing(0)
        
        # Row 1: Date, Type
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)
        
        # Date field
        date_label = QLabel("Date")
        date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
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
            }
        """)
        
        date_container = QVBoxLayout()
        date_container.addWidget(date_label)
        date_container.addWidget(self.date_edit)
        
        # Type field
        type_label = QLabel("Type")
        type_label.setStyleSheet("font-size: 16px; font-weight: bold;")
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
            }
        """)
        
        type_container = QVBoxLayout()
        type_container.addWidget(type_label)
        type_container.addWidget(self.type_combo)
        
        row1_layout.addLayout(date_container, 1)
        row1_layout.addLayout(type_container, 1)
        form_scroll_layout.addLayout(row1_layout)
        
        # Row 2: Pet Name
        pet_name_label = QLabel("Pet Name")
        pet_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
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
            }
        """)
        
        form_scroll_layout.addWidget(pet_name_label)
        form_scroll_layout.addWidget(self.pet_name_combo)
        
        # Row 3: Reason for Consultation
        reason_label = QLabel("Reason for Consultation")
        reason_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.reason_input = QTextEdit()
        self.reason_input.setReadOnly(True)
        self.reason_input.setFixedHeight(80)
        self.reason_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        form_scroll_layout.addWidget(reason_label)
        form_scroll_layout.addWidget(self.reason_input)
        
        # Row 4: Diagnosis
        diagnosis_label = QLabel("Diagnosis")
        diagnosis_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.diagnosis_input = QTextEdit()
        self.diagnosis_input.setReadOnly(True)
        self.diagnosis_input.setFixedHeight(80)
        self.diagnosis_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        form_scroll_layout.addWidget(diagnosis_label)
        form_scroll_layout.addWidget(self.diagnosis_input)
        
        # Row 5: Prescribed Treatment/Medication
        prescribed_label = QLabel("Prescribed Treatment/Medication")
        prescribed_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.prescribed_input = QTextEdit()
        self.prescribed_input.setReadOnly(True)
        self.prescribed_input.setFixedHeight(80)
        self.prescribed_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        form_scroll_layout.addWidget(prescribed_label)
        form_scroll_layout.addWidget(self.prescribed_input)
        
        # Row 6: Veterinarian/Staff In Charge
        vet_label = QLabel("Veterinarian/Staff In Charge")
        vet_label.setStyleSheet("font-size: 16px; font-weight: bold;")
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
            }
        """)
        
        form_scroll_layout.addWidget(vet_label)
        form_scroll_layout.addWidget(self.vet_combo)
        
        layout.addWidget(form_widget)
        
        # Close Button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
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
        
        button_layout.addWidget(close_btn)
        button_layout.setContentsMargins(0, 0, 50, 0)
        
        layout.addLayout(button_layout)
        
        # Set the data
        self.set_report_data(report_data)
        
    def set_report_data(self, data):
        """Set the form data from the report."""
        try:
            # Set date
            date = datetime.strptime(data[0], "%Y-%m-%d")
            self.date_edit.setDate(QDate(date.year, date.month, date.day))
            
            # Set type
            index = self.type_combo.findText(data[1])
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
            
            # Set pet name
            self.pet_name_combo.addItem(f"{data[3]} - {data[2]}")  # Client - Pet
            
            # Set other fields
            self.reason_input.setText(data[4])
            self.diagnosis_input.setText(data[5])
            self.prescribed_input.setText(data[6])
            self.vet_combo.addItem(data[7])
            
        except Exception as e:
            print(f"Error setting report data: {e}")


def get_report_widget():
    content = QWidget()
    layout = QVBoxLayout(content)
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 30)

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

    header_layout.addWidget(report_label)
    header_layout.addWidget(add_report_button)
    header_layout.addWidget(save_pdf_button)

    # Treatment Buttons
    treatment_buttons_widget = QWidget()
    treatment_layout = QHBoxLayout()
    treatment_layout.setContentsMargins(0, 0, 50, 0)
    treatment_layout.setSpacing(0)

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

    treatment_buttons = {}

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
                        
                        # Add items to table
                        target_table.setItem(row_position, 0, QTableWidgetItem(date))  # Date
                        if treatment == "All":
                            target_table.setItem(row_position, 1, QTableWidgetItem(record[1]))  # Type
                            target_table.setItem(row_position, 2, QTableWidgetItem(record[2]))  # Pet Name
                            target_table.setItem(row_position, 3, QTableWidgetItem(record[3]))  # Client Name
                            target_table.setItem(row_position, 4, QTableWidgetItem(record[4]))  # Reason
                            target_table.setItem(row_position, 5, QTableWidgetItem(record[5]))  # Diagnosis
                            target_table.setItem(row_position, 6, QTableWidgetItem(record[6]))  # Prescribed
                            target_table.setItem(row_position, 7, QTableWidgetItem(f"Dr. {record[7]}"))  # Vet
                        else:
                            target_table.setItem(row_position, 1, QTableWidgetItem(record[2]))  # Pet Name
                            target_table.setItem(row_position, 2, QTableWidgetItem(record[3]))  # Client Name
                            target_table.setItem(row_position, 3, QTableWidgetItem(record[4]))  # Reason
                            target_table.setItem(row_position, 4, QTableWidgetItem(record[5]))  # Diagnosis
                            target_table.setItem(row_position, 5, QTableWidgetItem(record[6]))  # Prescribed
                            target_table.setItem(row_position, 6, QTableWidgetItem(f"Dr. {record[7]}"))  # Vet

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

                            action_layout.addWidget(edit_button)
                            action_layout.addWidget(delete_button)
                            action_widget.setLayout(action_layout)
                            target_table.setCellWidget(row_position, 7, action_widget)

                            # Connect cell click event
                            target_table.cellClicked.connect(lambda row, col, t=treatment: on_cell_clicked(row, col, t))
                    except Exception as e:
                        print(f"Error adding row to table: {e}")
        except Exception as e:
            print(f"Error refreshing tables: {e}")
        finally:
            db.close_connection()

    def on_cell_clicked(row, col, treatment):
        """Handle cell click event to show report details."""
        try:
            table = tables[treatment]
            record = []
            
            # Get all data from the row
            for i in range(table.columnCount()):
                if i == 7 and treatment != "All":  # Skip action column for non-All tables
                    continue
                item = table.item(row, i)
                if item:
                    record.append(item.text())
                else:
                    record.append("")
            
            # Convert date back to yyyy-MM-dd format
            date = datetime.strptime(record[0], "%d/%m/%Y").strftime("%Y-%m-%d")
            record[0] = date
            
            # Show the view dialog
            dialog = ViewReportDialog(record)
            dialog.exec()
            
        except Exception as e:
            print(f"Error showing report details: {e}")

    # Initial load of data
    refresh_tables()

    add_report_button.clicked.connect(open_report_form)

    return content