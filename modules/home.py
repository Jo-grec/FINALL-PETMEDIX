from PySide6.QtWidgets import QWidget, QTextEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, QScrollBar, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize

class HomePage(QWidget):
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

        # Example navigation buttons
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
        self.button3.clicked.connect(self.show_reports_content)
        self.button4.clicked.connect(self.show_appointments_content)
        self.button5.clicked.connect(self.show_billings_content)
        self.button6.clicked.connect(self.show_settings_content)

    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
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

        # Create horizontal layout for the 3 boxes
        boxes_layout = QHBoxLayout()

        # Box 1
        box1 = QWidget()
        box1.setStyleSheet("background-color: #012547;")  # Example style for box
        box1.setFixedWidth(300)
        box1.setFixedHeight(150)
        box1.setObjectName("Box1")

        icon_label = QLabel(box1)
        icon_label.setObjectName("IconLabel")  # Set object name for the icon
        pixmap = QPixmap("assets/client.png")  # Path to your box image
        icon_label.setPixmap(pixmap)
        icon_label.setFixedWidth(100)
        icon_label.setScaledContents(True)
        icon_label.setAlignment(Qt.AlignCenter)

        number_label = QLabel("10", box1)
        number_label.setObjectName("NumberLabel")
        number_label.setAlignment(Qt.AlignCenter)

        clients_label = QLabel("clients", box1)
        clients_label.setObjectName("ClientsLabel")
        clients_label.setAlignment(Qt.AlignCenter)
        clients_label.setStyleSheet("color: white; font-size: 14px;")

        icon_and_number_layout = QHBoxLayout()
        icon_and_number_layout.addWidget(icon_label)
        icon_and_number_layout.addWidget(number_label)
        icon_and_number_layout.setAlignment(Qt.AlignCenter)

        box1_layout = QVBoxLayout(box1)
        box1_layout.addLayout(icon_and_number_layout)
        box1_layout.addWidget(clients_label)
        box1_layout.setAlignment(Qt.AlignCenter)

        boxes_layout.addWidget(box1)

        # Box 2
        box2 = QWidget()
        box2.setStyleSheet("background-color: #012547;")  # Example style for box
        box2.setFixedWidth(300)
        box2.setFixedHeight(150)
        box2.setObjectName("Box2")

        # Create a QLabel to hold the image (icon) for box2
        icon_label2 = QLabel(box2)
        icon_label2.setObjectName("IconLabel2")  # Set object name for the icon
        pixmap2 = QPixmap("assets/medical.png")  # Path to your second box image
        icon_label2.setPixmap(pixmap2)

        # Adjust the width of the icon
        icon_label2.setFixedWidth(100)  # Set the desired width for the icon
        icon_label2.setScaledContents(True)  # Ensures the image scales with the widget size
        icon_label2.setAlignment(Qt.AlignCenter)

        # Create a QLabel for the number for box2
        number_label2 = QLabel("30", box2)
        number_label2.setObjectName("NumberLabel2")  # Set object name for the number
        number_label2.setAlignment(Qt.AlignCenter)  # Keep the number centered

        # Create a QLabel for the text "Medical Records"
        medical_label = QLabel("medical records", box2)
        medical_label.setObjectName("MedicalLabel")  # Set object name for the text
        medical_label.setAlignment(Qt.AlignCenter)  # Keep the "Medical Records" text centered
        medical_label.setStyleSheet("color: white; font-size: 14px;")  # Optional styling for "Medical Records" text

        # Create a horizontal layout to align the icon and number for box2
        icon_and_number_layout2 = QHBoxLayout()
        icon_and_number_layout2.addWidget(icon_label2)
        icon_and_number_layout2.addWidget(number_label2)
        icon_and_number_layout2.setAlignment(Qt.AlignCenter)  # Keep icon and number aligned as before

        # Create a vertical layout for the icon, number, and medical label
        box2_layout = QVBoxLayout(box2)
        box2_layout.addLayout(icon_and_number_layout2)  # Add icon and number layout
        box2_layout.addWidget(medical_label)  # Add the "Medical Records" text below the number
        box2_layout.setAlignment(Qt.AlignCenter)  # Align everything to the center

        # Add the second box to the layout
        boxes_layout.addWidget(box2)

        # Box 3
        box3 = QWidget()
        box3.setStyleSheet("background-color: #012547;")  # Example style for box
        box3.setFixedWidth(300)
        box3.setFixedHeight(150)
        box3.setObjectName("Box3")

        # Create a QLabel to hold the image (icon) for box2
        icon_label3 = QLabel(box3)
        icon_label3.setObjectName("IconLabel3")  # Set object name for the icon
        pixmap3 = QPixmap("assets/appoint.png")  # Path to your second box image
        icon_label3.setPixmap(pixmap3)

        # Adjust the width of the icon
        icon_label3.setFixedWidth(100)  # Set the desired width for the icon
        icon_label3.setScaledContents(True)  # Ensures the image scales with the widget size
        icon_label3.setAlignment(Qt.AlignCenter)

        # Create a QLabel for the number for box2
        number_label3 = QLabel("5", box3)
        number_label3.setObjectName("NumberLabel3")  # Set object name for the number
        number_label3.setAlignment(Qt.AlignCenter)  # Keep the number centered

        # Create a QLabel for the text "Appointments"
        appointments_label = QLabel("appointments", box3)
        appointments_label.setObjectName("AppointmentsLabel")  # Set object name for the text
        appointments_label.setAlignment(Qt.AlignCenter)  # Keep the "Appointments" text centered
        appointments_label.setStyleSheet("color: white; font-size: 14px;")  # Optional styling for "Appointments" text

        # Create a horizontal layout to align the icon and number for box2
        icon_and_number_layout3 = QHBoxLayout()
        icon_and_number_layout3.addWidget(icon_label3)
        icon_and_number_layout3.addWidget(number_label3)
        icon_and_number_layout3.setAlignment(Qt.AlignCenter)  # Keep icon and number aligned as before

        # Create a vertical layout for the icon, number, and appointments label
        box3_layout = QVBoxLayout(box3)
        box3_layout.addLayout(icon_and_number_layout3)  # Add icon and number layout
        box3_layout.addWidget(appointments_label)  # Add the "Appointments" text below the number
        box3_layout.setAlignment(Qt.AlignCenter)  # Align everything to the center

        # Add the third box to the layout
        boxes_layout.addWidget(box3)

        # Add boxes layout to the content layout
        self.content_layout.addLayout(boxes_layout)

            # Create the text label "Recent Reports" and align it with the first box
        recent_reports_label = QLabel("Recent Reports")
        recent_reports_label.setMaximumHeight(80)  # Set a maximum height for the label
        recent_reports_label.setStyleSheet("background-color: #012547;")  # Set background color
        recent_reports_label.setAlignment(Qt.AlignLeft)  # Align to the left
        recent_reports_label.setObjectName("RecentReportsLabel")

        # Add the label below the boxes, aligned with the first box
        self.content_layout.addWidget(recent_reports_label)

        # Create the table for Consultation Data
        table_widget = QTableWidget(20, 4)
        table_widget.setObjectName("ConsultationTable")        
        table_widget.setHorizontalHeaderLabels(["Consultation Date", "Pet", "Owner/Client", "Veterinarian/Staff in Charge"])
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
            
        header = table_widget.horizontalHeader()
        header.setStyleSheet("""
                background-color: #012547;
                font-family: Poppins;
                color: #fff;
                font-weight: bold;
                font-size: 16px;
                font-style: normal;
                line-height: 20px;
            """)
            
            # Column widths
        table_widget.setColumnWidth(0, 312)
        table_widget.setColumnWidth(1, 312)
        table_widget.setColumnWidth(2, 312)
        table_widget.setColumnWidth(3, 312)

        # 🛠️ Hide vertical header (row numbers)
        table_widget.verticalHeader().setVisible(False)

        # 🛠️ Disable the visible scrollbars but keep scrolling functionality
        table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # 🛠️ Allow scrolling with mouse wheel
        table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        table_widget.setShowGrid(True)  # Optional: hide cell grid lines
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Optional: make it read-only
        table_widget.setFocusPolicy(Qt.NoFocus)  # Optional: remove ugly blue selection rectangle

        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        table_widget.setFixedHeight(300)

        table_container = QWidget()
        table_container_layout = QHBoxLayout(table_container)
        table_container_layout.setContentsMargins(0, 0, 0, 0)
        table_container_layout.addWidget(table_widget)

        self.content_layout.addWidget(table_container)
    
    #CLIENT TAB

    def show_client_content(self):
        self.clear_content()
        self.add_search_bar()

        client_space = QWidget()
        client_space.setMaximumHeight(600)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 30)

        # --- Client List Label ---
        client_list = QLabel("Client List")
        client_list.setObjectName("ClientList")
        client_list.setStyleSheet("background-color: #102547;")
        layout.addWidget(client_list)

        # --- Table and Client Info Layout ---
        table_info_layout = QHBoxLayout()
        table_info_layout.setContentsMargins(0, 0, 0, 0)
        table_info_layout.setSpacing(0)

        # --- Client Table ---
        table = QTableWidget()
        table.setColumnCount(1)
        table.setRowCount(16)
        table.setFixedWidth(250)
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.horizontalHeader().setVisible(False)
        table.setStyleSheet("background-color: white; color: black;")
        table_info_layout.addWidget(table)

        # --- Client Information Layout ---
        client_info_layout = QVBoxLayout()
        client_info_layout.setContentsMargins(0, 0, 0, 0)
        client_info_layout.setSpacing(10)

        # Client Information Label
        client_info_label_layout = QHBoxLayout()
        client_info_label = QLabel("CLIENT INFORMATION")
        client_info_label.setObjectName("ClientInformationLabel")
        client_info_label.setStyleSheet("background-color: #FED766;")
        client_info_label.setFixedHeight(50)
        client_info_layout.addWidget(client_info_label)

        # Client Information Fields
        labels = ["Name:", "Gender:", "Address:", "Contact Number:", "Email Address:"]
        object_names = ["NameLabel", "GenderLabel", "AddressLabel", "ContactLabel", "EmailLabel"]
        
        for text, obj_name in zip(labels, object_names):
            label = QLabel(text)
            label.setObjectName(obj_name)
            client_info_layout.addWidget(label)

        # --- PETS Section ---
        pet_info_label = QLabel("PETS")
        pet_info_label.setObjectName("PetsLabel")
        pet_info_label.setStyleSheet("background-color: #FED766;")
        pet_info_label.setFixedHeight(50)
        client_info_layout.addWidget(pet_info_label)

        pet_info_section = QHBoxLayout()

        # Pet Picture
        pet_picture = QLabel()
        pet_picture.setFixedSize(250, 150)
        pet_picture.setStyleSheet("background-color: gray;")
        pet_picture.setObjectName("PetPicture")
        pet_picture.setAlignment(Qt.AlignCenter)
        pet_info_section.addWidget(pet_picture)

        # Pet Details
        pet_details_layout = QVBoxLayout()
        pet_labels = ["Name:", "Gender:", "Pet Type:", "Breed:", "Color:", "Birthdate:", "Age:"]
        pet_object_names = [
            "PetNameLabel", "PetGenderLabel", "PetTypeLabel",
            "PetBreedLabel", "PetColorLabel", "PetBirthLabel", "PetAgeLabel"
        ]

        for text, obj_name in zip(pet_labels, pet_object_names):
            label = QLabel(text)
            label.setObjectName(obj_name)
            pet_details_layout.addWidget(label)

        pet_details_layout.setSpacing(0)
        pet_info_section.addLayout(pet_details_layout)

        # Pet Buttons
        pet_buttons_layout = QVBoxLayout()
        update_info_button = QPushButton("Update Info")
        check_schedule_button = QPushButton("Check Schedule")
        see_records_button = QPushButton("See Records")

        pet_buttons = [
            (update_info_button, "UpdateInfoButton"),
            (check_schedule_button, "CheckScheduleButton"),
            (see_records_button, "SeeRecordsButton")
        ]

        for button, obj_name in pet_buttons:
            button.setObjectName(obj_name)
            button.setStyleSheet("background-color: #012547; color: white;")
            button.setFixedSize(120, 40)
            pet_buttons_layout.addWidget(button)

        see_records_button.clicked.connect(self.show_pet_records)
        pet_buttons_layout.addStretch()
        pet_buttons_layout.setContentsMargins(0, 0, 120, 0)
        pet_info_section.addLayout(pet_buttons_layout)

        client_info_layout.addLayout(pet_info_section)
        client_info_layout.addStretch()

        table_info_layout.addLayout(client_info_layout)
        layout.addLayout(table_info_layout)

        # --- Previous and Next Buttons ---
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        prev_button = QPushButton("Previous")
        next_button = QPushButton("Next")
        
        prev_button.setObjectName("PreviousButton")
        next_button.setObjectName("NextButton")

        prev_button.setStyleSheet("background-color: #012547; color: white;")
        next_button.setStyleSheet("background-color: #012547; color: white;")

        button_layout.addWidget(prev_button)
        button_layout.addWidget(next_button)
        button_layout.setAlignment(Qt.AlignLeft)
        
        layout.addLayout(button_layout)

        client_space.setLayout(layout)
        self.content_layout.addWidget(client_space)
        
    def show_pet_records(self):
        self.clear_content()  
        self.add_search_bar()

        records_space = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 30)
        layout.setSpacing(0)

        see_record = QLabel("See Records")
        see_record.setObjectName("SeeRecords")
        see_record.setStyleSheet("background-color: #012547;")
        see_record.setFixedHeight(50)
        see_record.setAlignment(Qt.AlignLeft)

        pet_medical = QLabel("Pet Medical Records")
        pet_medical.setObjectName("PetMedical")
        pet_medical.setStyleSheet("background-color: #FED766;")
        pet_medical.setFixedHeight(50)
        pet_medical.setAlignment(Qt.AlignLeft)

        pet_medical_record = QLabel("PET MEDICAL<br>RECORD")
        pet_medical_record.setAlignment(Qt.AlignLeft)
        pet_medical_record.setTextFormat(Qt.RichText)
        pet_medical_record.setObjectName("PetMedicalRecord")

        veterinary_clinic = QLabel("VETERINARY CLINIC")
        veterinary_clinic.setAlignment(Qt.AlignLeft)
        veterinary_clinic.setObjectName("VeterinaryClinic")
        veterinary_clinic.setStyleSheet("background: rgba(0, 159, 183, 0.30);")
        veterinary_clinic.setFixedWidth(310)
        veterinary_clinic.setContentsMargins(0, 0, 0, 0)

        # Create a small form under 'Veterinary Clinic'
        form_widget = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(10, 0, 0, 10)
        form_layout.setAlignment(Qt.AlignLeft)

        # Define create_underlined_label function outside the form layout
        def create_underlined_label(text):
            label = QLabel(text)
            label.setAlignment(Qt.AlignLeft)
            label.setStyleSheet("""
                font-size: 10px;
                font-family: Lato;
                font-style: normal;
                font-weight: 400;
                line-height: normal;
                border-bottom: 1px solid black;
                min-width: 300px;
            """)
            return label

        form_layout.addWidget(create_underlined_label("CLINIC:"))
        form_layout.addWidget(create_underlined_label("ADDRESS:"))
        form_layout.addWidget(create_underlined_label("CONTACT NUMBER:"))
        form_layout.addWidget(create_underlined_label("EMAIL ADDRESS:"))
        form_widget.setLayout(form_layout)

        pet_information = QLabel("PET INFORMATION")
        pet_information.setAlignment(Qt.AlignLeft)
        pet_information.setObjectName("PetInformation")
        pet_information.setStyleSheet("background: rgba(0, 159, 183, 0.30);")
        pet_information.setFixedWidth(310)

        # Pet Information Form
        form2_widget = QWidget()
        form2_layout = QVBoxLayout()
        form2_layout.setContentsMargins(10, 0, 0, 10)
        form2_layout.setAlignment(Qt.AlignLeft)

        form2_layout.addWidget(create_underlined_label("NAME:"))
        form2_layout.addWidget(create_underlined_label("AGE:"))
        form2_layout.addWidget(create_underlined_label("GENDER:"))
        form2_layout.addWidget(create_underlined_label("SPECIES:"))
        form2_layout.addWidget(create_underlined_label("BREED:"))
        form2_layout.addWidget(create_underlined_label("COLOR:"))
        form2_layout.addWidget(create_underlined_label("WEIGHT:"))
        form2_layout.addWidget(create_underlined_label("HEIGHT:"))
        form2_layout.addWidget(create_underlined_label("BLOOD TYPE:"))
        form2_widget.setLayout(form2_layout)
        
        owner_info = QLabel("PET INFORMATION")
        owner_info.setAlignment(Qt.AlignLeft)
        owner_info.setObjectName("OwnerInformation")
        owner_info.setStyleSheet("background: rgba(0, 159, 183, 0.30);")
        owner_info.setFixedWidth(310)

        form3_widget = QWidget()
        form3_layout = QVBoxLayout()
        form3_layout.setContentsMargins(10, 0, 0, 10)
        form3_layout.setAlignment(Qt.AlignLeft)
        
        form3_layout.addWidget(create_underlined_label("NAME:"))
        form3_layout.addWidget(create_underlined_label("ADDRESS:"))
        form3_layout.addWidget(create_underlined_label("CONTACT NUMBER:"))
        form3_layout.addWidget(create_underlined_label("EMAIL ADDRESS:"))
        form3_widget.setLayout(form3_layout)
        
        notes = QLabel("NOTES")
        notes.setAlignment(Qt.AlignLeft)
        notes.setObjectName("Notes")
        notes.setStyleSheet("background: rgba(0, 159, 183, 0.30);")
        notes.setFixedWidth(310)

        # Add to layout
        layout.addWidget(see_record)
        layout.addWidget(pet_medical)
        layout.addWidget(pet_medical_record)
        layout.addWidget(veterinary_clinic)
        layout.addWidget(form_widget)
        layout.addWidget(pet_information)
        layout.addWidget(form2_widget)
        layout.addWidget(owner_info)
        layout.addWidget(form3_widget)
        layout.addWidget(notes)
        
        records_space.setLayout(layout)
        self.content_layout.addWidget(records_space)

    #REPORTS TAB

    def show_reports_content(self):
        self.clear_content()
        self.add_search_bar()
        
        report_space = QWidget()
        report_layout = QVBoxLayout()
        report_layout.setContentsMargins(0, 0, 0, 30)

        # --- Container for Label + Buttons with background ---
        header_widget = QWidget()
        header_widget.setFixedHeight(50)
        header_widget.setStyleSheet("background-color: #102547;")
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

        # --- Treatment Buttons ---
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
        self.treatment_buttons = {}

        for treatment in treatments:
            button = QPushButton(treatment)
            button.setFixedSize(160, 40)
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
            """)
            button.clicked.connect(lambda checked, b=button: self.select_treatment(b))
            treatment_layout.addWidget(button)
            self.treatment_buttons[treatment] = button
            
            treatment_buttons_widget.setLayout(treatment_layout)

        header_layout.addStretch()
        header_layout.addWidget(treatment_buttons_widget)
        header_widget.setLayout(header_layout)

        report_layout.addWidget(header_widget)

        # --- Consultation Table ---
        self.consultation_table = QTableWidget()
        self.consultation_table.setColumnCount(8)
        self.consultation_table.setRowCount(15)
        self.consultation_table.setHorizontalHeaderLabels([
            "Consultation Date",
            "Pet Name",
            "Owner/Client",
            "Reason for Consultation",
            "Diagnosis",
            "Prescribed Treatment",
            "Veterinarian In Charge",
            "Action"
        ])
        
        self.consultation_table.setColumnWidth(0, 150)  # Consultation Date
        self.consultation_table.setColumnWidth(1, 120)  # Pet Name
        self.consultation_table.setColumnWidth(2, 150)  # Owner/Client
        self.consultation_table.setColumnWidth(3, 200)  # Reason for Consultation
        self.consultation_table.setColumnWidth(4, 180)  # Diagnosis
        self.consultation_table.setColumnWidth(5, 200)  # Prescribed Treatment
        self.consultation_table.setColumnWidth(6, 150)  # Veterinarian In Charge
        self.consultation_table.setColumnWidth(7, 100)  # Action
        
        self.consultation_table.horizontalHeader().setStretchLastSection(True)
        self.consultation_table.setStyleSheet("""
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
        
        self.consultation_table.verticalHeader().setVisible(False)

        report_layout.addWidget(self.consultation_table)
        
                # --- Deworm Table ---
        self.deworm_table = QTableWidget()
        self.deworm_table.setColumnCount(8)
        self.deworm_table.setRowCount(15)
        self.deworm_table.setHorizontalHeaderLabels([
            "Deworming Date",
            "Pet Name",
            "Owner/Client",
            "Deworming Medication",
            "Dosage Administered",
            "Next Scheduled Deworming",
            "Veterinarian In Charge",
            "Action"
        ])

        # Set column widths
        self.deworm_table.setColumnWidth(0, 150)  # Deworming Date
        self.deworm_table.setColumnWidth(1, 120)  # Pet Name
        self.deworm_table.setColumnWidth(2, 150)  # Owner/Client
        self.deworm_table.setColumnWidth(3, 200)  # Deworming Medication
        self.deworm_table.setColumnWidth(4, 180)  # Dosage Administered
        self.deworm_table.setColumnWidth(5, 200)  # Next Scheduled Deworming
        self.deworm_table.setColumnWidth(6, 150)  # Veterinarian In Charge
        self.deworm_table.setColumnWidth(7, 100)  # Action

        self.deworm_table.horizontalHeader().setStretchLastSection(True)

        self.deworm_table.setStyleSheet("""
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
        self.deworm_table.hide()  # Initially hidden

        self.deworm_table.verticalHeader().setVisible(False)

        report_layout.addWidget(self.deworm_table)
        
            # --- Vaccination Table --- #
        self.vaccination_table = QTableWidget()
        self.vaccination_table.setColumnCount(8)
        self.vaccination_table.setRowCount(15)
        self.vaccination_table.setHorizontalHeaderLabels([
            "Vaccination Date",
            "Pet Name",
            "Owner/Client",
            "Vaccine Administered",
            "Dosage Administered",
            "Next Scheduled Vaccination",
            "Veterinarian In Charge",
            "Action"
        ])

        # Set column widths
        self.vaccination_table.setColumnWidth(0, 150)  # Deworming Date
        self.vaccination_table.setColumnWidth(1, 120)  # Pet Name
        self.vaccination_table.setColumnWidth(2, 150)  # Owner/Client
        self.vaccination_table.setColumnWidth(3, 200)  # Deworming Medication
        self.vaccination_table.setColumnWidth(4, 180)  # Dosage Administered
        self.vaccination_table.setColumnWidth(5, 200)  # Next Scheduled Deworming
        self.vaccination_table.setColumnWidth(6, 150)  # Veterinarian In Charge
        self.vaccination_table.setColumnWidth(7, 100)  # Action

        self.vaccination_table.horizontalHeader().setStretchLastSection(True)

        self.vaccination_table.setStyleSheet("""
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
        self.vaccination_table.hide()  # Initially hidden

        self.vaccination_table.verticalHeader().setVisible(False)

        report_layout.addWidget(self.vaccination_table)


            # --- Surgical Operation Table --- #
        self.surgical_table = QTableWidget()
        self.surgical_table.setColumnCount(8)
        self.surgical_table.setRowCount(15)
        self.surgical_table.setHorizontalHeaderLabels([
            "Surgery Date",
            "Pet Name",
            "Owner/Client",
            "Type of Surgery",
            "Anesthesia Used",
            "Next Follow-Up Date",
            "Veterinarian In Charge",
            "Action"
        ])

        # Set column widths
        self.surgical_table.setColumnWidth(0, 150)  # Deworming Date
        self.surgical_table.setColumnWidth(1, 120)  # Pet Name
        self.surgical_table.setColumnWidth(2, 150)  # Owner/Client
        self.surgical_table.setColumnWidth(3, 200)  # Deworming Medication
        self.surgical_table.setColumnWidth(4, 180)  # Dosage Administered
        self.surgical_table.setColumnWidth(5, 200)  # Next Scheduled Deworming
        self.surgical_table.setColumnWidth(6, 150)  # Veterinarian In Charge
        self.surgical_table.setColumnWidth(7, 100)  # Action

        self.surgical_table.horizontalHeader().setStretchLastSection(True)

        self.surgical_table.setStyleSheet("""
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
        self.surgical_table.hide()  # Initially hidden

        self.surgical_table.verticalHeader().setVisible(False)

        report_layout.addWidget(self.surgical_table)
        
                    # --- Grooming Table --- #
        self.grooming_table = QTableWidget()
        self.grooming_table.setColumnCount(8)
        self.grooming_table.setRowCount(15)
        self.grooming_table.setHorizontalHeaderLabels([
            "Grooming Date",
            "Pet Name",
            "Owner/Client",
            "Grooming Service/s Availed",
            "Notes",
            "Next Grooming Date",
            "Veterinarian In Charge",
            "Action"
        ])

        # Set column widths
        self.grooming_table.setColumnWidth(0, 150)  # Deworming Date
        self.grooming_table.setColumnWidth(1, 120)  # Pet Name
        self.grooming_table.setColumnWidth(2, 150)  # Owner/Client
        self.grooming_table.setColumnWidth(3, 200)  # Deworming Medication
        self.grooming_table.setColumnWidth(4, 180)  # Dosage Administered
        self.grooming_table.setColumnWidth(5, 200)  # Next Scheduled Deworming
        self.grooming_table.setColumnWidth(6, 150)  # Veterinarian In Charge
        self.grooming_table.setColumnWidth(7, 100)  # Action

        self.grooming_table.horizontalHeader().setStretchLastSection(True)

        self.grooming_table.setStyleSheet("""
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
        self.grooming_table.hide()  # Initially hidden

        self.grooming_table.verticalHeader().setVisible(False)

        report_layout.addWidget(self.grooming_table)

                    # --- Other Treatments Table --- #
        self.other_treatments_table = QTableWidget()
        self.other_treatments_table.setColumnCount(8)
        self.other_treatments_table.setRowCount(15)
        self.other_treatments_table.setHorizontalHeaderLabels([
            "Treatment Date",
            "Pet Name",
            "Owner/Client",
            "Type of Treatment",
            "Medication/Procedure Used",
            "Dosage/Duration",
            "Veterinarian In Charge",
            "Action"
        ])

        # Set column widths
        self.other_treatments_table.setColumnWidth(0, 150)  # Deworming Date
        self.other_treatments_table.setColumnWidth(1, 120)  # Pet Name
        self.other_treatments_table.setColumnWidth(2, 150)  # Owner/Client
        self.other_treatments_table.setColumnWidth(3, 200)  # Deworming Medication
        self.other_treatments_table.setColumnWidth(4, 180)  # Dosage Administered
        self.other_treatments_table.setColumnWidth(5, 200)  # Next Scheduled Deworming
        self.other_treatments_table.setColumnWidth(6, 150)  # Veterinarian In Charge
        self.other_treatments_table.setColumnWidth(7, 100)  # Action

        self.other_treatments_table.horizontalHeader().setStretchLastSection(True)

        self.other_treatments_table.setStyleSheet("""
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
        self.other_treatments_table.hide()  # Initially hidden

        self.other_treatments_table.verticalHeader().setVisible(False)

        report_layout.addWidget(self.other_treatments_table)
        
        report_space.setLayout(report_layout)
        self.content_layout.addWidget(report_space)
        
        # --- Button Connections ---
        self.treatment_buttons["Consultation"].clicked.connect(self.show_consultation_table)
        self.treatment_buttons["Deworm"].clicked.connect(self.show_deworm_table)
        self.treatment_buttons["Vaccination"].clicked.connect(self.show_vaccination_table)
        self.treatment_buttons["Surgical Operation"].clicked.connect(self.show_surgical_table)
        self.treatment_buttons["Grooming"].clicked.connect(self.show_grooming_table)
        self.treatment_buttons["Other Treatments"].clicked.connect(self.show_other_treatments)

    def show_consultation_table(self):
        self.consultation_table.show()
        self.deworm_table.hide()
        self.vaccination_table.hide()
        self.surgical_table.hide()
        self.grooming_table.hide()
        self.other_treatments_table.hide()
         
        
    def show_deworm_table(self):
        self.deworm_table.show()
        self.consultation_table.hide()
        self.vaccination_table.hide()
        self.surgical_table.hide()
        self.grooming_table.hide()
        self.other_treatments_table.hide()
    
    def show_vaccination_table(self):
        self.vaccination_table.show()
        self.consultation_table.hide()
        self.deworm_table.hide()
        self.surgical_table.hide()
        self.grooming_table.hide()
        self.other_treatments_table.hide()
        
    def show_surgical_table(self):
        self.surgical_table.show()
        self.consultation_table.hide()
        self.deworm_table.hide()
        self.vaccination_table.hide()
        self.grooming_table.hide()
        self.other_treatments_table.hide()
    
    def show_grooming_table(self):
        self.grooming_table.show()
        self.consultation_table.hide()
        self.deworm_table.hide()
        self.vaccination_table.hide()
        self.surgical_table.hide()
        self.other_treatments_table.hide()
        
    def show_other_treatments(self):
        self.other_treatments_table.show()
        self.consultation_table.hide()
        self.deworm_table.hide()
        self.vaccination_table.hide()
        self.surgical_table.hide()
        self.grooming_table.hide()
    
    # -- APPOINTMENT TAB -- #
    def show_appointments_content(self):
        self.clear_content()
        self.add_search_bar()
            
        appointments_space = QWidget()
        appointments_layout = QVBoxLayout()
        appointments_layout.setContentsMargins(0, 0, 0, 30)

        # --- Container for Label + Buttons with background --- #
        header_widget = QWidget()
        header_widget.setFixedHeight(50)
        header_widget.setStyleSheet("background-color: #102547;")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)

        # Appointment Label
        appointments_label = QLabel("Appointment")
        appointments_label.setObjectName("Appointment")
        appointments_label.setAlignment(Qt.AlignVCenter)

        # Add Appointment Button
        add_appointment_button = QPushButton("Add Appointment")
        add_appointment_button.setObjectName("AddAppointmentButton")
        add_appointment_button.setFixedSize(120, 40)
        add_appointment_button.setStyleSheet(
            "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px;"
        )

        # Save PDF Button
        save_pdf_button = QPushButton("Save PDF")
        save_pdf_button.setObjectName("SavePDFButton")
        save_pdf_button.setFixedSize(100, 40)
        save_pdf_button.setStyleSheet(
            "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px;"
        )

        header_layout.addWidget(appointments_label)
        header_layout.addWidget(add_appointment_button)
        header_layout.addWidget(save_pdf_button)
        header_layout.addStretch()

        # --- Appointment Filter Buttons (Urgent, All) --- #
        appointment_buttons_widget = QWidget()
        appointment_buttons_layout = QHBoxLayout()
        appointment_buttons_layout.setContentsMargins(0, 0, 50, 0)
        appointment_buttons_layout.setSpacing(0)

        appointment_categories = ["Urgent", "All"]

        # Store buttons for later use
        self.appointment_buttons = {}

        for category in appointment_categories:
            button = QPushButton(category)
            button.setFixedSize(160, 40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #F4F4F8;
                    font-family: Poppins;
                    font-style: normal;
                    font-weight: 300;
                    font-size: 15px;
                    border: none;
                    padding-left: 10px;
                    padding-right: 10px;
                }
                QPushButton:hover {
                    background-color: #FED766;
                }
            """)
            button.clicked.connect(lambda checked, b=category: self.select_appointment(b))
            appointment_buttons_layout.addWidget(button)
            self.appointment_buttons[category] = button

        appointment_buttons_widget.setLayout(appointment_buttons_layout)
        header_layout.addWidget(appointment_buttons_widget)
        header_widget.setLayout(header_layout)

        appointments_layout.addWidget(header_widget)

        # -- URGENT TABLE -- #
        self.urgent_table = QTableWidget()
        self.urgent_table.setColumnCount(8)
        self.urgent_table.setRowCount(15)
        self.urgent_table.setHorizontalHeaderLabels([
            "Date",
            "Pet Name",
            "Owner/Client",
            "Reason for Appointment",
            "Status",
            "Payment Status",
            "Veterinarian In Charge",
            "Action"
        ])
        self.configure_table(self.urgent_table)
        self.urgent_table.hide()  # Hide initially
        appointments_layout.addWidget(self.urgent_table)

        # -- ALL TABLE -- #
        self.all_table = QTableWidget()
        self.all_table.setColumnCount(8)
        self.all_table.setRowCount(15)
        self.all_table.setHorizontalHeaderLabels([
            "Date",
            "Pet Name",
            "Owner/Client",
            "Reason for Appointment",
            "Status",
            "Payment Status",
            "Veterinarian In Charge",
            "Action"
        ])
        self.configure_table(self.all_table)
        appointments_layout.addWidget(self.all_table)

        appointments_space.setLayout(appointments_layout)
        self.content_layout.addWidget(appointments_space)

        # Connect buttons to show tables
        self.appointment_buttons["Urgent"].clicked.connect(self.show_urgent_table)
        self.appointment_buttons["All"].clicked.connect(self.show_all_table)

    def configure_table(self, table):
        """Helper function to configure table appearance and settings."""
        table.setColumnWidth(0, 150)  # Date
        table.setColumnWidth(1, 120)  # Pet Name
        table.setColumnWidth(2, 150)  # Owner/Client
        table.setColumnWidth(3, 200)  # Reason for Appointment
        table.setColumnWidth(4, 180)  # Status
        table.setColumnWidth(5, 200)  # Payment Status
        table.setColumnWidth(6, 150)  # Veterinarian In Charge
        table.setColumnWidth(7, 100)  # Action

        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
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

    def show_urgent_table(self):
        self.urgent_table.show()
        self.all_table.hide()

    def show_all_table(self):
        self.all_table.show()
        self.urgent_table.hide()
            
    # -- Billings Tab -- #
    def show_billings_content(self):
        self.clear_content()
        self.add_search_bar()
        
        billings_space = QWidget()
        billings_layout = QVBoxLayout()
        billings_layout.setContentsMargins(0, 0, 0, 30)

        # --- Header (Label + Buttons) --- #
        header_widget = QWidget()
        header_widget.setFixedHeight(50)
        header_widget.setStyleSheet("background-color: #102547;")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 10, 0)
        header_layout.setSpacing(10)

        # Billing Label
        billings_label = QLabel("Billing Page")
        billings_label.setObjectName("Billings")
        billings_label.setAlignment(Qt.AlignVCenter)
        
        add_billing_button = QPushButton("Add Receipt")
        add_billing_button.setObjectName("AddReceiptButton")
        add_billing_button.setFixedSize(120, 40)
        add_billing_button.setStyleSheet(
            "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px;"
        )

        # Add widgets to header
        header_layout.addWidget(billings_label)
        header_layout.addWidget(add_billing_button)
        header_layout.addStretch()
        header_widget.setLayout(header_layout)

        # Add header to the layout
        billings_layout.addWidget(header_widget)

        # --- Table --- #
        self.billings_table = QTableWidget()
        self.billings_table.setRowCount(5)
        self.billings_table.setColumnCount(8)
        self.billings_table.setHorizontalHeaderLabels([
            "Receipt No.", "Date Issued", "Owner/Client", 
            "Pet Name", "Total Amount (Php)", "Payment", 
            "Payment Status", "Action"
        ])
        self.billings_table.horizontalHeader().setStretchLastSection(True)
        self.billings_table.verticalHeader().setVisible(False)

        self.billings_table.setStyleSheet("""
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
        self.billings_table.setColumnWidth(0, 150)  # Receipt No.
        self.billings_table.setColumnWidth(1, 120)  # Date Issued
        self.billings_table.setColumnWidth(2, 150)  # Owner/Client
        self.billings_table.setColumnWidth(3, 200)  # Pet Name
        self.billings_table.setColumnWidth(4, 180)  # Total Amount
        self.billings_table.setColumnWidth(5, 200)  # Payment
        self.billings_table.setColumnWidth(6, 150)  # Payment Status
        self.billings_table.setColumnWidth(7, 100)  # Action

        # Add table to layout
        billings_layout.addWidget(self.billings_table)

        billings_space.setLayout(billings_layout)
        self.content_layout.addWidget(billings_space)


    def show_settings_content(self):
        self.clear_content()
        self.content_layout.addWidget(QLabel("Settings Page"))
        
    def select_treatment(self, selected_button):
        # Reset all buttons to default color first
        for button in self.treatment_buttons.values():
            button.setStyleSheet("""
                QPushButton {;
                    border: none;
                    font-size: 15px;
                    background-color: #F4F4F8;
                    font-family: Poppins;
                    font-style: normal;
                    font-weight: 300;
                    line-height: normal
                    padding-left: 10px;
                    padding-right: 10px;
                }
                QPushButton:hover {
                    background-color: #FED766;
                }
            """)

        # Set the clicked button color to #FED766
        selected_button.setStyleSheet("""
            QPushButton {
                background-color: #FED766;
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
        """)
        
    def select_appointment(self, category):
        """Optional: Add behavior if you want to visually show which button is active."""
        for name, button in self.appointment_buttons.items():
            if name == category:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #FED766;
                        font-family: Poppins;
                        font-style: normal;
                        font-weight: 300;
                        font-size: 15px;
                        border: none;
                        padding-left: 10px;
                        padding-right: 10px;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #F4F4F8;
                        font-family: Poppins;
                        font-style: normal;
                        font-weight: 300;
                        font-size: 15px;
                        border: none;
                        padding-left: 10px;
                        padding-right: 10px;
                    }
                    QPushButton:hover {
                        background-color: #FED766;
                    }
                """)

if __name__ == "__main__":
        from PySide6.QtWidgets import QApplication
        import sys

        app = QApplication([])

        window = HomePage()
        window.showMaximized()
        app.exec()
