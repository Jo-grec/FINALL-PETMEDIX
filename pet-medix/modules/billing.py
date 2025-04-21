from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QComboBox, QTextEdit, QDateEdit, QCheckBox, QGridLayout,
    QScrollArea, QFrame, QGroupBox, QRadioButton, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont


class InvoiceFormDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Service Invoice")
        self.setFixedSize(850, 650)  # Reduced height to avoid scrolling
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547; border: 1px solid #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 10, 20, 10)
        title_label = QLabel("SERVICE INVOICE")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #FFF;")
        title_layout.addWidget(title_label)
        
        layout.addWidget(title_container)
        
        # Main content area
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Left column for client/patient info
        left_column = QVBoxLayout()
        left_column.setSpacing(8)
        
        # DETAILS section
        details_container = self._create_section("DETAILS")
        details_form = QFormLayout()
        details_form.setContentsMargins(5, 0, 5, 5)
        details_form.setVerticalSpacing(5)
        details_form.setHorizontalSpacing(5)
        
        date_label = QLabel("DATE:")
        date_label.setStyleSheet("font-size: 10px;")
        date_field = QLineEdit()
        date_field.setFixedHeight(20)
        details_form.addRow(date_label, date_field)
        
        invoice_label = QLabel("INVOICE NO.:")
        invoice_label.setStyleSheet("font-size: 10px;")
        invoice_field = QLineEdit()
        invoice_field.setFixedHeight(20)
        details_form.addRow(invoice_label, invoice_field)
        
        vet_label = QLabel("VETERINARIAN:")
        vet_label.setStyleSheet("font-size: 10px;")
        vet_field = QLineEdit()
        vet_field.setFixedHeight(20)
        details_form.addRow(vet_label, vet_field)
        
        reason_label = QLabel("REASON(S) FOR VISIT:")
        reason_label.setStyleSheet("font-size: 10px;")
        reason_field = QLineEdit()
        reason_field.setFixedHeight(20)
        details_form.addRow(reason_label, reason_field)
        
        details_container.setLayout(details_form)
        left_column.addWidget(details_container)
        
        # FROM section
        from_container = self._create_section("FROM")
        from_form = QFormLayout()
        from_form.setContentsMargins(5, 0, 5, 5)
        from_form.setVerticalSpacing(5)
        from_form.setHorizontalSpacing(5)
        
        clinic_label = QLabel("CLINIC:")
        clinic_label.setStyleSheet("font-size: 10px;")
        clinic_field = QLineEdit()
        clinic_field.setFixedHeight(20)
        from_form.addRow(clinic_label, clinic_field)
        
        address_label = QLabel("ADDRESS:")
        address_label.setStyleSheet("font-size: 10px;")
        address_field = QLineEdit()
        address_field.setFixedHeight(20)
        from_form.addRow(address_label, address_field)
        
        contact_label = QLabel("CONTACT NUMBER:")
        contact_label.setStyleSheet("font-size: 10px;")
        contact_field = QLineEdit()
        contact_field.setFixedHeight(20)
        from_form.addRow(contact_label, contact_field)
        
        email_label = QLabel("EMAIL ADDRESS:")
        email_label.setStyleSheet("font-size: 10px;")
        email_field = QLineEdit()
        email_field.setFixedHeight(20)
        from_form.addRow(email_label, email_field)
        
        from_container.setLayout(from_form)
        left_column.addWidget(from_container)
        
        # BILL TO section
        bill_to_container = self._create_section("BILL TO")
        bill_to_form = QFormLayout()
        bill_to_form.setContentsMargins(5, 0, 5, 5)
        bill_to_form.setVerticalSpacing(5)
        bill_to_form.setHorizontalSpacing(5)
        
        client_label = QLabel("CLIENT:")
        client_label.setStyleSheet("font-size: 10px;")
        client_field = QLineEdit()
        client_field.setFixedHeight(20)
        bill_to_form.addRow(client_label, client_field)
        
        client_address_label = QLabel("ADDRESS:")
        client_address_label.setStyleSheet("font-size: 10px;")
        client_address_field = QLineEdit()
        client_address_field.setFixedHeight(20)
        bill_to_form.addRow(client_address_label, client_address_field)
        
        client_contact_label = QLabel("CONTACT NUMBER:")
        client_contact_label.setStyleSheet("font-size: 10px;")
        client_contact_field = QLineEdit()
        client_contact_field.setFixedHeight(20)
        bill_to_form.addRow(client_contact_label, client_contact_field)
        
        client_email_label = QLabel("EMAIL ADDRESS:")
        client_email_label.setStyleSheet("font-size: 10px;")
        client_email_field = QLineEdit()
        client_email_field.setFixedHeight(20)
        bill_to_form.addRow(client_email_label, client_email_field)
        
        bill_to_container.setLayout(bill_to_form)
        left_column.addWidget(bill_to_container)
        
        # PET INFORMATION section
        pet_info_container = self._create_section("PET INFORMATION")
        pet_info_form = QFormLayout()
        pet_info_form.setContentsMargins(5, 0, 5, 5)
        pet_info_form.setVerticalSpacing(5)
        pet_info_form.setHorizontalSpacing(5)
        
        pet_name_label = QLabel("NAME:")
        pet_name_label.setStyleSheet("font-size: 10px;")
        pet_name_field = QLineEdit()
        pet_name_field.setFixedHeight(20)
        pet_info_form.addRow(pet_name_label, pet_name_field)
        
        pet_species_label = QLabel("SPECIES:")
        pet_species_label.setStyleSheet("font-size: 10px;")
        pet_species_field = QLineEdit()
        pet_species_field.setFixedHeight(20)
        pet_info_form.addRow(pet_species_label, pet_species_field)
        
        pet_breed_label = QLabel("BREED:")
        pet_breed_label.setStyleSheet("font-size: 10px;")
        pet_breed_field = QLineEdit()
        pet_breed_field.setFixedHeight(20)
        pet_info_form.addRow(pet_breed_label, pet_breed_field)
        
        pet_age_label = QLabel("AGE:")
        pet_age_label.setStyleSheet("font-size: 10px;")
        pet_age_field = QLineEdit()
        pet_age_field.setFixedHeight(20)
        pet_info_form.addRow(pet_age_label, pet_age_field)
        
        pet_info_container.setLayout(pet_info_form)
        left_column.addWidget(pet_info_container)
        
        # NOTES section
        notes_container = self._create_section("NOTES")
        notes_layout = QVBoxLayout()
        notes_layout.setContentsMargins(5, 5, 5, 5)
        
        notes_edit = QTextEdit()
        notes_edit.setFixedHeight(60)
        notes_layout.addWidget(notes_edit)
        
        notes_container.setLayout(notes_layout)
        left_column.addWidget(notes_container)
        
        # Right column for services and payment
        right_column = QVBoxLayout()
        right_column.setSpacing(5)
        
        # Services table
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        self.services_table = QTableWidget(8, 4)
        self.services_table.setHorizontalHeaderLabels(["SERVICE(S) RENDERED & CHARGES", "QUANTITY", "UNIT PRICE", "TOTAL"])
        self.services_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #CFDEF3; font-weight: bold; font-size: 10px; }")
        self.services_table.verticalHeader().setVisible(False)
        self.services_table.setShowGrid(True)
        
        # Calculate proportional column widths
        table_width = 450
        # Approximate available width
        self.services_table.setColumnWidth(0, int(table_width * 0.40))
        self.services_table.setColumnWidth(1, int(table_width * 0.15))
        self.services_table.setColumnWidth(2, int(table_width * 0.20))
        self.services_table.setColumnWidth(3, int(table_width * 0.25))
        
        self.services_table.setMaximumHeight(250)  # Limit table height
        table_layout.addWidget(self.services_table)
        right_column.addWidget(table_widget)
        
        # Payment info
        payment_widget = QWidget()
        payment_layout = QFormLayout(payment_widget)
        payment_layout.setContentsMargins(5, 10, 5, 5)
        payment_layout.setVerticalSpacing(5)
        payment_layout.setHorizontalSpacing(5)
        
        # Subtotal
        subtotal_label = QLabel("SUBTOTAL:")
        subtotal_label.setStyleSheet("font-size: 10px; font-weight: bold;")
        subtotal_field = QLineEdit()
        subtotal_field.setFixedHeight(20)
        payment_layout.addRow(subtotal_label, subtotal_field)
        
        # VAT
        vat_label = QLabel("VAT (if applicable):")
        vat_label.setStyleSheet("font-size: 10px;")
        vat_field = QLineEdit()
        vat_field.setFixedHeight(20)
        payment_layout.addRow(vat_label, vat_field)
        
        # Total amount
        total_label = QLabel("TOTAL AMOUNT:")
        total_label.setStyleSheet("font-size: 10px; font-weight: bold;")
        total_field = QLineEdit()
        total_field.setFixedHeight(20)
        payment_layout.addRow(total_label, total_field)
        
        # Payment status
        status_label = QLabel("PAYMENT STATUS:")
        status_label.setStyleSheet("font-size: 10px;")
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(10)
        
        paid_radio = QRadioButton("PAID")
        paid_radio.setStyleSheet("font-size: 10px;")
        unpaid_radio = QRadioButton("UNPAID")
        unpaid_radio.setStyleSheet("font-size: 10px;")
        partial_radio = QRadioButton("PARTIAL")
        partial_radio.setStyleSheet("font-size: 10px;")
        
        status_layout.addWidget(paid_radio)
        status_layout.addWidget(unpaid_radio)
        status_layout.addWidget(partial_radio)
        status_layout.addStretch()
        
        payment_layout.addRow(status_label, status_widget)
        
        # Payment method
        method_label = QLabel("PAYMENT METHOD:")
        method_label.setStyleSheet("font-size: 10px;")
        method_widget = QWidget()
        method_layout = QGridLayout(method_widget)
        method_layout.setContentsMargins(0, 0, 0, 0)
        method_layout.setHorizontalSpacing(10)
        method_layout.setVerticalSpacing(2)
        
        cash_checkbox = QCheckBox("CASH")
        cash_checkbox.setStyleSheet("font-size: 10px;")
        credit_card_checkbox = QCheckBox("CREDIT CARD")
        credit_card_checkbox.setStyleSheet("font-size: 10px;")
        gcash_checkbox = QCheckBox("GCASH")
        gcash_checkbox.setStyleSheet("font-size: 10px;")
        bank_transfer_checkbox = QCheckBox("BANK TRANSFER")
        bank_transfer_checkbox.setStyleSheet("font-size: 10px;")
        
        method_layout.addWidget(cash_checkbox, 0, 0)
        method_layout.addWidget(credit_card_checkbox, 0, 1)
        method_layout.addWidget(gcash_checkbox, 1, 0)
        method_layout.addWidget(bank_transfer_checkbox, 1, 1)
        
        payment_layout.addRow(method_label, method_widget)
        
        # Received by
        received_by_label = QLabel("RECEIVED BY:")
        received_by_label.setStyleSheet("font-size: 10px;")
        received_by_field = QLineEdit()
        received_by_field.setFixedHeight(20)
        payment_layout.addRow(received_by_label, received_by_field)
        
        right_column.addWidget(payment_widget)
        right_column.addStretch()
        
        # Add columns to main layout
        main_layout.addLayout(left_column, 45)  # 45% of width
        main_layout.addLayout(right_column, 55)  # 55% of width
        
        layout.addWidget(main_widget)
        
        # Thank you message
        thanks_widget = QWidget()
        thanks_layout = QVBoxLayout(thanks_widget)
        thanks_layout.setContentsMargins(10, 5, 10, 5)
        
        thank_you_label = QLabel("THANK YOU FOR TRUSTING US WITH YOUR PET'S CARE!")
        thank_you_label.setAlignment(Qt.AlignCenter)
        thank_you_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        thanks_layout.addWidget(thank_you_label)
        
        layout.addWidget(thanks_widget)
        
        # Bottom buttons
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(20, 10, 20, 10)
        
        button_layout.addStretch()
        
        download_btn = QPushButton("Download")
        download_btn.setFixedSize(120, 40)
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
                color: #002D5B;
                border: 1px solid #DDDDDD;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        
        save_btn = QPushButton("Save")
        save_btn.setFixedSize(120, 40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #002D5B;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #001E3D;
            }
        """)
        save_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(download_btn)
        button_layout.addWidget(save_btn)
        
        layout.addWidget(button_container)
    
    def _create_section(self, title):
        container = QGroupBox(title)
        container.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                border: 1px solid #AAAAAA;
                border-radius: 0px;
                margin-top: 8px;
                background-color: #D6EAF8;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        return container


def update_billing_widget():
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget
    )
    from PySide6.QtCore import Qt
    
    def get_billing_widget():
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 30)

        # Header
        header = QWidget()
        header.setFixedHeight(50)
        header.setStyleSheet("background-color: #102547;")
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 0, 10, 0)
        header_layout.setSpacing(20)

        billings_label = QLabel("Billing")
        billings_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        billings_label.setAlignment(Qt.AlignVCenter)

        add_receipt_button = QPushButton("Add Receipt")
        add_receipt_button.setObjectName("AddReceiptButton")
        add_receipt_button.setFixedSize(120, 40)
        add_receipt_button.setStyleSheet("""
            QPushButton {
                background-color: #F4F4F8; 
                border: none; 
                border-radius: 20px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E4E4E8;
            }
        """)

        # Connect button to show invoice dialog
        add_receipt_button.clicked.connect(open_invoice_form)

        header_layout.addWidget(billings_label)
        header_layout.addWidget(add_receipt_button)
        header_layout.addStretch()

        header.setLayout(header_layout)
        layout.addWidget(header)

        # Table
        billings_table = QTableWidget()
        billings_table.setRowCount(5)
        billings_table.setColumnCount(8)
        billings_table.setHorizontalHeaderLabels([
            "Receipt No.", "Date Issued", "Owner/Client", 
            "Pet Name", "Total Amount (Php)", "Payment", 
            "Payment Status", "Action"
        ])
        billings_table.horizontalHeader().setStretchLastSection(True)
        billings_table.verticalHeader().setVisible(False)

        billings_table.setStyleSheet("""
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

        billings_table.setColumnWidth(0, 150)
        billings_table.setColumnWidth(1, 120)
        billings_table.setColumnWidth(2, 150)
        billings_table.setColumnWidth(3, 200)
        billings_table.setColumnWidth(4, 180)
        billings_table.setColumnWidth(5, 200)
        billings_table.setColumnWidth(6, 150)
        billings_table.setColumnWidth(7, 100)

        layout.addWidget(billings_table)

        return content
    
    def open_invoice_form():
        dialog = InvoiceFormDialog()
        if dialog.exec():
            print("Invoice saved")
        else:
            print("Invoice creation cancelled")
            
    return get_billing_widget