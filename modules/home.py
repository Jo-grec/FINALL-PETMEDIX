from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QHeaderView, QTableWidget, QTableWidgetItem, QAbstractItemView, QScrollBar, QSizePolicy
from PySide6.QtGui import QPixmap, QIcon, QColor, QBrush
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QSizePolicy
from modules.database import Database  # Import the Database class
from datetime import datetime

def get_home_widget(user_role):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        boxes_layout = QHBoxLayout()
        boxes_layout.setAlignment(Qt.AlignLeft)  # Align boxes to the left
        boxes_layout.setContentsMargins(20, 0, 0, 0)  # Add left margin to align with search bar
        boxes_layout.setSpacing(6)  # Reduce spacing between boxes

        # Connect to the database and fetch counts
        db = Database()
        clients_count, medical_records_count, appointments_count = db.fetch_counts()
        db.close_connection()

        # Box 1: Clients
        box1 = QWidget()
        box1.setStyleSheet("background-color: #012547;")
        box1.setFixedWidth(200)
        box1.setFixedHeight(140)
        box1.setObjectName("Box1")

        clients_label = QLabel("Total Clients", box1)
        clients_label.setObjectName("ClientsLabel")
        clients_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        clients_label.setStyleSheet("color: white; font-size: 14px; font-family: Lato; font-weight: bold;")

        number_label = QLabel(str(clients_count), box1)  # Dynamic count
        number_label.setObjectName("NumberLabel")
        number_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        box1_layout = QVBoxLayout(box1)
        box1_layout.addWidget(clients_label)
        box1_layout.addWidget(number_label)
        box1_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        box1_layout.setContentsMargins(20, 10, 10, 10)  # Add left padding for better spacing

        boxes_layout.addWidget(box1)

        # Box 2: Medical Records
        box2 = QWidget()
        box2.setStyleSheet("background-color: #FFFFFF;")
        box2.setFixedWidth(200)
        box2.setFixedHeight(140)
        box2.setObjectName("Box2")

        medical_label = QLabel("Medical Reports", box2)
        medical_label.setObjectName("MedicalLabel")
        medical_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        medical_label.setStyleSheet("color: #1A1A1A; font-size: 14px; font-family: Lato; font-weight: bold;")

        number_label2 = QLabel(str(medical_records_count), box2)  # Dynamic count
        number_label2.setObjectName("NumberLabel2")
        number_label2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        box2_layout = QVBoxLayout(box2)
        box2_layout.addWidget(medical_label)
        box2_layout.addWidget(number_label2)
        box2_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        box2_layout.setContentsMargins(20, 10, 10, 10)  # Add left padding for better spacing

        boxes_layout.addWidget(box2)

        # Box 3: Appointments
        box3 = QWidget()
        box3.setStyleSheet("background-color: #FFFFFF;")
        box3.setFixedWidth(200)
        box3.setFixedHeight(140)
        box3.setObjectName("Box3")

        appointments_label = QLabel("Daily Appointments", box3)
        appointments_label.setObjectName("AppointmentsLabel")
        appointments_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        appointments_label.setStyleSheet("color: #1A1A1A; font-size: 14px; font-family: Lato; font-weight: bold;")

        number_label3 = QLabel(str(appointments_count), box3)  # Dynamic count
        number_label3.setObjectName("NumberLabel3")
        number_label3.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        box3_layout = QVBoxLayout(box3)
        box3_layout.addWidget(appointments_label)
        box3_layout.addWidget(number_label3)
        box3_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        box3_layout.setContentsMargins(20, 10, 10, 10)  # Add left padding for better spacing

        boxes_layout.addWidget(box3)

        # Create a new box below the 3 boxes with the same total width
        # Total width = 3 boxes (200px each) + 2 gaps (6px each) = 612px
        new_box = QWidget()
        new_box.setStyleSheet("background-color: #FFFFFF;")
        new_box.setFixedWidth(612)  # Same width as the 3 boxes combined
        new_box.setFixedHeight(140)
        new_box.setObjectName("Box4")
        
        # Create label for the new box
        new_box_label = QLabel("Total Patients Tended", new_box)
        new_box_label.setObjectName("NewBoxLabel")
        new_box_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        new_box_label.setStyleSheet("color: #1A1A1A; font-size: 14px; font-family: Lato; font-weight: bold;")
        
        # Create a number label (you can add dynamic data here)
        new_box_number = QLabel("0", new_box)  # Placeholder number
        new_box_number.setObjectName("NumberLabel4")
        new_box_number.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # Create vertical layout for the new box
        new_box_layout = QVBoxLayout(new_box)
        new_box_layout.addWidget(new_box_label)
        new_box_layout.addWidget(new_box_number)
        new_box_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        new_box_layout.setContentsMargins(20, 10, 10, 0)  # Add left padding for better spacing
        
        # Create a container widget for the new box to add left margin
        new_box_container = QWidget()
        new_box_container_layout = QHBoxLayout(new_box_container)
        new_box_container_layout.setContentsMargins(20, 0, 0, 0)  # Add left margin to align with search bar and boxes
        new_box_container_layout.setAlignment(Qt.AlignLeft)  # Align the box to the left within the container
        new_box_container_layout.addWidget(new_box)
        
        # Create a vertical layout for the left side (3 boxes + total patients box)
        left_side_layout = QVBoxLayout()
        left_side_layout.setSpacing(20)
        left_side_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add the 3 boxes layout to the left side
        left_side_layout.addLayout(boxes_layout)
        left_side_layout.addSpacing(0)  # No spacing between boxes and total patients box
        left_side_layout.addWidget(new_box_container)
        
        # Create the Reminders box on the right side
        # Height = 3 boxes (140px each) + total patients box (140px) = 420px
        reminders_box = QWidget()
        reminders_box.setStyleSheet("background-color: #FFFFFF;")
        reminders_box.setFixedWidth(640)  # Width for the reminders box
        reminders_box.setFixedHeight(300)  # Reduced height to prevent overlapping
        reminders_box.setObjectName("Box5")
        
        # Create label for the reminders box
        reminders_label = QLabel("Reminders", reminders_box)
        reminders_label.setObjectName("RemindersLabel")
        reminders_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        reminders_label.setStyleSheet("color: #1A1A1A; font-size: 14px; font-family: Lato; font-weight: bold;")
        reminders_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        # Create Add Reminder button with icon
        add_reminder_btn = QPushButton(reminders_box)
        add_reminder_btn.setObjectName("AddReminderBtn")
        add_reminder_btn.setFixedSize(40, 40)
        add_reminder_btn.setIcon(QIcon("assets/new icons/add-reminders.png"))  # Use your add icon
        add_reminder_btn.setIconSize(QSize(18, 18))
        add_reminder_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                margin: 0;
                padding: 0;
                padding-right: -40px;
            }
            QPushButton:hover {
                background-color: transparent;
            }
        """)
        
        # Create Edit Reminder button with icon
        edit_reminder_btn = QPushButton(reminders_box)
        edit_reminder_btn.setObjectName("EditReminderBtn")
        edit_reminder_btn.setFixedSize(40, 40)
        edit_reminder_btn.setIcon(QIcon("assets/new icons/edit-reminders.png"))  # Use your edit icon
        edit_reminder_btn.setIconSize(QSize(18, 18))
        edit_reminder_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                margin: 0;
                padding: 0;
            }
            QPushButton:hover {
                background-color: transparent;
            }
        """)
        
                # Create horizontal layout for the reminders header (label + buttons)
        reminders_header_layout = QHBoxLayout()
        reminders_header_layout.setContentsMargins(0, 0, 0, 0)
        reminders_header_layout.setSpacing(0)  # No default spacing between elements
        reminders_header_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Align items vertically center

        # Add label to the left
        reminders_header_layout.addWidget(reminders_label)
        reminders_header_layout.addStretch()  # Push buttons to the right

        # Add buttons to the right
        reminders_header_layout.addWidget(add_reminder_btn)
        reminders_header_layout.addWidget(edit_reminder_btn)

        # Create vertical layout for the reminders box
        reminders_layout = QVBoxLayout(reminders_box)
        reminders_layout.addLayout(reminders_header_layout)  # Add the header layout
        reminders_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        reminders_layout.setContentsMargins(20, 10, 10, 10)  # Add padding
        
        # Create a horizontal layout to hold left side and reminders box
        dashboard_layout = QHBoxLayout()
        dashboard_layout.setSpacing(20)  # Space between left side and reminders box
        dashboard_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add left side and reminders box to the dashboard layout
        dashboard_layout.addLayout(left_side_layout)
        dashboard_layout.addWidget(reminders_box)
        dashboard_layout.addStretch()  # Push everything to the left
        
        # Add the dashboard layout to the main layout
        layout.addLayout(dashboard_layout)
        
        layout.setSpacing(0)  # Ensure no spacing between main layout items
        layout.setContentsMargins(0, 0, 0, 0)  # Remove any default margins

        # Create container for title and table
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container.setStyleSheet("QWidget { margin: 0; padding: 0; }")

        # Title removed - no longer showing "Recent Reports" or "Recent Appointments"
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container.setStyleSheet("QWidget { margin: 0; padding: 0; }")
        layout.setSpacing(50)

        # Create a box container for the table
        table_box = QWidget()
        table_box.setStyleSheet("background-color: #FFFFFF; padding-top: 20px;")
        table_box.setObjectName("TableBox")
        table_box.setFixedWidth(900)  # Set the width of the table box
        
        # Create label for the table box
        table_label = QLabel("Today's Appointments", table_box)
        table_label.setObjectName("TableLabel")
        table_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        table_label.setStyleSheet("color: #1A1A1A; font-size: 14px; font-family: Lato; font-weight: bold;")

        # Create the table
        table_widget = QTableWidget()
        table_widget.setContentsMargins(0, 0, 0, 0)
        table_widget.setObjectName("RecentTable")
        table_widget.setStyleSheet("""
            QTableWidget {
                margin: 0;
                padding: 0;
                border: none;
                background-color: transparent;
                gridline-color: transparent;
                outline: none;
            }
            QHeaderView::section {
                margin: 0;
                padding: 8px;
                border: none;
                background-color: #012547;
            }
            QHeaderView {
                margin: 0;
                padding: 0;
                border: none;
            }
            QTableWidget::item {
                border-bottom: 1px solid #e0e0e0;
                border-right: none;
                border-left: none;
                border-top: none;
                background-color: transparent;
            }
            QTableWidget::item:selected {
                background-color: transparent;
                color: black;
            }
            QTableWidget::item:focus {
                background-color: transparent;
                border: none;
            }
            QTableCornerButton::section {
                background-color: #012547;
                border: none;
            }
        """)
        
        # Create vertical layout for the table box
        table_box_layout = QVBoxLayout(table_box)
        table_box_layout.addWidget(table_label) 
        table_box_layout.addWidget(table_widget)
        table_box_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        table_box_layout.setContentsMargins(20, 10, 10, 10)  # Add padding
        
        # Create calendar box on the right side
        calendar_box = QWidget()
        calendar_box.setStyleSheet("background-color: #FFFFFF; padding-top: 20px;")
        calendar_box.setObjectName("CalendarBox")
        calendar_box.setFixedWidth(350)  # Width for the calendar box
        calendar_box.setFixedHeight(315)  # Height for the calendar box
        
        # Create label for the calendar box
        calendar_label = QLabel("Calendar", calendar_box)
        calendar_label.setObjectName("CalendarLabel")
        calendar_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        calendar_label.setStyleSheet("color: #1A1A1A; font-size: 14px; font-family: Lato; font-weight: bold;")
        
        # Create vertical layout for the calendar box
        calendar_layout = QVBoxLayout(calendar_box)
        calendar_layout.addWidget(calendar_label)
        calendar_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        calendar_layout.setContentsMargins(20, 10, 10, 10)  # Add padding
        
        # Create a horizontal layout to hold table box and calendar box
        table_calendar_layout = QHBoxLayout()
        table_calendar_layout.setSpacing(20)  # Space between table and calendar
        table_calendar_layout.setContentsMargins(0, 0, 0, 0)
        table_calendar_layout.setAlignment(Qt.AlignTop)  # Align to top to prevent shifting down
        
        # Create a container widget to hold the table and calendar with fixed height
        table_calendar_container = QWidget()
        table_calendar_container.setFixedHeight(315)  # Set fixed height to prevent stretching
        table_calendar_container.setLayout(table_calendar_layout)
        
        # Add table box and calendar box to the horizontal layout
        table_calendar_layout.addWidget(table_box)
        table_calendar_layout.addWidget(calendar_box)
        table_calendar_layout.addStretch()  # Push everything to the left
        
        # Ensure no spacing between label and table
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(20, 0, 20, 20)  # Add left, right, and bottom margins
        container.setStyleSheet("QWidget { margin: 0; padding: 0; }")

        if user_role == "Veterinarian":
            # Set up table for appointments with new columns
            table_widget.setColumnCount(5)  # 5 columns as requested
            table_widget.setHorizontalHeaderLabels([
                "Patient Name",
                "Client Name", 
                "Time",
                "Type",
                "Status"
            ])
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table_widget.horizontalHeader().setFixedHeight(40)

            # Fetch and populate recent appointments
            db = Database()
            appointments = db.fetch_recent_appointments_summary(user_role)
            db.close_connection()

            table_widget.setRowCount(len(appointments))
            for row, appointment in enumerate(appointments):
                # Get time and convert to 12-hour format
                time_str = str(appointment[1])
                try:
                    time_obj = datetime.strptime(time_str, "%H:%M:%S")
                    display_time = time_obj.strftime("%I:%M %p")
                except ValueError as e:
                    print(f"Error parsing time {time_str}: {e}")
                    display_time = time_str
                
                # Patient Name (Pet Name)
                item = QTableWidgetItem(str(appointment[2]))
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row, 0, item)
                
                # Client Name (Owner/Client)
                item = QTableWidgetItem(str(appointment[4]))
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row, 1, item)
                
                # Time
                item = QTableWidgetItem(display_time)
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row, 2, item)
                
                # Type (Reason for Appointment)
                item = QTableWidgetItem(str(appointment[3]))
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row, 3, item)
                
                # Status
                status_value = str(appointment[5])
                item = QTableWidgetItem(status_value)
                item.setTextAlignment(Qt.AlignCenter)
                
                # Add color coding for status column
                status_lower = status_value.lower()
                if status_lower == "scheduled":
                    item.setBackground(QBrush(QColor("#FFEEBA")))  # Light yellow
                elif status_lower == "completed":
                    item.setBackground(QBrush(QColor("#DFF2BF")))  # Light green
                elif status_lower == "urgent":
                    item.setBackground(QBrush(QColor("#FFBABA")))  # Light red
                elif status_lower in ["cancelled", "no-show"]:
                    item.setBackground(QBrush(QColor("#D3D3D3")))  # Light gray
                elif status_lower == "rescheduled":
                    item.setBackground(QBrush(QColor("orange")))  # Orange
                
                table_widget.setItem(row, 4, item)
        else:
            # Set up table for reports
            table_widget.setColumnCount(5)
            table_widget.setHorizontalHeaderLabels([
                "Date",
                "Type",
                "Pet",
                "Owner/Client",
                "Veterinarian/Staff in Charge"
            ])
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
            table_widget.horizontalHeader().setFixedHeight(40)
            table_widget.setColumnWidth(0, 130)  # Date
            table_widget.setColumnWidth(1, 150)  # Type
            table_widget.setColumnWidth(2, 150)  # Pet
            table_widget.setColumnWidth(3, 150)  # Owner/Client
            table_widget.setColumnWidth(4, 150)  # Veterinarian/Staff

            # Fetch and populate recent reports
            db = Database()
            try:
                recent_reports = db.fetch_recent_reports_summary(user_role)
                if len(recent_reports) == 0:
                    table_widget.setRowCount(1)
                    no_data_item = QTableWidgetItem("No recent reports found")
                    no_data_item.setTextAlignment(Qt.AlignCenter)
                    table_widget.setSpan(0, 0, 1, 5)
                    table_widget.setItem(0, 0, no_data_item)
                else:
                    table_widget.setRowCount(len(recent_reports))
                    for row, report in enumerate(recent_reports):
                        for col, value in enumerate(report):
                            item = QTableWidgetItem(str(value))
                            item.setTextAlignment(Qt.AlignCenter)
                            table_widget.setItem(row, col, item)
            except Exception as e:
                print(f"Error populating reports table: {e}")
            finally:
                db.close_connection()

        # Common table settings
        table_widget.horizontalHeader().setStyleSheet("""
            QHeaderView::section:horizontal {
                background-color: #FFFFFF;
                font-family: Poppins;
                color: #012547;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
                margin: 0;
                border: none;
            }
        """)
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_widget.verticalHeader().setVisible(False)
        table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_widget.setShowGrid(True)
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_widget.setFocusPolicy(Qt.NoFocus)
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        table_widget.setFixedHeight(300)

        # Add table and calendar container to container with fixed positioning
        container_layout.addWidget(table_calendar_container)
        container_layout.setAlignment(Qt.AlignTop)  # Ensure container content stays at top

        # Add container to main layout
        layout.addWidget(container)

        # Store the table widget and user role as properties of the content widget
        content.table_widget = table_widget
        content.user_role = user_role

        # Add a method to filter the table
        def filter_table(search_text):
            filter_recent_table(search_text, table_widget, user_role)

        content.filter_table = filter_table

        return content

