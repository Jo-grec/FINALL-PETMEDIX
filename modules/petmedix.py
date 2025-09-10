from PySide6.QtWidgets import (QWidget, QTextEdit, QLabel, QHeaderView, QHBoxLayout, QVBoxLayout, 
    QPushButton, QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, QScrollBar, 
    QHeaderView, QScrollArea, QMenu, QDialog, QGridLayout, QStyledItemDelegate, QToolButton)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer, QSize
from modules.home import get_home_widget
from modules.client import get_client_widget, filter_clients_table
from modules.report import get_report_widget
from modules.appointment import get_appointment_widget
from modules.billing import update_billing_widget
from modules.setting import get_setting_widget
from modules.database import Database
import os

class CustomTableDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #009FB7;
                padding: 2px;
                selection-background-color: #e3f2fd;
            }
        """)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setText(str(value) if value is not None else "")

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, Qt.EditRole)

class TextEditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QTextEdit(parent)
        editor.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #009FB7;
                padding: 2px;
                selection-background-color: #e3f2fd;
                font-size: 11px;
            }
        """)
        # Set minimum height based on content
        text = index.model().data(index, Qt.DisplayRole)
        if text:
            lines = str(text).count('\n') + 1
            editor.setMinimumHeight(max(25, lines * 20))
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setPlainText(str(value) if value is not None else "")

    def setModelData(self, editor, model, index):
        value = editor.toPlainText()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        # Get the cell's content to determine height
        text = index.model().data(index, Qt.DisplayRole)
        if text:
            lines = str(text).count('\n') + 1
            height = max(25, lines * 20)
        else:
            height = 25
            
        # Set the editor geometry to match the cell
        editor.setGeometry(option.rect.x(), option.rect.y(), 
                         option.rect.width(), height)

