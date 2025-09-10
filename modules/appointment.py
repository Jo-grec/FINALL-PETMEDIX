import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QDialog, QMessageBox, QFileDialog, QComboBox, QTextEdit, QDateEdit,
    QHeaderView, QTableWidgetItem, QTimeEdit, QAbstractSpinBox
)
from PySide6.QtGui import QColor, QBrush, QIcon
from PySide6.QtCore import Qt, QDate, QSize, QTime
from modules.database import Database
from modules.utils import create_styled_message_box, show_message
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def format_datetime_for_display(dt_str):
    """Convert 'YYYY-MM-DD HH:MM:SS' to '1PM', '2AM', etc."""
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        # Use %I for hour (12-hour, zero-padded), %p for AM/PM, then strip leading zero
        return dt.strftime("%Y-%m-%d ") + dt.strftime("%I:%M%p").lstrip('0')
    except Exception:
        return dt_str

def set_datetime_fields(dialog, datetime_str):
    """Set date, time, and AM/PM fields in the dialog from a datetime string."""
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        dialog.date_edit.setDate(QDate(dt.year, dt.month, dt.day))
        hour = dt.hour
        minute = dt.minute
        ampm = "AM"
        if hour >= 12:
            ampm = "PM"
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12
        dialog.time_edit.setTime(dialog.time_edit.time().fromString(f"{hour_12:02d}:{minute:02d}", "hh:mm"))
        dialog.ampm_combo.setCurrentText(ampm)
    except Exception as e:
        print(f"Error setting datetime fields: {e}")

class AppointmentFormDialog(QDialog):
    def __init__(self, is_view_mode=False):
        super().__init__()
        self.setWindowTitle("Add Appointment" if not is_view_mode else "View Appointment")
        self.setFixedSize(800, 600)  # Consistent size with report form
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        # Title
        title_container = QWidget()
        title_container.setStyleSheet("background-color: #012547;")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(20, 10, 20, 10)
        # Title
        title_label = QLabel("Schedule Appointment" if not is_view_mode else "View Appointment")
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
        date_label = QLabel("Date & Time")
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
        
        # Time field (hour/minute only, 12-hour format)
        time_label = QLabel("")
        time_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(datetime.now().time())
        self.time_edit.setDisplayFormat("hh:mm")  # 12-hour format, no AM/PM
        self.time_edit.setMinimumHeight(40)
        self.time_edit.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)

        # AM/PM dropdown
        self.ampm_combo = QComboBox()
        self.ampm_combo.addItems(["AM", "PM"])
        self.ampm_combo.setMinimumHeight(40)
        self.ampm_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)

        # Set AM/PM based on current time
        if datetime.now().hour >= 12:
            self.ampm_combo.setCurrentText("PM")
        else:
            self.ampm_combo.setCurrentText("AM")

        date_time_container = QHBoxLayout()
        date_time_container.addWidget(self.date_edit)
        date_time_container.addWidget(time_label)
        date_time_container.addWidget(self.time_edit)
        date_time_container.addWidget(self.ampm_combo)

        date_container = QVBoxLayout()
        date_container.addWidget(date_label)
        date_container.addLayout(date_time_container)
        
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
        self.pet_name_combo.setPlaceholderText("Select Pet")  # <-- Add this line
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
        
        if is_view_mode:
            # In view mode, only show a centered Close button
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
            close_btn.clicked.connect(self.reject)
            button_layout.addWidget(close_btn)
        else:
            # In edit/add mode, show Cancel and Save buttons
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
        
        button_layout.addStretch()
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

            # Add placeholder text
            self.vet_combo.addItem("Select Veterinarian")
            self.vet_combo.setCurrentIndex(0)  # Set the placeholder as default

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
                vet_name = row[0]
                if not vet_name.startswith("Dr. "):
                    vet_name = f"Dr. {vet_name}"
                self.vet_combo.addItem(vet_name)  # Add each veterinarian name to the dropdown

            db.close_connection()
        except Exception as e:
            print("Failed to load veterinarian names:", e)
            self.vet_combo.addItem("Error loading veterinarians")

