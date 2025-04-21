from PySide6.QtWidgets import QWidget, QTextEdit, QLabel, QHeaderView, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, QScrollBar, QSizePolicy
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer
from modules.home import get_home_widget
from modules.client import get_client_widget
from modules.report import get_report_widget
from modules.appointment import get_appointment_widget
from modules.billing import update_billing_widget
from modules.setting import get_setting_widget

class PetMedix(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PetMedix - Home")

        # Apply styles from external QSS file
        with open("styles/login.qss", "r") as file:
            self.setStyleSheet(file.read())

        # Main layout (vertical layout for header and body)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create the header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header.setObjectName("Header")
        header_layout.setContentsMargins(50, 15, 50, 15)  # Padding

        # Logo on the left
        self.logo_label = QLabel()
        pixmap = QPixmap("assets/petmedix.png")  # Path to your PetMedix logo
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setFixedHeight(50)  # Adjust if needed
        self.logo_label.setScaledContents(True)

        # Username label
        self.username_label = QLabel("Hello, Dr. Smith")
        self.username_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.username_label.setObjectName("UsernameLabel")

        # User icon
        self.user_icon_label = QLabel()
        user_pixmap = QPixmap("assets/userlogo.png")  # 👉 Path to your user icon
        self.user_icon_label.setPixmap(user_pixmap)
        self.user_icon_label.setFixedSize(40, 40)
        self.user_icon_label.setScaledContents(True)

        # Mini layout for username + user icon
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.username_label)
        user_layout.addWidget(self.user_icon_label)
        user_layout.setSpacing(8)

        user_widget = QWidget()
        user_widget.setLayout(user_layout)

        # Add to the header layout
        header_layout.addWidget(self.logo_label, alignment=Qt.AlignLeft)
        header_layout.addStretch()
        header_layout.addWidget(user_widget, alignment=Qt.AlignRight)

        # Add header to the main layout
        main_layout.addWidget(header)

        # Create the body layout (horizontal layout with navbar on the left and content on the right)
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        # Create the left navigation bar (narrow)
        navbar = QWidget()
        navbar_layout = QVBoxLayout(navbar)
        navbar.setObjectName("NavBar")
        navbar_layout.setContentsMargins(10, 10, 10, 10)  # Padding for the navbar
        navbar_layout.setSpacing(10)

        navbar_logo = QLabel()
        navbar_logo_pixmap = QPixmap("assets/logo.png")  # Path to your navigation logo
        navbar_logo.setPixmap(navbar_logo_pixmap)
        navbar_logo.setObjectName("Navbarlogo")
        navbar_logo.setFixedHeight(240)
        navbar_logo.setAlignment(Qt.AlignCenter)
        navbar_logo.setScaledContents(True)

        # Add navbar logo to the navbar layout
        navbar_layout.addWidget(navbar_logo)

        clinic_name_label = QLabel("PetMedix<br> Animal Clinic")
        clinic_name_label.setAlignment(Qt.AlignCenter)
        clinic_name_label.setObjectName("ClinicNameLabel")
        navbar_layout.addWidget(clinic_name_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)  # Set the shape of the frame to a horizontal line
        line.setFrameShadow(QFrame.Sunken)  # Make the line appear sunken (optional)
        navbar_layout.addWidget(line)

        self.button1 = QPushButton("Home")
        self.button2 = QPushButton("Client")
        self.button3 = QPushButton("Reports")
        self.button4 = QPushButton("Appointments")
        self.button5 = QPushButton("Billings")
        self.button6 = QPushButton("Settings")

        navbar_layout.addWidget(self.button1)
        navbar_layout.addWidget(self.button2)
        navbar_layout.addWidget(self.button3)
        navbar_layout.addWidget(self.button4)
        navbar_layout.addWidget(self.button5)
        navbar_layout.addWidget(self.button6)

        self.button1.setFlat(True)
        self.button2.setFlat(True)
        self.button3.setFlat(True)
        self.button4.setFlat(True)
        self.button5.setFlat(True)
        self.button6.setFlat(True)

        # Add a stretch to move the buttons to the top
        navbar_layout.addStretch()  # This ensures the buttons are at the top

        # Set fixed width for the navbar (narrow width, e.g., 150px)
        navbar.setFixedWidth(260)

        # Add the navbar to the left side of the body layout
        body_layout.addWidget(navbar)

        # Create the right content area (takes the remaining space)
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area.setStyleSheet("background-color: #fff;")  # Optional: background color for content area

        # Add content area to the right side of the body layout
        body_layout.addWidget(self.content_area)

        # Add the body layout (navbar + content) to the main layout
        main_layout.addLayout(body_layout)

        # Set the main layout for the window
        self.setLayout(main_layout)

        # Connect buttons to content change functions
        self.button1.clicked.connect(self.show_home_content)
        self.button2.clicked.connect(self.show_client_content)
        self.button3.clicked.connect(self.show_report_content)
        self.button4.clicked.connect(self.show_appointments_content)
        self.button5.clicked.connect(self.show_billings_content)
        self.button6.clicked.connect(self.show_settings_content)
        
        self.show_home_content()

    def clear_content(self):
        if self.content_layout is not None:
            while self.content_layout.count():
                item = self.content_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
                
    def add_search_bar(self):
        search_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setFixedHeight(100)
        self.search_bar.setObjectName("SearchBar")
        self.search_bar.setFixedWidth(1000)

        search_layout.addWidget(self.search_bar)
        self.content_layout.addLayout(search_layout)

    def show_home_content(self):
        self.clear_content()
        self.add_search_bar()
        home_widget = get_home_widget()
        self.content_layout.addWidget(home_widget)
    
    #CLIENT TAB
    def show_client_content(self):
        self.clear_content()
        self.add_search_bar()
        client_widget = get_client_widget(self)
        self.content_layout.addWidget(client_widget)
        
    def show_pet_records(self):
        self.clear_content()  
        self.add_search_bar()

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
            font-size: 16px; 
            font-weight: bold;
            padding-left: 10px;
        """)
        see_record.setFixedHeight(40)
        see_record.setAlignment(Qt.AlignVCenter)

        pet_medical = QLabel("Pet Medical Record")
        pet_medical.setObjectName("PetMedical")
        pet_medical.setStyleSheet("""
            background-color: #FED766; 
            color: #012547; 
            font-size: 16px; 
            font-weight: bold;
            padding-left: 10px;
        """)
        pet_medical.setFixedHeight(40)
        pet_medical.setAlignment(Qt.AlignVCenter)

        # Add top labels to the main layout
        main_layout.addWidget(see_record)
        main_layout.addWidget(pet_medical)

        # Main content area with patient record and tables
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 10, 60, 10)
        content_layout.setSpacing(10)

        # Left side - Patient info
        left_panel = QWidget()
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
                font-family: Arial;
                font-size: 13px;
                font-weight: bold;
                padding-left: 5px;
                color: #012547;
            """)
            header.setAlignment(Qt.AlignVCenter)
            section_layout.addWidget(header)
            
            return section, section_layout

        # Create sections
        vet_section, vet_layout = create_info_section("VETERINARY CLINIC")
        pet_section, pet_layout = create_info_section("PET INFORMATION")
        owner_section, owner_layout = create_info_section("OWNER INFORMATION")
        notes_section, notes_layout = create_info_section("NOTES")

        # Create form fields
        def create_form_fields(layout, fields):
            form_widget = QWidget()
            form_layout = QVBoxLayout(form_widget)
            form_layout.setContentsMargins(5, 5, 5, 5)
            form_layout.setSpacing(3)  # Reduced spacing between fields
            
            for field in fields:
                field_layout = QVBoxLayout()
                field_layout.setSpacing(0)
                
                label = QLabel(field + ":")
                label.setStyleSheet("""
                    font-family: Arial;
                    font-size: 11px;
                    color: #333;
                    margin: 0;
                    padding: 0;
                """)
                
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                line.setStyleSheet("background-color: #333;")
                line.setFixedHeight(1)  # Thinner line
                
                field_layout.addWidget(label)
                field_layout.addWidget(line)
                form_layout.addLayout(field_layout)
            
            layout.addWidget(form_widget)
            return form_widget
        
        # Add fields to each section
        vet_fields = ["CLINIC", "ADDRESS", "CONTACT NUMBER", "EMAIL ADDRESS"]
        create_form_fields(vet_layout, vet_fields)
        
        pet_fields = ["NAME", "AGE", "GENDER", "SPECIES", "BREED", "COLOR", "WEIGHT", "HEIGHT", "BLOOD TYPE"]
        create_form_fields(pet_layout, pet_fields)
        
        owner_fields = ["NAME", "ADDRESS", "CONTACT NUMBER", "EMAIL ADDRESS"]
        create_form_fields(owner_layout, owner_fields)
        
        # Notes section
        notes_widget = QTextEdit()
        notes_widget.setStyleSheet("""
            background-color: white;
            border: none;
            font-family: Arial;
            font-size: 11px;
        """)
        notes_widget.setFixedHeight(80)  # Reduced height
        notes_layout.addWidget(notes_widget)
        
        # Add all sections to left panel
        left_layout.addWidget(vet_section)
        left_layout.addSpacing(3)  # Reduced spacing
        left_layout.addWidget(pet_section)
        left_layout.addSpacing(3)  # Reduced spacing
        left_layout.addWidget(owner_section)
        left_layout.addSpacing(3)  # Reduced spacing
        left_layout.addWidget(notes_section)
        left_layout.addStretch()

        # Right side - Medical data & records
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 0, 10, 0)
        right_layout.setSpacing(10)
        
        # Medical history tables (top row)
        medical_tables = QWidget()
        medical_tables_layout = QHBoxLayout(medical_tables)
        medical_tables_layout.setContentsMargins(0, 0, 0, 0)
        medical_tables_layout.setSpacing(10)
        
        # Past illnesses table
        past_illnesses = QWidget()
        past_illnesses.setStyleSheet("background-color: #eef8f9; border: 1px solid #d5d5d5;")
        past_illnesses_layout = QVBoxLayout(past_illnesses)
        past_illnesses_layout.setContentsMargins(5, 5, 5, 5)
        
        past_illnesses_header = QLabel("PAST ILLNESSES")
        past_illnesses_header.setAlignment(Qt.AlignCenter)
        past_illnesses_header.setStyleSheet("font-weight: bold; background-color: #eef8f9; font-size: 12px;")
        past_illnesses_layout.addWidget(past_illnesses_header)
        
        past_illnesses_content = QTextEdit()
        past_illnesses_content.setPlaceholderText("No past illnesses recorded")
        past_illnesses_content.setStyleSheet("border: none; background-color: white; font-size: 11px;")
        past_illnesses_content.setFixedHeight(120)  # Reduced height
        past_illnesses_layout.addWidget(past_illnesses_content)
        
        # Medical history table
        medical_history = QWidget()
        medical_history.setStyleSheet("background-color: #eef8f9; border: 1px solid #d5d5d5;")
        medical_history_layout = QVBoxLayout(medical_history)
        medical_history_layout.setContentsMargins(5, 5, 5, 5)
        
        medical_history_header = QLabel("MEDICAL HISTORY")
        medical_history_header.setAlignment(Qt.AlignCenter)
        medical_history_header.setStyleSheet("font-weight: bold; background-color: #eef8f9; font-size: 12px;")
        medical_history_layout.addWidget(medical_history_header)
        
        medical_history_content = QTextEdit()
        medical_history_content.setPlaceholderText("No medical history available")
        medical_history_content.setStyleSheet("border: none; background-color: white; font-size: 11px;")
        medical_history_content.setFixedHeight(120)  # Reduced height
        medical_history_layout.addWidget(medical_history_content)
        
        # Add tables to layout
        medical_tables_layout.addWidget(past_illnesses)
        medical_tables_layout.addWidget(medical_history)
        
        # Records section
        records_section = QWidget()
        records_layout = QVBoxLayout(records_section)
        records_layout.setContentsMargins(0, 0, 0, 0)
        
        records_header = QLabel("RECORDS")
        records_header.setAlignment(Qt.AlignCenter)
        records_header.setStyleSheet("font-weight: bold; background-color: #eef8f9; padding: 5px; font-size: 12px;")
        records_layout.addWidget(records_header)
        
        # Records table
        records_table = QTableWidget()
        records_table.setColumnCount(5)
        records_table.setHorizontalHeaderLabels([
            "DATE", "TYPE OF RECORD", "VETERINARIAN/STAFF IN CHARGE", "REMARKS", "NEXT DUE DATE\n(if applicable)"
        ])
        records_table.horizontalHeader().setStyleSheet("background-color: #eef8f9; font-size: 11px;")
        records_table.setStyleSheet("gridline-color: #d5d5d5; font-size: 11px;")
        
        # Set column widths
        header = records_table.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        records_table.setFixedHeight(160)  # Reduced height
        records_layout.addWidget(records_table)
        
        # Add to right layout
        right_layout.addWidget(medical_tables)
        right_layout.addWidget(records_section)
        right_layout.addStretch()

        # Action buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(10, 5, 10, 5)
        
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                color: white;
                border-radius: 5px;
                padding: 6px 15px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #023e70;
            }
        """)
        back_btn.setFixedSize(90, 30)
        
        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        
        # Add panels to content layout
        content_layout.addWidget(left_panel, 1)  # Give some stretch to left panel
        content_layout.addWidget(right_panel, 2)  # Give more stretch to right panel
        
        # Main layout assembly
        main_layout.addWidget(content_widget)
        main_layout.addWidget(button_widget)
        
        # Set the layout for the records space
        records_space.setLayout(main_layout)
        self.content_layout.addWidget(records_space)
        
        # EDIT AND DOWNLOAD BUTTONS - Fixed approach for PySide6
        # Create buttons directly on the parent widget instead of a separate container
        edit_btn = QPushButton(records_space)
        edit_btn.setToolTip("Edit")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #9FE7EF;
                border: none;
                padding: 5px;
                min-width: 40px;
                min-height: 40px;
            }
        """)
        # Use setText with an icon character if icons aren't loading
        edit_btn.setText("✏️")  # Unicode edit icon as fallback
        
        download_btn = QPushButton(records_space)
        download_btn.setToolTip("Download")
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #F89794;
                border: none;
                padding: 5px;
                min-width: 40px;
                min-height: 40px;
            }
        """)
        # Use setText with an icon character if icons aren't loading
        download_btn.setText("⬇️")  # Unicode download icon as fallback
        
        # Set fixed size for buttons
        edit_btn.setFixedSize(40, 40)
        download_btn.setFixedSize(40, 40)
        
        # Position the buttons
        def position_buttons():
            # Get the position relative to the parent widget
            x_position = records_space.width() - 45  # 5px from right edge
            edit_btn.move(x_position, 220)
            download_btn.move(x_position, 260)  # Below edit button
        
        # Use QTimer to position buttons after layout is set
        QTimer.singleShot(100, position_buttons)

    def position_side_buttons(self, buttons_widget, parent_widget):
        """Position the side buttons at the right edge of the parent widget"""
        buttons_widget.move(parent_widget.width() - buttons_widget.width(), 220)

    #REPORTS TAB
    def show_report_content(self):
        self.clear_content()
        self.add_search_bar()
        report_widget = get_report_widget()
        self.content_layout.addWidget(report_widget)
    
    # -- APPOINTMENT TAB -- #   
    def show_appointments_content(self):
        self.clear_content()
        self.add_search_bar()
        appointment_widget = get_appointment_widget()
        self.content_layout.addWidget(appointment_widget)
            
    # -- Billings Tab -- #
    def show_billings_content(self):
        self.clear_content()
        self.add_search_bar()
        get_billing_widget = update_billing_widget()
        billing_widget = get_billing_widget()
        self.content_layout.addWidget(billing_widget)
    
    # -- Settings Tab -- #
    def show_settings_content(self):
        self.clear_content()
        settings_widget = get_setting_widget()
        self.content_layout.addWidget(settings_widget)
        
if __name__ == "__main__":
        from PySide6.QtWidgets import QApplication
        import sys

        app = QApplication([])

        window = PetMedix()
        window.showMaximized()
        app.exec()
 