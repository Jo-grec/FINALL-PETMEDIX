from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QDialog, QFormLayout, QLineEdit, QComboBox, QTextEdit, QCheckBox, QGridLayout,
    QStyledItemDelegate, QGroupBox, QRadioButton, QTableWidgetItem, QHeaderView, QAbstractScrollArea, 
    QAbstractItemView, QButtonGroup, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QDoubleValidator, QIcon

from modules.database import Database
from datetime import datetime
from modules.utils import show_message


class InvoiceFormDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PetMedix - Billing")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background: none;")
        
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
        self.date_field = QLineEdit()
        self.date_field.setFixedHeight(20)
        self.date_field.setReadOnly(True)
        # Set current date
        self.date_field.setText(datetime.now().strftime("%Y-%m-%d"))
        details_form.addRow(date_label, self.date_field)
        
        invoice_label = QLabel("INVOICE NO.:")
        invoice_label.setStyleSheet("font-size: 10px;")
        invoice_field = QLineEdit()
        invoice_field.setFixedHeight(20)
        invoice_field.setReadOnly(True)
        details_form.addRow(invoice_label, invoice_field)
        
        self.invoice_field = invoice_field  # Save reference to use later
        
        vet_label = QLabel("VETERINARIAN:")
        vet_label.setStyleSheet("font-size: 10px;")
        self.vet_dropdown = QComboBox()
        self.vet_dropdown.setFixedHeight(20)
        details_form.addRow(vet_label, self.vet_dropdown)
        self.load_veterinarians()
        
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
        clinic_field.setReadOnly(True)
        from_form.addRow(clinic_label, clinic_field)
        
        address_label = QLabel("ADDRESS:")
        address_label.setStyleSheet("font-size: 10px;")
        address_field = QLineEdit()
        address_field.setFixedHeight(20)
        address_field.setReadOnly(True)
        from_form.addRow(address_label, address_field)
        
        contact_label = QLabel("CONTACT NUMBER:")
        contact_label.setStyleSheet("font-size: 10px;")
        contact_field = QLineEdit()
        contact_field.setFixedHeight(20)
        contact_field.setReadOnly(True)
        from_form.addRow(contact_label, contact_field)
        
        email_label = QLabel("EMAIL ADDRESS:")
        email_label.setStyleSheet("font-size: 10px;")
        email_field = QLineEdit()
        email_field.setFixedHeight(20)
        email_field.setReadOnly(True)
        from_form.addRow(email_label, email_field)
            
        from_container.setLayout(from_form)
        left_column.addWidget(from_container)
        
        self.clinic_field = clinic_field
        self.clinic_address_field = address_field
        self.clinic_contact_field = contact_field
        self.clinic_email_field = email_field
        
        # BILL TO section
        bill_to_container = self._create_section("BILL TO")
        bill_to_form = QFormLayout()
        bill_to_form.setContentsMargins(5, 0, 5, 5)
        bill_to_form.setVerticalSpacing(5)
        bill_to_form.setHorizontalSpacing(5)

        # Client dropdown instead of text field
        client_label = QLabel("CLIENT:")
        client_label.setStyleSheet("font-size: 10px;")
        self.client_dropdown = QComboBox()
        self.client_dropdown.setFixedHeight(20)
        self.client_dropdown.setObjectName("client_dropdown")
        # Connect signal for client selection change
        self.client_dropdown.currentIndexChanged.connect(self.on_client_selected)
        bill_to_form.addRow(client_label, self.client_dropdown)

        # These fields will be populated automatically
        self.client_address_field = QLineEdit()
        self.client_address_field.setFixedHeight(20)
        self.client_address_field.setReadOnly(True)  # Make it read-only
        client_address_label = QLabel("ADDRESS:")
        client_address_label.setStyleSheet("font-size: 10px;")
        bill_to_form.addRow(client_address_label, self.client_address_field)

        self.client_contact_field = QLineEdit()
        self.client_contact_field.setFixedHeight(20)
        self.client_contact_field.setReadOnly(True)  # Make it read-only
        client_contact_label = QLabel("CONTACT NUMBER:")
        client_contact_label.setStyleSheet("font-size: 10px;")
        bill_to_form.addRow(client_contact_label, self.client_contact_field)

        self.client_email_field = QLineEdit()
        self.client_email_field.setFixedHeight(20)
        self.client_email_field.setReadOnly(True)  # Make it read-only
        client_email_label = QLabel("EMAIL ADDRESS:")
        client_email_label.setStyleSheet("font-size: 10px;")
        bill_to_form.addRow(client_email_label, self.client_email_field)

        bill_to_container.setLayout(bill_to_form)
        left_column.addWidget(bill_to_container)
        
        # PET INFORMATION section
        pet_info_container = self._create_section("PET INFORMATION")
        pet_info_form = QFormLayout()
        pet_info_form.setContentsMargins(5, 0, 5, 5)
        pet_info_form.setVerticalSpacing(5)
        pet_info_form.setHorizontalSpacing(5)

        # Pet dropdown instead of text field
        pet_name_label = QLabel("NAME:")
        pet_name_label.setStyleSheet("font-size: 10px;")
        self.pet_dropdown = QComboBox()
        self.pet_dropdown.setFixedHeight(20)
        self.pet_dropdown.setObjectName("pet_dropdown")
        # Connect signal for pet selection change
        self.pet_dropdown.currentIndexChanged.connect(self.on_pet_selected)
        pet_info_form.addRow(pet_name_label, self.pet_dropdown)

        # These fields will be populated automatically
        self.pet_species_field = QLineEdit()
        self.pet_species_field.setFixedHeight(20)
        self.pet_species_field.setReadOnly(True)
        pet_species_label = QLabel("SPECIES:")
        pet_species_label.setStyleSheet("font-size: 10px;")
        pet_info_form.addRow(pet_species_label, self.pet_species_field)

        self.pet_breed_field = QLineEdit()
        self.pet_breed_field.setFixedHeight(20)
        self.pet_breed_field.setReadOnly(True)
        pet_breed_label = QLabel("BREED:")
        pet_breed_label.setStyleSheet("font-size: 10px;")
        pet_info_form.addRow(pet_breed_label, self.pet_breed_field)

        self.pet_age_field = QLineEdit()
        self.pet_age_field.setFixedHeight(20)
        self.pet_age_field.setReadOnly(True)
        pet_age_label = QLabel("AGE:")
        pet_age_label.setStyleSheet("font-size: 10px;")
        pet_info_form.addRow(pet_age_label, self.pet_age_field)

        pet_info_container.setLayout(pet_info_form)
        left_column.addWidget(pet_info_container)
        
        # NOTES section
        notes_container = self._create_section("NOTES")
        notes_layout = QVBoxLayout()
        notes_layout.setContentsMargins(5, 5, 5, 5)
        
        notes_edit = QTextEdit()
        notes_edit.setFixedHeight(60)
        notes_edit.setObjectName("notes_edit") 
        self.notes_edit = notes_edit
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
        self.services_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.services_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.services_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.services_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        # Set numeric-only delegate for Quantity and Unit Price columns
        numeric_delegate = NumericDelegate()
        self.services_table.setItemDelegateForColumn(1, numeric_delegate)
        self.services_table.setItemDelegateForColumn(2, numeric_delegate)

        # Connect the itemChanged signal to auto-update total
        self.services_table.itemChanged.connect(self.update_total)

        
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
        
        # Create a button group for payment methods
        self.payment_method_group = QButtonGroup(self)
        
        cash_radio = QRadioButton("CASH")
        credit_card_radio = QRadioButton("CREDIT CARD")
        gcash_radio = QRadioButton("GCASH")
        bank_transfer_radio = QRadioButton("BANK TRANSFER")

        # Style the radio buttons to look like checkboxes
        radio_style = """
            QRadioButton {
                spacing: 5px;
                font-size: 10px;
            }
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
            QRadioButton::indicator:unchecked {
                border: 1px solid #999;
                background: white;
                border-radius: 3px;
            }
            QRadioButton::indicator:checked {
                border: 1px solid #012547;
                background: #012547;
                border-radius: 3px;
            }
        """
        
        for radio in [cash_radio, credit_card_radio, gcash_radio, bank_transfer_radio]:
            radio.setStyleSheet(radio_style)
            self.payment_method_group.addButton(radio)

        # Store radio buttons as instance variables for later access
        self.payment_method_radios = {
            "CASH": cash_radio,
            "CREDIT CARD": credit_card_radio,
            "GCASH": gcash_radio,
            "BANK TRANSFER": bank_transfer_radio
        }
        
        method_layout.addWidget(cash_radio, 0, 0)
        method_layout.addWidget(credit_card_radio, 0, 1)
        method_layout.addWidget(gcash_radio, 1, 0)
        method_layout.addWidget(bank_transfer_radio, 1, 1)
        
        payment_layout.addRow(method_label, method_widget)
        
        # Replace the "Received By" field with a dropdown
        received_by_label = QLabel("RECEIVED BY:")
        received_by_label.setStyleSheet("font-size: 10px;")
        self.received_by_dropdown = QComboBox()
        self.received_by_dropdown.setFixedHeight(20)
        self.received_by_dropdown.setObjectName("received_by_dropdown")
        self.load_receptionists()  # Load receptionists into the dropdown
        payment_layout.addRow(received_by_label, self.received_by_dropdown)
        
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
        
        db = Database()
        try:
            new_invoice_no = db.generate_invoice_no()
            self.invoice_field.setText(new_invoice_no)
        finally:
            db.close_connection()
            
        db = Database()
        try:
            if db.conn:
                clinic = db.get_clinic_info()
                if clinic:
                    self.clinic_field.setText(clinic["name"] or "")
                    self.clinic_address_field.setText(clinic["address"] or "")
                    self.clinic_contact_field.setText(clinic["contact_number"] or "")
                    self.clinic_email_field.setText(clinic["email"] or "")
            else:
                print("❌ Could not connect to database.")
        finally:
            if db.conn:
                db.close_connection()
        
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
        
        # Load clients into the dropdown
        self.load_clients()
        
        # Set current date
        self.date_field.setText(datetime.now().strftime("%Y-%m-%d"))
        
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

        
    def update_total(self, item):
        """Update the total amount when quantity or unit price changes."""
        row = item.row()
        col = item.column()

        if col not in [1, 2]:  # Only process quantity and unit price columns
            return

        try:
            # Get quantity and unit price values
            quantity_item = self.services_table.item(row, 1)
            unit_price_item = self.services_table.item(row, 2)

            quantity = float(quantity_item.text()) if quantity_item and quantity_item.text() else 0.0
            unit_price = float(unit_price_item.text()) if unit_price_item and unit_price_item.text() else 0.0
            
            # Calculate row total
            total = quantity * unit_price

            # Update row total
            total_item = QTableWidgetItem(f"{total:.2f}")
            total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)  # Make total read-only
            self.services_table.setItem(row, 3, total_item)

            # Calculate and update subtotal
            subtotal = 0.0
            for r in range(self.services_table.rowCount()):
                total_item = self.services_table.item(r, 3)
                if total_item and total_item.text():
                    subtotal += float(total_item.text())

            # Update subtotal field
            subtotal_field = self.findChild(QLineEdit, "subtotal_field")
            if subtotal_field:
                subtotal_field.setText(f"{subtotal:.2f}")

            # Calculate and update VAT (assuming 12% VAT)
            vat = subtotal * 0.12
            vat_field = self.findChild(QLineEdit, "vat_field")
            if vat_field:
                vat_field.setText(f"{vat:.2f}")

            # Update total amount
            total_amount = subtotal + vat
            total_field = self.findChild(QLineEdit, "total_amount_field")
            if total_field:
                total_field.setText(f"{total_amount:.2f}")

        except ValueError:
            pass  # Ignore invalid input

    def get_invoice_data(self):
        """Get all the data from the invoice form."""
        # Find all form fields with their labels
        all_fields = {}
        
        # Find all QLineEdit objects in the dialog
        for line_edit in self.findChildren(QLineEdit):
            all_fields[line_edit.objectName()] = line_edit.text()
        
        # Get the date - look for date field or field containing 'date'
        date_field = self.findChild(QLineEdit, "date_field")
        if not date_field:
            # Try alternative names
            for name in all_fields.keys():
                if 'date' in name.lower():
                    date_field = self.findChild(QLineEdit, name)
                    break
        date_str = date_field.text() if date_field else datetime.now().strftime("%Y-%m-%d")
        
        # Get the invoice number - look for invoice_no or field containing 'invoice'
        invoice_field = self.findChild(QLineEdit, "invoice_no_field")
        if not invoice_field:
            for name in all_fields.keys():
                if 'invoice' in name.lower():
                    invoice_field = self.findChild(QLineEdit, name)
                    break
        invoice_no = invoice_field.text() if invoice_field else ""
        
        veterinarian = self.vet_dropdown.currentText() if self.vet_dropdown.currentIndex() > 0 else ""

        # Get the reason for visit
        reason_field = self.findChild(QLineEdit, "reason_field")
        if not reason_field:
            for name in all_fields.keys():
                if 'reason' in name.lower():
                    reason_field = self.findChild(QLineEdit, name)
                    break
        reason = reason_field.text() if reason_field else ""
        
        # Get client name
        client_field = self.findChild(QLineEdit, "client_field")
        if not client_field:
            for name in all_fields.keys():
                if 'client' in name.lower():
                    client_field = self.findChild(QLineEdit, name)
                    break
        client_name = client_field.text() if client_field else ""
        
        # Get pet name
        pet_name_field = self.findChild(QLineEdit, "pet_name_field")
        if not pet_name_field:
            for name in all_fields.keys():
                if 'pet' in name.lower() and 'name' in name.lower():
                    pet_name_field = self.findChild(QLineEdit, name)
                    break
        pet_name = pet_name_field.text() if pet_name_field else ""
        
        # Get notes directly using the class instance reference
        notes = self.notes_edit.toPlainText() if hasattr(self, 'notes_edit') and self.notes_edit else ""
                
        # Get payment information
        subtotal_field = self.findChild(QLineEdit, "subtotal_field")
        if not subtotal_field:
            for name in all_fields.keys():
                if 'subtotal' in name.lower():
                    subtotal_field = self.findChild(QLineEdit, name)
                    break
        subtotal_text = subtotal_field.text() if subtotal_field else "0"
        subtotal = float(subtotal_text) if subtotal_text and subtotal_text.strip() else 0
        
        vat_field = self.findChild(QLineEdit, "vat_field")
        if not vat_field:
            for name in all_fields.keys():
                if 'vat' in name.lower():
                    vat_field = self.findChild(QLineEdit, name)
                    break
        vat_text = vat_field.text() if vat_field else "0"
        vat = float(vat_text) if vat_text and vat_text.strip() else 0
        
        # Critical field: total amount - be more thorough in finding it
        total_field = self.findChild(QLineEdit, "total_amount_field")
        if not total_field:
            for name in all_fields.keys():
                if ('total' in name.lower() and 'amount' in name.lower()) or 'total_' in name.lower():
                    total_field = self.findChild(QLineEdit, name)
                    break
        
        # If still not found, look for any field with "total" in the name
        if not total_field:
            for name in all_fields.keys():
                if 'total' in name.lower():
                    total_field = self.findChild(QLineEdit, name)
                    break
        
        # If we have a total field, get its value and convert to float
        total_text = total_field.text() if total_field else "0"
        try:
            # Remove any currency symbols or commas
            cleaned_total = total_text.replace('₱', '').replace(',', '').strip()
            total_amount = float(cleaned_total) if cleaned_total else 0
        except ValueError:
            total_amount = 0
        
        # If the total is still 0, try calculating it from subtotal + VAT
        if total_amount == 0 and (subtotal > 0 or vat > 0):
            total_amount = subtotal + vat
        
        # Get payment status
        payment_status = "Unpaid"  # Default
        for radio in self.findChildren(QRadioButton):
            if radio.isChecked():
                if "paid" in radio.text().lower() and "un" not in radio.text().lower():
                    payment_status = "Paid"
                elif "partial" in radio.text().lower():
                    payment_status = "Partial"
        
        # Get payment method
        payment_method = None
        checked_button = self.payment_method_group.checkedButton()
        if checked_button:
            payment_method = checked_button.text()

        # Get received by
        received_by_field = self.findChild(QLineEdit, "received_by_field")
        if not received_by_field:
            for name in all_fields.keys():
                if 'received' in name.lower():
                    received_by_field = self.findChild(QLineEdit, name)
                    break
        received_by = received_by_field.text() if received_by_field else ""
        
        # For client name, get from the dropdown instead
        client_index = self.client_dropdown.currentIndex()
        client_name = self.client_dropdown.currentText() if client_index > 0 else ""
        client_id = self.client_dropdown.itemData(client_index) if client_index > 0 else None
        
        # For pet name, get from the dropdown instead
        pet_index = self.pet_dropdown.currentIndex()
        pet_name = self.pet_dropdown.currentText() if pet_index > 0 else ""
        pet_id = self.pet_dropdown.itemData(pet_index) if pet_index > 0 else None
        
        return {
            "date_issued": date_str,
            "invoice_no": invoice_no,
            "veterinarian": veterinarian,
            "reason": reason,
            "client_name": client_name,
            "client_id": client_id,
            "pet_name": pet_name,
            "pet_id": pet_id,
            "notes": notes,
            "total_amount": total_amount,
            "payment_status": payment_status,
            "payment_method": payment_method,
            "received_by": received_by
        }
        
    def load_clients(self):
        """Load all clients into the client dropdown."""
        db = Database()
        try:
            db.cursor.execute("SELECT client_id, name FROM clients ORDER BY name")
            clients = db.cursor.fetchall()
            
            # Clear the dropdown and add clients
            self.client_dropdown.clear()
            self.client_dropdown.addItem("-- Select Client --", None)  # Default empty option
            
            for client_id, name in clients:
                self.client_dropdown.addItem(name, client_id)  # Store client_id as user data
                
        except Exception as e:
            print(f"❌ Error loading clients: {e}")
        finally:
            db.close_connection()
            
    def load_receptionists(self):
        """Load receptionist names into the received_by_dropdown."""
        db = Database()
        try:
            # Fetch receptionist names from the database
            db.cursor.execute("SELECT user_id, name FROM users WHERE role = 'Receptionist' ORDER BY name")
            receptionists = db.cursor.fetchall()

            # Clear the dropdown and add receptionists
            self.received_by_dropdown.clear()
            self.received_by_dropdown.addItem("-- Select Receptionist --", None)  # Default placeholder

            for user_id, name in receptionists:
                self.received_by_dropdown.addItem(name, user_id)  # Store user_id as user data

        except Exception as e:
            print(f"❌ Error loading receptionists: {e}")
        finally:
            db.close_connection()
            
    def load_veterinarians(self):
        """Load all veterinarians into the vet dropdown."""
        db = Database()
        try:
            db.cursor.execute("SELECT user_id, name, last_name FROM users WHERE role = 'Veterinarian' ORDER BY name")
            vets = db.cursor.fetchall()

            self.vet_dropdown.clear()
            self.vet_dropdown.addItem("-- Select Veterinarian --", None)

            for user_id, name, last_name in vets:
                full_name = f"{name} {last_name}".strip()
                self.vet_dropdown.addItem(full_name, user_id)
        except Exception as e:
            print(f"❌ Error loading veterinarians: {e}")
        finally:
            db.close_connection()

    def on_client_selected(self, index):
        """Handle client selection and update related fields."""
        if index <= 0:  # Skip the default "Select Client" item
            # Clear client fields
            self.client_address_field.clear()
            self.client_contact_field.clear()
            self.client_email_field.clear()
            # Clear pet dropdown
            self.pet_dropdown.clear()
            return
            
        # Get the selected client_id
        client_id = self.client_dropdown.itemData(index)
        
        # Load client details
        db = Database()
        try:
            # Get client info
            db.cursor.execute("""
                SELECT name, address, contact_number, email 
                FROM clients 
                WHERE client_id = ?
            """, (client_id,))
            
            client_info = db.cursor.fetchone()
            if client_info:
                _, address, contact_number, email = client_info
                
                # Update client fields
                self.client_address_field.setText(address or "")
                self.client_contact_field.setText(contact_number or "")
                self.client_email_field.setText(email or "")
                
                # Load pets for this client
                self.load_pets_for_client(client_id)
                
        except Exception as e:
            print(f"❌ Error loading client details: {e}")
        finally:
            db.close_connection()

    def load_pets_for_client(self, client_id):
        """Load pets for the selected client."""
        db = Database()
        try:
            db.cursor.execute("""
                SELECT pet_id, name 
                FROM pets 
                WHERE client_id = ? 
                ORDER BY name
            """, (client_id,))
            
            pets = db.cursor.fetchall()
            
            # Clear and populate the pet dropdown
            self.pet_dropdown.clear()
            self.pet_dropdown.addItem("-- Select Pet --", None)  # Default empty option
            
            for pet_id, name in pets:
                self.pet_dropdown.addItem(name, pet_id)  # Store pet_id as user data
                
        except Exception as e:
            print(f"❌ Error loading pets: {e}")
        finally:
            db.close_connection()

    def on_pet_selected(self, index):
        """Handle pet selection and update related fields."""
        if index <= 0:  # Skip the default "Select Pet" item
            # Clear pet fields only, not client fields
            self.pet_species_field.clear()
            self.pet_breed_field.clear()
            self.pet_age_field.clear()
            # Clear services table
            self.services_table.setRowCount(0)
            return
            
        # Get the selected pet_id
        pet_id = self.pet_dropdown.itemData(index)
        
        # Load pet details
        db = Database()
        try:
            db.cursor.execute("""
                SELECT species, breed, age 
                FROM pets 
                WHERE pet_id = ?
            """, (pet_id,))
            
            pet_info = db.cursor.fetchone()
            if pet_info:
                species, breed, age = pet_info
                
                # Update pet fields ONLY, don't touch client fields
                self.pet_species_field.setText(species or "")
                self.pet_breed_field.setText(breed or "")
                self.pet_age_field.setText(str(age) if age else "")
                
                # Load services for this pet
                self.load_services_for_pet(pet_id)
                
        except Exception as e:
            print(f"❌ Error loading pet details: {e}")
        finally:
            db.close_connection()

    def load_services_for_pet(self, pet_id):
        """Load services from medical reports for the selected pet."""
        try:
            db = Database()
            cursor = db.cursor

            # Fetch medical records for this pet
            cursor.execute("""
                SELECT 
                    mr.date,
                    mr.type,
                    mr.reason,
                    mr.diagnosis,
                    mr.prescribed_treatment,
                    mr.veterinarian
                FROM medical_records mr
                WHERE mr.pet_id = ?
                ORDER BY mr.date DESC
            """, (pet_id,))
            
            services = cursor.fetchall()
            
            # Clear existing items in the services table
            self.services_table.setRowCount(0)
            
            # Add services to the table
            for row_num, service in enumerate(services):
                self.services_table.insertRow(row_num)
                
                # Create service description item with type as the main description
                service_desc = f"{service[1]}"  # Just use the type
                service_item = QTableWidgetItem(service_desc)
                service_item.setFlags(service_item.flags() & ~Qt.ItemIsEditable)  # Make read-only
                self.services_table.setItem(row_num, 0, service_item)
                
                # Add tooltip with full details
                tooltip = f"Date: {service[0]}\nReason: {service[2]}\nDiagnosis: {service[3]}\nTreatment: {service[4]}\nVeterinarian: {service[5]}"
                service_item.setToolTip(tooltip)
                
                # Add quantity field (default to 1)
                quantity_item = QTableWidgetItem("1")
                self.services_table.setItem(row_num, 1, quantity_item)
                
                # Add unit price field with default price based on service type
                default_price = self.get_default_price(service[1])  # Get default price based on service type
                price_item = QTableWidgetItem(f"{default_price:.2f}")
                self.services_table.setItem(row_num, 2, price_item)
                
                # Add total field (will be calculated)
                total_item = QTableWidgetItem(f"{default_price:.2f}")  # Initial total same as price
                total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)  # Make read-only
                self.services_table.setItem(row_num, 3, total_item)
            
            # Set column widths
            self.services_table.setColumnWidth(0, int(self.services_table.width() * 0.40))  # Service description
            self.services_table.setColumnWidth(1, int(self.services_table.width() * 0.15))  # Quantity
            self.services_table.setColumnWidth(2, int(self.services_table.width() * 0.20))  # Unit price
            self.services_table.setColumnWidth(3, int(self.services_table.width() * 0.25))  # Total
            
            db.close_connection()
            
        except Exception as e:
            print(f"Error loading services: {e}")
            
    def get_default_price(self, service_type):
        """Get default price based on service type."""
        prices = {
            "Consultation": 500.00,
            "Deworming": 300.00,
            "Vaccination": 800.00,
            "Surgery": 2000.00,
            "Grooming": 400.00,
            "Other": 200.00
        }
        return prices.get(service_type, 200.00)  # Default to 200.00 if service type not found

    def on_payment_method_changed(self, state):
        """Handle payment method checkbox state changes to ensure only one is checked."""
        if state == Qt.Checked:
            # Get the checkbox that triggered this signal
            sender = self.sender()
            # Uncheck all other checkboxes
            for checkbox in self.payment_method_radios.values():
                if checkbox != sender:
                    checkbox.setChecked(False)
            