def save_pdf(table, table_type):
    # Define the output folder relative to the project
    folder_path = os.path.join(os.getcwd(), "pdf_reports", "appointments")
    os.makedirs(folder_path, exist_ok=True)  # Create folder if not exists

    # Create file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{table_type}_Appointments_{timestamp}.pdf"
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
    c.drawString(width - 250, height - y_margin - 20, f"{table_type} Appointments")
    c.setFont("Helvetica", 12)
    c.drawString(width - 250, height - y_margin - 40, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Draw a line under the header
    c.setStrokeColorRGB(0.145098, 0.278431, 0.278431, 1.0)  # #012547 in RGB with full opacity
    c.line(x_margin, height - y_margin - header_height, width - x_margin, height - y_margin - header_height)

    # Table headers
    y_start = height - y_margin - header_height - 30
    headers = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
    
    # Calculate column widths based on content
    col_widths = []
    total_width = width - (2 * x_margin)
    for i in range(table.columnCount()):
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
            c.drawString(width - 250, height - y_margin - 20, f"{table_type} Appointments (continued)")
            c.setFont("Helvetica", 10)
            y_pos = height - y_margin - header_height - 30

        x_pos = x_margin
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item:
                # Only apply background color for status column (index 5)
                if col == 5:  # Status column
                    bg_color = item.background().color()
                    if bg_color:
                        r, g, b, _ = bg_color.getRgbF()
                        c.setFillColorRGB(r, g, b)
                        c.rect(x_pos, y_pos - 15, col_widths[col], row_height, fill=True)
                    c.setFillColorRGB(0, 0, 0)  # Reset to black for text after drawing background
                else:
                    c.setFillColorRGB(0, 0, 0)  # Ensure text is black for other columns

                # Draw text
                c.drawString(x_pos + 5, y_pos, item.text())
            x_pos += col_widths[col]
        y_pos -= row_height

    # Add footer
    c.setFont("Helvetica", 8)
    c.drawString(x_margin, y_margin, f"Generated by PetMedix System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(width - x_margin - 100, y_margin, f"Page 1")

    c.save()
    show_message(None, "PDF successfully saved to:\n{}".format(file_path), QMessageBox.Information)

def get_appointment_widget(user_role):
    content = QWidget()
    layout = QVBoxLayout(content)
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 30)

    # Store current search text
    current_search = ""

    def filter_appointments(search_text):
        """Filter both urgent and all appointments tables based on search text."""
        nonlocal current_search
        current_search = search_text.lower()
        
        visible_rows = 0
        for table in [urgent_table, all_table]:
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
        for table in [urgent_table, all_table]:
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

    # Make filter_appointments available to the main window
    content.filter_appointments = filter_appointments

    def save_pdf_clicked():
        # Detect which table is visible
        table = urgent_table if urgent_table.isVisible() else all_table
        table_type = "Urgent" if table is urgent_table else "All"
        save_pdf(table, table_type)

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

    # Hide the button if the user is not a receptionist
    if user_role.lower() != "receptionist":
        add_appointment_button.hide()

    # Save PDF Button
    save_pdf_button = QPushButton("Save PDF")
    save_pdf_button.setObjectName("SavePDFButton")
    save_pdf_button.setFixedSize(120, 40)
    save_pdf_button.setStyleSheet(
        "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px;"
    )
    
    # Hide the button if the user is not a receptionist
    if user_role.lower() != "receptionist":
        save_pdf_button.hide()
    
    save_pdf_button.clicked.connect(save_pdf_clicked)

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

    # View Button
    view_button = QPushButton()
    view_button.setObjectName("ViewButton")
    view_button.setFixedSize(40, 40)  # Make it square for round shape
    view_button.setIcon(QIcon("assets/eye open.png"))
    view_button.setIconSize(QSize(20, 20))
    view_button.setStyleSheet("""
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
    view_button.hide()  # Initially hidden

    # Delete Button
    delete_button = QPushButton()
    delete_button.setObjectName("DeleteButton")
    delete_button.setFixedSize(38, 38)  # Make it square for round shape
    delete_button.setIcon(QIcon("assets/trash-can.png"))
    delete_button.setIconSize(QSize(18, 18))
    delete_button.setStyleSheet("""
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
    delete_button.hide()  # Initially hidden

    # Create a container widget for the action buttons
    action_buttons_container = QWidget()
    action_buttons_layout = QHBoxLayout(action_buttons_container)
    action_buttons_layout.setContentsMargins(0, 0, 0, 0)
    action_buttons_layout.setSpacing(10)
    action_buttons_layout.setAlignment(Qt.AlignLeft)  # Align buttons to the left
    action_buttons_layout.addWidget(view_button)
    action_buttons_layout.addWidget(edit_button)
    action_buttons_layout.addWidget(delete_button)

    header_layout.addWidget(appointment_label)
    header_layout.addWidget(add_appointment_button)
    header_layout.addWidget(save_pdf_button)
    header_layout.addWidget(action_buttons_container)
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
        dialog = AppointmentFormDialog(is_view_mode=True)

        # Safely fetch data from the table
        def get_item_text(row, column):
            item = table.item(row, column)
            return item.text() if item else ""

        # Get date and time
        date = get_item_text(row, 0)
        time = get_item_text(row, 1)
        
        # Set date
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        dialog.date_edit.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
        
        # Set time
        try:
            # Parse the time string (e.g., "01:30 PM")
            time_obj = datetime.strptime(time, "%I:%M %p")
            # Create QTime object
            qtime = QTime(time_obj.hour, time_obj.minute)
            dialog.time_edit.setTime(qtime)
            dialog.ampm_combo.setCurrentText("PM" if time_obj.hour >= 12 else "AM")
        except ValueError as e:
            print(f"Error parsing time {time}: {e}")
            # Set default time if parsing fails
            dialog.time_edit.setTime(QTime(9, 0))
            dialog.ampm_combo.setCurrentText("AM")

        # Set other fields
        dialog.status_combo.setCurrentText(get_item_text(row, 5))
        dialog.payment_combo.setCurrentText(get_item_text(row, 6))
        select_pet_in_combo(dialog.pet_name_combo, get_item_text(row, 2))
        dialog.reason_input.setPlainText(get_item_text(row, 4))
        
        # Get the veterinarian name from the table
        vet_name = get_item_text(row, 7)
        # Clear the combo box and add the veterinarian name
        dialog.vet_combo.clear()
        dialog.vet_combo.addItem(vet_name)
        dialog.vet_combo.setCurrentText(vet_name)

        # Extract the last name from the "Owner/Client" column
        client_name = get_item_text(row, 3)
        last_name = client_name.split()[-1] if client_name else "Unknown"

        # Update the dialog title and window title
        dialog.setWindowTitle("View Appointment")
        dialog.findChild(QLabel, "TitleLabel").setText(f"{last_name}'s Appointment")

        # Disable all input fields to make the form read-only
        dialog.date_edit.setEnabled(False)
        dialog.time_edit.setEnabled(False)
        dialog.ampm_combo.setEnabled(False)
        dialog.status_combo.setEnabled(False)
        dialog.payment_combo.setEnabled(False)
        dialog.pet_name_combo.setEnabled(False)
        dialog.reason_input.setReadOnly(True)
        dialog.vet_combo.setEnabled(False)

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
        table.setSelectionBehavior(QTableWidget.SelectRows)  # Select entire rows
        table.setSelectionMode(QTableWidget.SingleSelection)  # Only one row can be selected at a time
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
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: black;
            }
        """)
        table.verticalHeader().setVisible(False)
        return table

    urgent_table = create_table([
        "Date",
        "Time",
        "Pet Name",
        "Owner/Client",
        "Reason for Appointment",
        "Status",
        "Payment Status",
        "Veterinarian In Charge"
    ])
    for i, width in enumerate([100, 100, 120, 150, 200, 180, 200, 150]):
        urgent_table.setColumnWidth(i, width)
    urgent_table.hide()
    layout.addWidget(urgent_table)

    all_table = create_table([
        "Date",
        "Time",
        "Pet Name",
        "Owner/Client",
        "Reason for Appointment",
        "Status",
        "Payment Status",
        "Veterinarian In Charge"
    ])
    for i, width in enumerate([100, 100, 120, 150, 200, 180, 200, 150]):
        all_table.setColumnWidth(i, width)
    layout.addWidget(all_table)
    
    def handle_row_selection():
        """Handle row selection and show/hide action buttons accordingly."""
        table = urgent_table if urgent_table.isVisible() else all_table
        selected_rows = table.selectionModel().selectedRows()
        
        if selected_rows:
            print("Row selected, showing buttons")  # Debug print
            view_button.show()
            # Only show edit and delete buttons for non-veterinarian users
            if user_role.lower() != "veterinarian":
                edit_button.show()
                delete_button.show()
            else:
                edit_button.hide()
                delete_button.hide()
        else:
            print("No row selected, hiding buttons")  # Debug print
            view_button.hide()
            edit_button.hide()
            delete_button.hide()

    # Connect the selection change signal for both tables
    urgent_table.selectionModel().selectionChanged.connect(handle_row_selection)
    all_table.selectionModel().selectionChanged.connect(handle_row_selection)

    # Connect the view, edit and delete buttons to their respective functions
    def handle_view():
        table = urgent_table if urgent_table.isVisible() else all_table
        selected_rows = table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            open_appointment_view_mode(table, row)
        else:
            show_message(None, "Please select an appointment to view.", QMessageBox.Warning)

    def handle_edit():
        table = urgent_table if urgent_table.isVisible() else all_table
        selected_rows = table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            dialog = AppointmentFormDialog()

            # Safely fetch data from the table
            def get_item_text(row, column):
                item = table.item(row, column)
                return item.text() if item else ""

            # Get date and time
            date = get_item_text(row, 0)
            time = get_item_text(row, 1)
            
            # Set date
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            dialog.date_edit.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
            
            # Set time
            try:
                # Parse the time string (e.g., "01:30 PM")
                time_obj = datetime.strptime(time, "%I:%M %p")
                # Create QTime object
                qtime = QTime(time_obj.hour, time_obj.minute)
                dialog.time_edit.setTime(qtime)
                dialog.ampm_combo.setCurrentText("PM" if time_obj.hour >= 12 else "AM")
            except ValueError as e:
                print(f"Error parsing time {time}: {e}")
                # Set default time if parsing fails
                dialog.time_edit.setTime(QTime(9, 0))
                dialog.ampm_combo.setCurrentText("AM")
            
            # Set other fields
            dialog.status_combo.setCurrentText(get_item_text(row, 5))
            dialog.payment_combo.setCurrentText(get_item_text(row, 6))
            select_pet_in_combo(dialog.pet_name_combo, get_item_text(row, 2))
            dialog.reason_input.setPlainText(get_item_text(row, 4))
            select_vet_in_combo(dialog.vet_combo, get_item_text(row, 7))

            # Show the dialog and save changes if accepted
            if dialog.exec():
                # Save changes to the database
                db = Database()
                try:
                    # Get new date and time
                    new_date = dialog.date_edit.date().toString("yyyy-MM-dd")
                    hour = dialog.time_edit.time().hour()
                    minute = dialog.time_edit.time().minute()
                    ampm = dialog.ampm_combo.currentText()
                    # Convert to 24-hour format
                    if ampm == "PM" and hour < 12:
                        hour += 12
                    if ampm == "AM" and hour == 12:
                        hour = 0
                    new_time = f"{hour:02d}:{minute:02d}:00"

                    # Convert original time to 24-hour format for comparison
                    original_time_obj = datetime.strptime(time, "%I:%M %p")
                    original_time_str = original_time_obj.strftime("%H:%M:%S")

                    # Get the pet_id and client_id for the update
                    pet_name = dialog.pet_name_combo.currentText().strip()
                    if " - " in pet_name:
                        pet_name = pet_name.split(" - ")[-1].strip()
                    
                    db.cursor.execute("""
                        SELECT p.pet_id, c.client_id
                        FROM pets p
                        JOIN clients c ON p.client_id = c.client_id
                        WHERE p.name = ?
                    """, (pet_name,))
                    pet_id, client_id = db.cursor.fetchone()

                    db.cursor.execute("""
                        UPDATE appointments
                        SET date = ?, time = ?, status = ?, payment_status = ?, 
                            reason = ?, veterinarian = ?, pet_id = ?, client_id = ?
                        WHERE date = ? AND time = ? AND reason = ?
                    """, (
                        new_date,
                        new_time,
                        dialog.status_combo.currentText(),
                        dialog.payment_combo.currentText(),
                        dialog.reason_input.toPlainText().strip(),
                        dialog.vet_combo.currentText().strip(),
                        pet_id,
                        client_id,
                        # Use the original date, time and reason as identifiers
                        date,
                        original_time_str,
                        get_item_text(row, 4)
                    ))
                    db.conn.commit()
                    show_message(None, "Appointment updated successfully!", QMessageBox.Information)

                    # Refresh the table
                    populate_tables()
                except Exception as e:
                    show_message(None, f"Failed to update appointment: {e}", QMessageBox.Critical)
                    print(f"Error updating appointment: {e}")
                finally:
                    db.close_connection()
        else:
            show_message(None, "Please select an appointment to edit.", QMessageBox.Warning)

    def handle_delete():
        table = urgent_table if urgent_table.isVisible() else all_table
        selected_rows = table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            
            # Get the appointment details
            date = table.item(row, 0).text()
            time = table.item(row, 1).text()
            reason = table.item(row, 4).text()
            pet_name = table.item(row, 2).text()
            client_name = table.item(row, 3).text()

            print(f"Attempting to delete appointment:")
            print(f"Date: {date}")
            print(f"Time: {time}")
            print(f"Reason: {reason}")
            print(f"Pet: {pet_name}")
            print(f"Client: {client_name}")

            confirmation = create_styled_message_box(
                QMessageBox.Question,
                "Delete Confirmation",
                "Are you sure you want to delete this appointment?"
            )
            confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirmation.setDefaultButton(QMessageBox.No)
            
            if confirmation.exec() == QMessageBox.Yes:
                # Delete the appointment from the database
                db = Database()
                try:
                    # First get the pet_id and client_id
                    db.cursor.execute("""
                        SELECT p.pet_id, c.client_id
                        FROM pets p
                        JOIN clients c ON p.client_id = c.client_id
                        WHERE p.name = ? AND c.name = ?
                    """, (pet_name, client_name))
                    
                    result = db.cursor.fetchone()
                    if not result:
                        raise Exception(f"Could not find pet '{pet_name}' for client '{client_name}'")
                    
                    pet_id, client_id = result
                    print(f"Found pet_id: {pet_id}, client_id: {client_id}")

                    # Convert time to 24-hour format for database
                    time_obj = datetime.strptime(time, "%I:%M %p")
                    time_str = time_obj.strftime("%H:%M:%S")
                    print(f"Converted time to 24-hour format: {time_str}")

                    # Debug: Check if the appointment exists
                    db.cursor.execute("""
                        SELECT a.*, p.name as pet_name, c.name as client_name 
                        FROM appointments a
                        JOIN pets p ON a.pet_id = p.pet_id
                        JOIN clients c ON a.client_id = c.client_id
                        WHERE p.pet_id = ? AND c.client_id = ? AND DATE(a.date) = ?
                    """, (pet_id, client_id, date))
                    
                    existing_appointments = db.cursor.fetchall()
                    if not existing_appointments:
                        print("Debug - No appointments found for this pet/client on this date")
                        raise Exception("No appointments found for this pet/client on this date.")
                    
                    print("\nFound these appointments for this pet/client on this date:")
                    for app in existing_appointments:
                        print(f"Date: {app[3]}, Time: {app[4]}, Reason: {app[7]}")

                    # Now delete using the IDs, date, time, and reason
                    db.cursor.execute("""
                        DELETE FROM appointments
                        WHERE pet_id = ? AND client_id = ? AND DATE(date) = ? AND time = ? AND reason = ?
                    """, (pet_id, client_id, date, time_str, reason))
                    
                    if db.cursor.rowcount == 0:
                        raise Exception("No appointment was deleted. Please check if the appointment exists.")
                    
                    db.conn.commit()
                    print("Appointment deleted successfully")
                    show_message(None, "Appointment deleted successfully!", QMessageBox.Information)

                    # Refresh the table
                    populate_tables()
                except Exception as e:
                    error_msg = f"Failed to delete appointment: {str(e)}"
                    print(error_msg)
                    show_message(None, error_msg, QMessageBox.Critical)
                finally:
                    db.close_connection()
        else:
            show_message(None, "Please select an appointment to delete.", QMessageBox.Warning)

    view_button.clicked.connect(handle_view)
    edit_button.clicked.connect(handle_edit)
    delete_button.clicked.connect(handle_delete)

    def populate_tables():
        db = Database()
        try:
            appointments = db.fetch_appointments()
            print(f"Fetched appointments: {appointments}")
            urgent_table.setRowCount(0)
            all_table.setRowCount(0)
            for appointment in appointments:
                date = str(appointment[0])
                time = str(appointment[1])
                display_date = date  # Already formatted by DATE_FORMAT
                
                # Convert time to 12-hour format
                try:
                    time_obj = datetime.strptime(time, "%H:%M:%S")
                    display_time = time_obj.strftime("%I:%M %p")
                except ValueError as e:
                    print(f"Error parsing time {time}: {e}")
                    display_time = time  # Use original time if parsing fails
                
                pet_name = str(appointment[2])
                client_name = str(appointment[3])
                reason = str(appointment[4])
                status = str(appointment[5])
                payment_status = str(appointment[6])
                veterinarian = str(appointment[7])  # Remove the Dr. prefix since it's already in the database

                # --- All Table ---
                all_row_position = all_table.rowCount()
                all_table.insertRow(all_row_position)
                # Date
                item = QTableWidgetItem(display_date)
                item.setTextAlignment(Qt.AlignCenter)
                all_table.setItem(all_row_position, 0, item)
                # Time
                item = QTableWidgetItem(display_time)
                item.setTextAlignment(Qt.AlignCenter)
                all_table.setItem(all_row_position, 1, item)
                # Pet Name
                item = QTableWidgetItem(pet_name)
                item.setTextAlignment(Qt.AlignCenter)
                all_table.setItem(all_row_position, 2, item)
                # Owner/Client
                item = QTableWidgetItem(client_name)
                item.setTextAlignment(Qt.AlignCenter)
                all_table.setItem(all_row_position, 3, item)
                # Reason
                item = QTableWidgetItem(reason)
                item.setTextAlignment(Qt.AlignCenter)
                all_table.setItem(all_row_position, 4, item)
                # Status
                status_item = QTableWidgetItem(status)
                status_item.setTextAlignment(Qt.AlignCenter)
                # Set background color based on status
                status_lower = status.lower()
                if status_lower == "scheduled":
                    status_item.setBackground(QBrush(QColor("#FFEEBA")))
                elif status_lower == "completed":
                    status_item.setBackground(QBrush(QColor("#DFF2BF")))
                elif status_lower == "urgent":
                    status_item.setBackground(QBrush(QColor("#FFBABA")))
                elif status_lower in ["cancelled", "no-show"]:
                    status_item.setBackground(QBrush(QColor("#D3D3D3")))
                elif status_lower == "rescheduled":
                    status_item.setBackground(QBrush(QColor("orange")))
                all_table.setItem(all_row_position, 5, status_item)
                # Payment Status
                item = QTableWidgetItem(payment_status)
                item.setTextAlignment(Qt.AlignCenter)
                all_table.setItem(all_row_position, 6, item)
                # Veterinarian
                item = QTableWidgetItem(veterinarian)
                item.setTextAlignment(Qt.AlignCenter)
                all_table.setItem(all_row_position, 7, item)

                # --- Urgent Table ---
                if status.lower() == "urgent":
                    urgent_row_position = urgent_table.rowCount()
                    urgent_table.insertRow(urgent_row_position)
                    item = QTableWidgetItem(display_date)
                    item.setTextAlignment(Qt.AlignCenter)
                    urgent_table.setItem(urgent_row_position, 0, item)
                    item = QTableWidgetItem(display_time)
                    item.setTextAlignment(Qt.AlignCenter)
                    urgent_table.setItem(urgent_row_position, 1, item)
                    item = QTableWidgetItem(pet_name)
                    item.setTextAlignment(Qt.AlignCenter)
                    urgent_table.setItem(urgent_row_position, 2, item)
                    item = QTableWidgetItem(client_name)
                    item.setTextAlignment(Qt.AlignCenter)
                    urgent_table.setItem(urgent_row_position, 3, item)
                    item = QTableWidgetItem(reason)
                    item.setTextAlignment(Qt.AlignCenter)
                    urgent_table.setItem(urgent_row_position, 4, item)
                    urgent_status_item = QTableWidgetItem(status)
                    urgent_status_item.setTextAlignment(Qt.AlignCenter)
                    urgent_status_item.setBackground(QBrush(QColor("#FFBABA")))
                    urgent_table.setItem(urgent_row_position, 5, urgent_status_item)
                    item = QTableWidgetItem(payment_status)
                    item.setTextAlignment(Qt.AlignCenter)
                    urgent_table.setItem(urgent_row_position, 6, item)
                    item = QTableWidgetItem(veterinarian)
                    item.setTextAlignment(Qt.AlignCenter)
                    urgent_table.setItem(urgent_row_position, 7, item)

        except Exception as e:
            print(f"❌ Error populating tables: {e}")
            import traceback
            traceback.print_exc()  # Print the full error traceback
        finally:
            db.close_connection()

    # Populate tables on widget load
    populate_tables()

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
            # Get date and time separately
            date = dialog.date_edit.date().toString("yyyy-MM-dd")
            hour = dialog.time_edit.time().hour()
            minute = dialog.time_edit.time().minute()
            ampm = dialog.ampm_combo.currentText()
            # Convert to 24-hour format
            if ampm == "PM" and hour < 12:
                hour += 12
            if ampm == "AM" and hour == 12:
                hour = 0
            time_str = f"{hour:02d}:{minute:02d}:00"  # Format as HH:MM:SS
            
            status = dialog.status_combo.currentText()
            payment = dialog.payment_combo.currentText()
            pet_name_display = dialog.pet_name_combo.currentText().strip()
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

                # Insert the appointment into the database with separate date and time
                db.cursor.execute("""
                    INSERT INTO appointments (pet_id, client_id, date, time, status, payment_status, reason, veterinarian)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (pet_id, client_id, date, time_str, status, payment, reason, veterinarian))
                db.conn.commit()

                # Show a success message
                show_message(dialog, "Appointment added successfully!", QMessageBox.Information)

                # Refresh the table
                populate_tables()
            except Exception as e:
                show_message(dialog, f"Failed to save appointment: {e}", QMessageBox.Critical)
            finally:
                db.close_connection()
        else:
            print("Appointment creation cancelled")

    add_appointment_button.clicked.connect(open_appointment_form)

    return content