class PetMedix(QWidget):
    def __init__(self, user_id, role, last_name, first_name):
        super().__init__()

        self.user_id = user_id
        self.user_role = role
        self.last_name = last_name
        self.first_name = first_name
        self.selected_pet_name = None
        self.selected_client_email = None
        
        self.setWindowTitle("PetMedix - Home")

        # Apply styles from external QSS file
        with open("styles/login.qss", "r") as file:
            self.setStyleSheet(file.read())

        # Main layout (vertical layout for body only)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create username label (dynamic greeting) for use with search bar
        greeting = self.get_greeting(role, self.first_name, self.last_name)
        self.username_label = QLabel(greeting)
        self.username_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.username_label.setObjectName("UsernameLabel")

        # Dropdown icon
        self.dropdown_icon = QLabel()
        dropdown_pixmap = QPixmap("assets/dropdown.png")
        self.dropdown_icon.setPixmap(dropdown_pixmap)
        self.dropdown_icon.setFixedSize(30, 30)  # Increased size to 30x30
        self.dropdown_icon.setScaledContents(True)
        self.dropdown_icon.setCursor(Qt.PointingHandCursor)  # Change cursor to hand when hovering
        self.dropdown_icon.mousePressEvent = self.show_user_menu  # Connect click event
        self.dropdown_icon.setStyleSheet("QLabel { background-color: transparent; } QLabel:hover { background-color: rgba(255, 255, 255, 0.1); }")

        # Apply color to the pixmap
        # Convert the pixmap to image to apply color overlay
        image = dropdown_pixmap.toImage()
        for x in range(image.width()):
            for y in range(image.height()):
                color = image.pixelColor(x, y)
                if color.alpha() > 0:  # If pixel is not transparent
                    color.setRed(255)
                    color.setGreen(255)
                    color.setBlue(255)
                    image.setPixelColor(x, y, color)
        
        white_pixmap = QPixmap.fromImage(image)
        self.dropdown_icon.setPixmap(white_pixmap)

        # Create the body layout (horizontal layout with navbar on the left and content on the right)
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Create the left navigation bar (narrow)
        navbar = QWidget()
        navbar_layout = QVBoxLayout(navbar)
        navbar.setObjectName("NavBar")
        navbar_layout.setContentsMargins(5, 10, 10, 10)  # Reduced left padding for the navbar
        navbar_layout.setSpacing(5)

        navbar_logo = QLabel()
        # Load clinic logo from database for navbar only
        db = Database()
        try:
            db.cursor.execute("SELECT logo_path FROM clinic_info LIMIT 1")
            logo_path = db.cursor.fetchone()
            if logo_path and logo_path[0] and os.path.exists(logo_path[0]):
                navbar_logo_pixmap = QPixmap(logo_path[0])
            else:
                navbar_logo_pixmap = QPixmap("assets/logo.png")  # Default logo
        except Exception as e:
            print(f"❌ Error loading clinic logo: {e}")
            navbar_logo_pixmap = QPixmap("assets/logo.png")  # Default logo
        finally:
            db.close_connection()
            
        navbar_logo.setPixmap(navbar_logo_pixmap)
        navbar_logo.setObjectName("Navbarlogo")
        navbar_logo.setFixedHeight(80)  # Made logo smaller
        navbar_logo.setFixedWidth(80)   # Set fixed width for square aspect ratio
        navbar_logo.setAlignment(Qt.AlignCenter)
        navbar_logo.setScaledContents(True)

        # Load clinic name from database
        db = Database()
        try:
            db.cursor.execute("SELECT name FROM clinic_info LIMIT 1")
            clinic_name = db.cursor.fetchone()
            if clinic_name and clinic_name[0]:
                clinic_name_text = clinic_name[0]  # Use the name directly without splitting
            else:
                clinic_name_text = "Petmedix Animal Clinic"
        except Exception as e:
            print(f"❌ Error loading clinic name: {e}")
            clinic_name_text = "Petmedix Animal Clinic"
        finally:
            db.close_connection()

        # Format the clinic name to display on two lines
        if "PetMedix" in clinic_name_text:
            formatted_name = "PetMedix\nClinic"
        else:
            # For other clinic names, try to split intelligently
            words = clinic_name_text.split()
            if len(words) >= 2:
                formatted_name = f"{words[0]}\n{' '.join(words[1:])}"
            else:
                formatted_name = clinic_name_text

        clinic_name_label = QLabel(formatted_name)
        clinic_name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Align left for side-by-side layout
        clinic_name_label.setObjectName("ClinicNameLabel")
        clinic_name_label.setStyleSheet("""
            QLabel {
                font-family: Lato;
                font-size: 16px;
                font-weight: bold;
                color: #012547;
                line-height: 1.1;
                font-family: Lato;
            }
        """)

        # Create a horizontal layout for logo and clinic name
        logo_name_layout = QHBoxLayout()
        logo_name_layout.addWidget(navbar_logo)
        logo_name_layout.addSpacing(8)  # Reduced spacing between logo and text
        logo_name_layout.addWidget(clinic_name_label)
        logo_name_layout.addStretch()  # Push logo and name to the left
        logo_name_layout.setContentsMargins(8, 8, 8, 8)  # Reduced padding

        # Add the logo and name layout to the navbar
        navbar_layout.addLayout(logo_name_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # Set the shape of the frame to a horizontal line
        line.setFrameShadow(QFrame.Sunken)  # Make the line appear sunken (optional)
        navbar_layout.addWidget(line)
        # Create nav buttons with consistent spacing
        self.button1 = QPushButton("DASHBOARD")  # Removed manual spacing, will be handled by CSS
        self.button1.setIcon(QIcon("assets/new icons/dashboard.png"))
        self.button1.setIconSize(QSize(20, 20))  # Set icon size
        
        self.button2 = QPushButton("CLIENT LIST")  # Removed manual spacing, will be handled by CSS
        self.button2.setIcon(QIcon("assets/new icons/clientlist.png"))
        self.button2.setIconSize(QSize(20, 20))  # Set icon size
        
        self.button3 = QPushButton("REPORTS")  # Removed manual spacing, will be handled by CSS
        self.button3.setIcon(QIcon("assets/new icons/reports.png"))
        self.button3.setIconSize(QSize(20, 20))  # Set icon size
        
        self.button4 = QPushButton("APPOINTMENTS")  # Removed manual spacing, will be handled by CSS
        self.button4.setIcon(QIcon("assets/new icons/appointments.png"))
        self.button4.setIconSize(QSize(20, 20))  # Set icon size
        
        self.button5 = QPushButton("BILLINGS")  # Removed manual spacing, will be handled by CSS
        self.button5.setIcon(QIcon("assets/new icons/billings.png"))
        self.button5.setIconSize(QSize(20, 20))  # Set icon size

        # Add to layout
        navbar_layout.addWidget(self.button1)
        navbar_layout.addWidget(self.button2)
        navbar_layout.addWidget(self.button3)
        navbar_layout.addWidget(self.button4)
        navbar_layout.addWidget(self.button5)

        # Optional: Make flat
        for btn in [self.button1, self.button2, self.button3, self.button4, self.button5]:
            btn.setFlat(True)
            btn.setObjectName("navbarButton")  # Give all nav buttons the same object name
            btn.setCheckable(True)

        # Store in a list for logic
        self.nav_buttons = [
            self.button1, self.button2, self.button3,
            self.button4, self.button5
        ]

        # Connect for active highlight
        for btn in self.nav_buttons:
            btn.clicked.connect(lambda checked, b=btn: self.set_active_button(b))
            
        # Add a stretch to move the buttons to the top
        navbar_layout.addStretch()  # This ensures the buttons are at the top

        # Set fixed width for the navbar (increased to accommodate logo and text)
        navbar.setFixedWidth(220)

        # Add the navbar to the left side of the body layout
        body_layout.addWidget(navbar)

        # Create the right content area (takes the remaining space)
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area.setStyleSheet("background-color: #F4F5FC;")  # Background color for content area

        # Add content area to the right side of the body layout
        body_layout.addWidget(self.content_area)

        # Add the body layout (navbar + content) to the main layout
        main_layout.addLayout(body_layout)

        # Set the main layout for the window
        self.setLayout(main_layout)

        # Connect buttons to content change functions
        self.button1.clicked.connect(self.show_dashboard_content)
        self.button2.clicked.connect(self.show_client_content)
        self.button3.clicked.connect(self.show_report_content)
        self.button4.clicked.connect(self.show_appointments_content)
        self.button5.clicked.connect(self.show_billings_content)
        
        self.show_dashboard_content()
        
    def set_active_button(self, active_button):
        for btn in self.nav_buttons:
            btn.setChecked(btn == active_button)
            if btn == active_button:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(74, 144, 226, 0.22);
                        border-left: 4px solid #FED766;
                    }
                """)
            else:
                btn.setStyleSheet("")

    def clear_content(self):
        if self.content_layout is not None:
            while self.content_layout.count():
                item = self.content_layout.takeAt(0)
                widget = item.widget()
                layout = item.layout()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                elif layout is not None:
                    # Clear the layout recursively
                    self.clear_layout(layout)
                    
    def clear_layout(self, layout):
        """Recursively clear a layout and all its child widgets and layouts."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                child_layout = item.layout()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                elif child_layout is not None:
                    self.clear_layout(child_layout)
                    
    def get_greeting(self, role, first_name, last_name):
        """Generate a greeting based on the user's role and full name."""
        if role.lower() == "receptionist":
            return f"{first_name} {last_name}"
        elif role.lower() == "veterinarian":
            return f"Dr. {first_name} {last_name}"
        else:
            return f"{first_name} {last_name}"
                
    def add_search_bar(self):
        # Create a container widget for the search bar area
        search_container = QWidget()
        search_container.setFixedHeight(100)  # Fixed height for consistent positioning
        search_container.setStyleSheet("background-color: transparent; border: none;")
        
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(20, 20, 20, 20)  # Add padding around the search bar

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setFixedHeight(50)  # Reduced height for better proportion
        self.search_bar.setObjectName("SearchBar")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                font-family: Lato;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                padding: 0 20px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #012547;
                background-color: white;
            }
        """)

        # Create user widget with username and dropdown
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.username_label)
        user_layout.addSpacing(5)  # Add 5 pixels of space between username and dropdown
        user_layout.addWidget(self.dropdown_icon)
        user_layout.setSpacing(0)  # Keep other spacing at 0

        user_widget = QWidget()
        user_widget.setLayout(user_layout)

        # Add search bar and user widget to the layout
        search_layout.addWidget(self.search_bar, 1)  # Give search bar stretch factor
        search_layout.addSpacing(20)  # Add space between search bar and username
        search_layout.addWidget(user_widget)
        
        # Add the search container widget to the content layout
        self.content_layout.addWidget(search_container)

    def show_dashboard_content(self):
        self.clear_content()
        self.set_active_button(self.button1)  # Set dashboard button as active
        
        # Reset content layout spacing and margins
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        self.add_search_bar()  # Keep the search bar
        home_widget = get_home_widget(self.user_role)
        self.content_layout.addWidget(home_widget)
        
        # Connect the search bar to the home filtering function if it exists
        if hasattr(home_widget, 'filter_table'):
            self.search_bar.textChanged.connect(home_widget.filter_table)
    
    #CLIENT TAB
    def show_client_content(self):
        self.clear_content()
        self.add_search_bar()
        client_widget = get_client_widget(self, self.user_role)
        self.content_layout.addWidget(client_widget)

        # Find the clients table in the client widget
        clients_table = client_widget.findChild(QTableWidget)

        # Connect the search bar to the filtering function
        if clients_table:
            self.search_bar.textChanged.connect(lambda text: filter_clients_table(text, clients_table))
            
            # If we have a selected client email, find and select that client in the table
            if hasattr(self, 'selected_client_email') and self.selected_client_email:
                for row in range(clients_table.rowCount()):
                    cell_widget = clients_table.cellWidget(row, 0)
                    if cell_widget:
                        name_label = cell_widget.findChild(QLabel)
                        if name_label:
                            db = Database()
                            try:
                                db.cursor.execute("SELECT email FROM clients WHERE name = ?", (name_label.text(),))
                                result = db.cursor.fetchone()
                                if result and result[0] == self.selected_client_email:
                                    # Select the row
                                    clients_table.selectRow(row)
                                    # Highlight the selected row
                                    cell_widget.setStyleSheet("background-color: rgba(74, 144, 226, 0.22);")
                                    # Simulate clicking the cell to select the client
                                    clients_table.cellClicked.emit(row, 0)
                                    break
                            except Exception as e:
                                print(f"Error finding selected client: {e}")
                            finally:
                                db.close_connection()

    def show_pet_records(self):
        # Store the current client email before showing records
        if hasattr(self, 'selected_client_email'):
            # Find the edit form widget in the current content
            for widget in self.findChildren(QWidget):
                if widget.property("original_email"):
                    self.selected_client_email = widget.property("original_email")
                    break
        
        self.clear_content()  
        self.add_search_bar()

        # Create the main widget that will contain the content
        records_space = QWidget()
        main_layout = QVBoxLayout()  # Main layout for the entire content
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Section - Headers
        see_record = QLabel("See Record")
        see_record.setObjectName("SeeRecords")
        see_record.setStyleSheet("""
            background-color: #012547; 
            color: white; 
            font-size: 24px; 
            font-weight: bold;
            padding-left: 10px;
            font-family: Poppins;
        """)
        see_record.setFixedHeight(50)
        see_record.setAlignment(Qt.AlignVCenter)

        pet_medical = QLabel("Pet Medical Record")
        pet_medical.setObjectName("PetMedical")
        pet_medical.setStyleSheet("""
            background-color: #FED766; 
            color: #012547; 
            font-size: 24px; 
            font-weight: bold;
            padding-left: 10px;
            font-family: Poppins;
        """)
        pet_medical.setFixedHeight(50)
        pet_medical.setAlignment(Qt.AlignVCenter)

        # Add top labels to the main layout
        main_layout.addWidget(see_record)
        main_layout.addWidget(pet_medical)

        # Main content area with patient record and tables
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 10, 0, 10)
        content_layout.setSpacing(10)

        # Left side - Patient info
        left_panel = QWidget()
        left_panel.setFixedWidth(300)  # Set fixed width for left panel
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 10, 0)
        left_layout.setSpacing(0)

        # Title
        header_label = QLabel("PET MEDICAL\nRECORD")
        header_label.setStyleSheet("""
            font-family: Arial;
            font-size: 18px;
            font-weight: bold;
            color: #009FB7;
            line-height: 1.2;
            margin-left:5px;
        """)
        left_layout.addWidget(header_label)
        left_layout.addSpacing(5)

        # Section creation helper
        def create_info_section(title):
            section = QWidget()
            section_layout = QVBoxLayout(section)
            section_layout.setContentsMargins(0, 0, 0, 0)
            section_layout.setSpacing(0)
            
            # Section header
            header = QLabel(title)
            header.setFixedHeight(25)
            header.setStyleSheet("""
                background: rgba(0, 159, 183, 0.30);
                font-family: Lato;
                font-size: 13px;
                font-weight: bold;
                padding-left: 5px;
                color: #012547;
            """)
            header.setAlignment(Qt.AlignVCenter)
            section_layout.addWidget(header)
            
            return section, section_layout

        # Create sections
        pet_section, pet_layout = create_info_section("PET INFORMATION")

        # Create form fields
        def create_form_fields(layout, fields):
            form_widget = QWidget()
            form_layout = QVBoxLayout(form_widget)
            form_layout.setContentsMargins(5, 5, 5, 5)
            form_layout.setSpacing(3)  # Reduced spacing between fields
            
            field_widgets = {}  # Dictionary to store field widgets
            
            for field in fields:
                field_layout = QVBoxLayout()
                field_layout.setSpacing(0)
                
                label = QLabel(field + ":")
                label.setStyleSheet("""
                    font-family: Lato;
                    font-size: 11px;
                    color: #333;
                    margin: 0;
                    padding: 0;
                """)
                
                value = QLabel("")  # Empty label for the value
                value.setStyleSheet("""
                    font-family: Lato;
                    font-size: 11px;
                    color: #000;
                    margin: 0;
                    padding: 0;
                """)
                
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                line.setStyleSheet("background-color: #333;")
                line.setFixedHeight(1)  # Thinner line
                
                field_layout.addWidget(label)
                field_layout.addWidget(value)
                field_layout.addWidget(line)
                form_layout.addLayout(field_layout)
                
                field_widgets[field] = value  # Store the value widget
            
            layout.addWidget(form_widget)
            return field_widgets
        
        # Add fields to each section
        pet_fields = ["NAME", "AGE", "GENDER", "SPECIES", "BREED", "COLOR", "WEIGHT", "HEIGHT"]
        pet_widgets = create_form_fields(pet_layout, pet_fields)
        
        # Add back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                color: white;
                padding: 2px;
                font-weight: bold;
                font-size: 12px;
                border-radius: 10px;
                margin: 10px 5px;
                font-family: Lato;
            }
            QPushButton:hover {
                background-color: #023b6d;
            }
        """)
        back_button.setFixedWidth(60)
        back_button.clicked.connect(self.show_client_content)
        pet_layout.addWidget(back_button)

        # Add all sections to left panel
        left_layout.addWidget(pet_section)
        left_layout.addStretch()

        # Right side - Medical data & records
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Medical history tables (top row)
        medical_tables = QWidget()
        medical_tables.setStyleSheet("background-color: #eef8f9; border: 1px solid #d5d5d5;")
        medical_tables_layout = QHBoxLayout(medical_tables)
        medical_tables_layout.setContentsMargins(5, 5, 5, 5)
        medical_tables_layout.setSpacing(10)
        
        # Past illnesses table
        past_illnesses = QWidget()
        past_illnesses.setStyleSheet("background-color: white; border: 1px solid #d5d5d5;")
        past_illnesses_layout = QVBoxLayout(past_illnesses)
        past_illnesses_layout.setContentsMargins(0, 0, 0, 0)
        past_illnesses_layout.setSpacing(0)
        
        past_illnesses_header = QLabel("PAST ILLNESSES")
        past_illnesses_header.setAlignment(Qt.AlignCenter)
        past_illnesses_header.setStyleSheet("font-weight: bold; background-color: #eef8f9; font-size: 12px; font-family: Lato;")
        past_illnesses_layout.addWidget(past_illnesses_header)
        
        past_illnesses_text = QTextEdit()
        past_illnesses_text.setReadOnly(True)  # Initially read-only
        past_illnesses_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: none;
                font-size: 11px;
                padding: 5px;
                font-family: Lato;
            }
        """)
        past_illnesses_text.setFixedHeight(160)
        past_illnesses_layout.addWidget(past_illnesses_text)
        
        # Medical history table
        medical_history = QWidget()
        medical_history.setStyleSheet("background-color: white; border: 1px solid #d5d5d5;")
        medical_history_layout = QVBoxLayout(medical_history)
        medical_history_layout.setContentsMargins(0, 0, 0, 0)
        medical_history_layout.setSpacing(0)
        
        medical_history_header = QLabel("MEDICAL HISTORY")
        medical_history_header.setAlignment(Qt.AlignCenter)
        medical_history_header.setStyleSheet("font-weight: bold; background-color: #eef8f9; font-size: 12px; font-family: Lato;")
        medical_history_layout.addWidget(medical_history_header)
        
        medical_history_text = QTextEdit()
        medical_history_text.setReadOnly(True)  # Initially read-only
        medical_history_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: none;
                font-size: 11px;
                padding: 5px;
                font-family: Lato;
            }
        """)
        medical_history_text.setFixedHeight(160)
        medical_history_layout.addWidget(medical_history_text)
        
        # Add tables to layout
        medical_tables_layout.addWidget(past_illnesses)
        medical_tables_layout.addWidget(medical_history)
        
        # Records section
        records_section = QWidget()
        records_section.setStyleSheet("background-color: white; border: 1px solid #d5d5d5;")
        records_layout = QVBoxLayout(records_section)
        records_layout.setContentsMargins(0, 0, 0, 0)
        records_layout.setSpacing(0)
        
        records_header = QLabel("RECORDS")
        records_header.setAlignment(Qt.AlignCenter)
        records_header.setStyleSheet("font-weight: bold; background-color: #eef8f9; font-size: 12px; font-family: Lato;")
        records_layout.addWidget(records_header)
        
        # Records table
        records_table = QTableWidget()
        records_table.setColumnCount(5)
        records_table.setHorizontalHeaderLabels([
            "DATE", "TYPE OF RECORD", "VETERINARIAN/STAFF IN CHARGE", "REMARKS", "NEXT DUE DATE\n(if applicable)"
        ])
        
        records_table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #eef8f9;
                padding: 5px;
                border: none;
                border-bottom: 1px solid #d5d5d5;
                font-size: 11px;
                font-weight: normal;
                font-family: Lato;
            }
        """)
        records_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #d5d5d5;
                font-size: 11px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
        """)
        
        # Disable header highlighting on selection
        records_table.horizontalHeader().setHighlightSections(False)
        
        # Set selection behavior to select entire row
        records_table.setSelectionBehavior(QTableWidget.SelectRows)
        records_table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Hide vertical header (row numbers)
        records_table.verticalHeader().setVisible(False)
        
        # Set column widths and word wrap
        header = records_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Date
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Veterinarian
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Remarks - stretch to fill space
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Next due date
        
        # Enable word wrap for all cells
        records_table.setWordWrap(True)
        
        # Set text alignment to top for better readability
        records_table.verticalHeader().setDefaultAlignment(Qt.AlignTop)
        
        # Always disable editing for records table
        records_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        records_table.setFixedHeight(200)
        records_layout.addWidget(records_table)
        
        # Add to right layout
        right_layout.addWidget(medical_tables)
        right_layout.addWidget(records_section)
        right_layout.addStretch()

        # Add panels to content layout
        content_layout.addWidget(left_panel, 1)  # Give some stretch to left panel
        content_layout.addWidget(right_panel, 2)  # Give more stretch to right panel

        # Create buttons panel
        buttons_panel = QWidget()
        buttons_panel.setFixedWidth(80)  # Fixed width for buttons panel
        buttons_layout = QVBoxLayout(buttons_panel)
        buttons_layout.setContentsMargins(5, 0, 0, 0)  # Small left margin
        buttons_layout.setSpacing(5)  # Reduced spacing between buttons

        # Create Edit/Save button
        self.edit_btn = QToolButton()
        self.edit_btn.setText("Edit")
        self.edit_btn.setIcon(QIcon("assets/edit.png"))
        self.edit_btn.setIconSize(QSize(20, 20))  # Slightly larger icon
        self.edit_btn.setStyleSheet("""
            QToolButton {
                background-color:rgba(0, 159, 183, 0.30);
                color: #000;
                padding: 5px;
                font-weight: bold;
                font-size: 11px;
                text-align: center;
                border-radius: 5px;
                font-family: Lato;
            }
            QToolButton:hover {
                background-color: #008ba0;
            }
        """)
        self.edit_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.edit_btn.setFixedHeight(60)  # Increased height to accommodate icon above text
        self.edit_btn.setFixedWidth(70)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)

        # Add buttons to layout
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addStretch()  # Add stretch to push buttons to the top

        # Add buttons panel to content layout
        content_layout.addWidget(buttons_panel)
        
        # Store references to tables
        self.past_illnesses_text = past_illnesses_text
        self.medical_history_text = medical_history_text
        self.records_table = records_table
        self.is_edit_mode = False

        # Main layout assembly
        main_layout.addWidget(content_widget)
        
        # Set the layout for the records space
        records_space.setLayout(main_layout)
        
        # Add the records space to the content layout
        self.content_layout.addWidget(records_space)
        
        # Load data from database
        db = Database()
        try:
            # Load pet and owner information
            if hasattr(self, 'selected_pet_name'):
                db.cursor.execute("""
                    SELECT 
                        p.name, p.age, p.gender, p.species, p.breed, p.color,
                        p.weight, p.height
                    FROM pets p
                    WHERE p.name = ?
                """, (self.selected_pet_name,))
                
                result = db.cursor.fetchone()
                if result:
                    # Set pet information
                    pet_widgets["NAME"].setText(result[0])
                    pet_widgets["AGE"].setText(str(result[1]))
                    pet_widgets["GENDER"].setText(result[2])
                    pet_widgets["SPECIES"].setText(result[3])
                    pet_widgets["BREED"].setText(result[4])
                    pet_widgets["COLOR"].setText(result[5])
                    pet_widgets["WEIGHT"].setText(f"{result[6]} kg")
                    pet_widgets["HEIGHT"].setText(f"{result[7]} in")
                    
                    # Load medical records
                    db.cursor.execute("""
                        SELECT 
                            DATE_FORMAT(date, '%d/%m/%Y') as date,
                            type,
                            veterinarian,
                            CASE
                                WHEN type = 'Consultation' THEN CONCAT('Diagnosis: ', diagnosis, '\nPrescribed: ', prescribed_treatment)
                                WHEN type = 'Deworming' THEN CONCAT('Medication: ', medication, '\nDosage: ', dosage)
                                WHEN type = 'Vaccination' THEN CONCAT('Vaccine: ', vaccine, '\nDosage: ', dosage)
                                WHEN type = 'Surgery' THEN CONCAT('Type: ', surgery_type, '\nAnesthesia: ', anesthesia)
                                WHEN type = 'Grooming' THEN CONCAT('Services: ', services, '\nNotes: ', notes)
                                WHEN type = 'Other Treatment' THEN CONCAT('Treatment Type: ', treatment_type, '\nMedication: ', medication, '\nDosage: ', dosage)
                            END as remarks,
                            CASE
                                WHEN type = 'Consultation' THEN NULL
                                WHEN type = 'Deworming' THEN DATE_FORMAT(next_scheduled, '%d/%m/%Y')
                                WHEN type = 'Vaccination' THEN DATE_FORMAT(next_scheduled, '%d/%m/%Y')
                                WHEN type = 'Surgery' THEN DATE_FORMAT(next_followup, '%d/%m/%Y')
                                WHEN type = 'Grooming' THEN DATE_FORMAT(next_scheduled, '%d/%m/%Y')
                                WHEN type = 'Other Treatment' THEN NULL
                            END as next_due_date
                        FROM (
                            SELECT date, 'Consultation' as type, veterinarian, diagnosis, prescribed_treatment, NULL as medication, NULL as dosage, NULL as vaccine, NULL as surgery_type, NULL as anesthesia, NULL as services, NULL as notes, NULL as treatment_type, NULL as next_scheduled, NULL as next_followup
                            FROM consultations
                            WHERE pet_id = (SELECT pet_id FROM pets WHERE name = ?)
                            UNION ALL
                            SELECT date, 'Deworming' as type, veterinarian, NULL as diagnosis, NULL as prescribed_treatment, medication, dosage, NULL as vaccine, NULL as surgery_type, NULL as anesthesia, NULL as services, NULL as notes, NULL as treatment_type, next_scheduled, NULL as next_followup
                            FROM deworming
                            WHERE pet_id = (SELECT pet_id FROM pets WHERE name = ?)
                            UNION ALL
                            SELECT date, 'Vaccination' as type, veterinarian, NULL as diagnosis, NULL as prescribed_treatment, NULL as medication, dosage, vaccine, NULL as surgery_type, NULL as anesthesia, NULL as services, NULL as notes, NULL as treatment_type, next_scheduled, NULL as next_followup
                            FROM vaccinations
                            WHERE pet_id = (SELECT pet_id FROM pets WHERE name = ?)
                            UNION ALL
                            SELECT date, 'Surgery' as type, veterinarian, NULL as diagnosis, NULL as prescribed_treatment, NULL as medication, NULL as dosage, NULL as vaccine, surgery_type, anesthesia, NULL as services, NULL as notes, NULL as treatment_type, NULL as next_scheduled, next_followup
                            FROM surgeries
                            WHERE pet_id = (SELECT pet_id FROM pets WHERE name = ?)
                            UNION ALL
                            SELECT date, 'Grooming' as type, veterinarian, NULL as diagnosis, NULL as prescribed_treatment, NULL as medication, NULL as dosage, NULL as vaccine, NULL as surgery_type, NULL as anesthesia, services, notes, NULL as treatment_type, next_scheduled, NULL as next_followup
                            FROM grooming
                            WHERE pet_id = (SELECT pet_id FROM pets WHERE name = ?)
                            UNION ALL
                            SELECT date, 'Other Treatment' as type, veterinarian, NULL as diagnosis, NULL as prescribed_treatment, medication, dosage, NULL as vaccine, NULL as surgery_type, NULL as anesthesia, NULL as services, NULL as notes, treatment_type, NULL as next_scheduled, NULL as next_followup
                            FROM other_treatments
                            WHERE pet_id = (SELECT pet_id FROM pets WHERE name = ?)
                        ) AS combined_records
                        ORDER BY date DESC
                    """, (self.selected_pet_name,) * 6)
                    
                    records = db.cursor.fetchall()
                    records_table.setRowCount(0)
                    
                    for row, record in enumerate(records):
                        records_table.insertRow(row)
                        for col, value in enumerate(record):
                            item = QTableWidgetItem(str(value) if value else "")
                            # Center align all columns except remarks (col 3)
                            if col == 3:  # Remarks column
                                item.setTextAlignment(Qt.AlignTop | Qt.AlignLeft)  # Left align for remarks
                                # Calculate the height needed based on content
                                text = str(value) if value else ""
                                lines = text.count('\n') + 1
                                height = max(25, lines * 20)  # Minimum height of 25, 20 pixels per line
                                records_table.setRowHeight(row, height)
                            else:  # All other columns
                                item.setTextAlignment(Qt.AlignCenter)  # Center align for other columns
                            records_table.setItem(row, col, item)
                    
                    # Load past illnesses and medical history notes
                    self.past_illnesses_text.clear()
                    self.medical_history_text.clear()
                    
                    # Load medical history notes
                    db.cursor.execute("""
                        SELECT notes 
                        FROM pet_notes 
                        WHERE pet_id = (SELECT pet_id FROM pets WHERE name = ?)
                        AND note_type = 'medical_history'
                    """, (self.selected_pet_name,))
                    result = db.cursor.fetchone()
                    if result and result[0]:
                        self.medical_history_text.setPlainText(result[0])
                    
                    # Load past illnesses notes
                    db.cursor.execute("""
                        SELECT notes 
                        FROM pet_notes 
                        WHERE pet_id = (SELECT pet_id FROM pets WHERE name = ?)
                        AND note_type = 'past_illnesses'
                    """, (self.selected_pet_name,))
                    result = db.cursor.fetchone()
                    if result and result[0]:
                        self.past_illnesses_text.setPlainText(result[0])
            
        except Exception as e:
            print(f"Error loading pet records: {e}")
        finally:
            db.close_connection()

    def position_side_buttons(self, buttons_widget, parent_widget):
        """Position the side buttons at the right edge of the parent widget"""
        buttons_widget.move(parent_widget.width() - buttons_widget.width(), 220)

    #REPORTS TAB
    def show_report_content(self):
        self.clear_content()
        self.add_search_bar()
        report_widget = get_report_widget(self.user_role)
        self.content_layout.addWidget(report_widget)
        
        # Connect the search bar to the report filtering function
        if hasattr(report_widget, 'filter_tables'):
            self.search_bar.textChanged.connect(report_widget.filter_tables)
    
    # -- APPOINTMENT TAB -- #   
    def show_appointments_content(self):
        self.clear_content()
        self.add_search_bar()
        appointment_widget = get_appointment_widget(self.user_role)
        self.content_layout.addWidget(appointment_widget)
        
        # Connect the search bar to the appointments filtering function
        if hasattr(appointment_widget, 'filter_appointments'):
            self.search_bar.textChanged.connect(appointment_widget.filter_appointments)
            
    # -- Billings Tab -- #
    def show_billings_content(self):
        self.clear_content()
        self.add_search_bar()
        get_billing_widget = update_billing_widget(self.user_role)
        billing_widget = get_billing_widget(self.user_role)
        self.content_layout.addWidget(billing_widget)
        
        # Connect the search bar to the billings filtering function
        if hasattr(billing_widget, 'filter_billings'):
            self.search_bar.textChanged.connect(billing_widget.filter_billings)
    
    # -- Settings Tab -- #
    def show_settings_content(self):
        self.clear_content()
        # Uncheck all navigation buttons when entering settings
        for btn in self.nav_buttons:
            btn.setChecked(False)
            btn.setStyleSheet("")
        settings_widget = get_setting_widget(user_id=self.user_id)
        self.content_layout.addWidget(settings_widget)
    
    def show_user_menu(self, event):
        """Show the user menu when clicking the user icon."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px 8px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #f0f0f0;
            }
        """)

        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(self.show_settings_content)
        logout_action = menu.addAction("Logout")
        logout_action.triggered.connect(self.logout)

        # Show menu at the bottom of the user icon
        menu.exec_(self.dropdown_icon.mapToGlobal(
            self.dropdown_icon.rect().bottomLeft()
        ))

    def logout(self):
        """Handle logout action."""
        from modules.login import LoginWindow
        self.close()  # Close current window
        self.login_window = LoginWindow()  # Create new login window
        self.login_window.showMaximized()  # Show login window in full screen

    def toggle_edit_mode(self):
        """Toggle between edit and save modes for the tables."""
        self.is_edit_mode = not self.is_edit_mode
        
        if self.is_edit_mode:
            # Switch to edit mode
            self.edit_btn.setText("Save")
            self.edit_btn.setIcon(QIcon("assets/save.png"))  # Change to save icon
            self.edit_btn.setStyleSheet("""
                QToolButton {
                    background-color: rgba(254, 215, 102, 0.50);
                    color: #000;
                    padding: 5px;
                    font-weight: bold;
                    font-size: 11px;
                    text-align: center;
                    border-radius: 5px;
                    font-family: Lato;
                }
                QToolButton:hover {
                    background-color: #218838;
                }
            """)
            
            # Enable editing only for text areas
            self.past_illnesses_text.setReadOnly(False)
            self.medical_history_text.setReadOnly(False)
            
        else:
            # Switch to save mode
            self.edit_btn.setText("Edit")
            self.edit_btn.setIcon(QIcon("assets/edit.png"))  # Change back to edit icon
            self.edit_btn.setStyleSheet("""
                QToolButton {
                    background-color: rgba(0, 159, 183, 0.30);
                    color: #000;
                    padding: 5px;
                    font-weight: bold;
                    font-size: 11px;
                    text-align: center;
                    border-radius: 5px;
                    font-family: Lato;
                }
                QToolButton:hover {
                    background-color: #008ba0;
                }
            """)
            
            # Disable editing for text areas
            self.past_illnesses_text.setReadOnly(True)
            self.medical_history_text.setReadOnly(True)
            
            # Save changes to database
            self.save_table_changes()

    def save_table_changes(self):
        """Save changes made to the tables back to the database."""
        try:
            db = Database()
            
            # Save medical history notes
            medical_history_notes = self.medical_history_text.toPlainText()
            db.cursor.execute("""
                INSERT INTO pet_notes (pet_id, note_type, notes)
                VALUES ((SELECT pet_id FROM pets WHERE name = ?), 'medical_history', ?)
                ON DUPLICATE KEY UPDATE 
                    notes = VALUES(notes),
                    last_updated = CURRENT_TIMESTAMP
            """, (self.selected_pet_name, medical_history_notes))
            
            # Save past illnesses notes
            past_illnesses_notes = self.past_illnesses_text.toPlainText()
            db.cursor.execute("""
                INSERT INTO pet_notes (pet_id, note_type, notes)
                VALUES ((SELECT pet_id FROM pets WHERE name = ?), 'past_illnesses', ?)
                ON DUPLICATE KEY UPDATE 
                    notes = VALUES(notes),
                    last_updated = CURRENT_TIMESTAMP
            """, (self.selected_pet_name, past_illnesses_notes))
                    
            db.conn.commit()
            print("✅ Changes saved successfully")
            
        except Exception as e:
            print(f"❌ Error saving changes: {e}")
        finally:
            db.close_connection()

if __name__ == "__main__":
        from PySide6.QtWidgets import QApplication
        import sys

        app = QApplication([])

        window = PetMedix()
        window.showMaximized()
        app.exec()
 