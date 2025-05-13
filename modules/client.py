from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QScroller, QScrollArea,
    QStackedLayout, QComboBox, QTabWidget, QDateEdit, QMessageBox,
    QFileDialog, QHeaderView, QDialog
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, QDate
from modules.database import Database
from modules.utils import create_styled_message_box, show_message
from datetime import datetime

class AddPetDialog(QDialog):
    def __init__(self, client_email, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Pet")
        self.setFixedSize(600, 700)
        self.client_email = client_email
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("Add New Pet")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #012547;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Form fields
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter pet name")
        self.name_input.setMinimumHeight(35)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)

        # Gender
        gender_layout = QHBoxLayout()
        gender_label = QLabel("Gender:")
        gender_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female"])
        self.gender_combo.setMinimumHeight(35)
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_combo)
        form_layout.addLayout(gender_layout)

        # Species
        species_layout = QHBoxLayout()
        species_label = QLabel("Species:")
        species_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.species_input = QLineEdit()
        self.species_input.setPlaceholderText("Enter species")
        self.species_input.setMinimumHeight(35)
        species_layout.addWidget(species_label)
        species_layout.addWidget(self.species_input)
        form_layout.addLayout(species_layout)

        # Breed
        breed_layout = QHBoxLayout()
        breed_label = QLabel("Breed:")
        breed_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.breed_input = QLineEdit()
        self.breed_input.setPlaceholderText("Enter breed")
        self.breed_input.setMinimumHeight(35)
        breed_layout.addWidget(breed_label)
        breed_layout.addWidget(self.breed_input)
        form_layout.addLayout(breed_layout)

        # Color
        color_layout = QHBoxLayout()
        color_label = QLabel("Color:")
        color_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("Enter color")
        self.color_input.setMinimumHeight(35)
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_input)
        form_layout.addLayout(color_layout)

        # Birthdate
        birthdate_layout = QHBoxLayout()
        birthdate_label = QLabel("Birthdate:")
        birthdate_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True)
        self.birthdate_input.setDate(QDate.currentDate())
        self.birthdate_input.setDisplayFormat("dd/MM/yyyy")
        self.birthdate_input.setMinimumHeight(35)
        birthdate_layout.addWidget(birthdate_label)
        birthdate_layout.addWidget(self.birthdate_input)
        form_layout.addLayout(birthdate_layout)

        # Age
        age_layout = QHBoxLayout()
        age_label = QLabel("Age:")
        age_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter age")
        self.age_input.setMinimumHeight(35)
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.age_input)
        form_layout.addLayout(age_layout)

        # Weight
        weight_layout = QHBoxLayout()
        weight_label = QLabel("Weight:")
        weight_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Enter weight in kg")
        self.weight_input.setMinimumHeight(35)
        weight_layout.addWidget(weight_label)
        weight_layout.addWidget(self.weight_input)
        form_layout.addLayout(weight_layout)

        # Height
        height_layout = QHBoxLayout()
        height_label = QLabel("Height:")
        height_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Enter height in meters")
        self.height_input.setMinimumHeight(35)
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_input)
        form_layout.addLayout(height_layout)

        # Blood Type
        blood_type_layout = QHBoxLayout()
        blood_type_label = QLabel("Blood Type:")
        blood_type_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.blood_type_combo = QComboBox()
        self.blood_type_combo.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])
        self.blood_type_combo.setMinimumHeight(35)
        blood_type_layout.addWidget(blood_type_label)
        blood_type_layout.addWidget(self.blood_type_combo)
        form_layout.addLayout(blood_type_layout)

        # Photo
        photo_layout = QHBoxLayout()
        photo_label = QLabel("Photo:")
        photo_label.setStyleSheet("font-size: 16px; font-weight: bold; min-width: 150px;")
        self.photo_path = None
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 150)
        self.photo_label.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                border: 2px dashed #012547;
                border-radius: 10px;
            }
        """)
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setText("Click to add photo")
        self.photo_label.mousePressEvent = self.select_photo
        photo_layout.addWidget(photo_label)
        photo_layout.addWidget(self.photo_label)
        form_layout.addLayout(photo_layout)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(120, 40)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Save")
        save_btn.setFixedSize(120, 40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #01315d;
            }
        """)
        save_btn.clicked.connect(self.save_pet)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)

    def select_photo(self, event):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Pet Photo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.photo_path = file_name
            pixmap = QPixmap(file_name)
            self.photo_label.setPixmap(pixmap.scaled(
                150, 150,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))

    def save_pet(self):
        name = self.name_input.text().strip()
        gender = self.gender_combo.currentText()
        species = self.species_input.text().strip()
        breed = self.breed_input.text().strip()
        color = self.color_input.text().strip()
        birthdate = self.birthdate_input.date().toString("yyyy-MM-dd")
        age = self.age_input.text().strip()
        weight = self.weight_input.text().strip()
        height = self.height_input.text().strip()
        blood_type = self.blood_type_combo.currentText()

        if not all([name, species, breed, color, age, weight, height]):
            show_message(self, "All fields are required!", QMessageBox.Warning)
            return

        if not age.isdigit():
            show_message(self, "Age must be a valid integer!", QMessageBox.Warning)
            return

        try:
            weight_float = float(weight)
            if weight_float <= 0:
                show_message(self, "Weight must be greater than 0!", QMessageBox.Warning)
                return
        except ValueError:
            show_message(self, "Weight must be a valid number!", QMessageBox.Warning)
            return

        try:
            height_float = float(height)
            if height_float <= 0:
                show_message(self, "Height must be greater than 0!", QMessageBox.Warning)
                return
        except ValueError:
            show_message(self, "Height must be a valid number!", QMessageBox.Warning)
            return

        age = int(age)

        db = Database()
        try:
            db.cursor.execute("SELECT client_id FROM clients WHERE email = ?", (self.client_email,))
            result = db.cursor.fetchone()
            if not result:
                show_message(self, "No client found with the provided email!", QMessageBox.Warning)
                return
            client_id = result[0]

            db.cursor.execute("""
                INSERT INTO pets (name, gender, species, breed, color, birthdate, age, weight, height, blood_type, photo_path, client_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, gender, species, breed, color, birthdate, age, weight_float, height_float, blood_type, self.photo_path, client_id))
            db.conn.commit()
            show_message(self, "New pet added successfully!")
            self.accept()
        except Exception as e:
            show_message(self, f"Error saving pet: {e}", QMessageBox.Critical)
        finally:
            db.close_connection()

def get_client_widget(main_window):
    content = QWidget()
    main_layout = QVBoxLayout(content)
    main_layout.setContentsMargins(0, -30, 0, 30)
    main_layout.setSpacing(0)
    
    main_window.tab_widget = QTabWidget()
    
    def open_edit_form():
        """Open the form for editing the selected client."""
        selected_row = table.currentRow()
        if selected_row == -1:
            print("❌ No client selected.")
            return

        selected_widget = table.cellWidget(selected_row, 0)  # 🛠 get the widget!
        if selected_widget:
            name_label = selected_widget.findChild(QLabel)
            if name_label:
                client_name = name_label.text()
            else:
                print("❌ Could not find client name label.")
                return
        else:
            print("❌ Could not find selected widget.")
            return

        # Fetch client data from the database
        db = Database()
        try:
            db.cursor.execute("SELECT name, address, contact_number, email FROM clients WHERE name = ?", (client_name,))
            client_data = db.cursor.fetchone()
        except Exception as e:
            print(f"❌ Error fetching client data: {e}")
            return
        finally:
            db.close_connection()

        if client_data:
            # Populate the form fields with the client's data
            inputs = edit_fields_widget.findChildren(QLineEdit)
            inputs[0].setText(client_data[0])  # Name
            inputs[1].setText(client_data[1])  # Address
            inputs[2].setText(client_data[2])  # Contact Number
            inputs[3].setText(client_data[3])  # Email

            # Store the original email for updating the correct client
            edit_form_widget.setProperty("original_email", client_data[3])

            client_info_stack.setCurrentIndex(1)  # Switch to the form ✅

    # --- Client Info Layout ---
    client_info_widget = QWidget()
    client_info_layout_inner = QHBoxLayout(client_info_widget)

    edit_client_button = QPushButton(client_info_widget)
    edit_client_button.setIcon(QIcon("assets/edit client button.png"))
    edit_client_button.setIconSize(QSize(30, 30))
    edit_client_button.setFixedSize(90, 60)
    edit_client_button.setStyleSheet("background-color: #FED766; border: none;")

    # Connect the edit button to the open_edit_form function
    edit_client_button.clicked.connect(open_edit_form)
    
    # Add the button to the layout
    client_info_layout_inner.addWidget(edit_client_button)    

    # Client header 

    client_header = QWidget()
    client_header.setFixedHeight(50)
    client_header.setStyleSheet("background-color: #102547;")
    client_header_layout = QHBoxLayout()
    client_header_layout.setContentsMargins(0, 0, 0, 0)
    client_header_layout.setSpacing(0)

    
    # --- Client List Label ---
    client_list = QLabel("Client List", content)
    client_list.setObjectName("ClientList")
    client_list.setStyleSheet("background-color: #102547;")
    client_list.setAlignment(Qt.AlignVCenter)

    # --- add client button --- #

    add_button = QPushButton("Add Client", content)
    add_button.setObjectName("AddClientButton")
    add_button.setFixedSize(60, 40)
    add_button.setStyleSheet(
        "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px;"
    )

    client_header_layout.addWidget(client_list)
    client_header_layout.addWidget(add_button)

    client_header_layout.addStretch()
    client_header.setLayout(client_header_layout)
    main_layout.addWidget(client_header)

    # --- Table and Client Info Layout ---
    table_info_layout = QHBoxLayout()
    table_info_layout.setContentsMargins(0, 0, 0, 0)
    table_info_layout.setSpacing(0)

   # --- Client Table ---
    table = QTableWidget(content)
    table.setColumnCount(1)
    table.setRowCount(16)
    table.setFixedWidth(325)
    table.setFixedHeight(500)
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setVisible(False)  

    # Hide the vertical scrollbar but allow scrolling
    table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # Enable touch/mouse scrolling
    QScroller.grabGesture(table.viewport(), QScroller.LeftMouseButtonGesture)

    table.setStyleSheet("""
        QHeaderView::section {
            height: 0px;
            padding: 0px;
            margin: 0px;
            border: none;
    }
        QTableWidget {
            background-color: transparent;
            color: black;
            border: 1px solid gray;
            margin-top: 0;
            padding-top: 0;
        }
                        
        QTableWidget::item {
            border-bottom: 1px solid gray; 
            padding-left: 10px;  /* Adds space between text and left border */
            padding-right: 10px;
            padding-top: -5px;
            padding-bottom: 5px;
            background-color:transparent;
        }
                               
        QTableWidget::item:selected {
        background-color:  #007a99;  /* Light cyan highlight */
        color: black;
        }
    """)


    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectRows)  # Allow row selection
    table.setSelectionMode(QTableWidget.SingleSelection)
    table_info_layout.addWidget(table)

    # --- Client Info Stack Widget and Layout ---
    client_info_stack_widget = QWidget(content)  # Set parent to content
    client_info_stack = QStackedLayout(client_info_stack_widget)  # Set parent

    # ===== VIEW MODE =====
    client_info_view = QWidget(client_info_stack_widget)  # Set parent
    client_info_layout = QVBoxLayout(client_info_view)
    client_info_layout.setContentsMargins(0, 0, 0, 0)
    client_info_layout.setSpacing(5)

    # Top bar (yellow background with label and edit button)
    client_info_widget = QWidget(client_info_view)
    client_info_widget.setFixedHeight(50)
    client_info_widget.setStyleSheet("background-color: #FED766;")
    client_info_layout_inner = QHBoxLayout(client_info_widget)
    client_info_layout_inner.setContentsMargins(0, 0, 0, 0)
    client_info_layout_inner.setSpacing(0)

    client_info_label = QLabel("CLIENT INFORMATION", client_info_widget)
    client_info_label.setObjectName("ClientInformationLabel")
    client_info_label.setAlignment(Qt.AlignVCenter)

    edit_client_button = QPushButton(client_info_widget)
    edit_client_button.setIcon(QIcon("assets/edit client button.png"))
    edit_client_button.setIconSize(QSize(30, 30))
    edit_client_button.setFixedSize(90, 60)
    edit_client_button.setStyleSheet("background-color: #FED766; border: none;")

    edit_client_button.clicked.connect(open_edit_form)  # 🛠️ Connect it here!

    client_info_layout_inner.addWidget(client_info_label)
    client_info_layout_inner.addStretch()  # push edit button to the right
    client_info_layout_inner.addWidget(edit_client_button)

    client_info_layout.addWidget(client_info_widget)

    ###########################################

    labels = ["Name:", "Address:", "Contact Number:", "Email Address:"]
    label_names = ["NameLabel", "AddressLabel", "ContactLabel", "EmailLabel"]
    input_names = ["NameInput", "AddressInput", "ContactInput", "EmailInput"]

    for i, (text, label_name, input_name) in enumerate(zip(labels, label_names, input_names)):
        pair_layout = QHBoxLayout()

        label = QLabel(text, client_info_view)
        label.setObjectName(label_name)
        label.setFixedWidth(180)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        input_field = QLineEdit(client_info_view)
        input_field.setObjectName(input_name)
        input_field.setMinimumWidth(250)

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_field)
        pair_layout.addStretch()  # optional, pushes input field left if there's space

        client_info_layout.addLayout(pair_layout)


    ################################################

    # PETS section
    
    pet_info_widget = QWidget(client_info_view)  # Set parent
    pet_info_widget.setFixedHeight(50)
    pet_info_widget.setStyleSheet("background-color: #FED766;")
    pet_info_layout = QHBoxLayout(pet_info_widget)
    pet_info_layout.setContentsMargins(0, 0, 0, 0)
    pet_info_layout.setSpacing(0)  # Remove spacing between items

    pet_info_label = QLabel("PETS", pet_info_widget)
    pet_info_label.setObjectName("PetsLabel")
    pet_info_label.setAlignment(Qt.AlignVCenter)

    edit_pet_button = QPushButton(pet_info_widget)
    edit_pet_button.setIcon(QIcon("assets/add pet button.png"))
    edit_pet_button.setIconSize(QSize(30, 30))
    edit_pet_button.setFixedSize(90, 60)
    edit_pet_button.setStyleSheet("background-color: #FED766; border: none;")

    pet_info_layout.addWidget(pet_info_label)
    pet_info_layout.addStretch()  # Add stretch to push arrows and button to the right
    pet_info_layout.addWidget(edit_pet_button)
    client_info_layout.addWidget(pet_info_widget)

    pet_picture = QLabel()
    pet_picture.setFixedSize(120, 120)
    pet_picture.setAlignment(Qt.AlignCenter)
    pet_picture.setStyleSheet("background-color: white; border-radius: 10px;")
    pet_picture.setText("No Photo")



    #####################################################
   # Scroll area setup (already correct)
    scroll_area = QScrollArea(client_info_view)
    scroll_area.setWidgetResizable(True)
    scroll_area.setFixedHeight(300)
    
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)
    scroll_layout.setSpacing(5)
    scroll_layout.setContentsMargins(10, 10, 10, 10)
    scroll_layout.setAlignment(Qt.AlignTop)
    scroll_area.setWidget(scroll_content)

    client_info_layout.addWidget(scroll_area)

    # ===== CLIENT EDIT FORM =====
    edit_form_widget = QWidget(client_info_stack_widget)  # Set parent
    edit_form_layout = QVBoxLayout(edit_form_widget)
    edit_form_layout.setContentsMargins(0, 0, 0, 10)

    edit_form_label = QLabel("CLIENT'S FORM", edit_form_widget)  # Set parent
    edit_form_label.setFixedHeight(50)
    edit_form_label.setObjectName("EditClientInfoLabel")
    edit_form_label.setStyleSheet("background-color: #FED766;")
    edit_form_layout.addWidget(edit_form_label)

    edit_fields_widget = QWidget(edit_form_widget)  # Set parent
    edit_fields_layout = QVBoxLayout(edit_fields_widget)
    edit_fields_layout.setContentsMargins(80, 0, 80, 10)

    edit_fields = ["Name", "Address", "Contact Number", "Email Address"]
    for field in edit_fields:
        line_edit = QLineEdit(edit_fields_widget)  # Set parent
        line_edit.setPlaceholderText(f"Enter {field}")
        line_edit.setStyleSheet("padding: 8px; margin: 10px; background-color: #f4f4f8; border: 1px solid gray; border-radius: 5px; font-size: 12px;")
        edit_fields_layout.addWidget(line_edit)

    edit_form_layout.addWidget(edit_fields_widget)

    button_layout = QHBoxLayout()
    button_layout.addStretch()

    cancel_button = QPushButton("Cancel", edit_form_widget)  # Set parent
    cancel_button.setFixedSize(40, 40)
    cancel_button.setStyleSheet("background-color: #f4f4f8; border-radius:20px; color: black; font-size: 12px;")

    save_button = QPushButton("Save", edit_form_widget)  # Set parent
    save_button.setFixedSize(40, 40)
    save_button.setStyleSheet("background-color: #012547; border-radius:20px; color: white; margin-right:90px; font-size: 12px;")

    button_layout.addWidget(cancel_button)
    button_layout.addWidget(save_button)
    edit_form_layout.addLayout(button_layout)
    edit_form_layout.addStretch()

    # ===== PETS EDIT FORM =====
    pets_edit_widget = QWidget(client_info_stack_widget)  # Set parent
    pets_edit_layout = QVBoxLayout(pets_edit_widget)
    pets_edit_layout.setContentsMargins(0, 0, 0, 10)

    pets_edit_label = QLabel("PET'S FORM", pets_edit_widget)  # Set parent
    pets_edit_label.setFixedHeight(50)
    pets_edit_label.setObjectName("EditPetInfoLabel")
    pets_edit_label.setStyleSheet("background-color: #FED766;")
    pets_edit_layout.addWidget(pets_edit_label)

    # --- QLineEdit Style ---
    line_edit_style = """
        padding: 8px;
        background-color: #f4f4f8;
        border: 1px solid gray;
        border-radius: 5px;
        font-size: 12px;
    """

    # Create pet fields layout
    pets_fields_widget = QWidget(pets_edit_widget)  # Set parent
    pets_fields_layout = QVBoxLayout(pets_fields_widget)
    pets_fields_layout.setContentsMargins(80, 10, 80, 10)

    # Row 1
    row1 = QHBoxLayout()
    name_input = QLineEdit(pets_fields_widget)  # Set parent
    name_input.setPlaceholderText("Enter Name")
    name_input.setMinimumHeight(35)
    name_input.setStyleSheet(line_edit_style)

    pet_gender = QComboBox(pets_fields_widget)  # Set parent
    pet_gender.addItems(["Male", "Female"])
    pet_gender.setMinimumHeight(35)
    pet_gender.setStyleSheet("""
        QComboBox {
            padding: 8px;
            border: 1px solid gray;
            border-radius: 5px;
            background-color: #f4f4f8;
            font-size: 12px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            selection-background-color: #FED766;
            font-size: 12px;
        }
    """)

    age_input = QLineEdit(pets_fields_widget)  # Set parent
    age_input.setPlaceholderText("Enter Age")
    age_input.setMinimumHeight(35)
    age_input.setStyleSheet(line_edit_style)

    row1.addWidget(name_input)
    row1.addWidget(pet_gender)
    row1.addWidget(age_input)
    pets_fields_layout.addLayout(row1)

    # Row 2
    row2 = QHBoxLayout()
    species_input = QLineEdit(pets_fields_widget)  # Set parent
    species_input.setPlaceholderText("Enter Species")
    species_input.setMinimumHeight(35)
    species_input.setStyleSheet(line_edit_style)

    breed_input = QLineEdit(pets_fields_widget)  # Set parent
    breed_input.setPlaceholderText("Enter Breed")
    breed_input.setMinimumHeight(35)
    breed_input.setStyleSheet(line_edit_style)

    row2.addWidget(species_input)
    row2.addWidget(breed_input)
    pets_fields_layout.addLayout(row2)

    # Row 3: Weight, Height, Blood Type
    row3 = QHBoxLayout()
    
    # Weight input
    weight_input = QLineEdit(pets_fields_widget)  # Set parent
    weight_input.setPlaceholderText("Enter Weight (kg)")
    weight_input.setMinimumHeight(35)
    weight_input.setStyleSheet(line_edit_style)
    
    # Height input
    height_input = QLineEdit(pets_fields_widget)  # Set parent
    height_input.setPlaceholderText("Enter Height (m)")
    height_input.setMinimumHeight(35)
    height_input.setStyleSheet(line_edit_style)
    
    # Blood Type combo
    blood_type_combo = QComboBox(pets_fields_widget)  # Set parent
    blood_type_combo.addItem("Select Blood Type")  # Add placeholder as first item
    blood_type_combo.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])
    blood_type_combo.setMinimumHeight(35)
    blood_type_combo.setStyleSheet("""
        QComboBox {
            padding: 8px;
            border: 1px solid gray;
            border-radius: 5px;
            background-color: #f4f4f8;
            font-size: 12px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            selection-background-color: #FED766;
            font-size: 12px;
        }
    """)
    
    # Make the placeholder item non-selectable
    blood_type_combo.model().item(0).setEnabled(False)
    
    row3.addWidget(weight_input)
    row3.addWidget(height_input)
    row3.addWidget(blood_type_combo)
    pets_fields_layout.addLayout(row3)

    # Add other input fields
    color_input = QLineEdit(pets_fields_widget)  # Set parent
    color_input.setPlaceholderText("Enter Color")
    color_input.setMinimumHeight(35)
    color_input.setStyleSheet(line_edit_style)
    pets_fields_layout.addWidget(color_input)

    # Replace QLineEdit for birthdate with QDateEdit
    birthdate_input = QDateEdit(pets_fields_widget)  # Set parent
    birthdate_input.setDisplayFormat("yyyy-MM-dd")  # Set the display format to YYYY-MM-DD
    birthdate_input.setCalendarPopup(True)  # Enable calendar popup for easier selection
    birthdate_input.setMinimumHeight(35)
    birthdate_input.setStyleSheet(line_edit_style)

    # Customize the calendar widget
    calendar_style = """
        QCalendarWidget {
            font-size: 16px;
            background-color: white;
            border: 1px solid gray;
            border-radius: 5px;
        }
        QCalendarWidget QToolButton {
            color: black;
            font-size: 18px;
            margin: 5px;
        }
        QCalendarWidget QToolButton::menu-indicator {
            subcontrol-position: right center;
            subcontrol-origin: padding;
        }
        QCalendarWidget QSpinBox {
            font-size: 16px;
        }
        QCalendarWidget QSpinBox::up-button, QCalendarWidget QSpinBox::down-button {
            width: 20px;
            height: 20px;
        }
        QCalendarWidget QTableView {
            font-size: 14px;
        }
    """
    birthdate_input.calendarWidget().setStyleSheet(calendar_style)
    pets_fields_layout.addWidget(birthdate_input)

    # Add fields layout to the main edit form layout
    pets_edit_layout.addWidget(pets_fields_widget)

    # Button row layout
    pets_button_row = QHBoxLayout()
    pets_button_row.addStretch()

    # Cancel button
    pets_cancel_btn = QPushButton("Cancel", pets_edit_widget)  # Set parent
    pets_cancel_btn.setFixedSize(40, 40)
    pets_cancel_btn.setStyleSheet("background-color: #f4f4f8; border-radius:20px; color: black; font-size: 12px;")

    # Save button
    pets_save_btn = QPushButton("Save", pets_edit_widget)  # Set parent
    pets_save_btn.setFixedSize(40, 40)
    pets_save_btn.setStyleSheet("background-color: #012547; border-radius:20px; color: white; margin-right:10px; font-size: 12px;")

    # Add buttons to layout
    pets_button_row.addWidget(pets_cancel_btn)
    pets_button_row.addWidget(pets_save_btn)
    pets_edit_layout.addLayout(pets_button_row)
    pets_edit_layout.addStretch()

    # --- Hook up button functionality ---
    save_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))
    cancel_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))

    edit_pet_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(2))
    pets_save_btn.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))
    pets_cancel_btn.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))

    client_info_stack.addWidget(client_info_view)
    client_info_stack.addWidget(edit_form_widget)
    client_info_stack.addWidget(pets_edit_widget)
    client_info_stack.setCurrentIndex(0)
    table_info_layout.addWidget(client_info_stack_widget)
    main_layout.addLayout(table_info_layout)

    button_layout = QHBoxLayout()
    button_layout.setContentsMargins(0, 0, 0, 20)  # Adjust margins
    button_layout.setSpacing(10)  # Add spacing between buttons

    # Force layout update
    content.update()

    def save_client_data():
        """Save the client data from the form."""
        inputs = edit_fields_widget.findChildren(QLineEdit)
        if len(inputs) >= 4:
            name = inputs[0].text().strip()
            address = inputs[1].text().strip()
            contact_number = inputs[2].text().strip()
            email = inputs[3].text().strip()

            # Validate inputs
            if not name or not address or not contact_number or not email:
                show_message(content, "All fields are required!", QMessageBox.Warning)
                return

            if "@" not in email or "." not in email:
                show_message(content, "Please enter a valid email address!", QMessageBox.Warning)
                return

            db = Database()
            try:
                # Check if we are editing an existing client or adding a new one
                original_email = edit_form_widget.property("original_email")
                if original_email:  # Edit mode
                    db.cursor.execute(
                        "UPDATE clients SET name = ?, address = ?, contact_number = ?, email = ? WHERE email = ?",
                        (name, address, contact_number, email, original_email)
                    )
                    show_message(content, "Client updated successfully!")
                else:  # Add mode
                    db.cursor.execute(
                        "INSERT INTO clients (name, address, contact_number, email) VALUES (?, ?, ?, ?)",
                        (name, address, contact_number, email)
                    )
                    show_message(content, "Client added successfully!")

                db.conn.commit()

                # Update the client table and client information display
                update_client_table()  # Refresh the table with the new data
                update_client_info(email)  # Update the client info display
                client_info_stack.setCurrentIndex(0)  # Go back to view mode

                # Clear the original_email property after saving
                edit_form_widget.setProperty("original_email", None)
            except Exception as e:
                show_message(content, f"Failed to save client: {e}", QMessageBox.Critical)
            finally:
                db.close_connection()
            
    save_button.clicked.connect(save_client_data)
    cancel_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))
    
    # Define the open_add_form function
    def open_add_form():
        """Open the form to add a new client."""
        # Clear all the line edits
        for line_edit in edit_fields_widget.findChildren(QLineEdit):
            line_edit.clear()

        # Clear the original_email property to indicate add mode
        edit_form_widget.setProperty("original_email", None)

        # Switch to the client form
        client_info_stack.setCurrentIndex(1)

    # Connect the "+" button to the open_add_form function
    add_button.clicked.connect(open_add_form)

    # --- Function to Update the Client Table ---
    def update_client_table():
        """Update the client table with data from the database."""
        db = Database()
        db.cursor.execute("SELECT name, email FROM clients")
        clients = db.cursor.fetchall()
        db.close_connection()

        table.clearContents()  # Clear previous contents
        table.setRowCount(0)   # Clear row count

        table.setRowCount(len(clients))  # New number of rows

        for row, client in enumerate(clients):
            client_name, client_email = client

            # Create a widget to hold the client name and delete button
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(5, 5, 5, 5)
            cell_widget.setStyleSheet("background-color: transparent;")
            cell_layout.setSpacing(5)

            cell_widget.setFixedHeight(34)

            name_label = QLabel(client_name)
            name_label.setStyleSheet("color: black; font-size: 14px; background-color: transparent;")
            cell_layout.addWidget(name_label)

            cell_layout.addStretch()

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("assets/trash-can.png"))
            delete_button.setObjectName("DeleteButton")

            delete_button.clicked.connect(lambda _, email=client_email: delete_client(email))
            cell_layout.addWidget(delete_button)

            table.setCellWidget(row, 0, cell_widget)
                
    def delete_client(email):
        """Delete a client from the database with confirmation."""
        confirmation = QMessageBox()
        confirmation.setIcon(QMessageBox.Question)
        confirmation.setText(f"Are you sure you want to delete the client with email: {email}?")
        confirmation.setWindowTitle("")
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)

        response = confirmation.exec()
        if response == QMessageBox.Yes:
            db = Database()
            try:
                db.cursor.execute("DELETE FROM clients WHERE email = ?", (email,))
                db.conn.commit()
                show_message(content, f"Client with email {email} deleted successfully.")
                update_client_table()  # Refresh the table after deletion
            except Exception as e:
                show_message(content, f"Failed to delete client: {e}", QMessageBox.Critical)
            finally:
                db.close_connection()
                
        update_client_table()
        
    main_layout.addLayout(table_info_layout)

  # --- Function to Update Client Info ---
    def update_client_info(email):
        """Update the client info labels with data from the database."""
        db = Database()
        client_data = db.get_client_info(email)
        db.close_connection()

        if client_data:
            name, address, contact_number, email = client_data

            # Find the input fields
            name_input = client_info_view.findChild(QLineEdit, "NameInput")
            address_input = client_info_view.findChild(QLineEdit, "AddressInput")
            contact_input = client_info_view.findChild(QLineEdit, "ContactInput")
            email_input = client_info_view.findChild(QLineEdit, "EmailInput")

            # Update the input fields
            if name_input:
                name_input.setText(name)
            if address_input:
                address_input.setText(address)
            if contact_input:
                contact_input.setText(contact_number)
            if email_input:
                email_input.setText(email)
                
    def update_pet_info(client_email):
        db = Database()
        try:
            db.cursor.execute("SELECT client_id FROM clients WHERE email = ?", (client_email,))
            result = db.cursor.fetchone()
            
            if not result:
                print("❌ No client found with email")
                return
            client_id = result[0]
            print(f"✅ Retrieved client_id: {client_id}")
        except Exception as e:
            print(f"❌ Error fetching client_id: {e}")
            return

        # Fetch pets associated with the client_id, including the photo_path
        try:
            db.cursor.execute("""
                SELECT name, gender, species, breed, color, birthdate, age, photo_path
                FROM pets
                WHERE client_id = ?
            """, (client_id,))
            pets = db.cursor.fetchall()

            for i in range(scroll_layout.count()):
                widget = scroll_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            # Create new pet cards and add them to the layout
            for idx, pet in enumerate(pets):
                card = create_pet_card(pet, idx)
                scroll_layout.addWidget(card)

        except Exception as e:
            print(f"❌ Error fetching pets: {e}")
            return
        finally:
            db.close_connection()

        # 🧹 Clear the scroll layout
        while scroll_layout.count():
            child = scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if pets:
            # Create cards for all pets and add to scroll area
            for index, pet in enumerate(pets):
                pet_card = create_pet_card(pet, index)
                scroll_layout.addWidget(pet_card)
        else:
            no_pet_label = QLabel("No pets found.")
            no_pet_label.setAlignment(Qt.AlignCenter)
            scroll_layout.addWidget(no_pet_label)

    def handle_update_pet(pet_data, index):
        pets = pet_info_widget.property("pets") or []
        pets.insert(0, pet_data)  # optional: update or replace existing list
        pet_info_widget.setProperty("pets", pets)
        pet_info_widget.setProperty("current_index", index)
        open_edit_pet_form(pet_data)
        
    def redirect_to_appointments_tab(pet_name):
        """Redirect to the Appointments Tab and filter appointments by the pet's name."""
        try:
            # Get the main window's tab widget
            tab_widget = main_window.tab_widget
            if not tab_widget:
                print("❌ Could not find tab widget")
                return

            # Find the Appointments tab by name
            for i in range(tab_widget.count()):
                if tab_widget.tabText(i) == "Appointments":
                    # Switch to the Appointments Tab
                    tab_widget.setCurrentIndex(i)
                    
                    # Get the Appointments Tab widget
                    appointments_tab = tab_widget.widget(i)
                    
                    # Call the filter method if it exists
                    if hasattr(appointments_tab, "filter_appointments_by_pet"):
                        appointments_tab.filter_appointments_by_pet(pet_name)
                        print(f"✅ Successfully filtered appointments for pet: {pet_name}")
                    else:
                        print("❌ Appointments tab does not have filter_appointments_by_pet method")
                    return
                
            print("❌ Could not find Appointments tab")
            
        except Exception as e:
            print(f"❌ Error in redirect_to_appointments_tab: {str(e)}")

    def create_pet_card(pet_data, index):
        pet_card = QWidget()
        pet_card.setFixedHeight(160)
        pet_card_layout = QHBoxLayout(pet_card)
        pet_card_layout.setContentsMargins(10, 10, 20, 10)
        pet_card_layout.setSpacing(10)

        pet_card.setStyleSheet("background-color: white; border-radius: 20px;")

        # 📷 Pet photo on the left
        pet_card_picture = QLabel()
        pet_card_picture.setFixedSize(150, 150)
        pet_card_picture.setAlignment(Qt.AlignCenter)
        pet_card_picture.setStyleSheet("background-color: white; border-radius: 10px;")

        photo_path = pet_data[7]
        if photo_path:
            pet_card_picture.setPixmap(QPixmap(photo_path).scaled(
                150, 150,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
        else:
            pet_card_picture.setText("No Photo")

        # 📄 Pet info in the middle
        pet_info_widget = QWidget()
        pet_info_layout = QVBoxLayout(pet_info_widget)
        pet_info_layout.setContentsMargins(0, 0, 0, 0)
        pet_info_layout.setSpacing(2)

        for label_text, value in zip(
            ["Name", "Gender", "Species", "Breed", "Color", "Birthdate", "Age"],
            pet_data[:7]
        ):
            row_layout = QHBoxLayout()

            label = QLabel(f"{label_text}:")
            label.setStyleSheet("font-weight: bold;")
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            value_label = QLabel(str(value))
            value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            # Optionally set fixed width for label to align values
            label.setFixedWidth(80)  # adjust width as needed

            row_layout.addWidget(label)
            row_layout.addWidget(value_label)
            row_layout.addStretch()  # Push items to the left

            pet_info_layout.addLayout(row_layout)

        # 🔘 Buttons on the right
        pet_buttons_widget = QWidget()
        pet_buttons_layout = QVBoxLayout(pet_buttons_widget)
        pet_buttons_layout.setContentsMargins(0, 0, 0, 0)
        pet_buttons_layout.setSpacing(5)  # Reduced spacing for compact layout
        
        # Create buttons
        update_info_button = QPushButton("Update Info")
        check_schedule_button = QPushButton("Check Schedule")
        see_records_button = QPushButton("See Records")

        # Style buttons
        button_style = """
            background-color: #012547; 
            color: white; 
            font-family: Lato; 
            font-size: 10px; 
            font-weight: 700; 
            border-radius: 15px; 
            padding: 0;
            margin: 0;
        """
        
        for btn in [update_info_button, check_schedule_button, see_records_button]:
            btn.setFixedSize(200, 20)
            btn.setStyleSheet(button_style)
            pet_buttons_layout.addWidget(btn)
        
        # Connect the "Check Schedule" button to show the appointments dialog
        pet_name = pet_data[0]  # Get the pet name
        check_schedule_button.clicked.connect(lambda checked, name=pet_name: show_pet_appointments(name))

        update_info_button.clicked.connect(lambda _, d=pet_data, i=index: handle_update_pet(d, i))
        see_records_button.clicked.connect(lambda: setattr(main_window, 'selected_pet_name', pet_data[0]) or main_window.show_pet_records())

        pet_buttons_layout.addStretch()

        # 🧩 Assemble layout: [Photo] [Info] [Buttons]
        pet_card_layout.addWidget(pet_card_picture)
        pet_card_layout.addWidget(pet_info_widget, 1)  # Give info widget more space
        pet_card_layout.addWidget(pet_buttons_widget)

        return pet_card

    def show_pet_appointments(pet_name):
        """Show a dialog with the pet's appointments."""
        from modules.appointment import PetAppointmentsDialog
        dialog = PetAppointmentsDialog(pet_name)
        dialog.exec()

    def upload_pet_photo(pet_label):
        """Open a file dialog to select a pet photo and display it inside the container."""
        file_dialog = QFileDialog()
        file_dialog.setNameFilters(["Image files (*.jpg *.jpeg *.png)"])
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            file_name = selected_file.split("/")[-1]

            pet_label.setPixmap(QPixmap(selected_file).scaled(
                pet_label.width() - 4, pet_label.height() - 4,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            pet_label.setProperty("photo_path", selected_file)

            success_message = create_styled_message_box(
                QMessageBox.Information, 
                "Photo Uploaded", 
                f"✅ \"{file_name}\" was successfully uploaded."
            )
            success_message.exec()

     # 2. THEN create the button and connect it
    upload_photo_button = QPushButton("Upload Photo", pets_fields_widget)
    upload_photo_button.setStyleSheet("""
        background-color: white; 
        color: black; 
        border: 2px solid black;
        border-radius: 5px; 
        font-size: 20px; 
        padding: 8px;
    """)
    pets_fields_layout.addWidget(upload_photo_button)
    # Add photo preview label before the button
    pets_fields_layout.addWidget(pet_picture)

    # 3. Connect after both exist
    upload_photo_button.clicked.connect(lambda: upload_pet_photo(pet_picture))

    def open_add_pet_form():
        """Open the form to add a new pet."""
        # Clear all pet input fields
        name_input.clear()
        age_input.clear()
        species_input.clear()
        breed_input.clear()
        color_input.clear()
        weight_input.clear()
        height_input.clear()
        birthdate_input.setDate(datetime.now())
        pet_gender.setCurrentIndex(0)
        blood_type_combo.setCurrentIndex(0)
        pet_picture.setPixmap(QPixmap())
        pet_picture.setText("No Photo")
        pets_edit_widget.setProperty("mode", "add")

        client_info_stack.setCurrentIndex(2)

    def open_edit_pet_form(pet_data):
        """Open the form to edit the currently selected pet."""
        pets = pet_info_widget.property("pets")
        current_index = pet_info_widget.property("current_index")
        if not pets or current_index is None:
            print("❌ No pet selected.")
            return

        pet_data = pets[current_index]

        # Fill the input fields with existing pet data
        name_input.setText(pet_data[0])
        pet_gender.setCurrentText(pet_data[1])
        species_input.setText(pet_data[2])
        breed_input.setText(pet_data[3])
        color_input.setText(pet_data[4])
        birthdate_input.setDate(pet_data[5])
        age_input.setText(str(pet_data[6]))
        weight_input.setText(str(pet_data[7]))
        height_input.setText(str(pet_data[8]))
        blood_type_combo.setCurrentText(pet_data[9])

        # 🖼️ Set the photo preview in pet_picture
        photo_path = pet_data[10]
        if photo_path:
            pet_picture.setPixmap(QPixmap(photo_path).scaled(
                pet_picture.width(), pet_picture.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            pet_picture.setProperty("photo_path", photo_path)
        else:
            pet_picture.setPixmap(QPixmap())
            pet_picture.setText("No Photo")
            pet_picture.setProperty("photo_path", None)

        pets_edit_widget.setProperty("mode", "edit")  # 🆕 Mark as editing mode

        client_info_stack.setCurrentIndex(2)  # Switch to pet form
        
    # update_info_button.clicked.connect(open_edit_pet_form)
    edit_pet_button.clicked.connect(open_add_pet_form)

    def save_pet_data():
        """Save the pet data from the form."""
        name = name_input.text().strip()
        gender = pet_gender.currentText()
        species = species_input.text().strip()
        breed = breed_input.text().strip()
        color = color_input.text().strip()
        birthdate = birthdate_input.date().toString("yyyy-MM-dd")
        age = age_input.text().strip()
        weight = weight_input.text().strip()
        height = height_input.text().strip()
        blood_type = blood_type_combo.currentText()

        if not all([name, species, breed, color, age, weight, height]):
            show_message(pets_edit_widget, "All fields are required!", QMessageBox.Warning)
            return

        if not age.isdigit():
            show_message(pets_edit_widget, "Age must be a valid integer!", QMessageBox.Warning)
            return

        try:
            weight_float = float(weight)
            if weight_float <= 0:
                show_message(pets_edit_widget, "Weight must be greater than 0!", QMessageBox.Warning)
                return
        except ValueError:
            show_message(pets_edit_widget, "Weight must be a valid number!", QMessageBox.Warning)
            return

        try:
            height_float = float(height)
            if height_float <= 0:
                show_message(pets_edit_widget, "Height must be greater than 0!", QMessageBox.Warning)
                return
        except ValueError:
            show_message(pets_edit_widget, "Height must be a valid number!", QMessageBox.Warning)
            return

        age = int(age)

        client_email = edit_form_widget.property("original_email")
        if not client_email:
            show_message(pets_edit_widget, "No client selected for adding a pet!", QMessageBox.Warning)
            return

        db = Database()
        try:
            db.cursor.execute("SELECT client_id FROM clients WHERE email = ?", (client_email,))
            result = db.cursor.fetchone()
            if not result:
                show_message(pets_edit_widget, "No client found with the provided email!", QMessageBox.Warning)
                return
            client_id = result[0]

            mode = pets_edit_widget.property("mode")

            # Get the photo path from the pet_picture label
            photo_path = pet_picture.property("photo_path")

            if mode == "add":
                db.cursor.execute("""
                    INSERT INTO pets (name, gender, species, breed, color, birthdate, age, weight, height, blood_type, photo_path, client_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, gender, species, breed, color, birthdate, age, weight_float, height_float, blood_type, photo_path, client_id))
                db.conn.commit()
                show_message(pets_edit_widget, "New pet added successfully!")
            elif mode == "edit":
                current_pet_name = pet_info_widget.property("pets")[pet_info_widget.property("current_index")][0]
                db.cursor.execute("""
                    UPDATE pets 
                    SET name = ?, gender = ?, species = ?, breed = ?, color = ?, birthdate = ?, age = ?, weight = ?, height = ?, blood_type = ?, photo_path = ?
                    WHERE name = ? AND client_id = ?
                """, (name, gender, species, breed, color, birthdate, age, weight_float, height_float, blood_type, photo_path, current_pet_name, client_id))
                db.conn.commit()
                show_message(pets_edit_widget, "Pet updated successfully!")

            update_pet_info(client_email)
            pet_info_widget.setProperty("current_index", 0)
            client_info_stack.setCurrentIndex(0)

        except Exception as e:
            show_message(pets_edit_widget, f"Failed to save pet data: {e}", QMessageBox.Critical)
        finally:
            db.close_connection()
                
    pets_save_btn.clicked.connect(save_pet_data)

    def delete_pet():
        """Delete the currently displayed pet."""
        pets = pet_info_widget.property("pets")
        current_index = pet_info_widget.property("current_index")
        if not pets or current_index is None:
            show_message(pets_edit_widget, "No pet selected!", QMessageBox.Warning)
            return

        pet_data = pets[current_index]
        pet_name = pet_data[0]

        client_email = edit_form_widget.property("original_email")
        if not client_email:
            show_message(pets_edit_widget, "No client selected for deleting a pet!", QMessageBox.Warning)
            return

        # Confirmation dialog
        confirmation = create_styled_message_box(
            QMessageBox.Warning,
            "Delete Pet",
            f"Are you sure you want to delete the pet: {pet_name}?"
        )
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)

        response = confirmation.exec()
        if response == QMessageBox.Yes:
            db = Database()
            try:
                db.cursor.execute("""
                    DELETE FROM pets 
                    WHERE name = ? 
                    AND client_id = (SELECT client_id FROM clients WHERE email = ?)
                """, (pet_name, client_email))
                db.conn.commit()
                show_message(pets_edit_widget, f"Pet \"{pet_name}\" was successfully deleted!")

                # Update the pet info section
                update_pet_info(client_email)
                client_info_stack.setCurrentIndex(0)

            except Exception as e:
                show_message(pets_edit_widget, f"Failed to delete pet: {e}", QMessageBox.Critical)
            finally:
                db.close_connection()

    # 2. THEN create and configure the delete button
    pets_delete_btn = QPushButton("Delete", pets_edit_widget)  # Parent is pets_edit_widget
    pets_delete_btn.setFixedSize(40, 40)
    pets_delete_btn.setStyleSheet("""
        background-color: red; 
        border-radius: 20px; 
        color: white; 
        margin-right: 90px;
    """)

    # 3. Add the delete button to the layout
    pets_button_row.addWidget(pets_delete_btn)

    # 4. Connect the button to the delete_pet function
    pets_delete_btn.clicked.connect(delete_pet)

    def on_client_selected(row, column, table):
            """Handle client selection from the table and highlight the active row."""
            # Reset the style of all rows
            for r in range(table.rowCount()):
                cell_widget = table.cellWidget(r, 0)
                if cell_widget:
                    cell_widget.setStyleSheet("background-color:transparent")  # Default background color

            # Highlight the selected row
            selected_item = table.cellWidget(row, 0)
            if selected_item:
                selected_item.setStyleSheet("background-color: transparent")  # Highlight color (yellow)

                # Fetch the client name
                name_label = selected_item.findChild(QLabel)
                if name_label:
                    client_name = name_label.text()

                    db = Database()
                    try:
                        db.cursor.execute("SELECT email FROM clients WHERE name = ?", (client_name,))
                        result = db.cursor.fetchone()
                    except Exception as e:
                        print(f"❌ Error fetching client email: {e}")
                        return
                    finally:
                        db.close_connection()

                    if result:
                        email = result[0]
                        update_client_info(email)
                        update_pet_info(email)  # ✅ Also load pets immediately
                        edit_form_widget.setProperty("original_email", email)  # ✅ Remember client email for pets

        # Connect the table's cell click signal to the function
    table.cellClicked.connect(lambda row, column: on_client_selected(row, column, table))

        # Add the layout to the main layout
    main_layout.addLayout(table_info_layout)
        
    update_client_table()

    return content

def filter_clients_table(search_text, table):
    """Filter the clients table based on the search text."""
    search_text = search_text.strip().lower()  # Normalize the search text
    for row in range(table.rowCount()):
        cell_widget = table.cellWidget(row, 0)
        if cell_widget:
            name_label = cell_widget.findChild(QLabel)
            if name_label:
                client_name = name_label.text().strip().lower()  # Normalize the client name
                # Show or hide the row based on the search text
                table.setRowHidden(row, search_text not in client_name)