class PetAppointmentsDialog(QDialog):
    def __init__(self, pet_name):
        super().__init__()
        self.setWindowTitle(f"Appointments for {pet_name}")
        
        # Calculate total width needed for the table
        column_widths = [150, 120, 150, 200, 180, 200, 150]  # Widths for each column
        total_table_width = sum(column_widths) + 20  # Add 20 for scrollbar
        
        # Set dialog width to accommodate the table plus margins
        dialog_width = total_table_width + 40  # Add 40 for left and right margins
        self.setFixedWidth(dialog_width)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel(f"{pet_name}'s Appointments")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #012547;
            margin-bottom: 10px;
        """)
        layout.addWidget(title_label)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Date", "Pet Name", "Owner/Client", "Reason", 
            "Status", "Payment Status", "Veterinarian"
        ])
        
        # Set column widths
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)
            
        self.table.setStyleSheet("""
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
        
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.setFixedSize(120, 40)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                color: white;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #01315d;
            }
        """)
        close_button.clicked.connect(self.accept)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        # Load appointments
        self.load_pet_appointments(pet_name)
        
    def load_pet_appointments(self, pet_name):
        """Load appointments for the specific pet from the database."""
        db = Database()
        try:
            # Fetch appointments for the specific pet
            db.cursor.execute("""
                SELECT a.date, p.name, c.name, a.reason, a.status, 
                       a.payment_status, a.veterinarian
                FROM appointments a
                JOIN pets p ON a.pet_id = p.pet_id
                JOIN clients c ON a.client_id = c.client_id
                WHERE p.name = ?
                ORDER BY a.date DESC
            """, (pet_name,))
            
            appointments = db.cursor.fetchall()
            
            # Clear existing rows
            self.table.setRowCount(0)
            
            # Add appointments to table
            for row, appointment in enumerate(appointments):
                self.table.insertRow(row)
                for col, value in enumerate(appointment):
                    if col == 0:  # Date column
                        display_time = format_datetime_for_display(str(value))
                        item = QTableWidgetItem(display_time)
                    else:
                        item = QTableWidgetItem(str(value))
                    
                    # Set background color for status
                    if col == 4:  # Status column
                        if value.lower() == "scheduled":
                            item.setBackground(QBrush(QColor("#FFEEBA")))
                        elif value.lower() == "completed":
                            item.setBackground(QBrush(QColor("#DFF2BF")))
                        elif value.lower() == "urgent":
                            item.setBackground(QBrush(QColor("#FFBABA")))
                        elif value.lower() in ["cancelled", "no-show"]:
                            item.setBackground(QBrush(QColor("#D3D3D3")))
                        elif value.lower() == "rescheduled":
                            item.setBackground(QBrush(QColor("orange")))
                    
                    self.table.setItem(row, col, item)
            
            # Show message if no appointments found
            if not appointments:
                self.table.insertRow(0)
                placeholder = QTableWidgetItem("No appointments found for this pet")
                placeholder.setTextAlignment(Qt.AlignCenter)
                self.table.setSpan(0, 0, 1, self.table.columnCount())
                self.table.setItem(0, 0, placeholder)
            
            # Calculate dialog height based on table content
            row_height = 40  # Height of each row
            header_height = 40  # Height of the header
            min_height = 300  # Minimum dialog height
            max_height = 800  # Maximum dialog height
            
            # Calculate total height needed
            total_rows = self.table.rowCount()
            table_height = (total_rows * row_height) + header_height
            dialog_height = table_height + 150  # Add space for title and button
            
            # Set dialog height within limits
            dialog_height = max(min_height, min(dialog_height, max_height))
            self.setFixedHeight(dialog_height)
                
        except Exception as e:
            print(f"Error loading pet appointments: {e}")
        finally:
            db.close_connection()

def select_pet_in_combo(combo, pet_name):
    """Select the pet in the combo box, ignoring owner labels and spaces."""
    for i in range(combo.count()):
        text = combo.itemText(i).strip()
        # Skip owner group labels
        if text.endswith("- Owner"):
            continue
        if text == pet_name.strip():
            combo.setCurrentIndex(i)
            break
        
def select_vet_in_combo(combo, vet_name):
    """Select the veterinarian in the combo box, ignoring 'Dr. ' prefix."""
    vet_name = vet_name.replace("Dr. ", "").strip()
    for i in range(combo.count()):
        text = combo.itemText(i).replace("Dr. ", "").strip()
        if text == vet_name:
            combo.setCurrentIndex(i)
            break