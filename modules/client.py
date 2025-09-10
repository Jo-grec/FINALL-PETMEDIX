from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QScroller, QScrollArea,
    QStackedLayout, QComboBox, QTabWidget, QDateEdit, QMessageBox,
    QFileDialog, QHeaderView, QDialog, QFrame
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPainterPath
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
        name_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; min-width: 150px;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter pet name")
        self.name_input.setMinimumHeight(35)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)

        # Gender
        gender_layout = QHBoxLayout()
        gender_label = QLabel("Gender:")
        gender_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; min-width: 150px;")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female"])
        self.gender_combo.setMinimumHeight(35)
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_combo)
        form_layout.addLayout(gender_layout)

        # Species
        species_layout = QHBoxLayout()
        species_label = QLabel("Species:")
        species_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; min-width: 150px;")
        self.species_input = QLineEdit()
        self.species_input.setPlaceholderText("Enter species")
        self.species_input.setMinimumHeight(35)
        species_layout.addWidget(species_label)
        species_layout.addWidget(self.species_input)
        form_layout.addLayout(species_layout)

        # Breed
        breed_layout = QHBoxLayout()
        breed_label = QLabel("Breed:")
        breed_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; min-width: 150px;")
        self.breed_input = QLineEdit()
        self.breed_input.setPlaceholderText("Enter breed")
        self.breed_input.setMinimumHeight(35)
        breed_layout.addWidget(breed_label)
        breed_layout.addWidget(self.breed_input)
        form_layout.addLayout(breed_layout)

        # Color
        color_layout = QHBoxLayout()
        color_label = QLabel("Color:")
        color_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; min-width: 150px;")
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("Enter color")
        self.color_input.setMinimumHeight(35)
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_input)
        form_layout.addLayout(color_layout)

        # Birthdate
        birthdate_layout = QHBoxLayout()
        birthdate_label = QLabel("Birthdate:")
        birthdate_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; min-width: 150px;")
        self.birthdate_input = QLineEdit()
        self.birthdate_input.setPlaceholderText("yyyy-MM-dd")
        self.birthdate_input.setMinimumHeight(35)
        birthdate_layout.addWidget(birthdate_label)
        birthdate_layout.addWidget(self.birthdate_input)
        form_layout.addLayout(birthdate_layout)

        # Age
        age_layout = QHBoxLayout()
        age_label = QLabel("Age:")
        age_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; min-width: 150px;")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("")
        self.age_input.setMinimumHeight(35)
        self.age_input.setReadOnly(True)  # Make it read-only since it's auto-computed
        self.age_input.setStyleSheet("""
            padding: 8px;
            background-color: #f4f4f8;
            border: 1px solid gray;
            border-radius: 5px;
            font-size: 12px;
            color: #666;  /* Gray color to indicate it's read-only */
        """)
        age_layout.addWidget(age_label)
        age_layout.addWidget(self.age_input)
        form_layout.addLayout(age_layout)

        # Weight
        weight_layout = QHBoxLayout()
        weight_label = QLabel("Weight:")
        weight_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; min-width: 150px;")
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Enter weight in kg")
        self.weight_input.setMinimumHeight(35)
        weight_layout.addWidget(weight_label)
        weight_layout.addWidget(self.weight_input)
        form_layout.addLayout(weight_layout)

        # Height
        height_layout = QHBoxLayout()
        height_label = QLabel("Height:")
        height_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; min-width: 150px;")
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Enter height in inches")
        self.height_input.setMinimumHeight(35)
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_input)
        form_layout.addLayout(height_layout)

        # Photo
        photo_layout = QHBoxLayout()
        photo_label = QLabel("Photo:")
        photo_label.setStyleSheet("font-size: 16px; font-family: Lato; font-weight: bold; min-width: 150px;")
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
        button_layout.setContentsMargins(0, 0, 0, 0)  # Move buttons to the left
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(120, 40)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
                color: #000;
                font-family: Lato;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Submit")
        save_btn.setFixedSize(120, 40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
                color: white;
                font-family: Lato;
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
        birthdate = self.birthdate_input.text().strip()
        age = self.age_input.text().strip()
        weight = self.weight_input.text().strip()
        height = self.height_input.text().strip()

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
                INSERT INTO pets (name, gender, species, breed, color, birthdate, age, weight, height, photo_path, client_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, gender, species, breed, color, birthdate, age, weight_float, height_float, self.photo_path, client_id))
            db.conn.commit()
            show_message(self, "New pet added successfully!")
            self.accept()
        except Exception as e:
            show_message(self, f"Error saving pet: {e}", QMessageBox.Critical)
        finally:
            db.close_connection()