def open_invoice_form():
    """Open the invoice form dialog."""
    dialog = InvoiceFormDialog()
    if dialog.exec():
        # If the dialog was accepted (Save button clicked)
        try:
            # Get the form data
            invoice_data = dialog.get_invoice_data()
            
            # Save to database
            db = Database()
            try:
                # Save the main billing record
                billing_id = db.save_billing(
                    client_id=invoice_data['client_id'],
                    pet_id=invoice_data['pet_id'],
                    date_issued=invoice_data['date_issued'],
                    total_amount=invoice_data['total_amount'],
                    payment_status=invoice_data['payment_status'],
                    payment_method=invoice_data['payment_method'],
                    received_by=invoice_data['received_by'],
                    invoice_no=invoice_data['invoice_no'],
                    reason=invoice_data['reason'],
                    veterinarian=invoice_data['veterinarian'],
                    notes=invoice_data['notes']
                )
                
                if billing_id:
                    # Save the services
                    for row in range(dialog.services_table.rowCount()):
                        service_desc = dialog.services_table.item(row, 0).text()
                        quantity = float(dialog.services_table.item(row, 1).text())
                        unit_price = float(dialog.services_table.item(row, 2).text())
                        line_total = float(dialog.services_table.item(row, 3).text())
                        
                        db.cursor.execute("""
                            INSERT INTO billing_services 
                            (billing_id, service_description, quantity, unit_price, line_total)
                            VALUES (?, ?, ?, ?, ?)
                        """, (billing_id, service_desc, quantity, unit_price, line_total))
                    
                    db.conn.commit()
                    show_message(None, "Invoice saved successfully!")
                    return True
                else:
                    show_message(None, "Failed to save invoice", QMessageBox.Critical)
                    return False
                    
            except Exception as e:
                print(f"❌ Error saving invoice: {e}")
                show_message(None, f"Error saving invoice: {str(e)}", QMessageBox.Critical)
                return False
            finally:
                db.close_connection()
                
        except Exception as e:
            print(f"❌ Error processing invoice form: {e}")
            show_message(None, f"Error processing invoice: {str(e)}", QMessageBox.Critical)
            return False
    return False

