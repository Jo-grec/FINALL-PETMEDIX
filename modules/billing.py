from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QDialog, QFormLayout, QLineEdit, QComboBox, QTextEdit, QCheckBox, QGridLayout,
    QStyledItemDelegate, QGroupBox, QRadioButton, QTableWidgetItem, QHeaderView, QAbstractScrollArea, 
    QAbstractItemView, QButtonGroup, QMessageBox, QFileDialog, QCalendarWidget
)
from PySide6.QtCore import Qt, QDate, QSize, QTimer
from PySide6.QtGui import QDoubleValidator, QIcon
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import datetime
import os

from modules.database import Database
from modules.utils import show_message, create_styled_message_box


class InvoiceFormDialog(QDialog):
    def __init__(self, is_view_mode=False, user_role=None):
        try:
            print("\n=== Debug: Initializing InvoiceFormDialog ===")
            super().__init__()
            self.setWindowTitle("PetMedix - Billing")
            self.setFixedSize(1000, 750)
            self.setStyleSheet("background: none;")
            
            # Store signal connection state
            self.services_table_connected = False
            self.is_partial_amount_valid = True  # Track partial amount validity
            self.is_view_mode = is_view_mode
            self.partial_amount_connected = False  # Track if partial amount signal is connected
            self.user_role = user_role  # Store user_role
            
            # Add a timer for delayed loading
            self.load_timer = QTimer(self)
            self.load_timer.setSingleShot(True)
            self.load_timer.timeout.connect(self.delayed_load_services)
            self.pending_pet_id = None
            
            # Initialize database connection
            self.db = None
            try:
                self.db = Database()
                print("Database connection established")
            except Exception as db_error:
                print(f"Error connecting to database: {db_error}")
                QMessageBox.critical(self, "Error", "Failed to connect to database. Please try again.")
                raise
            
            # Create the UI
            print("Setting up UI...")
            self.setup_ui()
            print("UI setup complete")
            
        except Exception as e:
            print(f"Error in InvoiceFormDialog initialization: {e}")
            import traceback
            traceback.print_exc()
            raise

    def __del__(self):
        """Cleanup when dialog is destroyed."""
        try:
            if hasattr(self, 'db') and self.db:
                self.db.close_connection()
        except:
            pass

    def setup_ui(self):
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
        self.date_field.setReadOnly(True)  # Make date field read-only
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
        self.reason_dropdown = QComboBox()
        self.reason_dropdown.setFixedHeight(20)
        self.reason_dropdown.addItems([
            "-- Select Treatment Type --",
            "Consultation",
            "Deworming",
            "Vaccination",
            "Surgery",
            "Grooming",
            "Other Treatments"
        ])
        details_form.addRow(reason_label, self.reason_dropdown)
        
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

        # Add control number field
        self.client_control_number_field = QLineEdit()
        self.client_control_number_field.setFixedHeight(20)
        self.client_control_number_field.setReadOnly(True)  # Make it read-only
        client_control_label = QLabel("CONTROL NUMBER:")
        client_control_label.setStyleSheet("font-size: 10px;")
        bill_to_form.addRow(client_control_label, self.client_control_number_field)

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
        notes_layout.setContentsMargins(1, 1, 1, 1)
        
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
        
        self.services_table = QTableWidget(0, 6)  # Start with 0 rows instead of 8
        self.services_table.setHorizontalHeaderLabels([
            "",  # For the checkbox
            "SERVICES",
            "DATE",
            "QTY",
            "UNIT PRICE",
            "TOTAL"
        ])
        self.services_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #CFDEF3; font-weight: bold; font-size: 10px; }")
        self.services_table.verticalHeader().setVisible(False)
        self.services_table.setShowGrid(True)
        self.services_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.services_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.services_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.services_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        
        # Set numeric-only delegate for Quantity and Unit Price columns
        numeric_delegate = NumericDelegate()
        self.services_table.setItemDelegateForColumn(3, numeric_delegate)  # Quantity
        self.services_table.setItemDelegateForColumn(4, numeric_delegate)  # Unit Price

        # Don't connect itemChanged signal here - we'll do it after loading data
        self.services_table_connected = False

        # Calculate proportional column widths
        table_width = 450
        self.services_table.setColumnWidth(0, 20)  # Checkbox
        self.services_table.setColumnWidth(1, 200)  # Service description
        self.services_table.setColumnWidth(2, 90)  # Date
        self.services_table.setColumnWidth(3, 60)  # Quantity
        self.services_table.setColumnWidth(4, 80)  # Unit price
        self.services_table.setColumnWidth(5, 80)  # Total
        
        self.services_table.setMaximumHeight(300)  # Limit table height
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
        self.subtotal_field = QLineEdit()
        self.subtotal_field.setFixedHeight(20)
        self.subtotal_field.setReadOnly(True)  # Make subtotal read-only
        self.subtotal_field.setText("0.00")  # Initialize to zero
        payment_layout.addRow(subtotal_label, self.subtotal_field)
        
        # VAT
        vat_label = QLabel("VAT (if applicable):")
        vat_label.setStyleSheet("font-size: 10px;")
        self.vat_field = QLineEdit()
        self.vat_field.setFixedHeight(20)
        self.vat_field.setReadOnly(True)  # Make VAT read-only
        self.vat_field.setText("0.00")  # Initialize to zero
        payment_layout.addRow(vat_label, self.vat_field)
        
        # Total amount
        total_label = QLabel("TOTAL AMOUNT:")
        total_label.setStyleSheet("font-size: 10px; font-weight: bold;")
        self.total_field = QLineEdit()
        self.total_field.setFixedHeight(20)
        self.total_field.setReadOnly(True)  # Make total read-only
        self.total_field.setText("0.00")  # Initialize to zero
        payment_layout.addRow(total_label, self.total_field)
        
        # Payment status
        status_label = QLabel("PAYMENT STATUS:")
        status_label.setStyleSheet("font-size: 10px;")
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(10)
        
        # Create button group for payment status
        self.payment_status_group = QButtonGroup(self)
        
        paid_radio = QRadioButton("PAID")
        paid_radio.setStyleSheet("font-size: 10px;")
        unpaid_radio = QRadioButton("UNPAID")
        unpaid_radio.setStyleSheet("font-size: 10px;")
        partial_radio = QRadioButton("PARTIAL")
        partial_radio.setStyleSheet("font-size: 10px;")
        
        # Add radio buttons to button group
        self.payment_status_group.addButton(paid_radio)
        self.payment_status_group.addButton(unpaid_radio)
        self.payment_status_group.addButton(partial_radio)
        
        status_layout.addWidget(paid_radio)
        status_layout.addWidget(unpaid_radio)
        status_layout.addWidget(partial_radio)
        status_layout.addStretch()
        
        payment_layout.addRow(status_label, status_widget)
        
        # Partial payment amount field (initially hidden)
        self.partial_amount_label = QLabel("PARTIAL PAYMENT AMOUNT:")
        self.partial_amount_label.setStyleSheet("font-size: 10px;")
        self.partial_amount_field = QLineEdit()
        self.partial_amount_field.setFixedHeight(20)
        self.partial_amount_field.setValidator(QDoubleValidator(0.0, 999999.99, 2))
        self.partial_amount_field.setPlaceholderText("Enter partial payment amount")
        
        # Hide partial payment field initially
        self.partial_amount_label.hide()
        self.partial_amount_field.hide()
        
        # Add partial payment field to layout
        payment_layout.addRow(self.partial_amount_label, self.partial_amount_field)
        
        # Connect radio button signals
        partial_radio.toggled.connect(self.on_payment_status_changed)
        paid_radio.toggled.connect(self.on_payment_status_changed)
        unpaid_radio.toggled.connect(self.on_payment_status_changed)
        
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
        
        # Only create and show download button if not a veterinarian
        if not self.user_role or self.user_role.lower() != "veterinarian":
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
            download_btn.clicked.connect(self.download_invoice)
            button_layout.addWidget(download_btn)
        
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
        
        if not self.is_view_mode:
            button_layout.addWidget(save_btn)
        
        layout.addWidget(button_container)
        
        # Load clients into the dropdown
        self.load_clients()
        
        # Set current date
        self.date_field.setText(datetime.now().strftime("%Y-%m-%d"))
        
        # Connect reason dropdown to refresh services
        self.reason_dropdown.currentTextChanged.connect(self.refresh_services)
        
        # If in view mode, make all fields read-only
        if self.is_view_mode:
            self.make_fields_readonly()

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
        """Update the total amount when quantity or unit price changes or when checkbox state changes."""
        try:
            # Block all signals and updates to prevent event propagation
            self.services_table.blockSignals(True)
            self.services_table.setUpdatesEnabled(False)
            
            try:
                if not item:
                    return
                    
                row = item.row()
                col = item.column()

                # Get checkbox state safely
                checkbox_item = self.services_table.item(row, 0)
                if not checkbox_item:
                    return
                    
                is_checked = checkbox_item.checkState() == Qt.Checked

                # Get quantity and unit price values safely
                quantity_item = self.services_table.item(row, 3)
                unit_price_item = self.services_table.item(row, 4)

                if not quantity_item or not unit_price_item:
                    return

                # Safely convert values to float with defaults
                try:
                    quantity = float(quantity_item.text() or "0")
                except (ValueError, TypeError):
                    quantity = 0.0
                    
                try:
                    unit_price = float(unit_price_item.text() or "0")
                except (ValueError, TypeError):
                    unit_price = 0.0
                
                # Calculate row total safely
                total = quantity * unit_price if is_checked else 0.0

                # Update row total safely
                total_item = QTableWidgetItem(f"{total:.2f}")
                total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
                self.services_table.setItem(row, 5, total_item)

                # Calculate and update subtotal safely
                subtotal = 0.0
                for r in range(self.services_table.rowCount()):
                    try:
                        checkbox = self.services_table.item(r, 0)
                        if checkbox and checkbox.checkState() == Qt.Checked:
                            total_item = self.services_table.item(r, 5)
                            if total_item and total_item.text():
                                try:
                                    subtotal += float(total_item.text() or "0")
                                except (ValueError, TypeError):
                                    continue
                    except Exception:
                        continue

                # Update subtotal field safely
                self.subtotal_field.setText(f"{subtotal:.2f}")

                # Calculate and update VAT safely
                try:
                    vat = subtotal * 0.12
                    self.vat_field.setText(f"{vat:.2f}")

                    # Update total amount safely
                    total_amount = subtotal + vat
                    self.total_field.setText(f"{total_amount:.2f}")
                except Exception:
                    self.vat_field.setText("0.00")
                    self.total_field.setText(f"{subtotal:.2f}")

            except Exception as calc_error:
                print(f"Error in calculations: {calc_error}")
                # Set safe default values
                self.subtotal_field.setText("0.00")
                self.vat_field.setText("0.00")
                self.total_field.setText("0.00")
                
        except Exception as e:
            print(f"Error in update_total: {e}")
            import traceback
            traceback.print_exc()
            # Set safe default values
            self.subtotal_field.setText("0.00")
            self.vat_field.setText("0.00")
            self.total_field.setText("0.00")
            
        finally:
            # Always re-enable signals and updates
            try:
                self.services_table.setUpdatesEnabled(True)
                self.services_table.blockSignals(False)
            except:
                pass

    def get_invoice_data(self):
        """Get all data from the invoice form."""
        try:
            print("\n=== Debug: Getting Invoice Data ===")
            
            # Get client and pet IDs
            client_id = self.client_dropdown.currentData()
            pet_id = self.pet_dropdown.currentData()
            print(f"Client ID: {client_id}")
            print(f"Pet ID: {pet_id}")
            
            # Get date and convert to YYYY-MM-DD format
            try:
                date_text = self.date_field.text()
                date_obj = datetime.strptime(date_text, "%Y-%m-%d")
                date_issued = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                # If date is in DD/MM/YYYY format, convert it
                try:
                    date_obj = datetime.strptime(date_text, "%d/%m/%Y")
                    date_issued = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    # If conversion fails, use current date
                    date_issued = datetime.now().strftime("%Y-%m-%d")
            print(f"Date Issued: {date_issued}")
            
            # Get payment details
            payment_status = self.payment_status_group.checkedButton().text()
            payment_method = None
            if payment_status != "UNPAID":
                payment_method = self.payment_method_group.checkedButton().text()
            received_by = self.received_by_dropdown.currentText()
            print(f"Payment Status: {payment_status}")
            print(f"Payment Method: {payment_method}")
            print(f"Received By: {received_by}")
            
            # Get amounts
            subtotal = float(self.subtotal_field.text().replace('₱', '').replace(',', ''))
            vat = float(self.vat_field.text().replace('₱', '').replace(',', ''))
            total_amount = float(self.total_field.text().replace('₱', '').replace(',', ''))
            partial_amount = float(self.partial_amount_field.text() or '0')
            print(f"Subtotal: {subtotal}")
            print(f"VAT: {vat}")
            print(f"Total Amount: {total_amount}")
            print(f"Partial Amount: {partial_amount}")
            
            # Get other details
            reason = self.reason_dropdown.currentText()
            veterinarian = self.vet_dropdown.currentText()
            notes = self.notes_edit.toPlainText().strip()  # Get notes and remove leading/trailing whitespace
            print(f"Reason: {reason}")
            print(f"Veterinarian: {veterinarian}")
            print(f"Notes: {notes}")
            
            # Generate invoice number
            invoice_no = self.invoice_field.text()
            print(f"Generated Invoice No: {invoice_no}")
            
            # Validate required fields
            if not client_id or not pet_id or not date_issued or not total_amount or not payment_status:
                print("❌ Missing required fields")
                return None
                
            if payment_status == 'PARTIAL' and partial_amount <= 0:
                print("❌ Partial payment amount must be greater than 0")
                return None
                
            if payment_status == 'PARTIAL' and partial_amount >= total_amount:
                print("❌ Partial payment amount must be less than total amount")
                return None
            
            data = {
                'client_id': client_id,
                'pet_id': pet_id,
                'date_issued': date_issued,
                'total_amount': total_amount,
                'payment_status': payment_status,
                'payment_method': payment_method,
                'received_by': received_by,
                'invoice_no': invoice_no,
                'reason': reason,
                'veterinarian': veterinarian,
                'notes': notes,
                'subtotal': subtotal,
                'vat': vat,
                'partial_amount': partial_amount
            }
            
            print("\nFinal Invoice Data:")
            for key, value in data.items():
                print(f"{key}: {value}")
            
            return data
            
        except Exception as e:
            print(f"❌ Error getting invoice data: {e}")
            import traceback
            traceback.print_exc()
            return None
        
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
        try:
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
            if not client_id:
                return
            
            # Load client details
            db = Database()
            try:
                # Get client info
                db.cursor.execute("""
                    SELECT name, control_number, address, contact_number, email 
                    FROM clients 
                    WHERE client_id = ?
                """, (client_id,))
                
                client_info = db.cursor.fetchone()
                if client_info:
                    _, control_number, address, contact_number, email = client_info
                    
                    # Update client fields with safe defaults
                    self.client_control_number_field.setText(str(control_number or ""))
                    self.client_address_field.setText(str(address or ""))
                    self.client_contact_field.setText(str(contact_number or ""))
                    self.client_email_field.setText(str(email or ""))
                    
                    # Load pets for this client
                    self.load_pets_for_client(client_id)
                    
            except Exception as e:
                print(f"Error loading client details: {e}")
                import traceback
                traceback.print_exc()
                # Set safe default values
                self.client_address_field.clear()
                self.client_contact_field.clear()
                self.client_email_field.clear()
                self.pet_dropdown.clear()
            finally:
                db.close_connection()
        except Exception as e:
            print(f"Error in client selection: {e}")
            import traceback
            traceback.print_exc()

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
        try:
            if index <= 0:  # Skip the default "Select Pet" item
                # Clear pet fields only, not client fields
                self.pet_species_field.clear()
                self.pet_breed_field.clear()
                self.pet_age_field.clear()
                # Clear services table only if we're not loading an existing invoice
                if not hasattr(self, 'loading_invoice') or not self.loading_invoice:
                    self.services_table.setRowCount(0)
                return
                
            # Get the selected pet_id
            pet_id = self.pet_dropdown.itemData(index)
            if not pet_id:
                return
            
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
                    
                    # Update pet fields with safe defaults
                    self.pet_species_field.setText(str(species or ""))
                    self.pet_breed_field.setText(str(breed or ""))
                    self.pet_age_field.setText(str(age) if age is not None else "")
                    
                    # Only schedule service loading if we're not loading an existing invoice
                    if not hasattr(self, 'loading_invoice') or not self.loading_invoice:
                        self.pending_pet_id = pet_id
                        self.load_timer.start(100)  # 100ms delay
                    
            except Exception as e:
                print(f"Error loading pet details: {e}")
                import traceback
                traceback.print_exc()
                # Set safe default values
                self.pet_species_field.clear()
                self.pet_breed_field.clear()
                self.pet_age_field.clear()
                if not hasattr(self, 'loading_invoice') or not self.loading_invoice:
                    self.services_table.setRowCount(0)
            finally:
                db.close_connection()
        except Exception as e:
            print(f"Error in pet selection: {e}")
            import traceback
            traceback.print_exc()

    def delayed_load_services(self):
        """Load services in a delayed manner to avoid Qt event issues."""
        if not self.pending_pet_id:
            return
            
        try:
            # Skip loading services if we're loading an existing invoice
            if hasattr(self, 'loading_invoice') and self.loading_invoice:
                print("Skipping service loading for existing invoice")
                return
                
            # Disconnect any existing itemChanged connection
            if self.services_table_connected:
                try:
                    self.services_table.itemChanged.disconnect(self.update_total)
                    self.services_table_connected = False
                except:
                    pass
            
            # Block all signals and updates
            self.services_table.blockSignals(True)
            self.services_table.setUpdatesEnabled(False)
            
            try:
                # Clear existing items safely
                while self.services_table.rowCount() > 0:
                    self.services_table.removeRow(0)
                
                db = Database()
                cursor = db.cursor

                # Get the selected reason for visit safely
                selected_reason = self.reason_dropdown.currentText() if hasattr(self, 'reason_dropdown') else "-- Select Treatment Type --"
                print(f"Selected reason: {selected_reason}")

                # Base query for all treatment types
                base_query = """
                    SELECT 
                        'Consultation' as type,
                        date,
                        COALESCE(prescribed_treatment, '') as treatment_details,
                        COALESCE(veterinarian, '') as veterinarian
                    FROM consultations
                    WHERE pet_id = ?
                    UNION ALL
                    SELECT 
                        'Deworming' as type,
                        date,
                        COALESCE(medication, '') as treatment_details,
                        COALESCE(veterinarian, '') as veterinarian
                    FROM deworming
                    WHERE pet_id = ?
                    UNION ALL
                    SELECT 
                        'Vaccination' as type,
                        date,
                        COALESCE(vaccine, '') as treatment_details,
                        COALESCE(veterinarian, '') as veterinarian
                    FROM vaccinations
                    WHERE pet_id = ?
                    UNION ALL
                    SELECT 
                        'Surgery' as type,
                        date,
                        COALESCE(surgery_type, '') as treatment_details,
                        COALESCE(veterinarian, '') as veterinarian
                    FROM surgeries
                    WHERE pet_id = ?
                    UNION ALL
                    SELECT 
                        'Grooming' as type,
                        date,
                        COALESCE(services, '') as treatment_details,
                        COALESCE(veterinarian, '') as veterinarian
                    FROM grooming
                    WHERE pet_id = ?
                    UNION ALL
                    SELECT 
                        'Other Treatments' as type,
                        date,
                        COALESCE(medication, '') as treatment_details,
                        COALESCE(veterinarian, '') as veterinarian
                    FROM other_treatments
                    WHERE pet_id = ?
                """

                # If a specific reason is selected, filter by that type
                if selected_reason and selected_reason != "-- Select Treatment Type --":
                    query = f"""
                        SELECT * FROM (
                            {base_query}
                        ) AS combined_services
                        WHERE type = ?
                        ORDER BY date DESC
                    """
                    cursor.execute(query, (self.pending_pet_id,) * 6 + (selected_reason,))
                else:
                    # If no specific reason selected, show all records
                    query = f"""
                        {base_query}
                        ORDER BY date DESC
                    """
                    cursor.execute(query, (self.pending_pet_id,) * 6)
                
                services = cursor.fetchall()
                print(f"Found {len(services)} services")
                
                # Add services to the table safely
                for row_num, service in enumerate(services):
                    try:
                        # Insert row safely
                        self.services_table.insertRow(row_num)
                        
                        # Add checkbox for selection
                        checkbox = QTableWidgetItem()
                        checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        checkbox.setCheckState(Qt.Unchecked)
                        self.services_table.setItem(row_num, 0, checkbox)
                        
                        # Format date safely
                        try:
                            date = datetime.strptime(str(service[1]), "%Y-%m-%d").strftime("%d/%m/%Y")
                        except (ValueError, TypeError):
                            date = str(service[1] or "")
                        
                        # Create service description safely
                        service_desc = f"{service[0] or ''}: {service[2] or ''}"
                        service_item = QTableWidgetItem(service_desc)
                        service_item.setFlags(service_item.flags() & ~Qt.ItemIsEditable)
                        self.services_table.setItem(row_num, 1, service_item)
                        
                        # Add date column safely
                        date_item = QTableWidgetItem(date)
                        date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
                        self.services_table.setItem(row_num, 2, date_item)
                        
                        # Add quantity field safely
                        quantity_item = QTableWidgetItem("1")
                        self.services_table.setItem(row_num, 3, quantity_item)
                        
                        # Add unit price field safely
                        default_price = self.get_default_price(service[0] or "")
                        price_item = QTableWidgetItem(f"{default_price:.2f}")
                        self.services_table.setItem(row_num, 4, price_item)
                        
                        # Add total field safely
                        total_item = QTableWidgetItem(f"{default_price:.2f}")
                        total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
                        self.services_table.setItem(row_num, 5, total_item)

                    except Exception as row_error:
                        print(f"Error processing service row {row_num}: {row_error}")
                        continue

            except Exception as db_error:
                print(f"Database error: {db_error}")
                import traceback
                traceback.print_exc()
            finally:
                # Always ensure database connection is closed
                try:
                    if db and db.conn:
                        db.close_connection()
                except:
                    pass
                
                # Re-enable signals and updates
                self.services_table.setUpdatesEnabled(True)
                self.services_table.blockSignals(False)
                
                # Reconnect the itemChanged signal
                try:
                    self.services_table.itemChanged.connect(self.update_total)
                    self.services_table_connected = True
                except:
                    pass
                
                # Clear pending pet_id
                self.pending_pet_id = None

        except Exception as e:
            print(f"Error in delayed_load_services: {e}")
            import traceback
            traceback.print_exc()
            # Ensure signals and updates are re-enabled
            try:
                self.services_table.setUpdatesEnabled(True)
                self.services_table.blockSignals(False)
            except:
                pass
            self.pending_pet_id = None

    def get_default_price(self, service_type):
        """Get default price based on service type."""
        # All prices set to 0.00 as requested
        prices = {
            "Consultation": 0.00,
            "Deworming": 0.00,
            "Vaccination": 0.00,
            "Surgery": 0.00,
            "Grooming": 0.00,
            "Other": 0.00
        }
        return prices.get(service_type, 0.00)  # Default to 0.00 if service type not found

    def on_payment_method_changed(self, state):
        """Handle payment method checkbox state changes to ensure only one is checked."""
        if state == Qt.Checked:
            # Get the checkbox that triggered this signal
            sender = self.sender()
            # Uncheck all other checkboxes
            for checkbox in self.payment_method_radios.values():
                if checkbox != sender:
                    checkbox.setChecked(False)
            
    def refresh_services(self):
        """Refresh services when reason for visit changes."""
        if hasattr(self, 'pet_dropdown') and self.pet_dropdown.currentData():
            # Use the delayed loading mechanism
            self.pending_pet_id = self.pet_dropdown.currentData()
            self.load_timer.start(100)  # 100ms delay

    def on_payment_status_changed(self, checked):
        """Handle payment status radio button changes."""
        sender = self.sender()
        if checked:
            if sender.text() == "PARTIAL":
                self.partial_amount_label.show()
                self.partial_amount_field.show()
                # Validate that partial amount is less than total
                try:
                    total = float(self.total_field.text())
                    self.partial_amount_field.setValidator(QDoubleValidator(0.0, total, 2))
                    # Connect the textChanged signal when showing the field
                    if not self.partial_amount_connected:
                        self.partial_amount_field.textChanged.connect(self.validate_partial_amount)
                        self.partial_amount_connected = True
                except ValueError:
                    pass
            elif sender.text() == "UNPAID":
                # Hide partial payment fields
                self.partial_amount_label.hide()
                self.partial_amount_field.hide()
                self.partial_amount_field.clear()
                # Disable payment method selection
                for radio in self.payment_method_radios.values():
                    radio.setEnabled(False)
                    radio.setChecked(False)
            else:  # PAID
                # Hide partial payment fields
                self.partial_amount_label.hide()
                self.partial_amount_field.hide()
                self.partial_amount_field.clear()
                # Enable payment method selection
                for radio in self.payment_method_radios.values():
                    radio.setEnabled(True)
        else:
            self.partial_amount_label.hide()
            self.partial_amount_field.hide()
            self.partial_amount_field.clear()
            # Reset validation state
            self.is_partial_amount_valid = True
            # Disconnect the signal when hiding the field
            if self.partial_amount_connected:
                try:
                    self.partial_amount_field.textChanged.disconnect(self.validate_partial_amount)
                    self.partial_amount_connected = False
                except TypeError:
                    self.partial_amount_connected = False  # Reset state even if disconnect fails

    def validate_partial_amount(self, text):
        """Validate that partial amount doesn't exceed total amount."""
        try:
            total = float(self.total_field.text())
            partial = float(text) if text else 0.0
            
            if partial > total:
                self.partial_amount_field.setStyleSheet("QLineEdit { color: red; }")
                self.is_partial_amount_valid = False
            else:
                self.partial_amount_field.setStyleSheet("")
                self.is_partial_amount_valid = True
        except ValueError:
            # Reset to default state if input is not a valid number
            self.partial_amount_field.setStyleSheet("")
            self.is_partial_amount_valid = False

    def accept(self):
        """Override accept to add validation."""
        if self.payment_status_group.checkedButton() and \
           self.payment_status_group.checkedButton().text() == "PARTIAL":
            if not self.is_partial_amount_valid:
                show_message(None, "Partial amount cannot exceed total amount", QMessageBox.Warning)
                return
            if not self.partial_amount_field.text():
                show_message(None, "Please enter partial payment amount", QMessageBox.Warning)
                return
        super().accept()

    def get_selected_payment_status(self):
        """Get the selected payment status."""
        selected_button = self.payment_status_group.checkedButton()
        return selected_button.text() if selected_button else "UNPAID"

    def get_selected_payment_method(self):
        """Get the selected payment method."""
        selected_button = self.payment_method_group.checkedButton()
        return selected_button.text() if selected_button else None

    def make_fields_readonly(self):
        """Make all input fields read-only when in view mode."""
        # Disable all dropdowns but keep them visible
        self.client_dropdown.setEnabled(False)
        self.pet_dropdown.setEnabled(False)
        self.vet_dropdown.setEnabled(False)
        self.reason_dropdown.setEnabled(False)
        self.received_by_dropdown.setEnabled(False)
        
        # Make sure received_by dropdown is visible
        self.received_by_dropdown.setVisible(True)

        # Disable all text fields (they're already read-only)
        self.notes_edit.setReadOnly(True)

        # Disable but keep visible all radio buttons for payment method
        for radio in self.payment_method_radios.values():
            radio.setEnabled(False)
            radio.setVisible(True)
        
        # Disable but keep visible payment status radio buttons
        for button in self.payment_status_group.buttons():
            button.setEnabled(False)
            button.setVisible(True)

        # Make sure services table is visible and properly styled
        self.services_table.setVisible(True)
        self.services_table.setEnabled(True)  # Keep enabled for scrolling
        self.services_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.services_table.setSelectionMode(QTableWidget.NoSelection)
        self.services_table.setFocusPolicy(Qt.NoFocus)
        
        # Set consistent column widths
        self.services_table.setColumnWidth(0, 20)  # Checkbox
        self.services_table.setColumnWidth(1, 200)  # Service description
        self.services_table.setColumnWidth(2, 90)  # Date
        self.services_table.setColumnWidth(3, 60)  # Quantity
        self.services_table.setColumnWidth(4, 80)  # Unit price
        self.services_table.setColumnWidth(5, 80)  # Total
        
        # Disable checkboxes in services table
        for row in range(self.services_table.rowCount()):
            checkbox = self.services_table.item(row, 0)
            if checkbox:
                checkbox.setFlags(Qt.NoItemFlags)  # Remove all flags to make it completely disabled
                checkbox.setCheckState(Qt.Checked)  # Keep it checked
        
        self.services_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #CCCCCC;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #EEEEEE;
            }
            QHeaderView::section {
                background-color: #CFDEF3;
                color: black;
                padding: 5px;
                border: none;
            }
        """)

        # Make sure payment fields are visible
        self.subtotal_field.setVisible(True)
        self.vat_field.setVisible(True)
        self.total_field.setVisible(True)
        
        # Make sure partial payment field is visible if applicable
        if self.partial_amount_field.text():
            self.partial_amount_label.setVisible(True)
            self.partial_amount_field.setVisible(True)
            self.partial_amount_field.setReadOnly(True)

        # Ensure table has proper height
        self.services_table.setMinimumHeight(200)  # Ensure table is tall enough to be visible
        
        # Make sure all amounts are formatted properly
        try:
            # Format monetary values
            subtotal = float(self.subtotal_field.text() or 0)
            vat = float(self.vat_field.text() or 0)
            total = float(self.total_field.text() or 0)
            
            self.subtotal_field.setText(f"{subtotal:.2f}")
            self.vat_field.setText(f"{vat:.2f}")
            self.total_field.setText(f"{total:.2f}")
        except ValueError:
            pass

    def load_invoice_data(self, billing_id):
        """Load invoice data for viewing."""
        try:
            print(f"\n=== Debug: Loading invoice data for billing_id {billing_id} ===")
            if not billing_id:
                raise ValueError("Invalid billing ID")

            # Set loading_invoice flag to prevent service reloading
            self.loading_invoice = True

            if not self.db or not self.db.conn:
                print("Database connection not available, attempting to reconnect...")
                try:
                    self.db = Database()
                except Exception as db_error:
                    print(f"Failed to reconnect to database: {db_error}")
                    raise ValueError("Database connection failed")

            try:
                # Get billing data with named columns for better readability
                print("Fetching billing data...")
                self.db.cursor.execute("""
                    SELECT 
                        b.billing_id,
                        b.invoice_no,
                        b.date_issued,
                        b.reason,
                        b.veterinarian,
                        b.payment_method,
                        b.payment_status,
                        b.partial_amount,
                        b.notes,
                        b.total_amount,
                        b.subtotal,
                        b.vat,
                        b.received_by,
                        c.name as client_name,
                        c.address,
                        c.contact_number,
                        c.email,
                        p.name as pet_name,
                        p.species,
                        p.breed,
                        p.age,
                        c.client_id,
                        p.pet_id
                    FROM billing b
                    LEFT JOIN clients c ON b.client_id = c.client_id
                    LEFT JOIN pets p ON b.pet_id = p.pet_id
                    WHERE b.billing_id = ?
                """, (billing_id,))
                
                result = self.db.cursor.fetchone()
                if not result:
                    print(f"No invoice found with ID {billing_id}")
                    raise ValueError(f"Invoice with ID {billing_id} not found")
                    
                columns = [desc[0] for desc in self.db.cursor.description]
                billing_data = dict(zip(columns, result))
                print("Billing data fetched successfully")

                # First load all clients and pets to populate dropdowns
                print("Loading clients...")
                self.load_clients()
                print("Loading pets...")
                self.load_pets_for_client(billing_data.get('client_id'))

                # Set the values in the form with safe defaults
                print("Setting form values...")
                try:
                    self.date_field.setText(str(billing_data.get('date_issued', '')))
                    self.invoice_field.setText(str(billing_data.get('invoice_no', '')))
                    
                    # Set client info
                    client_id = billing_data.get('client_id')
                    if client_id:
                        index = self.client_dropdown.findData(client_id)
                        if index >= 0:
                            self.client_dropdown.setCurrentIndex(index)
                    self.client_address_field.setText(str(billing_data.get('address', '')))
                    self.client_contact_field.setText(str(billing_data.get('contact_number', '')))
                    self.client_email_field.setText(str(billing_data.get('email', '')))

                    # Set pet info
                    pet_id = billing_data.get('pet_id')
                    if pet_id:
                        index = self.pet_dropdown.findData(pet_id)
                        if index >= 0:
                            self.pet_dropdown.setCurrentIndex(index)
                    self.pet_species_field.setText(str(billing_data.get('species', '')))
                    self.pet_breed_field.setText(str(billing_data.get('breed', '')))
                    self.pet_age_field.setText(str(billing_data.get('age', '')))

                    # Set reason and veterinarian
                    self.reason_dropdown.blockSignals(True)
                    self.reason_dropdown.setCurrentText(str(billing_data.get('reason', '')))
                    self.reason_dropdown.blockSignals(False)
                    self.vet_dropdown.setCurrentText(str(billing_data.get('veterinarian', '')))
                    
                    # Set notes
                    notes = billing_data.get('notes', '')
                    if notes:
                        self.notes_edit.setPlainText(str(notes))
                    else:
                        self.notes_edit.clear()
                    
                    # Set payment method
                    payment_method = billing_data.get('payment_method')
                    if payment_method and payment_method in self.payment_method_radios:
                        self.payment_method_radios[payment_method].setChecked(True)
                        self.payment_method_radios[payment_method].setVisible(True)

                    # Set payment status
                    payment_status = billing_data.get('payment_status')
                    if payment_status:
                        for button in self.payment_status_group.buttons():
                            if button.text() == payment_status:
                                button.setChecked(True)
                                button.setVisible(True)
                                if payment_status == "PARTIAL":
                                    partial_amount = billing_data.get('partial_amount', 0)
                                    self.partial_amount_field.setText(f"{float(partial_amount):.2f}")
                                    self.partial_amount_label.setVisible(True)
                                    self.partial_amount_field.setVisible(True)
                                break

                    # Set receptionist
                    received_by = billing_data.get('received_by')
                    if received_by:
                        self.load_receptionists()
                        index = self.received_by_dropdown.findText(received_by)
                        if index >= 0:
                            self.received_by_dropdown.setCurrentIndex(index)
                    self.received_by_dropdown.setVisible(True)

                    # Set totals with safe defaults
                    try:
                        subtotal = float(billing_data.get('subtotal', 0) or 0)
                        vat = float(billing_data.get('vat', 0) or 0)
                        total = float(billing_data.get('total_amount', 0) or 0)
                        
                        self.subtotal_field.setText(f"{subtotal:.2f}")
                        self.vat_field.setText(f"{vat:.2f}")
                        self.total_field.setText(f"{total:.2f}")
                    except (ValueError, TypeError):
                        self.subtotal_field.setText("0.00")
                        self.vat_field.setText("0.00")
                        self.total_field.setText("0.00")

                    print("Loading services...")
                    # Load services from billing_services instead of pet history
                    self.db.cursor.execute("""
                        SELECT service_description, service_date, quantity, unit_price, line_total 
                        FROM billing_services 
                        WHERE billing_id = ?
                        ORDER BY service_date DESC
                    """, (billing_id,))
                    services = self.db.cursor.fetchall()
                    print(f"Found {len(services)} services")

                    # Ensure we're disconnected from itemChanged
                    if self.services_table_connected:
                        try:
                            self.services_table.itemChanged.disconnect(self.update_total)
                            self.services_table_connected = False
                        except:
                            pass

                    # Block all signals and updates
                    self.services_table.blockSignals(True)
                    self.services_table.setUpdatesEnabled(False)

                    try:
                        # Clear the table
                        self.services_table.setRowCount(0)
                        
                        # Create all rows first
                        for _ in range(len(services)):
                            self.services_table.insertRow(self.services_table.rowCount())
                        
                        # Now populate all cells
                        for row, service in enumerate(services):
                            # Create checkbox and set it to checked since these are the saved services
                            checkbox = QTableWidgetItem()
                            checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                            checkbox.setCheckState(Qt.Checked)  # Set to checked since these are saved services
                            self.services_table.setItem(row, 0, checkbox)
                            
                            # Create other items
                            description_item = QTableWidgetItem(str(service[0] or ""))
                            description_item.setFlags(description_item.flags() & ~Qt.ItemIsEditable)
                            
                            date_item = QTableWidgetItem(str(service[1] or ""))
                            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
                            
                            quantity_item = QTableWidgetItem(str(service[2] or "0"))
                            if not self.is_view_mode:
                                quantity_item.setFlags(quantity_item.flags() | Qt.ItemIsEditable)
                            
                            unit_price_item = QTableWidgetItem(f"{float(service[3] or 0):.2f}")
                            if not self.is_view_mode:
                                unit_price_item.setFlags(unit_price_item.flags() | Qt.ItemIsEditable)
                            
                            total_item = QTableWidgetItem(f"{float(service[4] or 0):.2f}")
                            total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
                            
                            # Set all items at once
                            self.services_table.setItem(row, 1, description_item)
                            self.services_table.setItem(row, 2, date_item)
                            self.services_table.setItem(row, 3, quantity_item)
                            self.services_table.setItem(row, 4, unit_price_item)
                            self.services_table.setItem(row, 5, total_item)
                            
                            # Add tooltip
                            description_item.setToolTip(f"Date: {service[1]}\nDescription: {service[0]}")

                        # If in view mode, make checkboxes read-only after all items are set
                        if self.is_view_mode:
                            for row in range(self.services_table.rowCount()):
                                checkbox = self.services_table.item(row, 0)
                                if checkbox:
                                    checkbox.setFlags(Qt.ItemIsUserCheckable)
                                    checkbox.setCheckState(Qt.Checked)  # Keep checked in view mode

                    finally:
                        # Re-enable updates and signals
                        self.services_table.setUpdatesEnabled(True)
                        self.services_table.blockSignals(False)
                        
                        # Reconnect itemChanged signal
                        try:
                            self.services_table.itemChanged.connect(self.update_total)
                            self.services_table_connected = True
                        except:
                            pass

                    # Force an update of totals
                    self.update_total(None)

                    print("Services loaded successfully")
                    print("All form data set successfully")

                except Exception as form_error:
                    print(f"Error setting form values: {form_error}")
                    raise

            except Exception as db_error:
                print(f"Database error: {db_error}")
                raise
            finally:
                # Clear loading_invoice flag
                self.loading_invoice = False
                if self.db:
                    self.db.close_connection()
                    self.db = None

        except Exception as e:
            print(f"Error loading invoice data: {e}")
            import traceback
            traceback.print_exc()
            QTimer.singleShot(0, lambda: QMessageBox.critical(self, "Error", f"Failed to load invoice data: {str(e)}"))
            return False
        return True

    def download_invoice(self):
        """Generate and download the invoice as a PDF."""
        try:
            invoice_data = self.get_invoice_data()
            if not invoice_data:
                show_message(None, "No invoice data to download", QMessageBox.Warning)
                return

            # Create invoices directory if it doesn't exist
            folder_path = os.path.join(os.getcwd(), "pdf_reports", "invoices")
            os.makedirs(folder_path, exist_ok=True)

            default_name = f"Invoice_{invoice_data['invoice_no']}.pdf"
            file_path = os.path.join(folder_path, default_name)
            if not file_path:
                return

            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            width, height = height, width
            c.setPageSize((width, height))

            x_margin = 50
            y_margin = 50
            header_height = 100
            content_width = width - (2 * x_margin)
            left_column_width = content_width * 0.45
            right_column_width = content_width * 0.55
            right_column_x = x_margin + left_column_width + 20
            section_gap = 25
            line_gap = 12

            # Header
            logo_path = "assets/logologin.png"
            if os.path.exists(logo_path):
                c.drawImage(logo_path, x_margin, height - y_margin - 50, width=50, height=50)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(x_margin + 60, height - y_margin - 20, self.clinic_field.text())
            
            # Get clinic license number
            db = Database()
            try:
                db.cursor.execute("SELECT vet_license FROM clinic_info LIMIT 1")
                result = db.cursor.fetchone()
                if result and result[0]:
                    c.setFont("Helvetica", 10)
                    c.drawString(x_margin + 60, height - y_margin - 35, f"License No: {result[0]}")
            except Exception as e:
                print(f"Error getting clinic license number: {e}")
            finally:
                db.close_connection()
            
            c.setFont("Helvetica", 12)
            c.drawString(x_margin + 60, height - y_margin - 50, self.clinic_address_field.text())
            c.drawString(x_margin + 60, height - y_margin - 70, f"Contact: {self.clinic_contact_field.text()}")
            c.setFont("Helvetica-Bold", 14)
            c.drawString(width - 250, height - y_margin - 20, "SERVICE BILLING")
            c.setFont("Helvetica", 12)
            c.drawString(width - 250, height - y_margin - 40, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            c.setStrokeColorRGB(0.003922, 0.145098, 0.278431)
            c.line(x_margin, height - y_margin - header_height, width - x_margin, height - y_margin - header_height)

            # Start content below header
            y_start = height - y_margin - header_height - 30
            y_left = y_start
            y_right = y_start

            # LEFT COLUMN
            c.setFont("Helvetica-Bold", 12)
            c.drawString(x_margin, y_left, "Invoice Details")
            y_left -= section_gap
            c.setFont("Helvetica", 9)
            
            # Get veterinarian's license number
            db = Database()
            vet_display = invoice_data['veterinarian']
            try:
                license_number = db.get_vet_license_number(invoice_data['veterinarian'])
                if license_number:
                    vet_display = f"{invoice_data['veterinarian']} ({license_number})"
            except Exception as e:
                print(f"Error getting license number: {e}")
            finally:
                db.close_connection()
            
            details = [
                ("Invoice No:", invoice_data['invoice_no']),
                ("Date:", invoice_data['date_issued']),
                ("Veterinarian:", vet_display),
                ("Reason:", invoice_data['reason'])
            ]
            for label, value in details:
                c.drawString(x_margin, y_left, f"{label} {value}")
                y_left -= line_gap
            y_left -= section_gap

            c.setFont("Helvetica-Bold", 12)
            c.drawString(x_margin, y_left, "Client Information")
            y_left -= section_gap
            c.setFont("Helvetica", 9)
            client_details = [
                ("Client:", self.client_dropdown.currentText()),
                ("Control Number:", self.client_control_number_field.text()),
                ("Address:", self.client_address_field.text()),
                ("Contact:", self.client_contact_field.text()),
                ("Email:", self.client_email_field.text())
            ]
            for label, value in client_details:
                c.drawString(x_margin, y_left, f"{label} {value}")
                y_left -= line_gap
            y_left -= section_gap

            c.setFont("Helvetica-Bold", 12)
            c.drawString(x_margin, y_left, "Pet Information")
            y_left -= section_gap
            c.setFont("Helvetica", 9)
            pet_details = [
                ("Pet Name:", self.pet_dropdown.currentText()),
                ("Species:", self.pet_species_field.text()),
                ("Breed:", self.pet_breed_field.text()),
                ("Age:", self.pet_age_field.text())
            ]
            for label, value in pet_details:
                c.drawString(x_margin, y_left, f"{label} {value}")
                y_left -= line_gap
            y_left -= section_gap

            # Notes (if any)
            if invoice_data['notes']:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(x_margin, y_left, "Notes:")
                y_left -= section_gap
                c.setFont("Helvetica", 9)
                words = invoice_data['notes'].split()
                line = ""
                for word in words:
                    if len(line + " " + word) < 60:
                        line += " " + word if line else word
                    else:
                        c.drawString(x_margin, y_left, line)
                        y_left -= line_gap
                        line = word
                if line:
                    c.drawString(x_margin, y_left, line)
                    y_left -= line_gap
                y_left -= section_gap

            # RIGHT COLUMN
            c.setFont("Helvetica-Bold", 12)
            c.drawString(right_column_x, y_right, "Services")
            y_right -= section_gap
            c.setFont("Helvetica", 9)
            for row in range(self.services_table.rowCount()):
                checkbox = self.services_table.item(row, 0)
                if checkbox and checkbox.checkState() == Qt.Checked:
                    desc = self.services_table.item(row, 1).text()
                    date = self.services_table.item(row, 2).text()
                    qty = self.services_table.item(row, 3).text()
                    unit_price = self.services_table.item(row, 4).text()
                    total = self.services_table.item(row, 5).text()
                    indent = 20
                    max_width = 4.5*inch
                    from reportlab.pdfbase.pdfmetrics import stringWidth
                    # Service label and value
                    c.setFont("Helvetica-Bold", 9)
                    c.drawString(right_column_x, y_right, "Service:")
                    y_right -= line_gap
                    c.setFont("Helvetica", 9)
                    words = desc.split()
                    line = ""
                    for word in words:
                        test_line = (line + " " + word) if line else word
                        if stringWidth(test_line, "Helvetica", 9) < max_width:
                            line = test_line
                        else:
                            c.drawString(right_column_x + indent, y_right, line)
                            y_right -= line_gap
                            line = word
                    if line:
                        c.drawString(right_column_x + indent, y_right, line)
                        y_right -= line_gap
                    # Date label and value
                    c.setFont("Helvetica-Bold", 9)
                    c.drawString(right_column_x, y_right, "Date:")
                    y_right -= line_gap
                    c.setFont("Helvetica", 9)
                    c.drawString(right_column_x + indent, y_right, date)
                    y_right -= line_gap
                    # Quantity label and value
                    c.setFont("Helvetica-Bold", 9)
                    c.drawString(right_column_x, y_right, "Quantity:")
                    y_right -= line_gap
                    c.setFont("Helvetica", 9)
                    c.drawString(right_column_x + indent, y_right, qty)
                    y_right -= line_gap
                    # Unit Price label and value
                    c.setFont("Helvetica-Bold", 9)
                    c.drawString(right_column_x, y_right, "Unit Price:")
                    y_right -= line_gap
                    c.setFont("Helvetica", 9)
                    c.drawString(right_column_x + indent, y_right, unit_price)
                    y_right -= line_gap
                    # Total label and value
                    c.setFont("Helvetica-Bold", 9)
                    c.drawString(right_column_x, y_right, "Total:")
                    y_right -= line_gap
                    c.setFont("Helvetica", 9)
                    c.drawString(right_column_x + indent, y_right, total)
                    y_right -= line_gap
                    # Blank line between services
                    y_right -= line_gap

            # Totals
            c.setFont("Helvetica-Bold", 10)
            totals = [
                ("Subtotal:", f"PHP {self.subtotal_field.text()}"),
                ("VAT:", f"PHP {self.vat_field.text()}"),
                ("Total Amount:", f"PHP {self.total_field.text()}")
            ]
            for label, value in totals:
                c.drawString(right_column_x, y_right, f"{label} {value}")
                y_right -= line_gap + 2
            y_right -= section_gap

            # Payment Information
            c.setFont("Helvetica-Bold", 12)
            c.drawString(right_column_x, y_right, "Payment Information")
            y_right -= section_gap
            c.setFont("Helvetica", 9)
            payment_details = [
                ("Payment Status:", invoice_data['payment_status']),
                ("Payment Method:", invoice_data['payment_method']),
                ("Received By:", invoice_data['received_by'])
            ]
            if invoice_data['payment_status'] == 'PARTIAL':
                payment_details.append(("Partial Amount:", f"PHP {invoice_data['partial_amount']:.2f}"))
            for label, value in payment_details:
                c.drawString(right_column_x, y_right, f"{label} {value}")
                y_right -= line_gap
            y_right -= section_gap

            # Calculate where to put the thank you message
            y_final = min(y_left, y_right) - 30
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(width/2, y_final, "THANK YOU FOR TRUSTING US WITH YOUR PET'S CARE!")

            # Footer
            c.setFont("Helvetica", 8)
            c.drawString(x_margin, y_margin, f"Generated by PetMedix System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.drawString(width - x_margin - 100, y_margin, f"Page 1")

            c.save()
            show_message(None, "Invoice PDF generated successfully!", QMessageBox.Information)
            os.startfile(file_path)
        except Exception as e:
            print(f"Error generating PDF: {e}")
            import traceback
            traceback.print_exc()
            show_message(None, f"Error generating PDF: {str(e)}", QMessageBox.Critical)

    def show_date_picker(self):
        """Show a date picker dialog and update the date field."""
        try:
            current_date = QDate.fromString(self.date_field.text(), "yyyy-MM-dd")
            if not current_date.isValid():
                current_date = QDate.currentDate()
                
            date_picker = QCalendarWidget(self)
            date_picker.setSelectedDate(current_date)
            date_picker.setGridVisible(True)
            date_picker.setWindowFlags(Qt.Popup)
            
            # Position the calendar below the date field
            pos = self.date_field.mapToGlobal(self.date_field.rect().bottomLeft())
            date_picker.move(pos)
            
            # Connect the selection signal
            date_picker.clicked.connect(lambda date: self.date_field.setText(date.toString("yyyy-MM-dd")))
            date_picker.clicked.connect(date_picker.close)
            
            date_picker.show()
        except Exception as e:
            print(f"Error showing date picker: {e}")

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
                    notes=invoice_data['notes'],
                    subtotal=invoice_data['subtotal'],
                    vat=invoice_data['vat'],
                    partial_amount=invoice_data['partial_amount']
                )
                
                if billing_id:
                    # Get selected services from the table
                    services = []
                    for row in range(dialog.services_table.rowCount()):
                        checkbox = dialog.services_table.item(row, 0)
                        if checkbox and checkbox.checkState() == Qt.Checked:
                            service = {
                                'description': dialog.services_table.item(row, 1).text(),
                                'date': dialog.services_table.item(row, 2).text(),
                                'quantity': float(dialog.services_table.item(row, 3).text()),
                                'unit_price': float(dialog.services_table.item(row, 4).text()),
                                'total': float(dialog.services_table.item(row, 5).text())
                            }
                            services.append(service)
                    
                    # Save the services
                    for service in services:
                        try:
                            # Convert date from DD/MM/YYYY to YYYY-MM-DD
                            try:
                                service_date = datetime.strptime(service['date'], '%d/%m/%Y').strftime('%Y-%m-%d')
                            except ValueError:
                                # If date is already in YYYY-MM-DD format or invalid, use as is
                                service_date = service['date']
                                
                            db.cursor.execute("""
                                INSERT INTO billing_services 
                                (billing_id, service_description, quantity, unit_price, line_total, service_date)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                billing_id,
                                service['description'],
                                service['quantity'],
                                service['unit_price'],
                                service['total'],
                                service_date
                            ))
                        except Exception as e:
                            print(f"❌ Error saving service: {e}")
                            continue
                    
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