def get_client_widget(main_window, user_role=None):
    content = QWidget()
    main_layout = QVBoxLayout(content)
    main_layout.setContentsMargins(0, 0, 0, 0)
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
            db.cursor.execute("SELECT name, control_number, address, contact_number, email FROM clients WHERE name = ?", (client_name,))
            client_data = db.cursor.fetchone()
        except Exception as e:
            print(f"❌ Error fetching client data: {e}")
            return
        finally:
            db.close_connection()

        if client_data:
            # Populate the form fields with the client's data (skip control number)
            inputs = edit_fields_widget.findChildren(QLineEdit)
            inputs[0].setText(client_data[0])  # Name
            inputs[1].setText(client_data[2])  # Address
            inputs[2].setText(client_data[3])  # Contact Number
            inputs[3].setText(client_data[4])  # Email

            # Store the original email for updating the correct client
            edit_form_widget.setProperty("original_email", client_data[4])

            client_info_stack.setCurrentIndex(1)  # Switch to the form ✅

    # --- Client Info Layout ---
    client_info_widget = QWidget()
    client_info_layout_inner = QHBoxLayout(client_info_widget)

    edit_client_button = QPushButton(client_info_widget)
    edit_client_button.setIcon(QIcon("assets/edit client button.png"))
    edit_client_button.setIconSize(QSize(30, 30))
    edit_client_button.setFixedSize(90, 60)
    edit_client_button.setStyleSheet("background-color: #FED766; border: none;")
    if user_role and user_role.lower() == "veterinarian":
        edit_client_button.hide()

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
    client_list.setStyleSheet("background-color: #102547; font-family: Poppins;")
    client_list.setAlignment(Qt.AlignVCenter)

    # --- add client button --- #

    add_button = QPushButton("Add Client", content)
    add_button.setObjectName("AddClientButton")
    add_button.setFixedSize(60, 40)
    add_button.setStyleSheet(
        "background-color: #F4F4F8; border: none; border-radius: 20px; margin-bottom: 5px; font-family: Lato;"
    )
    if user_role and user_role.lower() == "veterinarian":
        add_button.hide()

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
    table.setFixedHeight(557)
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
            font-family: Lato;
            outline: none;  /* Remove the focus outline */
        }
                        
        QTableWidget::item {
            border-bottom: 1px solid gray; 
            padding-left: 20px;  /* Adds space between text and left border */
            padding-right: 10px;
            padding-top: -5px;
            padding-bottom: 5px;
            background-color: transparent;
        }
                               
        QTableWidget::item:selected {
            background-color: #CFDEF3;  /* Light cyan highlight */
            color: black;
            border: none;
            outline: none;  /* Remove the focus outline */
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
    client_info_layout.setSpacing(1)  # Increased spacing between fields

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
    if user_role and user_role.lower() == "veterinarian":
        edit_client_button.hide()

    edit_client_button.clicked.connect(open_edit_form)  # 🛠️ Connect it here!

    client_info_layout_inner.addWidget(client_info_label)
    client_info_layout_inner.addStretch()  # push edit button to the right
    client_info_layout_inner.addWidget(edit_client_button)

    client_info_layout.addWidget(client_info_widget)

    labels = ["Control Number:", "Name:", "Address:", "Contact Number:", "Email Address:"]
    label_names = ["ControlNumberLabel", "NameLabel", "AddressLabel", "ContactLabel", "EmailLabel"]
    input_names = ["ControlNumberInput", "NameInput", "AddressInput", "ContactInput", "EmailInput"]

    for i, (text, label_name, input_name) in enumerate(zip(labels, label_names, input_names)):
        pair_layout = QHBoxLayout()

        label = QLabel(text, client_info_view)
        label.setObjectName(label_name)
        label.setFixedWidth(180)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #012547; font-family: Poppins;")

        input_field = QLineEdit(client_info_view)
        input_field.setObjectName(input_name)
        input_field.setMinimumWidth(250)
        input_field.setReadOnly(True)
        input_field.setStyleSheet("font-size: 16px; color: #000; font-family: Poppins; background: transparent; border: none;")

        pair_layout.addWidget(label)
        pair_layout.addWidget(input_field)
        pair_layout.addStretch()  # optional, pushes input field left if there's space

        client_info_layout.addLayout(pair_layout)

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
    edit_pet_button.setStyleSheet("""
        QPushButton {
            background-color: #FED766; 
            border: none;
        }
        QPushButton:selected {
            outline: none;
        }
    """)
    if user_role and user_role.lower() == "veterinarian":
        edit_pet_button.hide()

    pet_info_layout.addWidget(pet_info_label)
    pet_info_layout.addStretch()  # Add stretch to push arrows and button to the right
    pet_info_layout.addWidget(edit_pet_button)
    client_info_layout.addWidget(pet_info_widget)

    pet_picture = QLabel()
    pet_picture.setFixedSize(120, 120)
    pet_picture.setAlignment(Qt.AlignCenter)
    pet_picture.setStyleSheet("background-color: white; border-radius: 10px;")
    pet_picture.setText("No Photo")


   # Scroll area setup
    scroll_area = QScrollArea(client_info_view)
    scroll_area.setWidgetResizable(True)
    scroll_area.setFixedHeight(300)
    scroll_area.setStyleSheet("""
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 10px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #012547;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """)
    
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)
    scroll_layout.setSpacing(10)
    scroll_layout.setContentsMargins(0, 0, 0, 0)
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
        # Create a vertical layout for each field
        field_layout = QVBoxLayout()
        field_layout.setSpacing(0)  # Space between label and input
        
        # Create and style the label
        label = QLabel(field)
        label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #012547;
            margin-left: 10px;
            font-family: Poppins;
        """)
        
        # Create and style the input field
        line_edit = QLineEdit(edit_fields_widget)
        line_edit.setPlaceholderText(f"Enter {field}")
        line_edit.setStyleSheet("padding: 15px; margin: 10px; background-color: #f4f4f8; border: 1px solid gray; border-radius: 5px; font-size: 14px;")
        
        # Add label and input to the field layout
        field_layout.addWidget(label)
        field_layout.addWidget(line_edit)
        
        # Add the field layout to the main layout
        edit_fields_layout.addLayout(field_layout)

    edit_form_layout.addWidget(edit_fields_widget)

    button_layout = QHBoxLayout()
    button_layout.addStretch()

    cancel_button = QPushButton("Cancel", edit_form_widget)  # Set parent
    cancel_button.setFixedSize(40, 40)
    cancel_button.setStyleSheet("background-color: #f4f4f8; border-radius:20px; font-family: Lato; color: black; font-size: 12px;")

    save_button = QPushButton("Save", edit_form_widget)  # Set parent
    save_button.setFixedSize(40, 40)
    save_button.setStyleSheet("background-color: #012547; border-radius:20px; font-family: Lato; color: white; margin-right:90px; font-size: 12px;")

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

    # Create pet fields layout
    pets_fields_widget = QWidget(pets_edit_widget)  # Set parent
    pets_fields_layout = QVBoxLayout(pets_fields_widget)
    pets_fields_layout.setContentsMargins(80, 5, 80, 5)
    pets_fields_layout.setSpacing(5)  # Adjust this value to change spacing between fields

    # Add the fields widget to the main layout
    pets_edit_layout.addWidget(pets_fields_widget)

    # Row 1: Name, Gender, Birthdate, Age
    row1 = QHBoxLayout()
    
    # Name field with label
    name_field_layout = QVBoxLayout()
    name_label = QLabel("Name")
    name_label.setStyleSheet("""
        font-size: 14px;
        font-weight: bold;
        color: #012547;
        margin-left: 0px;
        font-family: Poppins;
    """)
    name_input = QLineEdit(pets_fields_widget)
    name_input.setPlaceholderText("Enter Name")
    name_input.setMinimumHeight(35)
    name_input.setStyleSheet("""
        padding: 8px;
        background-color: #f4f4f8;
        border: 1px solid gray;
        border-radius: 5px;
        font-size: 12px;
    """)
    name_field_layout.addWidget(name_label)
    name_field_layout.addWidget(name_input)
    row1.addLayout(name_field_layout)

    # Gender field with label
    gender_field_layout = QVBoxLayout()
    gender_label = QLabel("Gender")
    gender_label.setStyleSheet("""
        font-size: 14px;
        font-weight: bold;
        color: #012547;
        margin-left: 0px;
        font-family: Poppins;
    """)
    pet_gender = QComboBox(pets_fields_widget)
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
    gender_field_layout.addWidget(gender_label)
    gender_field_layout.addWidget(pet_gender)
    row1.addLayout(gender_field_layout)

    # Birthdate field with label
    birthdate_field_layout = QVBoxLayout()
    birthdate_label = QLabel("Birthdate")
    birthdate_label.setStyleSheet("""
        font-size: 14px;
        font-weight: bold;
        color: #012547;
        margin-left: 0px;
        font-family: Poppins;
    """)
    birthdate_input = QLineEdit(pets_fields_widget)
    birthdate_input.setPlaceholderText("yyyy-MM-dd")
    birthdate_input.setMinimumHeight(35)
    birthdate_input.setFixedWidth(120)
    birthdate_input.setStyleSheet("""
        padding: 8px;
        background-color: #f4f4f8;
        border: 1px solid gray;
        border-radius: 5px;
        font-size: 12px;
    """)
    birthdate_field_layout.addWidget(birthdate_label)
    birthdate_field_layout.addWidget(birthdate_input)
    row1.addLayout(birthdate_field_layout)

    # Age field with label
    age_field_layout = QVBoxLayout()
    age_label = QLabel("Age")
    age_label.setStyleSheet("""
        font-size: 14px;
        font-weight: bold;
        color: #012547;
        margin-left: 0px;
        font-family: Poppins;
    """)
    age_input = QLineEdit(pets_fields_widget)
    age_input.setPlaceholderText("")
    age_input.setMinimumHeight(35)
    age_input.setReadOnly(True)  # Make it read-only since it's auto-computed
    age_input.setStyleSheet("""
        padding: 8px;
        background-color: #f4f4f8;
        border: 1px solid gray;
        border-radius: 5px;
        font-size: 12px;
        color: #666;  /* Gray color to indicate it's read-only */
    """)
    age_field_layout.addWidget(age_label)
    age_field_layout.addWidget(age_input)
    row1.addLayout(age_field_layout)

    # Function to calculate age from birthdate
    def calculate_age():
        try:
            birthdate = QDate.fromString(birthdate_input.text(), "yyyy-MM-dd")
            if not birthdate.isValid():
                age_input.setText("")
                return
                
            today = QDate.currentDate()
            
            years = today.year() - birthdate.year()
            months = today.month() - birthdate.month()
            
            # Adjust for days of the month
            if today.day() < birthdate.day():
                months -= 1
                
            if months < 0:
                years -= 1
                months += 12
                
            # Calculate total days
            days = birthdate.daysTo(today)
            weeks = days // 7
                
            # Format age text based on age
            if years >= 1:
                age_text = f"{years} year{'s' if years > 1 else ''}"
            elif months >= 1:
                age_text = f"{months} month{'s' if months > 1 else ''}"
            else:
                age_text = f"{weeks} week{'s' if weeks > 1 else ''}"
                
            age_input.setText(age_text)
            
            # Store the actual age in years for database
            age_input.setProperty("years", years)
            age_input.setProperty("months", months)
            age_input.setProperty("weeks", weeks)
        except:
            age_input.setText("")

    # Connect birthdate changes to age calculation
    birthdate_input.textChanged.connect(calculate_age)
    
    # Calculate initial age
    calculate_age()

    pets_fields_layout.addLayout(row1)

    # Row 2: Species, Breed
    row2 = QHBoxLayout()
    
    # Species field with label
    species_field_layout = QVBoxLayout()
    species_label = QLabel("Species")
    species_label.setStyleSheet("""
        font-size: 14px;
        font-weight: bold;
        color: #012547;
        margin-left: 0px;
        font-family: Poppins;
    """)
    species_input = QLineEdit(pets_fields_widget)
    species_input.setPlaceholderText("Enter Species")
    species_input.setMinimumHeight(35)
    species_input.setStyleSheet("""
        padding: 8px;
        background-color: #f4f4f8;
        border: 1px solid gray;
        border-radius: 5px;
        font-size: 12px;
    """)
    species_field_layout.addWidget(species_label)
    species_field_layout.addWidget(species_input)
    row2.addLayout(species_field_layout)

    # Breed field with label
    breed_field_layout = QVBoxLayout()
    breed_label = QLabel("Breed")
    breed_label.setStyleSheet("""
        font-size: 14px;
        font-weight: bold;
        color: #012547;
        margin-left: 0px;
        font-family: Poppins;
    """)
    breed_input = QLineEdit(pets_fields_widget)
    breed_input.setPlaceholderText("Enter Breed")
    breed_input.setMinimumHeight(35)
    breed_input.setStyleSheet("""
        padding: 8px;
        background-color: #f4f4f8;
        border: 1px solid gray;
        border-radius: 5px;
        font-size: 12px;
    """)
    breed_field_layout.addWidget(breed_label)
    breed_field_layout.addWidget(breed_input)
    row2.addLayout(breed_field_layout)

    pets_fields_layout.addLayout(row2)

    # Row 3: Weight, Height
    row3 = QHBoxLayout()
    
    # Weight field with label
    weight_field_layout = QVBoxLayout()
    weight_label = QLabel("Weight")
    weight_label.setStyleSheet("""
        font-size: 14px;
        font-weight: bold;
        color: #012547;
        margin-left: 0px;
        font-family: Poppins;
    """)
    weight_input = QLineEdit(pets_fields_widget)
    weight_input.setPlaceholderText("Enter Weight (kg)")
    weight_input.setMinimumHeight(35)
    weight_input.setStyleSheet("""
        padding: 8px;
        background-color: #f4f4f8;
        border: 1px solid gray;
        border-radius: 5px;
        font-size: 12px;
    """)
    weight_field_layout.addWidget(weight_label)
    weight_field_layout.addWidget(weight_input)
    row3.addLayout(weight_field_layout)
    
    # Height field with label
    height_field_layout = QVBoxLayout()
    height_label = QLabel("Height")
    height_label.setStyleSheet("""
        font-size: 14px;
        font-weight: bold;
        color: #012547;
        margin-left: 0px;
        font-family: Poppins;
    """)
    height_input = QLineEdit(pets_fields_widget)
    height_input.setPlaceholderText("Enter Height (in)")
    height_input.setMinimumHeight(35)
    height_input.setStyleSheet("""
        padding: 8px;
        background-color: #f4f4f8;
        border: 1px solid gray;
        border-radius: 5px;
        font-size: 12px;
    """)
    height_field_layout.addWidget(height_label)
    height_field_layout.addWidget(height_input)
    row3.addLayout(height_field_layout)
    
    pets_fields_layout.addLayout(row3)

    # Color field with label
    color_field_layout = QVBoxLayout()
    color_label = QLabel("Color")
    color_label.setStyleSheet("""
        font-size: 14px;
        font-weight: bold;
        color: #012547;
        margin-left: 0px;
        font-family: Poppins;
    """)
    color_input = QLineEdit(pets_fields_widget)
    color_input.setPlaceholderText("Enter Color")
    color_input.setMinimumHeight(35)
    color_input.setStyleSheet("""
        padding: 8px;
        background-color: #f4f4f8;
        border: 1px solid gray;
        border-radius: 5px;
        font-size: 12px;
    """)
    color_field_layout.addWidget(color_label)
    color_field_layout.addWidget(color_input)
    pets_fields_layout.addLayout(color_field_layout)

    # Photo upload and preview
    photo_layout = QHBoxLayout()
    photo_layout.setContentsMargins(0, 1, 0, 0)
    
    # Upload photo button
    upload_photo_button = QPushButton("Upload Photo", pets_fields_widget)
    upload_photo_button.setFixedWidth(120)
    upload_photo_button.setStyleSheet("""
        background-color: white; 
        color: black; 
        border: 1px solid black;
        border-radius: 5px; 
        font-size: 14px; 
        padding: 5px;
        font-family: Lato;
    """)
    
    # Photo preview label
    pet_picture = QLabel()
    pet_picture.setFixedSize(120, 120)
    pet_picture.setAlignment(Qt.AlignCenter)
    pet_picture.setStyleSheet("""
        QLabel {
            background-color: white;
        }
    """)
    pet_picture.setText("No Photo")
    
    # Connect upload button to photo selection
    def select_photo():
        file_name, _ = QFileDialog.getOpenFileName(
            pets_edit_widget,
            "Select Pet Photo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            pet_picture.setPixmap(QPixmap(file_name).scaled(
                120, 120,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
            pet_picture.setProperty("photo_path", file_name)
    
    upload_photo_button.clicked.connect(select_photo)
    
    photo_layout.addWidget(upload_photo_button)
    photo_layout.addWidget(pet_picture)
    photo_layout.addStretch()
    
    pets_fields_layout.addLayout(photo_layout)

    # Button row layout
    pets_button_row = QHBoxLayout()
    pets_button_row.setContentsMargins(0, 1, 100, 0)  # Move buttons to the left
    pets_button_row.addStretch()

    # Cancel button
    pets_cancel_btn = QPushButton("Cancel", pets_edit_widget)  # Set parent
    pets_cancel_btn.setFixedSize(40, 40)
    pets_cancel_btn.setStyleSheet("""
        background-color: #F4F4F8; 
        border-radius: 20px; 
        font-size: 12px;
        color: #000; 
        font-family: Lato;
    """)

    # Save button
    pets_save_btn = QPushButton("Save", pets_edit_widget)  # Set parent
    pets_save_btn.setFixedSize(40, 40)
    pets_save_btn.setStyleSheet("""
        background-color: #012547; 
        color: white; 
        font-family: Lato; 
        font-size: 10px; 
        font-weight: 700; 
        border-radius: 15px; 
        padding: 0;
        margin: 0;
        font-family: Lato;
    """)

    # Add buttons to layout
    pets_button_row.addWidget(pets_cancel_btn)
    pets_button_row.addWidget(pets_save_btn)
    pets_edit_layout.addLayout(pets_button_row)
    pets_edit_layout.addStretch()

    # --- Hook up button functionality ---
    def save_pet_data():
        """Save the pet data from the form."""
        print("Starting save_pet_data function...")
        
        name = name_input.text().strip()
        gender = pet_gender.currentText()
        species = species_input.text().strip()
        breed = breed_input.text().strip()
        color = color_input.text().strip()
        birthdate = birthdate_input.text().strip()
        age = age_input.property("years")
        weight = weight_input.text().strip()
        height = height_input.text().strip()

        print(f"Form data collected: name={name}, gender={gender}, species={species}, breed={breed}, color={color}, birthdate={birthdate}, age={age}, weight={weight}, height={height}")

        if not all([name, species, breed, color, birthdate, weight, height]):
            show_message(pets_edit_widget, "All fields are required!", QMessageBox.Warning)
            return

        # Validate birthdate format
        try:
            QDate.fromString(birthdate, "yyyy-MM-dd")
        except:
            show_message(pets_edit_widget, "Invalid birthdate format! Use yyyy-MM-dd", QMessageBox.Warning)
            return

        # Validate age
        if age is None or not isinstance(age, int):
            show_message(pets_edit_widget, "Invalid age value!", QMessageBox.Warning)
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

        # Get the client email from the selected client
        client_email = edit_form_widget.property("original_email")
        print(f"Initial client_email from property: {client_email}")
        
        if not client_email:
            # Try to get the email from the client info view
            email_input = client_info_view.findChild(QLineEdit, "EmailInput")
            if email_input:
                client_email = email_input.text().strip()
                print(f"Got client_email from EmailInput: {client_email}")
            
        if not client_email:
            show_message(pets_edit_widget, "No client selected for adding a pet!", QMessageBox.Warning)
            return

        db = Database()
        try:
            # Get client_id
            print(f"Querying database for client_id with email: {client_email}")
            db.cursor.execute("SELECT client_id FROM clients WHERE email = ?", (client_email,))
            result = db.cursor.fetchone()
            if not result:
                show_message(pets_edit_widget, "No client found with the provided email!", QMessageBox.Warning)
                return
            client_id = result[0]
            print(f"Found client_id: {client_id}")

            # Get the photo path from the pet_picture label
            photo_path = pet_picture.property("photo_path")
            print(f"Photo path: {photo_path}")

            mode = pets_edit_widget.property("mode")
            print(f"Current mode: {mode}")

            # If mode is None, default to "add" mode
            if mode is None:
                mode = "add"
                print("Mode was None, defaulting to add mode")

            if mode == "add":
                print("Attempting to add new pet...")
                # Check if pet with same name already exists for this client
                db.cursor.execute("""
                    SELECT COUNT(*) FROM pets 
                    WHERE name = ? AND client_id = ?
                """, (name, client_id))
                if db.cursor.fetchone()[0] > 0:
                    show_message(pets_edit_widget, "A pet with this name already exists for this client!", QMessageBox.Warning)
                    return

                # Insert new pet
                print("Inserting new pet into database...")
                db.cursor.execute("""
                    INSERT INTO pets (name, gender, species, breed, color, birthdate, age, weight, height, photo_path, client_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, gender, species, breed, color, birthdate, age, weight_float, height_float, photo_path, client_id))
                db.conn.commit()
                print("Pet successfully added to database")
                show_message(pets_edit_widget, "New pet added successfully!")
            elif mode == "edit":
                print("Attempting to update existing pet...")
                # Get the current pet name for updating
                current_pet_name = pet_info_widget.property("pets")[pet_info_widget.property("current_index")][0]
                print(f"Updating pet: {current_pet_name}")
                
                # Update existing pet
                db.cursor.execute("""
                    UPDATE pets 
                    SET name = ?, gender = ?, species = ?, breed = ?, color = ?, birthdate = ?, age = ?, weight = ?, height = ?, photo_path = ?
                    WHERE name = ? AND client_id = ?
                """, (name, gender, species, breed, color, birthdate, age, weight_float, height_float, photo_path, current_pet_name, client_id))
                db.conn.commit()
                print("Pet successfully updated in database")
                show_message(pets_edit_widget, "Pet updated successfully!")

            # Update the pet info display
            print("Updating pet info display...")
            update_pet_info(client_email)
            
            # Clear the form and switch back to view mode
            print("Clearing form and switching to view mode...")
            name_input.clear()
            age_input.clear()
            species_input.clear()
            breed_input.clear()
            color_input.clear()
            weight_input.clear()
            height_input.clear()
            birthdate_input.clear()
            birthdate_input.setPlaceholderText("yyyy-MM-dd")
            pet_gender.setCurrentIndex(0)
            pet_picture.setPixmap(QPixmap())
            pet_picture.setText("No Photo")
            pet_picture.setProperty("photo_path", None)
            
            client_info_stack.setCurrentIndex(0)
            print("Save process completed successfully")

        except Exception as e:
            print(f"Error occurred while saving pet: {str(e)}")
            show_message(pets_edit_widget, f"Failed to save pet data: {e}", QMessageBox.Critical)
        finally:
            db.close_connection()
            print("Database connection closed")

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
        birthdate_input.clear()
        birthdate_input.setPlaceholderText("yyyy-MM-dd")
        pet_gender.setCurrentIndex(0)
        pet_picture.setPixmap(QPixmap())
        pet_picture.setText("No Photo")
        pet_picture.setProperty("photo_path", None)
        
        # Set the form mode to add
        pets_edit_widget.setProperty("mode", "add")
        print("Set form mode to: add")
        
        # Hide delete button in add mode
        pets_delete_btn.hide()
        
        # Clear any stored pet data
        pet_info_widget.setProperty("pets", None)
        pet_info_widget.setProperty("current_index", None)

        client_info_stack.setCurrentIndex(2)

    save_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))
    cancel_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))

    edit_pet_button.clicked.connect(open_add_pet_form)
    pets_save_btn.clicked.connect(save_pet_data)
    
    # Define cancel handler for pet form
    def handle_pet_cancel():
        # Clear all form fields
        name_input.clear()
        age_input.clear()
        species_input.clear()
        breed_input.clear()
        color_input.clear()
        weight_input.clear()
        height_input.clear()
        birthdate_input.clear()
        birthdate_input.setPlaceholderText("yyyy-MM-dd")
        pet_gender.setCurrentIndex(0)
        pet_picture.setPixmap(QPixmap())
        pet_picture.setText("No Photo")
        pet_picture.setProperty("photo_path", None)
        
        # Clear stored pet data
        pet_info_widget.setProperty("pets", None)
        pet_info_widget.setProperty("current_index", None)
        
        # Switch back to view mode
        client_info_stack.setCurrentIndex(0)
    
    # Connect cancel button to handler
    pets_cancel_btn.clicked.connect(handle_pet_cancel)

    client_info_stack.addWidget(client_info_view)
    client_info_stack.addWidget(edit_form_widget)
    client_info_stack.addWidget(pets_edit_widget)
    client_info_stack.setCurrentIndex(0)
    table_info_layout.addWidget(client_info_stack_widget)
    main_layout.addLayout(table_info_layout)

    button_layout = QHBoxLayout()
    button_layout.setContentsMargins(0, 1, 0, 20)  # Adjust margins
    button_layout.setSpacing(10)  # Add spacing between buttons

    # Force layout update
    content.update()

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
            name_label.setStyleSheet("color: black; font-family: Lato; font-size: 14px; background-color: transparent;")
            cell_layout.addWidget(name_label)

            cell_layout.addStretch()

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("assets/trash-can.png"))
            delete_button.setObjectName("DeleteButton")
            
            # Hide delete button for veterinarians
            if user_role and user_role.lower() == "veterinarian":
                delete_button.hide()

            delete_button.clicked.connect(lambda _, email=client_email: delete_client(email))
            cell_layout.addWidget(delete_button)

            table.setCellWidget(row, 0, cell_widget)
                
    def delete_client(email):
        """Delete a client from the database with confirmation."""
        confirmation = create_styled_message_box(
            QMessageBox.Question,
            "Delete Client",
            f"Are you sure you want to delete the client with email: {email}?"
        )
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)

        response = confirmation.exec()
        if response == QMessageBox.Yes:
            db = Database()
            try:
                db.cursor.execute("DELETE FROM clients WHERE email = ?", (email,))
                db.conn.commit()
                show_message(content, f"Client with email {email} deleted successfully.")
                
                # Clear client information display
                name_input = client_info_view.findChild(QLineEdit, "NameInput")
                control_number_input = client_info_view.findChild(QLineEdit, "ControlNumberInput")
                address_input = client_info_view.findChild(QLineEdit, "AddressInput")
                contact_input = client_info_view.findChild(QLineEdit, "ContactInput")
                email_input = client_info_view.findChild(QLineEdit, "EmailInput")
                
                if name_input: name_input.clear()
                if control_number_input: control_number_input.clear()
                if address_input: address_input.clear()
                if contact_input: contact_input.clear()
                if email_input: email_input.clear()
                
                # Clear pet information display
                while scroll_layout.count():
                    child = scroll_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                
                # Update the client table
                update_client_table()
                
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
        try:
            db.cursor.execute("SELECT name, control_number, address, contact_number, email FROM clients WHERE email = ?", (email,))
            client_data = db.cursor.fetchone()
        except Exception as e:
            print(f"❌ Error fetching client data: {e}")
            return
        finally:
            db.close_connection()

        if client_data:
            name, control_number, address, contact_number, email = client_data

            # Find the input fields
            name_input = client_info_view.findChild(QLineEdit, "NameInput")
            control_number_input = client_info_view.findChild(QLineEdit, "ControlNumberInput")
            address_input = client_info_view.findChild(QLineEdit, "AddressInput")
            contact_input = client_info_view.findChild(QLineEdit, "ContactInput")
            email_input = client_info_view.findChild(QLineEdit, "EmailInput")

            # Update the input fields
            if name_input:
                name_input.setText(name)
            if control_number_input:
                control_number_input.setText(control_number)
            if address_input:
                address_input.setText(address)
            if contact_input:
                contact_input.setText(contact_number)
            if email_input:
                email_input.setText(email)
                
    def update_pet_info(client_email=None):
        """Update the pet info section with either all pets or filtered by client."""
        db = Database()
        try:
            if client_email:
                # Get client_id for filtering
                db.cursor.execute("SELECT client_id FROM clients WHERE email = ?", (client_email,))
                result = db.cursor.fetchone()
                
                if not result:
                    print("❌ No client found with email")
                    return
                client_id = result[0]
                print(f"✅ Retrieved client_id: {client_id}")

                # Fetch pets for specific client
                db.cursor.execute("""
                    SELECT name, gender, species, breed, color, birthdate, age, weight, height, photo_path
                    FROM pets
                    WHERE client_id = ?
                """, (client_id,))
            else:
                # Fetch all pets
                db.cursor.execute("""
                    SELECT name, gender, species, breed, color, birthdate, age, weight, height, photo_path
                    FROM pets
                """)

            pets = db.cursor.fetchall()

            # Clear existing widgets in the scroll layout
            while scroll_layout.count():
                child = scroll_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            if pets:
                # Create cards for all pets and add to scroll area
                for index, pet in enumerate(pets):
                    pet_card = create_pet_card(pet, index, user_role)
                    scroll_layout.addWidget(pet_card)
                    
                    # Add separator after each pet card except the last one
                    if index < len(pets) - 1:
                        separator = QFrame()
                        separator.setFrameShape(QFrame.HLine)
                        separator.setStyleSheet("background-color: #012547;")
                        separator.setFixedHeight(3)
                        scroll_layout.addWidget(separator)
            else:
                no_pet_label = QLabel("No pets found.")
                no_pet_label.setAlignment(Qt.AlignCenter)
                scroll_layout.addWidget(no_pet_label)

        except Exception as e:
            print(f"❌ Error fetching pets: {e}")
            return
        finally:
            db.close_connection()

    def handle_update_pet(pet_data, index):
        """Handle updating a pet's information."""
        # Store the pet data and index in the widget's properties
        pet_info_widget.setProperty("pets", [pet_data])  # Store as a list with single item
        pet_info_widget.setProperty("current_index", 0)  # Index will always be 0 since we store single item
        
        # Open the edit form with the pet data
        open_edit_pet_form(pet_data)

    def open_edit_pet_form(pet_data):
        """Open the form to edit the currently selected pet."""
        # Fill the input fields with existing pet data
        name_input.setText(pet_data[0])
        pet_gender.setCurrentText(pet_data[1])
        species_input.setText(pet_data[2])
        breed_input.setText(pet_data[3])
        color_input.setText(pet_data[4])
        # Convert date to string format
        birthdate_input.setText(pet_data[5].toString("yyyy-MM-dd") if isinstance(pet_data[5], QDate) else str(pet_data[5]))
        age_input.setText(str(pet_data[6]))
        weight_input.setText(str(pet_data[7]))
        height_input.setText(str(pet_data[8]))  # Display height as is, in inches

        # Set the photo preview in pet_picture
        photo_path = pet_data[9]
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

        pets_edit_widget.setProperty("mode", "edit")  # Mark as editing mode
        
        # Show delete button in edit mode only if not veterinarian
        if user_role and user_role.lower() == "veterinarian":
            pets_delete_btn.hide()
        else:
            pets_delete_btn.show()
        
        # Add cancel button handler
        def handle_cancel():
            # Clear all form fields
            name_input.clear()
            age_input.clear()
            species_input.clear()
            breed_input.clear()
            color_input.clear()
            weight_input.clear()
            height_input.clear()
            birthdate_input.clear()
            birthdate_input.setPlaceholderText("yyyy-MM-dd")
            pet_gender.setCurrentIndex(0)
            pet_picture.setPixmap(QPixmap())
            pet_picture.setText("No Photo")
            pet_picture.setProperty("photo_path", None)
            
            # Clear stored pet data
            pet_info_widget.setProperty("pets", None)
            pet_info_widget.setProperty("current_index", None)
            
            # Switch back to view mode
            client_info_stack.setCurrentIndex(0)
        
        # Connect cancel button to handler
        cancel_btn = pets_edit_widget.findChild(QPushButton, "cancel_btn")
        if cancel_btn:
            cancel_btn.clicked.disconnect()  # Disconnect any existing connections
            cancel_btn.clicked.connect(handle_cancel)
        
        client_info_stack.setCurrentIndex(2)  # Switch to pet form

    def create_pet_card(pet_data, index, user_role=None):
            pet_card = QWidget()
            pet_card.setFixedHeight(160)
            pet_card_layout = QHBoxLayout(pet_card)
            pet_card_layout.setContentsMargins(10, 0, 20, 0)
            pet_card_layout.setSpacing(20)  # Increased spacing from 10 to 20 pixels

            pet_card.setStyleSheet("background-color: white; border-radius: 20px;")

            # 📷 Pet photo on the left
            pet_card_picture = QLabel()
            pet_card_picture.setFixedSize(150, 150)
            pet_card_picture.setAlignment(Qt.AlignCenter)
            pet_card_picture.setStyleSheet("""
                QLabel {
                    background-color: white;
                    border-radius: 75px;  /* Half of width/height for perfect circle */
                    border: 2px solid #012547;
                }
            """)

            # Extract photo path from the last element of pet_data
            photo_path = pet_data[-1]  # Get the last element which should be the photo path
            if photo_path:
                # Create a circular pixmap
                pixmap = QPixmap(photo_path)
                circular_pixmap = QPixmap(150, 150)
                circular_pixmap.fill(Qt.transparent)
                
                # Create a painter to draw the circular mask
                painter = QPainter(circular_pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                
                # Create a circular path
                path = QPainterPath()
                path.addEllipse(0, 0, 150, 150)
                painter.setClipPath(path)
                
                # Calculate scaling to fill the circle
                scaled_pixmap = pixmap.scaled(
                    150, 150,
                    Qt.KeepAspectRatioByExpanding,  # Changed to fill mode
                    Qt.SmoothTransformation
                )
                
                # Center the scaled pixmap
                x = (150 - scaled_pixmap.width()) // 2
                y = (150 - scaled_pixmap.height()) // 2
                
                # Draw the scaled pixmap centered
                painter.drawPixmap(x, y, scaled_pixmap)
                painter.end()
                
                pet_card_picture.setPixmap(circular_pixmap)
            else:
                pet_card_picture.setText("No Photo")
                pet_card_picture.setStyleSheet("""
                    QLabel {
                        background-color: white;
                        border-radius: 75px;
                        border: 2px solid #012547;
                        color: #012547;
                        font-weight: bold;
                        font-family: Lato;
                    }
                """)

            # 📄 Pet info in the middle (two columns)
            pet_info_widget = QWidget()
            pet_info_main_layout = QHBoxLayout(pet_info_widget)
            pet_info_main_layout.setContentsMargins(0, 0, 0, 0)
            pet_info_main_layout.setSpacing(20)

            left_column = QVBoxLayout()
            right_column = QVBoxLayout()
            left_column.setSpacing(2)
            right_column.setSpacing(2)

            # Define the fields and their corresponding indices in pet_data
            fields = [
                ("Name", 0),
                ("Gender", 1),
                ("Species", 2),
                ("Breed", 3),
                ("Color", 4),
                ("Birthdate", 5),
                ("Age", 6),
                ("Weight", 7),
                ("Height", 8)
            ]

            # Split fields into two columns
            mid = (len(fields) + 1) // 2
            left_fields = fields[:mid]
            right_fields = fields[mid:]

            for label_text, index in left_fields:
                row_layout = QHBoxLayout()
                value = pet_data[index]
                label = QLabel(f"{label_text}:")
                label.setStyleSheet("font-weight: bold; font-family: Lato;")
                label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                
                # Format value based on field type
                if label_text == "Age" and value is not None:
                    try:
                        # Convert age to float first to handle decimal values
                        age_value = float(value)
                        if age_value >= 1:
                            value = f"{int(age_value)} year{'s' if age_value > 1 else ''}"
                        else:
                            # Calculate months (multiply by 12 since age is in years)
                            months = int(age_value * 12)
                            if months >= 1:
                                value = f"{months} month{'s' if months > 1 else ''}"
                            else:
                                # Calculate weeks (multiply by 52 since age is in years)
                                weeks = int(age_value * 52)
                                value = f"{weeks} week{'s' if weeks > 1 else ''}"
                    except (ValueError, TypeError):
                        value = "N/A"
                elif label_text == "Weight" and value is not None:
                    try:
                        value = f"{float(value):.2f} kg"
                    except (ValueError, TypeError):
                        value = "N/A"
                elif label_text == "Height" and value is not None:
                    try:
                        value = f"{float(value):.2f} in"
                    except (ValueError, TypeError):
                        value = "N/A"
                
                value_label = QLabel(str(value))
                value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                label.setFixedWidth(80)
                row_layout.addWidget(label)
                row_layout.addWidget(value_label)
                row_layout.addStretch()
                left_column.addLayout(row_layout)

            for label_text, index in right_fields:
                row_layout = QHBoxLayout()
                value = pet_data[index]
                label = QLabel(f"{label_text}:")
                label.setStyleSheet("font-weight: bold; font-family: Lato;")
                label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                
                # Format value based on field type
                if label_text == "Age" and value is not None:
                    try:
                        # Convert age to float first to handle decimal values
                        age_value = float(value)
                        if age_value >= 1:
                            value = f"{int(age_value)} year{'s' if age_value > 1 else ''}"
                        else:
                            # Calculate months (multiply by 12 since age is in years)
                            months = int(age_value * 12)
                            if months >= 1:
                                value = f"{months} month{'s' if months > 1 else ''}"
                            else:
                                # Calculate weeks (multiply by 52 since age is in years)
                                weeks = int(age_value * 52)
                                value = f"{weeks} week{'s' if weeks > 1 else ''}"
                    except (ValueError, TypeError):
                        value = "N/A"
                elif label_text == "Weight" and value is not None:
                    try:
                        value = f"{float(value):.2f} kg"
                    except (ValueError, TypeError):
                        value = "N/A"
                elif label_text == "Height" and value is not None:
                    try:
                        value = f"{float(value):.2f} in"
                    except (ValueError, TypeError):
                        value = "N/A"
                
                value_label = QLabel(str(value))
                value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                label.setFixedWidth(80)
                row_layout.addWidget(label)
                row_layout.addWidget(value_label)
                row_layout.addStretch()
                right_column.addLayout(row_layout)

            pet_info_main_layout.addLayout(left_column)
            pet_info_main_layout.addLayout(right_column)

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

            # Hide "See Records" button for Receptionist
            if user_role and user_role.lower() == "receptionist":
                see_records_button.hide()

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
        font-size: 12px;
        color: white; 
        font-family: Lato;
    """)

    # Hide delete button for veterinarians
    if user_role and user_role.lower() == "veterinarian":
        pets_delete_btn.hide()

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
                    # Store the selected client email in the main window
                    main_window = table.window()
                    if hasattr(main_window, 'selected_client_email'):
                        main_window.selected_client_email = email
                    update_client_info(email)
                    update_pet_info(email)  # Update pets for selected client
                    edit_form_widget.setProperty("original_email", email)  # Remember client email for pets
                    
                    # Show the edit client button and add pet button only if not veterinarian
                    if user_role and user_role.lower() == "veterinarian":
                        edit_client_button.hide()
                        edit_pet_button.hide()
                    else:
                        edit_client_button.show()
                        edit_pet_button.show()
        else:
            # If no client is selected, show all pets
            update_pet_info(None)
            edit_form_widget.setProperty("original_email", None)
            
            # Hide the edit client button and add pet button
            edit_client_button.hide()
            edit_pet_button.hide()
            
            # Clear client information display
            name_input = client_info_view.findChild(QLineEdit, "NameInput")
            control_number_input = client_info_view.findChild(QLineEdit, "ControlNumberInput")
            address_input = client_info_view.findChild(QLineEdit, "AddressInput")
            contact_input = client_info_view.findChild(QLineEdit, "ContactInput")
            email_input = client_info_view.findChild(QLineEdit, "EmailInput")
            
            if name_input: name_input.clear()
            if control_number_input: control_number_input.clear()
            if address_input: address_input.clear()
            if contact_input: contact_input.clear()
            if email_input: email_input.clear()

    # Initially hide the edit client button and add pet button
    edit_client_button.hide()
    edit_pet_button.hide()

    # Connect the table's cell click signal to the function
    table.cellClicked.connect(lambda row, column: on_client_selected(row, column, table))

    # Add the layout to the main layout
    main_layout.addLayout(table_info_layout)
        
    # Update the client table
    update_client_table()

    # Initial load of all pets
    update_pet_info(None)

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

            try:
                db = Database()
                # Check if we are editing an existing client or adding a new one
                original_email = edit_form_widget.property("original_email")
                if original_email:  # Edit mode
                    # Get the client_id first
                    db.cursor.execute("SELECT client_id FROM clients WHERE email = ?", (original_email,))
                    result = db.cursor.fetchone()
                    if not result:
                        show_message(content, "Client not found!", QMessageBox.Warning)
                        return
                    client_id = result[0]
                    
                    # Generate control number: first 3 letters of address (uppercase) + client_id padded to 4 digits
                    control_number = f"{address[:3].upper()}{client_id:04d}"
                    
                    # Update existing client
                    db.cursor.execute(
                        "UPDATE clients SET name = ?, address = ?, contact_number = ?, email = ?, control_number = ? WHERE email = ?",
                        (name, address, contact_number, email, control_number, original_email)
                    )
                    db.conn.commit()
                    show_message(content, "Client updated successfully!")
                else:  # Add mode
                    # Insert new client first to get the client_id
                    db.cursor.execute(
                        "INSERT INTO clients (name, address, contact_number, email) VALUES (?, ?, ?, ?)",
                        (name, address, contact_number, email)
                    )
                    db.conn.commit()
                    
                    # Get the new client_id
                    client_id = db.cursor.lastrowid
                    
                    # Generate control number: first 3 letters of address (uppercase) + client_id padded to 4 digits
                    control_number = f"{address[:3].upper()}{client_id:04d}"
                    
                    # Update the control number
                    db.cursor.execute(
                        "UPDATE clients SET control_number = ? WHERE client_id = ?",
                        (control_number, client_id)
                    )
                    db.conn.commit()
                    show_message(content, "Client added successfully!")

                # Update the client table
                update_client_table()
                
                # Find and select the updated/added client in the table
                for row in range(table.rowCount()):
                    cell_widget = table.cellWidget(row, 0)
                    if cell_widget:
                        name_label = cell_widget.findChild(QLabel)
                        if name_label and name_label.text() == name:
                            # Select the row
                            table.selectRow(row)
                            # Trigger the selection handler
                            on_client_selected(row, 0, table)
                            break

                # Update the client info display
                update_client_info(email)
                
                # Switch back to view mode
                client_info_stack.setCurrentIndex(0)

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