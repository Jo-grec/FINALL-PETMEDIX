import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QDialog, QMessageBox, QFileDialog, QComboBox, QTextEdit, QDateEdit,
    QHeaderView, QTableWidgetItem
)
from PySide6.QtGui import QColor, QBrush, QIcon
from PySide6.QtCore import Qt, QDate
from modules.database import Database
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from modules.utils import show_message


class AppointmentFormDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PetMedix - Appointments")
        self.setFixedSize(800, 600)  # Consistent size with report form
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 10, 20, 10)
        # Title
        title_label = QLabel("Schedule Appointment")
        title_label.setObjectName("TitleLabel")  # Assign an object name
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
        """Load pet names grouped by their owners into the pet_name_combo."""
        try:
            db = Database()
            cursor = db.cursor

            # Fetch pet names along with their owners
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

            # Group pets by their owners
            current_owner = None
            for client_name, pet_name in rows:
                if client_name != current_owner:
                    # Add owner group label
                    self.pet_name_combo.addItem(f"{client_name} - Owner")
                    index = self.pet_name_combo.count() - 1
                    self.pet_name_combo.model().item(index).setEnabled(False)
                    current_owner = client_name

                # Add pet name under the owner
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

    # Define the save_pdf function before connecting it
    def save_pdf():
        # Detect which table is visible
        table = urgent_table if urgent_table.isVisible() else all_table
        table_type = "Urgent" if table is urgent_table else "All"

        # Define the output folder relative to the project
        folder_path = os.path.join(os.getcwd(), "pdf_reports")
        os.makedirs(folder_path, exist_ok=True)  # Create folder if not exists

        # Create file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{table_type}_Appointments_{timestamp}.pdf"
        file_path = os.path.join(folder_path, file_name)

        # Create PDF
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        x_margin = 50
        y_start = height - 50
        row_height = 20

        # Write table headers
        for col in range(table.columnCount()):
            header = table.horizontalHeaderItem(col).text()
            c.drawString(x_margin + col * 100, y_start, header)

        # Write table rows
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    text = item.text()
                elif table.cellWidget(row, col):
                    text = "[Buttons]"
                else:
                    text = ""
                c.drawString(x_margin + col * 100, y_start - (row + 1) * row_height, text)

        c.save()
        show_message(None, f"PDF successfully saved to:\n{file_path}")

    # Connect the save_pdf function to the button
    save_pdf_button.clicked.connect(save_pdf)

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

        # Safely fetch data from the table
        def get_item_text(row, column):
            item = table.item(row, column)
            return item.text() if item else ""

        # Populate the form fields with data from the selected row
        dialog.date_edit.setDate(QDate.fromString(get_item_text(row, 0), "yyyy-MM-dd"))
        dialog.status_combo.setCurrentText(get_item_text(row, 4))
        dialog.payment_combo.setCurrentText(get_item_text(row, 5))

        # Extract the actual pet name (remove " - Owner" if present)
        pet_name_with_owner = get_item_text(row, 1).strip()
        pet_name = pet_name_with_owner.split(" - ")[0]  # Extract the pet name
        dialog.pet_name_combo.clear()  # Clear existing items in the combo box
        dialog.pet_name_combo.addItem(pet_name)  # Add the actual pet name
        dialog.pet_name_combo.setCurrentText(pet_name)  # Set the current text to the pet name

        dialog.reason_input.setPlainText(get_item_text(row, 3))
        dialog.vet_combo.setCurrentText(get_item_text(row, 6).strip())

        # Update the dialog title and window title
        dialog.setWindowTitle("View Appointment")
        dialog.findChild(QLabel, "TitleLabel").setText(f"{pet_name}'s Appointment")  # Use pet's name

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
        table.horizontalHeader().setSectionsClickable(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make cells non-editable
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;  /* Ensure text is black */
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

        # Make the table scrollable but hide the scrollbars
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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
    for i, width in enumerate([150, 120, 150, 200, 180, 150, 150, 80]):
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
    for i, width in enumerate([150, 120, 150, 200, 180, 150, 150, 80]):
        all_table.setColumnWidth(i, width)
    layout.addWidget(all_table)
    
    urgent_table.cellClicked.connect(lambda row, column: handle_table_click(urgent_table, row, column))
    all_table.cellClicked.connect(lambda row, column: handle_table_click(all_table, row, column))
        
    def populate_tables():
        """Fetch appointments from the database and populate the tables."""
        db = Database()
        try:
            # Fetch appointments from the database
            appointments = db.fetch_appointments()

            # Clear existing rows in the tables
            urgent_table.setRowCount(0)  # Clear all rows in urgent table
            all_table.setRowCount(0)  # Clear all rows in all table

            # Populate the tables with fetched data
            for appointment in appointments:
                # Ensure all data is converted to strings
                date = str(appointment[0])  # Convert date to string
                pet_name = str(appointment[1])
                client_name = str(appointment[2])
                reason = str(appointment[3])
                status = str(appointment[4])
                payment_status = str(appointment[5])
                veterinarian = f"Dr. {str(appointment[6])}"  # Add "Dr." prefix to veterinarian's name

                # Insert into the "All" table
                all_row_position = all_table.rowCount()
                all_table.insertRow(all_row_position)
                all_table.setItem(all_row_position, 0, QTableWidgetItem(date))
                all_table.setItem(all_row_position, 1, QTableWidgetItem(pet_name))
                all_table.setItem(all_row_position, 2, QTableWidgetItem(client_name))
                all_table.setItem(all_row_position, 3, QTableWidgetItem(reason))

                # Set the background color for the "Status" column
                status_item = QTableWidgetItem(status)
                if status.lower() == "scheduled":
                    status_item.setBackground(QBrush(QColor("#FFEEBA")))
                elif status.lower() == "completed":
                    status_item.setBackground(QBrush(QColor("#DFF2BF")))  # Green
                elif status.lower() == "urgent":
                    status_item.setBackground(QBrush(QColor("#FFBABA")))  # Red
                elif status.lower() in ["cancelled", "no-show"]:
                    status_item.setBackground(QBrush(QColor("#D3D3D3")))  # Gray
                elif status.lower() == "rescheduled":
                    status_item.setBackground(QBrush(QColor("orange")))  # Orange
                all_table.setItem(all_row_position, 4, status_item)

                all_table.setItem(all_row_position, 5, QTableWidgetItem(payment_status))
                all_table.setItem(all_row_position, 6, QTableWidgetItem(veterinarian))  # Add veterinarian with "Dr." prefix

                # Add "Edit" and "Delete" buttons in the "Action" column for the "All" table
                all_action_widget = QWidget()
                all_action_layout = QHBoxLayout(all_action_widget)
                all_action_layout.setContentsMargins(0, 0, 0, 0)
                all_action_layout.setSpacing(0)

                all_edit_button = QPushButton("Edit")
                all_edit_button.setFixedWidth(70)
                all_edit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FED766;
                        border: none;
                        border-radius: 5px;
                        font-size: 10px;
                        padding: 5px;
                        min-height: 10px;
                        min-width: 30px;
                    }
                    QPushButton:hover {
                        background-color: #FFC107;
                    }
                """)
                all_edit_button.clicked.connect(lambda _, r=all_row_position: edit_appointment(all_table, r))

                all_delete_button = QPushButton("Delete")
                all_delete_button.setFixedWidth(70)
                all_delete_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FF6F61;
                        border: none;
                        border-radius: 5px;
                        font-size: 10px;
                        padding: 5px;
                        min-height: 10px;
                        min-width: 30px;
                    }
                    QPushButton:hover {
                        background-color: #E53935;
                    }
                """)
                all_delete_button.clicked.connect(lambda _, r=all_row_position: delete_appointment(all_table, r))

                all_action_layout.addWidget(all_edit_button)
                all_action_layout.addWidget(all_delete_button)
                all_action_widget.setLayout(all_action_layout)
                all_table.setCellWidget(all_row_position, 7, all_action_widget)

                # If the appointment is urgent, also add it to the "Urgent" table
                if status.lower() == "urgent":
                    urgent_row_position = urgent_table.rowCount()
                    urgent_table.insertRow(urgent_row_position)
                    urgent_table.setItem(urgent_row_position, 0, QTableWidgetItem(date))
                    urgent_table.setItem(urgent_row_position, 1, QTableWidgetItem(pet_name))
                    urgent_table.setItem(urgent_row_position, 2, QTableWidgetItem(client_name))
                    urgent_table.setItem(urgent_row_position, 3, QTableWidgetItem(reason))

                    # Set the background color for the "Status" column in the urgent table
                    urgent_status_item = QTableWidgetItem(status)
                    urgent_status_item.setBackground(QBrush(QColor("#FFBABA")))  # Red for urgent
                    urgent_table.setItem(urgent_row_position, 4, urgent_status_item)

                    urgent_table.setItem(urgent_row_position, 5, QTableWidgetItem(payment_status))
                    urgent_table.setItem(urgent_row_position, 6, QTableWidgetItem(veterinarian))  # Add veterinarian with "Dr." prefix

                    # Add "Edit" and "Delete" buttons in the "Action" column for the "Urgent" table
                    urgent_action_widget = QWidget()
                    urgent_action_layout = QHBoxLayout(urgent_action_widget)
                    urgent_action_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
                    urgent_action_layout.setSpacing(0)  # Adjust spacing

                    urgent_edit_button = QPushButton("Edit")
                    urgent_edit_button.setFixedWidth(70)
                    urgent_edit_button.setStyleSheet("""
                        QPushButton {
                            background-color: #FED766;
                            border: none;
                            border-radius: 5px;
                            font-size: 10px;
                            padding: 5px;
                            min-height: 10px;
                            min-width: 30px;
                        }
                        QPushButton:hover {
                            background-color: #FFC107;
                        }
                    """)
                    urgent_edit_button.clicked.connect(lambda _, r=urgent_row_position: edit_appointment(urgent_table, r))

                    urgent_delete_button = QPushButton("Delete")
                    urgent_delete_button.setFixedWidth(70)
                    urgent_delete_button.setStyleSheet("""
                        QPushButton {
                            background-color: #FF6F61;
                            border: none;
                            border-radius: 5px;
                            font-size: 10px;
                            color: black;
                            padding: 5px;
                            min-height: 10px;
                            min-width: 30px;
                        }
                        QPushButton:hover {
                            background-color: #E53935;
                        }
                    """)
                    urgent_delete_button.clicked.connect(lambda _, r=urgent_row_position: delete_appointment(urgent_table, r))

                    urgent_action_layout.addWidget(urgent_edit_button)
                    urgent_action_layout.addWidget(urgent_delete_button)
                    urgent_action_widget.setLayout(urgent_action_layout)
                    urgent_table.setCellWidget(urgent_row_position, 7, urgent_action_widget)

            # Add placeholder if no appointments are found
            if all_table.rowCount() == 0:
                all_table.insertRow(0)
                placeholder_item = QTableWidgetItem("No appointments added")
                placeholder_item.setTextAlignment(Qt.AlignCenter)
                all_table.setSpan(0, 0, 1, all_table.columnCount())  # Span across all columns
                all_table.setItem(0, 0, placeholder_item)

            if urgent_table.rowCount() == 0:
                urgent_table.insertRow(0)
                placeholder_item = QTableWidgetItem("No urgent appointments added")
                placeholder_item.setTextAlignment(Qt.AlignCenter)
                urgent_table.setSpan(0, 0, 1, urgent_table.columnCount())  # Span across all columns
                urgent_table.setItem(0, 0, placeholder_item)

            # Debug: Print the number of rows added
            print(f"✅ {len(appointments)} appointments loaded into the tables.")
        except Exception as e:
            print(f"❌ Error populating tables: {e}")
        finally:
            db.close_connection()

    # Populate tables on widget load
    populate_tables()

    def show_table(table_to_show):
        for table in [urgent_table, all_table]:
            table.hide()
        table_to_show.show()
        
    # Connect cellClicked signals with a check for placeholder rows
    def handle_table_click(table, row, column):
        """Handle table clicks, ignoring placeholder rows."""
        # Check if the first row contains a placeholder
        if table.item(row, 0) and table.item(row, 0).text() in ["No appointments added", "No urgent appointments added"]:
            return  # Ignore clicks on placeholder rows

        # Open the appointment view mode for valid rows
        open_appointment_view_mode(table, row)

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
        
    def edit_appointment(table, row):
        """Handle the Edit button click."""
        dialog = AppointmentFormDialog()

        # Safely fetch data from the table
        def get_item_text(row, column):
            item = table.item(row, column)
            return item.text() if item else ""

        # Populate the form fields with data from the selected row
        dialog.date_edit.setDate(QDate.fromString(get_item_text(row, 0), "yyyy-MM-dd"))
        dialog.status_combo.setCurrentText(get_item_text(row, 4))
        dialog.payment_combo.setCurrentText(get_item_text(row, 5))
        dialog.pet_name_combo.setCurrentText(get_item_text(row, 1).strip())
        dialog.reason_input.setPlainText(get_item_text(row, 3))
        dialog.vet_combo.setCurrentText(get_item_text(row, 6).strip())

        # Show the dialog and save changes if accepted
        if dialog.exec():
            # Save changes to the database
            db = Database()
            try:
                db.cursor.execute("""
                    UPDATE appointments
                    SET date = ?, status = ?, payment_status = ?, reason = ?, veterinarian = ?
                    WHERE date = ? AND reason = ?
                """, (
                    dialog.date_edit.date().toString("yyyy-MM-dd"),
                    dialog.status_combo.currentText(),
                    dialog.payment_combo.currentText(),
                    dialog.reason_input.toPlainText().strip(),
                    dialog.vet_combo.currentText().strip(),
                    get_item_text(row, 0),  # Original date
                    get_item_text(row, 3)   # Original reason
                ))
                db.conn.commit()
                show_message(None, "Appointment updated successfully!")

                # Refresh the table
                populate_tables()
            except Exception as e:
                show_message(None, f"Failed to update appointment: {e}", QMessageBox.Critical)
            finally:
                db.close_connection()
                
    def delete_appointment(table, row):
        """Handle the Delete button click."""
        confirmation = QMessageBox()
        confirmation.setIcon(QMessageBox.Question)
        confirmation.setText("Are you sure you want to delete this appointment?")
        confirmation.setWindowTitle("")
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if confirmation.exec() == QMessageBox.Yes:
            # Get the appointment details
            date = table.item(row, 0).text()
            reason = table.item(row, 3).text()

            # Delete the appointment from the database
            db = Database()
            try:
                db.cursor.execute("""
                    DELETE FROM appointments
                    WHERE date = ? AND reason = ?
                """, (date, reason))
                db.conn.commit()
                show_message(None, "Appointment deleted successfully!")

                # Refresh the table
                populate_tables()
            except Exception as e:
                show_message(None, f"Failed to delete appointment: {e}", QMessageBox.Critical)
            finally:
                db.close_connection()

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
            pet_name = pet_name_display.split(" - ")[-1].strip()

            # Validate the data
            if not (pet_name and reason and veterinarian):
                show_message(dialog, "All fields are required!", QMessageBox.Warning)
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
                    show_message(dialog, f"Pet '{pet_name}' not found in the database! Please ensure the pet is registered.", QMessageBox.Warning)
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
                row_position = target_table.rowCount()
                target_table.insertRow(row_position)

                # Add items to the table
                target_table.setItem(row_position, 0, QTableWidgetItem(date))
                target_table.setItem(row_position, 1, QTableWidgetItem(pet_name_display))  # Use the display name
                target_table.setItem(row_position, 2, QTableWidgetItem(client_name))  # Display the client name
                target_table.setItem(row_position, 3, QTableWidgetItem(reason))

                # Set the background color for the "Status" column
                status_item = QTableWidgetItem(status)
                if status.lower() == "scheduled":
                    status_item.setBackground(QBrush(QColor("#FFEEBA")))
                elif status.lower() == "completed":
                    status_item.setBackground(QBrush(QColor("#DFF2BF")))  # Green
                elif status.lower() == "urgent":
                    status_item.setBackground(QBrush(QColor("#FFBABA")))  # Red
                elif status.lower() in ["cancelled", "no-show"]:
                    status_item.setBackground(QBrush(QColor("#D3D3D3")))  # Gray
                elif status.lower() == "rescheduled":
                    status_item.setBackground(QBrush(QColor("orange")))  # Orange
                target_table.setItem(row_position, 4, status_item)

                target_table.setItem(row_position, 5, QTableWidgetItem(payment))
                target_table.setItem(row_position, 6, QTableWidgetItem(f"Dr. {veterinarian}"))

                # Add "Edit" and "Delete" buttons in the "Action" column
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
                edit_button.clicked.connect(lambda _, r=row_position: edit_appointment(target_table, r))

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
                delete_button.clicked.connect(lambda _, r=row_position: delete_appointment(target_table, r))

                action_layout.addWidget(edit_button)
                action_layout.addWidget(delete_button)
                action_widget.setLayout(action_layout)
                target_table.setCellWidget(row_position, 7, action_widget)

                # Scroll to the newly added row
                target_table.scrollToItem(target_table.item(row_position, 0))

                # Show a success message
                show_message(dialog, "Appointment added successfully!")
            except Exception as e:
                show_message(dialog, f"Failed to save appointment: {e}", QMessageBox.Critical)
            finally:
                db.close_connection()
        else:
            print("Appointment creation cancelled")

    add_appointment_button.clicked.connect(open_appointment_form)

    return content