def update_billing_widget():
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
        QTableWidgetItem, QMessageBox
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

        # Create the table
        billings_table = QTableWidget()
        billings_table.setEditTriggers(QTableWidget.NoEditTriggers)
        billings_table.setObjectName("BillingsTable")
        billings_table.setRowCount(0)
        billings_table.setColumnCount(8)
        billings_table.setHorizontalHeaderLabels([
            "Receipt No.", "Date Issued", "Owner/Client",
            "Pet Name", "Total Amount (Php)", "Payment",
            "Payment Status", "Action"
        ])
        billings_table.horizontalHeader().setStretchLastSection(True)
        billings_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Make columns non-resizable
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

        # Set column widths
        for i, width in enumerate([150, 120, 150, 200, 180, 150, 150, 80]):
            billings_table.setColumnWidth(i, width)

        def view_invoice_details(row):
            """Show invoice details in view-only mode."""
            try:
                # Get the billing ID from the row
                receipt_no = billings_table.item(row, 0).text()
                billing_id = int(receipt_no.split('-')[-1]) if '-' in receipt_no else int(receipt_no)

                # Create a view-only version of the invoice form
                dialog = InvoiceFormDialog()
                dialog.setWindowTitle("View Invoice Details")
                
                # Make all fields read-only
                for widget in dialog.findChildren((QLineEdit, QTextEdit, QComboBox)):
                    if isinstance(widget, QLineEdit):
                        widget.setReadOnly(True)
                    elif isinstance(widget, QTextEdit):
                        widget.setReadOnly(True)
                    elif isinstance(widget, QComboBox):
                        widget.setEnabled(False)

                # Disable all radio buttons
                for radio in dialog.findChildren(QRadioButton):
                    radio.setEnabled(False)

                # Disable the services table
                dialog.services_table.setEditTriggers(QTableWidget.NoEditTriggers)

                # Load the invoice data
                db = Database()
                try:
                    # Fetch complete invoice data
                    db.cursor.execute("""
                        SELECT b.*, c.name as client_name, p.name as pet_name,
                               c.address as client_address, c.contact_number as client_contact,
                               c.email as client_email, p.species, p.breed, p.age
                        FROM billing b
                        JOIN clients c ON b.client_id = c.client_id
                        JOIN pets p ON b.pet_id = p.pet_id
                        WHERE b.billing_id = ?
                    """, (billing_id,))
                    
                    invoice_data = db.cursor.fetchone()
                    if invoice_data:
                        # Populate the form with invoice data
                        dialog.invoice_field.setText(invoice_data['invoice_no'])
                        
                        # Set client info
                        dialog.client_dropdown.addItem(invoice_data['client_name'])
                        dialog.client_address_field.setText(invoice_data['client_address'])
                        dialog.client_contact_field.setText(invoice_data['client_contact'])
                        dialog.client_email_field.setText(invoice_data['client_email'])
                        
                        # Set pet info
                        dialog.pet_dropdown.addItem(invoice_data['pet_name'])
                        dialog.pet_species_field.setText(invoice_data['species'])
                        dialog.pet_breed_field.setText(invoice_data['breed'])
                        dialog.pet_age_field.setText(str(invoice_data['age']))
                        
                        # Set other fields
                        dialog.notes_edit.setText(invoice_data['notes'] or "")
                        
                        # Set payment status
                        for radio in dialog.findChildren(QRadioButton):
                            if radio.text().upper() == invoice_data['payment_status'].upper():
                                radio.setChecked(True)
                                break
                        
                        # Set payment method
                        for radio in dialog.payment_method_radios.values():
                            if radio.text() == invoice_data['payment_method']:
                                radio.setChecked(True)
                                break
                        
                        # Load services for this invoice
                        db.cursor.execute("""
                            SELECT service_description, quantity, unit_price, line_total
                            FROM billing_services
                            WHERE billing_id = ?
                        """, (billing_id,))
                        
                        services = db.cursor.fetchall()
                        dialog.services_table.setRowCount(len(services))
                        
                        for i, service in enumerate(services):
                            dialog.services_table.setItem(i, 0, QTableWidgetItem(service[0]))
                            dialog.services_table.setItem(i, 1, QTableWidgetItem(str(service[1])))
                            dialog.services_table.setItem(i, 2, QTableWidgetItem(f"{service[2]:.2f}"))
                            dialog.services_table.setItem(i, 3, QTableWidgetItem(f"{service[3]:.2f}"))

                except Exception as e:
                    print(f"❌ Error loading invoice details: {e}")
                finally:
                    db.close_connection()

                # Show the dialog
                dialog.exec()

            except Exception as e:
                print(f"❌ Error viewing invoice details: {e}")

        def edit_invoice(billing_id):
            print(f"✏️ Edit invoice: {billing_id}")
            # Open the InvoiceFormDialog in edit mode
            dialog = InvoiceFormDialog()
            # TODO: Load the invoice data into the dialog for editing
            if dialog.exec():
                # Save changes to the database
                load_billing_data()

        def delete_invoice(billing_id):
            confirm = QMessageBox()
            confirm.setIcon(QMessageBox.Question)
            confirm.setText("Are you sure you want to delete this invoice?")
            confirm.setWindowTitle("")
            confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if confirm.exec() == QMessageBox.Yes:
                try:
                    db = Database()
                    db.delete_invoice(billing_id)
                    load_billing_data()  # Changed from refresh_tables to load_billing_data
                    show_message(None, "Invoice deleted successfully.")
                except Exception as e:
                    show_message(None, f"Error deleting invoice: {str(e)}", QMessageBox.Critical)

        def create_action_buttons(billing_id):
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(10)
            action_layout.setAlignment(Qt.AlignCenter)  # Center the buttons

            edit_btn = QPushButton("Edit")
            edit_btn.setFixedWidth(70)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FED766;
                    border: none;
                    border-radius: 5px;
                    font-size: 10px;
                    padding: 5px 8px;
                    min-height: 10px;
                    min-width: 50px
                }
                QPushButton:hover {
                    background-color: #FFC107;
                }
            """)
            edit_btn.clicked.connect(lambda _, bid=billing_id: edit_invoice(bid))

            delete_btn = QPushButton("Delete")
            delete_btn.setFixedWidth(70)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF6F61;
                    border: none;
                    border-radius: 5px;
                    font-size: 10px;
                    padding: 5px 8px;
                    min-height: 10px;
                    min-width: 50px
                }
                QPushButton:hover {
                    background-color: #E53935;
                }
            """)
            delete_btn.clicked.connect(lambda _, bid=billing_id: delete_invoice(bid))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)

            return action_widget

        # Function to load data into the table
        def load_billing_data():
            db = Database()
            try:
                billing_data = db.fetch_billing_data()

                billings_table.setRowCount(0)  # Clear the table

                for row_num, data in enumerate(billing_data):
                    billings_table.insertRow(row_num)

                    # Create table items
                    receipt_no = QTableWidgetItem(str(data[1] or f"REC-{data[0]}"))
                    date_issued = QTableWidgetItem(data[2].strftime("%Y-%m-%d") if isinstance(data[2], datetime) else str(data[2]))
                    client_name = QTableWidgetItem(str(data[3]))
                    pet_name = QTableWidgetItem(str(data[4]))
                    total_amount = QTableWidgetItem(f"₱ {data[5]:.2f}")
                    payment_method = QTableWidgetItem(str(data[6] or ""))
                    payment_status = QTableWidgetItem(str(data[7]))

                    # Create action buttons for THIS row
                    action_widget = create_action_buttons(data[0])

                    # Add items to table
                    billings_table.setItem(row_num, 0, receipt_no)
                    billings_table.setItem(row_num, 1, date_issued)
                    billings_table.setItem(row_num, 2, client_name)
                    billings_table.setItem(row_num, 3, pet_name)
                    billings_table.setItem(row_num, 4, total_amount)
                    billings_table.setItem(row_num, 5, payment_method)
                    billings_table.setItem(row_num, 6, payment_status)
                    billings_table.setCellWidget(row_num, 7, action_widget)

                # Connect the cellClicked signal to handle row clicks
                billings_table.cellClicked.connect(lambda row, col: view_invoice_details(row))

            except Exception as e:
                print(f"❌ Error loading billing data: {e}")
            finally:
                db.close_connection()

        # Connect button to the function
        add_receipt_button.clicked.connect(open_invoice_form)
        
        header_layout.addWidget(billings_label)
        header_layout.addWidget(add_receipt_button)
        header_layout.addStretch()

        header.setLayout(header_layout)
        layout.addWidget(header)
        layout.addWidget(billings_table)

        # Load existing billing data when the widget is created
        load_billing_data()

        return content
            
    return get_billing_widget

class NumericDelegate(QStyledItemDelegate):
    """Delegate for handling numeric input in table cells."""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QDoubleValidator(0.0, 999999.99, 2, parent)
        editor.setValidator(validator)
        return editor


    


