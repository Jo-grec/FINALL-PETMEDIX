from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QScroller,
    QStackedLayout, QComboBox, QSizePolicy, QDateEdit, QMessageBox,
    QFileDialog, QHeaderView
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from modules.database import Database
from modules.utils import create_styled_message_box
from datetime import datetime

def get_client_widget(main_window):
    content = QWidget()
    main_layout = QVBoxLayout(content)
    main_layout.setContentsMargins(0, 0, 0, 30)
    main_layout.setSpacing(0)
    
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
    table.setColumnCount(1)  # Single column for client name and delete button
    table.setHorizontalHeaderLabels(["Client Name"])  # Add header
    table.setRowCount(16)
    table.setFixedWidth(325)
    table.setFixedHeight(500)  # Set a maximum height for the table
    table.horizontalHeader().setStretchLastSection(True)  # Stretch the single column
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    table.verticalHeader().setVisible(False)

    # Hide the vertical scrollbar but allow scrolling
    table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # Enable touch/mouse scrolling
    QScroller.grabGesture(table.viewport(), QScroller.LeftMouseButtonGesture)

    table.setStyleSheet("""
        QTableWidget {
            background-color: white;
            color: black;
            border: 1px solid gray;
        }
        QHeaderView::section {
            background-color: #f4f4f8;
            color: black;
            font-weight: bold;
            border: 1px solid gray;
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
    client_info_layout.setSpacing(10)

    # Top bar (yellow background with label and edit button)
    client_info_widget = QWidget(client_info_view)
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

    edit_client_button.clicked.connect(open_edit_form)  # 🛠️ Connect it here!

    client_info_layout_inner.addWidget(client_info_label)
    client_info_layout_inner.addStretch()  # push edit button to the right
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
    pet_picture.setFixedSize(250, 150)  # Set the size of the container
    pet_picture.setStyleSheet("""
        background-color: white;  /* White background for the frame */
        border: 2px solid #012547;  /* Dark blue border for the frame */
        border-radius: 5px;  /* Rounded corners */
    """)
    pet_picture.setObjectName("PetPicture")
    pet_picture.setAlignment(Qt.AlignCenter)  # Center the image inside the container
    
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

    # Replace QLineEdit for birthdate with QDateEdit
    birthdate_input = QDateEdit(pets_fields_widget)  # Set parent
    birthdate_input.setDisplayFormat("yyyy-MM-dd")  # Set the display format to YYYY-MM-DD
    birthdate_input.setCalendarPopup(True)  # Enable calendar popup for easier selection
    birthdate_input.setStyleSheet(line_edit_style)

    # Customize the calendar widget
    calendar_style = """
        QCalendarWidget {
            font-size: 16px;  /* Make the calendar text bigger */
            background-color: white;
            border: 1px solid gray;
            border-radius: 5px;
        }
        QCalendarWidget QToolButton {
            color: black;  /* Change the color of the month and year to black */
            font-size: 18px;  /* Make the month and year text bigger */
            margin: 5px;
        }
        QCalendarWidget QToolButton::menu-indicator {
            subcontrol-position: right center;
            subcontrol-origin: padding;
        }
        QCalendarWidget QSpinBox {
            font-size: 16px;  /* Adjust the size of the spinbox text */
        }
        QCalendarWidget QSpinBox::up-button, QCalendarWidget QSpinBox::down-button {
            width: 20px;
            height: 20px;
        }
        QCalendarWidget QTableView {
            font-size: 14px;  /* Adjust the size of the calendar days */
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
    pets_cancel_btn.setStyleSheet("background-color: #f4f4f8; border-radius:20px; color: black;")

    # Save button
    pets_save_btn = QPushButton("Save", pets_edit_widget)  # Set parent
    pets_save_btn.setFixedSize(40, 40)
    pets_save_btn.setStyleSheet("background-color: #012547; border-radius:20px; color: white; margin-right:10px;")

    # Add buttons to layout
    pets_button_row.addWidget(pets_cancel_btn)
    pets_button_row.addWidget(pets_save_btn)
    pets_edit_layout.addLayout(pets_button_row)
    pets_edit_layout.addStretch()

    client_info_stack.addWidget(pets_edit_widget)

    # --- Hook up button functionality ---
    save_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))
    cancel_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))

    edit_pet_button.clicked.connect(lambda: client_info_stack.setCurrentIndex(2))
    pets_save_btn.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))
    pets_cancel_btn.clicked.connect(lambda: client_info_stack.setCurrentIndex(0))

    client_info_stack.setCurrentIndex(0)
    table_info_layout.addWidget(client_info_stack_widget)
    main_layout.addLayout(table_info_layout)

    button_layout = QHBoxLayout()
    button_layout.setContentsMargins(0, 0, 0, 20)  # Adjust margins
    button_layout.setSpacing(10)  # Add spacing between buttons

    # Create Previous, Next, and Add buttons
    prev_button = QPushButton("<", content)
    next_button = QPushButton(">", content)
    add_button = QPushButton("+", content)

    # Force adjust the size of the buttons
    for btn in [prev_button, next_button, add_button]:
        btn.setFixedSize(80, 40)  # Set fixed size
        btn.setMinimumSize(80, 40)  # Set minimum size
        btn.setMaximumSize(80, 40)  # Set maximum size
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Ensure fixed size policy
        btn.setStyleSheet("background-color: #012547; color: white; border-radius:10px; font-size: 14px")

    # Add buttons to the layout
    button_layout.addWidget(prev_button)
    button_layout.addWidget(next_button)
    button_layout.addWidget(add_button)

    # Add stretch to align buttons to the left
    button_layout.addStretch()

    # Add the layout to the main layout
    main_layout.addLayout(button_layout)

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
                create_styled_message_box(
                    QMessageBox.Warning,
                    "Validation Error",
                    "❌ All fields are required."
                ).exec()
                return

            if "@" not in email or "." not in email:
                create_styled_message_box(
                    QMessageBox.Warning,
                    "Validation Error",
                    "❌ Invalid email address."
                ).exec()
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
                    create_styled_message_box(
                        QMessageBox.Information,
                        "Success",
                        "✅ Client data updated successfully."
                    ).exec()
                else:  # Add mode
                    db.cursor.execute(
                        "INSERT INTO clients (name, address, contact_number, email) VALUES (?, ?, ?, ?)",
                        (name, address, contact_number, email)
                    )
                    create_styled_message_box(
                        QMessageBox.Information,
                        "Success",
                        "✅ New client added successfully."
                    ).exec()

                db.conn.commit()

                # Update the client table and client information display
                update_client_table()  # Refresh the table with the new data
                update_client_info(email)  # Update the client info display
                client_info_stack.setCurrentIndex(0)  # Go back to view mode

                # Clear the original_email property after saving
                edit_form_widget.setProperty("original_email", None)
            except Exception as e:
                create_styled_message_box(
                    QMessageBox.Critical,
                    "Error",
                    f"❌ Error saving client data: {e}"
                ).exec()
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
            cell_layout.setSpacing(5)

            cell_widget.setFixedHeight(34)

            name_label = QLabel(client_name)
            name_label.setStyleSheet("color: black; font-size: 14px;")
            cell_layout.addWidget(name_label)

            cell_layout.addStretch()

            delete_button = QPushButton()
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    border: none;
                    border-radius: 10px;  /* Exactly half of width/height */
                    min-width: 20px;
                    min-height: 20px;
                    max-width: 20px;
                    max-height: 20px;
                }
                QPushButton:hover {
                    background-color: darkred;
                }
            """)

            delete_button.clicked.connect(lambda _, email=client_email: delete_client(email))
            cell_layout.addWidget(delete_button)

            table.setCellWidget(row, 0, cell_widget)
                
    def delete_client(email):
        """Delete a client from the database with confirmation."""
        # Show a confirmation dialog
        confirmation = QMessageBox()
        confirmation.setIcon(QMessageBox.Warning)
        confirmation.setWindowTitle("Delete Client")
        confirmation.setText(f"Are you sure you want to delete the client with email: {email}?")
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setDefaultButton(QMessageBox.No)

        # Check the user's response
        response = confirmation.exec()
        if response == QMessageBox.Yes:
            db = Database()
            try:
                db.cursor.execute("DELETE FROM clients WHERE email = ?", (email,))
                db.conn.commit()
                QMessageBox(f"✅ Client with email {email} deleted successfully.")
                update_client_table()  # Refresh the table after deletion
            except Exception as e:
                print(f"❌ Error deleting client: {e}")
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

            # Update the labels
            name_label = client_info_view.findChild(QLabel, "NameLabel")
            address_label = client_info_view.findChild(QLabel, "AddressLabel")
            contact_label = client_info_view.findChild(QLabel, "ContactLabel")
            email_label = client_info_view.findChild(QLabel, "EmailLabel")

            if name_label:
                name_label.setText(f"Name: {name}")
            if address_label:
                address_label.setText(f"Address: {address}")
            if contact_label:
                contact_label.setText(f"Contact Number: {contact_number}")
            if email_label:
                email_label.setText(f"Email Address: {email}")
                
    def update_pet_info(client_email):
        """Update the pet info section with data from the database."""
        db = Database()

        # Fetch the client_id using the client_email
        try:
            db.cursor.execute("SELECT client_id FROM clients WHERE email = ?", (client_email,))
            result = db.cursor.fetchone()
            if not result:
                print("❌ No client found with the provided email.")
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
            print(f"✅ Retrieved pets: {pets}")
        except Exception as e:
            print(f"❌ Error fetching pets: {e}")
            return
        finally:
            db.close_connection()

        if pets:
            # Store pets in a list for navigation
            pet_info_widget.setProperty("pets", pets)
            pet_info_widget.setProperty("current_index", 0)

            # Display the first pet's information and picture
            first_pet = pets[0]
            display_pet_info(first_pet)

            # Update the pet picture
            photo_path = first_pet[7]  # Assuming the 8th column in the pets table is the photo path
            if photo_path:
                pet_picture.setPixmap(QPixmap(photo_path).scaled(
                    pet_picture.width(), pet_picture.height(),
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                ))
            else:
                pet_picture.clear()
                pet_picture.setText("No Photo")
        else:
            print("❌ No pets found for the selected client.")
            # Clear the pet display if no pets are found
            label_names = [
                "PetNameLabel", "PetGenderLabel", "PetTypeLabel",
                "PetBreedLabel", "PetColorLabel", "PetBirthLabel", "PetAgeLabel"
            ]
            for name in label_names:
                label = client_info_view.findChild(QLabel, name)
                if label:
                    label.setText(name.replace('Label', '') + ":")
            pet_picture.clear()
            pet_picture.setText("No Photo")

    def display_pet_info(pet_data):
        """Display the information of a single pet."""
        pet_labels = [
            ("PetNameLabel", f"Name: {pet_data[0]}"),
            ("PetGenderLabel", f"Gender: {pet_data[1]}"),
            ("PetTypeLabel", f"Species: {pet_data[2]}"),
            ("PetBreedLabel", f"Breed: {pet_data[3]}"),
            ("PetColorLabel", f"Color: {pet_data[4]}"),
            ("PetBirthLabel", f"Birthdate: {pet_data[5]}"),
            ("PetAgeLabel", f"Age: {pet_data[6]}")
        ]
        for obj_name, text in pet_labels:
            label = client_info_view.findChild(QLabel, obj_name)
            if label:
                label.setText(text)
            else:
                print(f"❌ Label with object name '{obj_name}' not found.")

    # Add navigation functionality to the Next and Previous buttons
    left_arrow_button.clicked.connect(lambda: navigate_pets("prev"))
    right_arrow_button.clicked.connect(lambda: navigate_pets("next"))

    def navigate_pets(direction):
        """Navigate between pets using the arrow buttons."""
        pets = pet_info_widget.property("pets")
        if not pets or len(pets) == 0:
            print("❌ No pets available to navigate.")
            return

        current_index = pet_info_widget.property("current_index")
        if direction == "next":
            current_index = (current_index + 1) % len(pets)
        elif direction == "prev":
            current_index = (current_index - 1) % len(pets)

        pet_info_widget.setProperty("current_index", current_index)
        pet_data = pets[current_index]
        display_pet_info(pet_data)

        # Update the pet picture
        photo_path = pet_data[7]  # Assuming the 8th column in the pets table is the photo path
        if photo_path:
            pet_picture.setPixmap(QPixmap(photo_path).scaled(
                pet_picture.width(), pet_picture.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        else:
            pet_picture.clear()  # Clear the picture if no photo is available
            pet_picture.setText("No Photo")  # Optional: Display a placeholder text

    # 1. Define the function first
    def upload_pet_photo():
        """Open a file dialog to select a pet photo and display it inside the container."""
        file_dialog = QFileDialog()
        file_dialog.setNameFilters(["Image files (*.jpg *.jpeg *.png)"])
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            file_name = selected_file.split("/")[-1]  # Extract file name

            # Set the image in the pet_picture label
            pet_picture.setPixmap(QPixmap(selected_file).scaled(
                pet_picture.width() - 4, pet_picture.height() - 4,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            pet_picture.setProperty("photo_path", selected_file)

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
        border: 2px solid black
        border-radius: 5px; 
        font-size: 20px; 
        padding: 8px;
    """)
    pets_fields_layout.addWidget(upload_photo_button)

    # 3. Connect after both exist
    upload_photo_button.clicked.connect(upload_pet_photo)

    def open_add_pet_form():
        """Open the form to add a new pet."""
        # Clear all pet input fields
        name_input.clear()
        age_input.clear()
        species_input.clear()
        breed_input.clear()
        color_input.clear()
        birthdate_input.setDate(datetime.now())  # Reset to today
        pet_gender.setCurrentIndex(0)  # Reset gender dropdown

        pets_edit_widget.setProperty("mode", "add")  # 🆕 Mark as adding mode

        client_info_stack.setCurrentIndex(2)  # Switch to pet form

    def open_edit_pet_form():
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

        pets_edit_widget.setProperty("mode", "edit")  # 🆕 Mark as editing mode

        client_info_stack.setCurrentIndex(2)  # Switch to pet form
        
    update_info_button.clicked.connect(open_edit_pet_form)
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

        if not name or not species or not breed or not color or not birthdate or not age:
            create_styled_message_box(
                QMessageBox.Warning,
                "Validation Error",
                "❌ All fields are required."
            ).exec()
            return

        if not age.isdigit():
            create_styled_message_box(
                QMessageBox.Warning,
                "Validation Error",
                "❌ Age must be a valid integer."
            ).exec()
            return

        age = int(age)

        client_email = edit_form_widget.property("original_email")
        if not client_email:
            create_styled_message_box(
                QMessageBox.Warning,
                "Validation Error",
                "❌ No client selected for adding a pet."
            ).exec()
            return

        db = Database()
        try:
            db.cursor.execute("SELECT client_id FROM clients WHERE email = ?", (client_email,))
            result = db.cursor.fetchone()
            if not result:
                create_styled_message_box(
                    QMessageBox.Warning,
                    "Validation Error",
                    "❌ No client found with the provided email."
                ).exec()
                return
            client_id = result[0]

            mode = pets_edit_widget.property("mode")

            # Get the photo path from the pet_picture label
            photo_path = pet_picture.property("photo_path")

            if mode == "add":
                db.cursor.execute("""
                    INSERT INTO pets (name, gender, species, breed, color, birthdate, age, photo_path, client_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, gender, species, breed, color, birthdate, age, photo_path, client_id))
                db.conn.commit()
                create_styled_message_box(
                    QMessageBox.Information,
                    "Success",
                    "✅ New pet added successfully."
                ).exec()
            elif mode == "edit":
                current_pet_name = pet_info_widget.property("pets")[pet_info_widget.property("current_index")][0]
                db.cursor.execute("""
                    UPDATE pets 
                    SET name = ?, gender = ?, species = ?, breed = ?, color = ?, birthdate = ?, age = ?, photo_path = ?
                    WHERE name = ? AND client_id = ?
                """, (name, gender, species, breed, color, birthdate, age, photo_path, current_pet_name, client_id))
                db.conn.commit()
                create_styled_message_box(
                    QMessageBox.Information,
                    "Success",
                    "✅ Pet updated successfully."
                ).exec()

            # ✅ Update pet info display after save
            update_pet_info(client_email)
            pet_info_widget.setProperty("current_index", 0)
            client_info_stack.setCurrentIndex(0)

        except Exception as e:
            create_styled_message_box(
                QMessageBox.Critical,
                "Error",
                f"❌ Error saving pet data: {e}"
            ).exec()
        finally:
            db.close_connection()
                
    pets_save_btn.clicked.connect(save_pet_data)
            
    def delete_pet():
        """Delete the currently displayed pet."""
        pets = pet_info_widget.property("pets")
        current_index = pet_info_widget.property("current_index")
        if not pets or current_index is None:
            create_styled_message_box(
                QMessageBox.Warning,
                "Error",
                "❌ No pet selected."
            ).exec()
            return

        pet_data = pets[current_index]
        pet_name = pet_data[0]

        client_email = edit_form_widget.property("original_email")
        if not client_email:
            create_styled_message_box(
                QMessageBox.Warning,
                "Error",
                "❌ No client selected for deleting a pet."
            ).exec()
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
                create_styled_message_box(
                    QMessageBox.Information,
                    "Success",
                    f"✅ Pet \"{pet_name}\" was successfully deleted."
                ).exec()

                # Update the pet info section
                update_pet_info(client_email)

            except Exception as e:
                create_styled_message_box(
                    QMessageBox.Critical,
                    "Error",
                    f"❌ Error deleting pet: {e}"
                ).exec()
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
                cell_widget.setStyleSheet("background-color: white;")  # Default background color

        # Highlight the selected row
        selected_item = table.cellWidget(row, 0)
        if selected_item:
            selected_item.setStyleSheet("background-color: #FED766;")  # Highlight color (yellow)

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