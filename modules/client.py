from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget,
    QStackedLayout, QComboBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

def get_client_widget(main_window):
    content = QWidget()
    main_layout = QVBoxLayout(content)
    main_layout.setContentsMargins(0, 0, 0, 30)
    main_layout.setSpacing(0)

    # --- Client List Label ---
    client_list = QLabel("Client List", content)
    client_list.setObjectName("ClientList")
    client_list.setStyleSheet("background-color: #102547;")
    main_layout.addWidget(client_list)

    # --- Table and Client Info Layout ---
    table_info_layout = QHBoxLayout()
    table_info_layout.setContentsMargins(0, 0, 0, 0)
    table_info_layout.setSpacing(0)

    # --- Client Table ---
    table = QTableWidget(content)
    table.setColumnCount(1)
    table.setRowCount(16)
    table.setFixedWidth(250)
    table.horizontalHeader().setStretchLastSection(True)
    table.verticalHeader().setVisible(False)
    table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    table.horizontalHeader().setVisible(False)
    table.setStyleSheet("background-color: white; color: black;")
    table_info_layout.addWidget(table)

    # --- Client Info Stack Widget and Layout ---
    client_info_stack_widget = QWidget(content)  # Set parent to content
    client_info_stack = QStackedLayout(client_info_stack_widget)  # Set parent

    # ===== VIEW MODE =====
    client_info_view = QWidget(client_info_stack_widget)  # Set parent
    client_info_layout = QVBoxLayout(client_info_view)
    client_info_layout.setContentsMargins(0, 0, 0, 0)
    client_info_layout.setSpacing(10)

    client_info_widget = QWidget(client_info_view)  # Set parent
    client_info_widget.setFixedHeight(50)
    client_info_widget.setStyleSheet("background-color: #FED766;")
    client_info_layout_inner = QHBoxLayout(client_info_widget)
    client_info_layout_inner.setContentsMargins(0, 0, 0, 0)
    client_info_layout_inner.setSpacing(10)

    client_info_label = QLabel("CLIENT INFORMATION", client_info_widget)
    client_info_label.setObjectName("ClientInformationLabel")
    client_info_label.setAlignment(Qt.AlignVCenter)

    edit_client_button = QPushButton(client_info_widget)
    edit_client_button.setIcon(QIcon("assets/edit client button.png"))
    edit_client_button.setIconSize(QSize(30, 30))
    edit_client_button.setFixedSize(90, 60)
    edit_client_button.setStyleSheet("background-color: #FED766; border: none;")

    client_info_layout_inner.addWidget(client_info_label)
    client_info_layout_inner.addWidget(edit_client_button)

    client_info_layout.addWidget(client_info_widget)

    labels = ["Name:", "Address:", "Contact Number:", "Email Address:"]
    object_names = ["NameLabel", "AddressLabel", "ContactLabel", "EmailLabel"]
    for text, obj_name in zip(labels, object_names):
        label = QLabel(text, client_info_view)  # Set parent
        label.setObjectName(obj_name)
        client_info_layout.addWidget(label)

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
    
    # Create a container widget for the arrow buttons to keep them together
    arrow_container = QWidget(pet_info_widget)
    arrow_container_layout = QHBoxLayout(arrow_container)
    arrow_container_layout.setContentsMargins(0, 0, 0, 0)
    arrow_container_layout.setSpacing(0)  # No spacing between arrows

    # Add left arrow button
    left_arrow_button = QPushButton(arrow_container)
    left_arrow_button.setText("<")
    left_arrow_button.setFixedSize(25, 40)
    left_arrow_button.setStyleSheet("background-color: #FED766; border: none;")

    # Add right arrow button
    right_arrow_button = QPushButton(arrow_container)
    right_arrow_button.setText(">")
    right_arrow_button.setFixedSize(25, 40)
    right_arrow_button.setStyleSheet("background-color: #FED766; border: none; margin-left:-20px;")

    arrow_container_layout.addWidget(left_arrow_button)
    arrow_container_layout.addWidget(right_arrow_button)

    edit_pet_button = QPushButton(pet_info_widget)
    edit_pet_button.setIcon(QIcon("assets/add pet button.png"))
    edit_pet_button.setIconSize(QSize(30, 30))
    edit_pet_button.setFixedSize(90, 60)
    edit_pet_button.setStyleSheet("background-color: #FED766; border: none;")

    pet_info_layout.addWidget(pet_info_label)
    pet_info_layout.addStretch()  # Add stretch to push arrows and button to the right
    pet_info_layout.addWidget(arrow_container)
    pet_info_layout.addWidget(edit_pet_button)
    client_info_layout.addWidget(pet_info_widget)

    pet_info_section = QHBoxLayout()

    pet_picture = QLabel(client_info_view)  # Set parent
    pet_picture.setFixedSize(250, 150)
    pet_picture.setStyleSheet("background-color: gray;")
    pet_picture.setObjectName("PetPicture")
    pet_picture.setAlignment(Qt.AlignCenter)
    pet_info_section.addWidget(pet_picture)

    pet_details_layout = QVBoxLayout()
    pet_labels = ["Name:", "Gender:", "Pet Type:", "Breed:", "Color:", "Birthdate:", "Age:"]
    pet_object_names = [
        "PetNameLabel", "PetGenderLabel", "PetTypeLabel",
        "PetBreedLabel", "PetColorLabel", "PetBirthLabel", "PetAgeLabel"
    ]
    for text, obj_name in zip(pet_labels, pet_object_names):
        label = QLabel(text, client_info_view)  # Set parent
        label.setObjectName(obj_name)
        pet_details_layout.addWidget(label)
    pet_info_section.addLayout(pet_details_layout)

    pet_buttons_layout = QVBoxLayout()
    update_info_button = QPushButton("Update Info", client_info_view)  # Set parent
    check_schedule_button = QPushButton("Check Schedule", client_info_view)  # Set parent
    see_records_button = QPushButton("See Records", client_info_view)  # Set parent

    for btn in [update_info_button, check_schedule_button, see_records_button]:
        btn.setStyleSheet("background-color: #012547; color: white; font-size: 14px")
        btn.setFixedSize(120, 40)
        pet_buttons_layout.addWidget(btn)

    pet_buttons_layout.addStretch()
    pet_buttons_layout.setContentsMargins(0, 0, 120, 0)

    see_records_button.clicked.connect(main_window.show_pet_records)

    pet_info_section.addLayout(pet_buttons_layout)
    client_info_layout.addLayout(pet_info_section)
    client_info_layout.addStretch()

    client_info_stack.addWidget(client_info_view)

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
        line_edit.setStyleSheet("padding: 8px; margin: 10px; background-color: #f4f4f8; border: 1px solid gray; border-radius: 5px;")
        edit_fields_layout.addWidget(line_edit)

    edit_form_layout.addWidget(edit_fields_widget)

    button_layout = QHBoxLayout()
    button_layout.addStretch()

    cancel_button = QPushButton("Cancel", edit_form_widget)  # Set parent
    cancel_button.setFixedSize(40, 40)
    cancel_button.setStyleSheet("background-color: #f4f4f8; border-radius:20px; color: black;")

    save_button = QPushButton("Save", edit_form_widget)  # Set parent
    save_button.setFixedSize(40, 40)
    save_button.setStyleSheet("background-color: #012547; border-radius:20px; color: white; margin-right:90px;")

    button_layout.addWidget(cancel_button)
    button_layout.addWidget(save_button)
    edit_form_layout.addLayout(button_layout)
    edit_form_layout.addStretch()

    client_info_stack.addWidget(edit_form_widget)

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
    """

    # Create pet fields layout
    pets_fields_widget = QWidget(pets_edit_widget)  # Set parent
    pets_fields_layout = QVBoxLayout(pets_fields_widget)
    pets_fields_layout.setContentsMargins(80, 10, 80, 10)

    # Row 1
    row1 = QHBoxLayout()
    name_input = QLineEdit(pets_fields_widget)  # Set parent
    name_input.setPlaceholderText("Enter Name")
    name_input.setStyleSheet(line_edit_style)

    pet_gender = QComboBox(pets_fields_widget)  # Set parent
    pet_gender.addItems(["Male", "Female"])
    pet_gender.setFixedSize(200, 41)
    pet_gender.setStyleSheet("""
        QComboBox {
            padding: 8px;
            border: 1px solid gray;
            border-radius: 5px;
            background-color: #f4f4f8;        
            }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            selection-background-color: #FED766;
        }
    """)

    age_input = QLineEdit(pets_fields_widget)  # Set parent
    age_input.setPlaceholderText("Enter Age")
    age_input.setStyleSheet(line_edit_style)

    row1.addWidget(name_input)
    row1.addWidget(pet_gender)
    row1.addWidget(age_input)
    pets_fields_layout.addLayout(row1)

    # Row 2
    row2 = QHBoxLayout()
    species_input = QLineEdit(pets_fields_widget)  # Set parent
    species_input.setPlaceholderText("Enter Species")
    species_input.setStyleSheet(line_edit_style)

    breed_input = QLineEdit(pets_fields_widget)  # Set parent
    breed_input.setPlaceholderText("Enter Breed")
    breed_input.setStyleSheet(line_edit_style)

    row2.addWidget(species_input)
    row2.addWidget(breed_input)
    pets_fields_layout.addLayout(row2)

    # Add other input fields
    color_input = QLineEdit(pets_fields_widget)  # Set parent
    color_input.setPlaceholderText("Enter Color")
    color_input.setStyleSheet(line_edit_style)
    pets_fields_layout.addWidget(color_input)

    birthdate_input = QLineEdit(pets_fields_widget)  # Set parent
    birthdate_input.setPlaceholderText("Enter Birthdate")
    birthdate_input.setStyleSheet(line_edit_style)
    pets_fields_layout.addWidget(birthdate_input)

    # Add fields layout to the main edit form layout
    pets_edit_layout.addWidget(pets_fields_widget)

    # Button row layout
    pets_button_row = QHBoxLayout()
    pets_button_row.addStretch()

    # Cancel button
    pets_cancel_btn = QPushButton("Cancel", pets_edit_widget)  # Set parent
    pets_cancel_btn.setFixedSize(40, 40)
    pets_cancel_btn.setStyleSheet("background-color: #f4f4f8; border-radius:20px; color: black;")

    # Save button
    pets_save_btn = QPushButton("Save", pets_edit_widget)  # Set parent
    pets_save_btn.setFixedSize(40, 40)
    pets_save_btn.setStyleSheet("background-color: #012547; border-radius:20px; color: white; margin-right:90px;")

    # Add buttons to layout
    pets_button_row.addWidget(pets_cancel_btn)
    pets_button_row.addWidget(pets_save_btn)
    pets_edit_layout.addLayout(pets_button_row)
    pets_edit_layout.addStretch()

    client_info_stack.addWidget(pets_edit_widget)

    # --- Hook up button functionality ---
    edit_client_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(1))
    save_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))
    cancel_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))

    edit_pet_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(2))
    pets_save_btn.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))
    pets_cancel_btn.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))

    client_info_stack.setCurrentIndex(0)
    table_info_layout.addWidget(client_info_stack_widget)
    main_layout.addLayout(table_info_layout)

    button_layout = QHBoxLayout()
    button_layout.setContentsMargins(40, 0, 0, 20)
    button_layout.setSpacing(10)

    prev_button = QPushButton("Previous", content)  # Set parent
    next_button = QPushButton("Next", content)  # Set parent

    for btn in [prev_button, next_button]:
        btn.setStyleSheet("background-color: #012547; color: white; border-radius:20px; font-size: 14px")
        btn.setFixedSize(120, 40)
        button_layout.addWidget(btn)

    button_layout.setAlignment(Qt.AlignLeft)
    main_layout.addLayout(button_layout)

    return content