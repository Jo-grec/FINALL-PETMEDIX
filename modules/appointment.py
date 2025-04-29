from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QDialog, QMessageBox, QLineEdit, QComboBox, QTextEdit, QDateEdit,
    QHeaderView, QTableWidgetItem
)
from PySide6.QtCore import Qt, QDate
from modules.database import Database


class AppointmentFormDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Appointment")
        self.setFixedSize(800, 600)  # Consistent size with report form
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 10, 20, 10)
        title_label = QLabel("Appointment Form")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFF;")
        title_layout.addWidget(title_label)
        layout.addWidget(title_container)
        
        # Form Layout
        form_widget = QWidget()
        form_scroll_layout = QVBoxLayout(form_widget)
        form_scroll_layout.setContentsMargins(40, 20, 40, 10)
        form_scroll_layout.setSpacing(0)
        
        # Row 1: Date, Status, Payment
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
        
        # Status field
        status_label = QLabel("Status")
        status_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Scheduled", "Completed", "Cancelled", "No-Show", "Rescheduled", "Urgent"])
        self.status_combo.setMinimumHeight(40)  # Ensure minimum height
        self.status_combo.setStyleSheet("""
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
    
        status_container = QVBoxLayout()
        status_container.addWidget(status_label)
        status_container.addWidget(self.status_combo)
        
        # Payment field
        payment_label = QLabel("Payment")
        payment_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Pending", "Paid", "Unpaid"])
        self.payment_combo.setMinimumHeight(40)  # Ensure minimum height
        self.payment_combo.setStyleSheet("""
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
        
        payment_container = QVBoxLayout()
        payment_container.addWidget(payment_label)
        payment_container.addWidget(self.payment_combo)
        
        row1_layout.addLayout(date_container, 1)
        row1_layout.addLayout(status_container, 1)
        row1_layout.addLayout(payment_container, 1)
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
        
        # Row 3: Reason for Appointment
        reason_label = QLabel("Reason for Appointment")
        reason_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText("Reason for Appointment")
        self.reason_input.setFixedHeight(120)  # Larger text area
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
        
        # Row 4: Veterinarian/Staff In Charge
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

        # Populate the dropdown with veterinarian names
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
        save_btn.setObjectName("SaveButton")  # Assign an object name
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
        """Load pet names into the pet_name_combo grouped by owners."""
        try:
            db = Database()
            cursor = db.cursor

            cursor.execute("""
                SELECT c.name AS client_name, p.name AS pet_name
                FROM pets p
                JOIN clients c ON p.client_id = c.client_id
                ORDER BY c.name ASC, p.name ASC
            """)
            rows = cursor.fetchall()

            if not rows:
                self.pet_name_combo.addItem("No pets found")
                return

            current_owner = None
            for client_name, pet_name in rows:
                if client_name != current_owner:
                    # Owner group label
                    self.pet_name_combo.addItem(f"{client_name} - Owner")
                    index = self.pet_name_combo.count() - 1
                    self.pet_name_combo.model().item(index).setEnabled(False)
                    current_owner = client_name

                # Add pet name
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

            # Fetch veterinarian names from the database
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
                self.vet_combo.addItem(row[0])  # Add each veterinarian name to the dropdown

            db.close_connection()
        except Exception as e:
            print("Failed to load veterinarian names:", e)
            self.vet_combo.addItem("Error loading veterinarians")

def get_appointment_widget(user_role):
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

    # Appointment Label
    appointment_label = QLabel("Appointment")
    appointment_label.setObjectName("Appointment")
    appointment_label.setAlignment(Qt.AlignVCenter)

    # Add Appointment Button
    add_appointment_button = QPushButton("Add Appointment")
    add_appointment_button.setObjectName("AddAppointmentButton")
    add_appointment_button.setFixedSize(120, 40)
    add_appointment_button.setStyleSheet(
        "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px;"
    )

    # Disable the button if the user is not a receptionist
    if user_role.lower() != "receptionist":
        add_appointment_button.setEnabled(False)
        add_appointment_button.setStyleSheet(
            "background-color: #d3d3d3; border: none; border-radius: 20px; margin-bottom: 5px; color: #888;"
        )

    # Save PDF Button
    save_pdf_button = QPushButton("Save PDF")
    save_pdf_button.setObjectName("SavePDFButton")
    save_pdf_button.setFixedSize(120, 40)
    save_pdf_button.setStyleSheet(
        "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px;"
    )

    header_layout.addWidget(appointment_label)
    header_layout.addWidget(add_appointment_button)
    header_layout.addWidget(save_pdf_button)
    header_layout.addStretch()

    # --- Appointment Filter Buttons (Urgent, All) ---
    appointment_buttons_widget = QWidget()
    appointment_layout = QHBoxLayout()
    appointment_layout.setContentsMargins(0, 0, 50, 0)
    appointment_layout.setSpacing(0)

    appointments = ["Urgent", "All"]
    appointment_buttons = {}

    for appointment in appointments:
        button = QPushButton(appointment)
        button.setFixedSize(180, 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #F4F4F8;
                font-family: Poppins;
                font-style: normal;
                font-weight: 300;
                line-height: normal;
                font-size: 15px;
                border: none;
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
        appointment_layout.addWidget(button)
        appointment_buttons[appointment] = button

    appointment_buttons_widget.setLayout(appointment_layout)
    header_layout.addWidget(appointment_buttons_widget)
    header.setLayout(header_layout)
    layout.addWidget(header)
    
    def open_appointment_view_mode(table, row):
        """Open the Appointment Form in view mode with data from the selected row."""
        dialog = AppointmentFormDialog()

        # Populate the form fields with data from the selected row
        dialog.date_edit.setDate(QDate.fromString(table.item(row, 0).text(), "yyyy-MM-dd"))
        dialog.status_combo.setCurrentText(table.item(row, 4).text())
        dialog.payment_combo.setCurrentText(table.item(row, 5).text())
        dialog.pet_name_combo.setCurrentText(table.item(row, 1).text().strip())
        dialog.reason_input.setPlainText(table.item(row, 3).text())
        dialog.vet_combo.setCurrentText(table.item(row, 6).text().strip())

        # Disable all input fields to make the form read-only
        dialog.date_edit.setEnabled(False)
        dialog.status_combo.setEnabled(False)
        dialog.payment_combo.setEnabled(False)
        dialog.pet_name_combo.setEnabled(False)
        dialog.reason_input.setReadOnly(True)
        dialog.vet_combo.setEnabled(False)

       # Disable the Save button
        save_button = dialog.findChild(QPushButton, "SaveButton")
        if save_button:
            save_button.setEnabled(False)

        # Show the dialog
        dialog.exec()

    # --- Tables Setup ---
    def create_table(headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setRowCount(15)
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Make columns non-resizable
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make cells non-editable
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

    urgent_table = create_table([
        "Date",
        "Pet Name",
        "Owner/Client",
        "Reason for Appointment",
        "Status",
        "Payment Status",
        "Veterinarian In Charge",
        "Action"
    ])
    for i, width in enumerate([150, 120, 150, 200, 180, 200, 150, 100]):
        urgent_table.setColumnWidth(i, width)
    urgent_table.hide()
    layout.addWidget(urgent_table)

    all_table = create_table([
        "Date",
        "Pet Name",
        "Owner/Client",
        "Reason for Appointment",
        "Status",
        "Payment Status",
        "Veterinarian In Charge",
        "Action"
    ])
    for i, width in enumerate([150, 120, 150, 200, 180, 200, 150, 100]):
        all_table.setColumnWidth(i, width)
    layout.addWidget(all_table)
    
    urgent_table.cellClicked.connect(lambda row, column: open_appointment_view_mode(urgent_table, row))
    all_table.cellClicked.connect(lambda row, column: open_appointment_view_mode(all_table, row))

    def show_table(table_to_show):
        for table in [urgent_table, all_table]:
            table.hide()
        table_to_show.show()

    def select_appointment(selected_button):
        for button in appointment_buttons.values():
            button.setProperty('selected', False)
            button.style().unpolish(button)
            button.style().polish(button)

        selected_button.setProperty('selected', True)
        selected_button.style().unpolish(selected_button)
        selected_button.style().polish(selected_button)

    # Connect buttons to show tables
    appointment_buttons["Urgent"].clicked.connect(lambda: [show_table(urgent_table), select_appointment(appointment_buttons["Urgent"])])
    appointment_buttons["All"].clicked.connect(lambda: [show_table(all_table), select_appointment(appointment_buttons["All"])])

    # Show all_table by default
    all_table.show()
    select_appointment(appointment_buttons["All"])

    def open_appointment_form():
        dialog = AppointmentFormDialog()
        if dialog.exec():
            # Capture the form data
            date = dialog.date_edit.date().toString("yyyy-MM-dd")
            status = dialog.status_combo.currentText()
            payment = dialog.payment_combo.currentText()
            pet_name_display = dialog.pet_name_combo.currentText().strip()  # Get the displayed pet name
            reason = dialog.reason_input.toPlainText().strip()
            veterinarian = dialog.vet_combo.currentText().strip()

            # Extract the actual pet name (remove " - owner" if present)
            pet_name = pet_name_display.split(" - ")[0].strip()

            # Validate the data
            if not (pet_name and reason and veterinarian):
                QMessageBox.warning(dialog, "Input Error", "All fields are required!")
                return

            # Save the data to the database
            db = Database()
            try:
                # Fetch the pet, client IDs, and client name
                print(f"DEBUG: Searching for pet name '{pet_name}' in the database.")
                db.cursor.execute("""
                    SELECT p.pet_id, c.client_id, c.name AS client_name
                    FROM pets p
                    JOIN clients c ON p.client_id = c.client_id
                    WHERE LOWER(p.name) = LOWER(?)
                """, (pet_name,))
                result = db.cursor.fetchone()
                print(f"DEBUG: Query result for pet_name '{pet_name}': {result}")
                if not result:
                    QMessageBox.warning(dialog, "Error", f"Pet '{pet_name}' not found in the database! Please ensure the pet is registered.")
                    return

                pet_id, client_id, client_name = result

                # Insert the appointment into the database
                db.cursor.execute("""
                    INSERT INTO appointments (pet_id, client_id, date, status, payment_status, reason, veterinarian)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (pet_id, client_id, date, status, payment, reason, veterinarian))
                db.conn.commit()

                # Add the data to the appropriate table
                target_table = urgent_table if status.lower() == "urgent" else all_table
                target_table.insertRow(0)
                target_table.setItem(0, 0, QTableWidgetItem(date))
                target_table.setItem(0, 1, QTableWidgetItem(pet_name_display))  # Use the display name
                target_table.setItem(0, 2, QTableWidgetItem(client_name))  # Display the client name
                target_table.setItem(0, 3, QTableWidgetItem(reason))
                target_table.setItem(0, 4, QTableWidgetItem(status))
                target_table.setItem(0, 5, QTableWidgetItem(payment))
                target_table.setItem(0, 6, QTableWidgetItem(veterinarian))
                target_table.setItem(0, 7, QTableWidgetItem("Action"))

                # Scroll to the top of the table
                target_table.scrollToItem(target_table.item(0, 0))

                # Show a success message
                QMessageBox.information(dialog, "Success", "Appointment added successfully!")
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Failed to save appointment: {e}")
            finally:
                db.close_connection()
        else:
            print("Appointment creation cancelled")

    add_appointment_button.clicked.connect(open_appointment_form)

    return content