class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PetMedix - Home")
        self.setup_ui()

    def setup_ui(self):
        content = get_home_widget("Veterinarian")
        self.setLayout(content)
        
        
        
def filter_clients_table(search_text, table):
    """Filter the clients table based on the search text."""
    search_text = search_text.strip().lower()  # Normalize the search text
    
    # If search text is empty, show all rows
    if not search_text:
        for row in range(table.rowCount()):
            table.setRowHidden(row, False)
        return
        
    # Get all client names and their associated pet names from the database
    db = Database()
    try:
        db.cursor.execute("""
            SELECT c.name as client_name, GROUP_CONCAT(p.name) as pet_names
            FROM clients c
            LEFT JOIN pets p ON c.client_id = p.client_id
            GROUP BY c.client_id
        """)
        client_pet_data = db.cursor.fetchall()
    except Exception as e:
        print(f"Error fetching client and pet data: {e}")
        return
    finally:
        db.close_connection()
    
    # Create a mapping of client names to their pet names
    client_pet_map = {client: pets.split(',') if pets else [] for client, pets in client_pet_data}
    
    # Filter the table rows
    for row in range(table.rowCount()):
        cell_widget = table.cellWidget(row, 0)
        if cell_widget:
            name_label = cell_widget.findChild(QLabel)
            if name_label:
                client_name = name_label.text().strip().lower()
                pet_names = [pet.lower() for pet in client_pet_map.get(name_label.text(), [])]
                
                # Show row if search text matches either client name or any pet name
                should_show = (
                    search_text in client_name or
                    any(search_text in pet for pet in pet_names)
                )
                table.setRowHidden(row, not should_show)

def filter_recent_table(search_text, table, user_role):
    """Filter the recent appointments or reports table based on the search text."""
    search_text = search_text.strip().lower()  # Normalize the search text
    
    # If search text is empty, show all rows
    if not search_text:
        for row in range(table.rowCount()):
            table.setRowHidden(row, False)
        return
    
    # Get the column indices for pet name and owner/client based on user role
    if user_role == "Veterinarian":
        # For appointments table
        pet_name_col = 2  # Pet Name column
        owner_col = 4     # Owner/Client column
    else:
        # For reports table
        pet_name_col = 2  # Pet column
        owner_col = 3     # Owner/Client column
    
    # Filter the table rows
    for row in range(table.rowCount()):
        pet_name_item = table.item(row, pet_name_col)
        owner_item = table.item(row, owner_col)
        
        if pet_name_item and owner_item:
            pet_name = pet_name_item.text().strip().lower()
            owner_name = owner_item.text().strip().lower()
            
            # Show row if search text matches either pet name or owner name
            should_show = (
                search_text in pet_name or
                search_text in owner_name
            )
            table.setRowHidden(row, not should_show)