def update_billing_widget(user_role=None):
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
        QTableWidgetItem, QMessageBox
    )
    from PySide6.QtCore import Qt, QSize
    from PySide6.QtGui import QIcon

    class BillingWidget(QWidget):
        def __init__(self, user_role=None):
            super().__init__()
            self.user_role = user_role  # Store user_role
            self.setup_ui()
            
        def setup_ui(self):
            layout = QVBoxLayout(self)
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 30)

            # Store current search text
            self.current_search = ""

            def filter_billings(search_text):
                """Filter the billings table based on search text."""
                self.current_search = search_text.lower()
                
                visible_rows = 0
                for row in range(self.billings_table.rowCount()):
                    show_row = False
                    for col in range(self.billings_table.columnCount()):
                        item = self.billings_table.item(row, col)
                        if item and self.current_search in item.text().lower():
                            show_row = True
                            break
                    self.billings_table.setRowHidden(row, not show_row)
                    if show_row:
                        visible_rows += 1

                # Update table header to show search status
                header = self.billings_table.horizontalHeader()
                if self.current_search:
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
                        header.setToolTip(f"Showing {visible_rows} results for '{self.current_search}'")
                    else:
                        header.setToolTip(f"No results found for '{self.current_search}'")
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

            # Make filter_billings available to the main window
            self.filter_billings = filter_billings

            # Title
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
            if user_role and user_role.lower() == "veterinarian":
                add_receipt_button.hide()  # Hide the button for veterinarians
            add_receipt_button.clicked.connect(self.on_add_receipt)

            # Create action buttons (initially hidden)
            self.view_button = QPushButton()
            self.view_button.setObjectName("ViewButton")
            self.view_button.setFixedSize(40, 40)
            self.view_button.setIcon(QIcon("assets/eye open.png"))
            self.view_button.setIconSize(QSize(20, 20))
            self.view_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    border: none;
                    border-radius: 20px;
                    margin-bottom: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.view_button.clicked.connect(self.view_invoice)
            self.view_button.hide()

            self.edit_button = QPushButton()
            self.edit_button.setObjectName("EditButton")
            self.edit_button.setFixedSize(40, 40)
            self.edit_button.setIcon(QIcon("assets/edit client button.png"))
            self.edit_button.setIconSize(QSize(20, 20))
            self.edit_button.setStyleSheet("""
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
            self.edit_button.clicked.connect(self.edit_invoice)
            self.edit_button.hide()

            self.delete_button = QPushButton()
            self.delete_button.setObjectName("DeleteButton")
            self.delete_button.setFixedSize(38, 38)
            self.delete_button.setIcon(QIcon("assets/trash-can.png"))
            self.delete_button.setIconSize(QSize(18, 18))
            self.delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF6F61;
                    border: none;
                    border-radius: 20px;
                    margin-bottom: 5px;
                    margin-top: -1px;
                }
                QPushButton:hover {
                    background-color: #E53935;
                }
            """)
            self.delete_button.clicked.connect(self.delete_invoice)
            self.delete_button.hide()

            # Create a container for action buttons
            action_buttons_container = QWidget()
            action_buttons_layout = QHBoxLayout(action_buttons_container)
            action_buttons_layout.setContentsMargins(0, 0, 0, 0)
            action_buttons_layout.setSpacing(10)
            action_buttons_layout.addWidget(self.view_button)
            action_buttons_layout.addWidget(self.edit_button)
            action_buttons_layout.addWidget(self.delete_button)

            header_layout.addWidget(billings_label)
            header_layout.addWidget(add_receipt_button)
            header_layout.addWidget(action_buttons_container)
            header_layout.addStretch()
            header.setLayout(header_layout)

            # Create the table
            self.billings_table = QTableWidget()
            self.billings_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.billings_table.setObjectName("BillingsTable")
            self.billings_table.setRowCount(0)
            self.billings_table.setColumnCount(7)  # Removed Action column
            self.billings_table.setHorizontalHeaderLabels([
                "Receipt No.", "Date Issued", "Owner/Client",
                "Pet Name", "Total Amount (Php)", "Payment",
                "Payment Status"
            ])
            self.billings_table.horizontalHeader().setStretchLastSection(True)
            self.billings_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.billings_table.verticalHeader().setVisible(False)
            self.billings_table.setSelectionBehavior(QTableWidget.SelectRows)
            self.billings_table.setSelectionMode(QTableWidget.SingleSelection)

            self.billings_table.setStyleSheet("""
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
                QTableWidget::item:selected {
                    background-color: #E3F2FD;
                    color: black;
                }
            """)

            # Set column widths
            for i, width in enumerate([150, 120, 150, 200, 180, 150, 150]):
                self.billings_table.setColumnWidth(i, width)

            # Connect selection change signal
            self.billings_table.selectionModel().selectionChanged.connect(self.handle_row_selection)

            layout.addWidget(header)
            layout.addWidget(self.billings_table)

            # Load initial data
            self.load_billing_data()

        def handle_row_selection(self):
            """Handle row selection and show/hide action buttons accordingly."""
            selected_rows = self.billings_table.selectionModel().selectedRows()
            
            if selected_rows:
                self.view_button.show()
                # Only show edit and delete buttons for non-veterinarian users
                if user_role and user_role.lower() != "veterinarian":
                    self.edit_button.show()
                    self.delete_button.show()
                else:
                    self.edit_button.hide()
                    self.delete_button.hide()
            else:
                self.view_button.hide()
                self.edit_button.hide()
                self.delete_button.hide()

        def on_add_receipt(self):
            """Handle adding a new receipt."""
            if open_invoice_form():
                self.load_billing_data()  # Refresh table after successful addition

        def view_invoice(self):
            """View the selected invoice."""
            try:
                print("\n=== Debug: Starting view_invoice ===")
                selected_rows = self.billings_table.selectionModel().selectedRows()
                if not selected_rows:
                    QMessageBox.warning(self, "Warning", "Please select an invoice to view")
                    return
                    
                row = selected_rows[0].row()
                print(f"Selected row: {row}")
                
                billing_id_item = self.billings_table.item(row, 0)
                if not billing_id_item:
                    print("Error: Could not get billing_id_item")
                    QMessageBox.critical(self, "Error", "Could not retrieve invoice data")
                    return
                    
                billing_id = billing_id_item.data(Qt.UserRole)  # Get billing_id from hidden data
                print(f"Billing ID: {billing_id}")
                
                if not billing_id:
                    print("Error: Invalid billing_id")
                    QMessageBox.critical(self, "Error", "Invalid invoice ID")
                    return
                
                # Create and show the invoice dialog in view mode
                try:
                    print("Creating InvoiceFormDialog...")
                    dialog = InvoiceFormDialog(is_view_mode=True, user_role=self.user_role)  # Pass user_role here
                    print("Dialog created successfully")
                    
                    print("Loading invoice data...")
                    if not dialog.load_invoice_data(billing_id):
                        print("Error: Failed to load invoice data")
                        return  # Error already shown by load_invoice_data
                    print("Invoice data loaded successfully")
                    
                    print("Showing dialog...")
                    dialog.exec()
                    print("Dialog closed")
                    
                except Exception as dialog_error:
                    print(f"Error in dialog creation/execution: {dialog_error}")
                    import traceback
                    traceback.print_exc()
                    QMessageBox.critical(self, "Error", "Failed to display invoice form. Please try again.")
                    return
                    
            except Exception as e:
                print(f"Error in view_invoice: {e}")
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "Error", "An unexpected error occurred while viewing the invoice. Please try again.")
                return

        def edit_invoice(self):
            """Edit the selected invoice."""
            try:
                print("\n=== Debug: Starting edit_invoice ===")
                selected_rows = self.billings_table.selectionModel().selectedRows()
                if not selected_rows:
                    show_message(self, "Please select an invoice to edit", QMessageBox.Warning)
                    return False
                    
                row = selected_rows[0].row()
                print(f"Selected row: {row}")
                
                billing_id_item = self.billings_table.item(row, 0)
                if not billing_id_item:
                    print("Error: Could not get billing_id_item")
                    show_message(self, "Could not retrieve invoice data", QMessageBox.Critical)
                    return False
                    
                billing_id = billing_id_item.data(Qt.UserRole)  # Get billing_id from hidden data
                print(f"Billing ID: {billing_id}")
                
                if not billing_id:
                    print("Error: Invalid billing_id")
                    show_message(self, "Invalid invoice ID", QMessageBox.Critical)
                    return False
                
                # Create and show the invoice dialog
                try:
                    print("Creating InvoiceFormDialog...")
                    dialog = InvoiceFormDialog(is_view_mode=False)
                    print("Dialog created successfully")
                    
                    print("Loading invoice data...")
                    if not dialog.load_invoice_data(billing_id):
                        print("Error: Failed to load invoice data")
                        return False  # Error already shown by load_invoice_data
                    print("Invoice data loaded successfully")
                    
                    print("Showing dialog...")
                    if dialog.exec():
                        print("Dialog accepted")
                        try:
                            # Get the form data
                            print("Getting invoice data...")
                            invoice_data = dialog.get_invoice_data()
                            if not invoice_data:
                                print("Error: Invalid invoice data")
                                show_message(self, "Invalid invoice data", QMessageBox.Critical)
                                return False
                            print("Invoice data retrieved successfully")
                            
                            # Save to database
                            print("Saving to database...")
                            db = Database()
                            try:
                                # Update the main billing record
                                print("Updating billing record...")
                                db.cursor.execute("""
                                    UPDATE billing SET
                                        client_id = ?,
                                        pet_id = ?,
                                        date_issued = ?,
                                        total_amount = ?,
                                        payment_status = ?,
                                        payment_method = ?,
                                        received_by = ?,
                                        reason = ?,
                                        veterinarian = ?,
                                        notes = ?,
                                        subtotal = ?,
                                        vat = ?,
                                        partial_amount = ?
                                    WHERE billing_id = ?
                                """, (
                                    invoice_data['client_id'],
                                    invoice_data['pet_id'],
                                    invoice_data['date_issued'],
                                    invoice_data['total_amount'],
                                    invoice_data['payment_status'],
                                    invoice_data['payment_method'],
                                    invoice_data['received_by'],
                                    invoice_data['reason'],
                                    invoice_data['veterinarian'],
                                    invoice_data['notes'],
                                    invoice_data['subtotal'],
                                    invoice_data['vat'],
                                    invoice_data['partial_amount'],
                                    billing_id
                                ))
                                print("Billing record updated successfully")
                                
                                # Delete existing services
                                print("Deleting existing services...")
                                db.cursor.execute("DELETE FROM billing_services WHERE billing_id = ?", (billing_id,))
                                print("Existing services deleted")
                                
                                # Get selected services from the table
                                print("Processing services...")
                                services = []
                                for row in range(dialog.services_table.rowCount()):
                                    try:
                                        checkbox = dialog.services_table.item(row, 0)
                                        if checkbox and checkbox.checkState() == Qt.Checked:
                                            service = {
                                                'description': dialog.services_table.item(row, 1).text(),
                                                'date': dialog.services_table.item(row, 2).text(),
                                                'quantity': float(dialog.services_table.item(row, 3).text() or 0),
                                                'unit_price': float(dialog.services_table.item(row, 4).text() or 0),
                                                'total': float(dialog.services_table.item(row, 5).text() or 0)
                                            }
                                            services.append(service)
                                    except (ValueError, AttributeError) as e:
                                        print(f"Error processing service row {row}: {e}")
                                        continue
                                
                                # Save the updated services
                                print(f"Saving {len(services)} services...")
                                for service in services:
                                    try:
                                        # Convert date from DD/MM/YYYY to YYYY-MM-DD
                                        try:
                                            service_date = datetime.strptime(service['date'], '%d/%m/%Y').strftime('%Y-%m-%d')
                                        except ValueError:
                                            # If date is already in YYYY-MM-DD format or invalid, use as is
                                            service_date = service['date']
                                            
                                        db.cursor.execute("""
                                            INSERT INTO billing_services 
                                            (billing_id, service_description, quantity, unit_price, line_total, service_date)
                                            VALUES (?, ?, ?, ?, ?, ?)
                                        """, (
                                            billing_id,
                                            service['description'],
                                            service['quantity'],
                                            service['unit_price'],
                                            service['total'],
                                            service_date
                                        ))
                                    except Exception as e:
                                        print(f"Error saving service: {e}")
                                        continue
                                
                                print("Committing changes...")
                                db.conn.commit()
                                print("Changes committed successfully")
                                
                                # Show success message
                                show_message(self, "Invoice updated successfully!", QMessageBox.Information)
                                self.load_billing_data()  # Refresh the table
                                return True
                                
                            except Exception as db_error:
                                print(f"Database error updating invoice: {db_error}")
                                import traceback
                                traceback.print_exc()
                                show_message(self, "Failed to update invoice in database. Please try again.", QMessageBox.Critical)
                                return False
                            finally:
                                db.close_connection()
                                
                        except Exception as form_error:
                            print(f"Error processing form data: {form_error}")
                            import traceback
                            traceback.print_exc()
                            show_message(self, "Failed to process invoice data. Please try again.", QMessageBox.Critical)
                            return False
                        else:
                            print("Dialog rejected")
                            return False
                            
                except Exception as dialog_error:
                    print(f"Error in dialog creation/execution: {dialog_error}")
                    import traceback
                    traceback.print_exc()
                    show_message(self, "Failed to display invoice form. Please try again.", QMessageBox.Critical)
                    return False
                    
            except Exception as e:
                print(f"Error in edit_invoice: {e}")
                import traceback
                traceback.print_exc()
                show_message(self, "An unexpected error occurred while editing the invoice. Please try again.", QMessageBox.Critical)
                return False

        def delete_invoice(self):
            """Delete the selected invoice."""
            selected_rows = self.billings_table.selectionModel().selectedRows()
            if selected_rows:
                row = selected_rows[0].row()
                billing_id = self.billings_table.item(row, 0).data(Qt.UserRole)
                
                # Create confirmation message box
                confirm = create_styled_message_box(
                    QMessageBox.Question,
                    "Delete Invoice",
                    "Are you sure you want to delete this invoice?"
                )
                confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                confirm.setDefaultButton(QMessageBox.No)
                
                reply = confirm.exec()
                
                if reply == QMessageBox.Yes:
                    db = Database()
                    try:
                        # First delete associated services
                        db.cursor.execute("DELETE FROM billing_services WHERE billing_id = ?", (billing_id,))
                        
                        # Then delete the main billing record
                        db.cursor.execute("DELETE FROM billing WHERE billing_id = ?", (billing_id,))
                        
                        db.conn.commit()
                        self.load_billing_data()  # Refresh the table
                        
                        # Show success message
                        show_message(self, "Invoice deleted successfully!", QMessageBox.Information)
                    except Exception as e:
                        db.conn.rollback()  # Rollback changes if there's an error
                        show_message(self, f"Failed to delete invoice: {str(e)}", QMessageBox.Critical)
                    finally:
                        db.close_connection()

        def load_billing_data(self):
            """Load billing data into the table."""
            db = Database()
            try:
                billing_data = db.fetch_billing_data()

                self.billings_table.setRowCount(0)  # Clear the table

                for row_num, data in enumerate(billing_data):
                    self.billings_table.insertRow(row_num)

                    # Create table items with center alignment
                    receipt_no = QTableWidgetItem(str(data[1] or f"REC-{data[0]}"))
                    receipt_no.setData(Qt.UserRole, data[0])  # Store billing_id
                    receipt_no.setTextAlignment(Qt.AlignCenter)
                    
                    date_issued = QTableWidgetItem(data[2].strftime("%Y-%m-%d") if isinstance(data[2], datetime) else str(data[2]))
                    date_issued.setTextAlignment(Qt.AlignCenter)
                    
                    client_name = QTableWidgetItem(str(data[3]))
                    client_name.setTextAlignment(Qt.AlignCenter)
                    
                    pet_name = QTableWidgetItem(str(data[4]))
                    pet_name.setTextAlignment(Qt.AlignCenter)
                    
                    total_amount = QTableWidgetItem(f"₱ {data[5]:.2f}")
                    total_amount.setTextAlignment(Qt.AlignCenter)
                    
                    payment_method = QTableWidgetItem(str(data[6] or ""))
                    payment_method.setTextAlignment(Qt.AlignCenter)
                    
                    payment_status = QTableWidgetItem(str(data[7]))
                    payment_status.setTextAlignment(Qt.AlignCenter)

                    # Add items to table
                    self.billings_table.setItem(row_num, 0, receipt_no)
                    self.billings_table.setItem(row_num, 1, date_issued)
                    self.billings_table.setItem(row_num, 2, client_name)
                    self.billings_table.setItem(row_num, 3, pet_name)
                    self.billings_table.setItem(row_num, 4, total_amount)
                    
                    # Display "UNPAID" in payment column if payment status is "UNPAID"
                    if data[7] == "UNPAID":
                        payment_method = QTableWidgetItem("UNPAID")
                        payment_method.setTextAlignment(Qt.AlignCenter)
                    
                    self.billings_table.setItem(row_num, 5, payment_method)
                    self.billings_table.setItem(row_num, 6, payment_status)

            except Exception as e:
                print(f"Error loading billing data: {e}")
            finally:
                db.close_connection()

    return BillingWidget  # Return the class, not an instance

class NumericDelegate(QStyledItemDelegate):
    """Delegate for handling numeric input in table cells."""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QDoubleValidator(0.0, 999999.99, 2, parent)
        editor.setValidator(validator)
        return editor