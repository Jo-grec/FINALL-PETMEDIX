from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QDialog, QFormLayout, QLineEdit, QComboBox, QTextEdit, QDateEdit
)
from PySide6.QtCore import Qt, QDate


class ReportFormDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Report")
        self.setFixedSize(800, 700)  # Increased height to give more space
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 10, 20, 10)
        title_label = QLabel("Report Form")
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
        self.date_edit.setMinimumHeight(40)  # Ensure minimum height
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
        self.type_combo.addItems(["Consultation", "Deworming", "Vaccination", "Surgical Operation", "Grooming", "Other Treatments"])
        self.type_combo.setMinimumHeight(40)  # Ensure minimum height
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
        
        row1_layout.addLayout(date_container, 1)  # Add stretch factor
        row1_layout.addLayout(type_container, 1)  # Add stretch factor
        form_scroll_layout.addLayout(row1_layout)
        
        # Row 2: Pet Name, Client Name
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(10)
        
        # Pet Name field
        pet_name_label = QLabel("Pet Name")
        pet_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.pet_name_input = QLineEdit()
        self.pet_name_input.setPlaceholderText("Pet Name")
        self.pet_name_input.setMinimumHeight(40)  # Ensure minimum height
        self.pet_name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        pet_name_container = QVBoxLayout()
        pet_name_container.addWidget(pet_name_label)
        pet_name_container.addWidget(self.pet_name_input)
        
        # Client Name field
        client_name_label = QLabel("Client Name")
        client_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("Client Name")
        self.client_input.setMinimumHeight(40)  # Ensure minimum height
        self.client_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        client_name_container = QVBoxLayout()
        client_name_container.addWidget(client_name_label)
        client_name_container.addWidget(self.client_input)
        
        row2_layout.addLayout(pet_name_container, 1)  # Add stretch factor
        row2_layout.addLayout(client_name_container, 1)  # Add stretch factor
        form_scroll_layout.addLayout(row2_layout)
        
        # Row 3: Reason for Consultation
        reason_label = QLabel("Reason for Consultation")
        reason_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText("Reason for Consultation")
        self.reason_input.setFixedHeight(80)  # Slightly reduced height
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
        
        # Row 5: Prescribed Treatment/Medication - FIXED PLACEHOLDER TEXT
        prescribed_label = QLabel("Prescribed Treatment/Medication")
        prescribed_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.prescribed_input = QTextEdit()
        self.prescribed_input.setPlaceholderText("Prescribed Treatment/Medication")  # FIXED
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
        self.vet_input = QLineEdit()
        self.vet_input.setPlaceholderText("Veterinarian/Staff In Charge")
        self.vet_input.setMinimumHeight(40)  # Ensure minimum height
        self.vet_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        form_scroll_layout.addWidget(vet_label)
        form_scroll_layout.addWidget(self.vet_input)
        
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
    add_report_button.setFixedSize(60, 40)
    add_report_button.setStyleSheet(
        "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px;"
    )

    # Save PDF Button
    save_pdf_button = QPushButton("Save PDF")
    save_pdf_button.setObjectName("SavePDFButton")
    save_pdf_button.setFixedSize(60, 40)
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
        "Consultation",
        "Deworm",
        "Vaccination",
        "Surgical Operation",
        "Grooming",
        "Other Treatments"
    ]

    # Store buttons for later use
    treatment_buttons = {}

    for treatment in treatments:
        button = QPushButton(treatment)
        button.setFixedSize(180, 40)
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

    # --- Tables Setup ---
    def create_table(headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setRowCount(15)
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setStretchLastSection(True)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #FFF;
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
        return table

    # Consultation Table
    consultation_table = create_table([
        "Consultation Date", "Pet Name", "Owner/Client", "Reason for Consultation",
        "Diagnosis", "Prescribed Treatment", "Veterinarian In Charge", "Action"
    ])
    for i, width in enumerate([150, 120, 150, 200, 180, 200, 150, 100]):
        consultation_table.setColumnWidth(i, width)
    layout.addWidget(consultation_table)

    # Deworm Table
    deworm_table = create_table([
        "Deworming Date", "Pet Name", "Owner/Client", "Deworming Medication",
        "Dosage Administered", "Next Scheduled Deworming", "Veterinarian In Charge", "Action"
    ])
    for i, width in enumerate([150, 120, 150, 200, 180, 200, 150, 100]):
        deworm_table.setColumnWidth(i, width)
    deworm_table.hide()
    layout.addWidget(deworm_table)

    # Vaccination Table
    vaccination_table = create_table([
        "Vaccination Date", "Pet Name", "Owner/Client", "Vaccine Administered",
        "Dosage Administered", "Next Scheduled Vaccination", "Veterinarian In Charge", "Action"
    ])
    for i, width in enumerate([150, 120, 150, 200, 180, 200, 150, 100]):
        vaccination_table.setColumnWidth(i, width)
    vaccination_table.hide()
    layout.addWidget(vaccination_table)

    # Surgical Operation Table
    surgical_table = create_table([
        "Surgery Date", "Pet Name", "Owner/Client", "Type of Surgery",
        "Anesthesia Used", "Next Follow-Up Date", "Veterinarian In Charge", "Action"
    ])
    for i, width in enumerate([150, 120, 150, 200, 180, 200, 150, 100]):
        surgical_table.setColumnWidth(i, width)
    surgical_table.hide()
    layout.addWidget(surgical_table)

    # Grooming Table
    grooming_table = create_table([
        "Grooming Date", "Pet Name", "Owner/Client", "Grooming Service/s Availed",
        "Notes", "Next Grooming Date", "Veterinarian In Charge", "Action"
    ])
    for i, width in enumerate([150, 120, 150, 200, 180, 200, 150, 100]):
        grooming_table.setColumnWidth(i, width)
    grooming_table.hide()
    layout.addWidget(grooming_table)

    # Other Treatments Table
    other_treatments_table = create_table([
        "Treatment Date", "Pet Name", "Owner/Client", "Type of Treatment",
        "Medication/Procedure Used", "Dosage/Duration", "Veterinarian In Charge", "Action"
    ])
    for i, width in enumerate([150, 120, 150, 200, 180, 200, 150, 100]):
        other_treatments_table.setColumnWidth(i, width)
    other_treatments_table.hide()
    layout.addWidget(other_treatments_table)

    # --- Button Connections ---
    def show_table(table_to_show):
        for table in [
            consultation_table, deworm_table, vaccination_table,
            surgical_table, grooming_table, other_treatments_table
        ]:
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

    # Connect buttons to their respective functions
    treatment_buttons["Consultation"].clicked.connect(lambda: [show_table(consultation_table), select_treatment(treatment_buttons["Consultation"])])
    treatment_buttons["Deworm"].clicked.connect(lambda: [show_table(deworm_table), select_treatment(treatment_buttons["Deworm"])])
    treatment_buttons["Vaccination"].clicked.connect(lambda: [show_table(vaccination_table), select_treatment(treatment_buttons["Vaccination"])])
    treatment_buttons["Surgical Operation"].clicked.connect(lambda: [show_table(surgical_table), select_treatment(treatment_buttons["Surgical Operation"])])
    treatment_buttons["Grooming"].clicked.connect(lambda: [show_table(grooming_table), select_treatment(treatment_buttons["Grooming"])])
    treatment_buttons["Other Treatments"].clicked.connect(lambda: [show_table(other_treatments_table), select_treatment(treatment_buttons["Other Treatments"])])

    consultation_table.show()
    select_treatment(treatment_buttons["Consultation"])
    
    # Connect add report button
    def open_report_form():
        dialog = ReportFormDialog()
        if dialog.exec():
            # Process the form data here
            print("Report Saved:")
            print("Date:", dialog.date_edit.date().toString())
            print("Type:", dialog.type_combo.currentText())
            print("Client Name:", dialog.client_input.text())
            print("Pet Name:", dialog.pet_name_input.text())
            print("Reason:", dialog.reason_input.toPlainText())
            print("Prescribed Treatment:", dialog.prescribed_input.toPlainText())
            print("Diagnosis:", dialog.diagnosis_input.toPlainText())
            print("Veterinarian:", dialog.vet_input.text())
            
            # Here you would actually save the data to your database
            # and update the appropriate table
            
        else:
            print("Report creation cancelled")

    add_report_button.clicked.connect(open_report_form)

    return content