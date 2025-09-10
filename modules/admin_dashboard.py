from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QLineEdit,
    QComboBox, QHeaderView, QFrame, QGridLayout, QFileDialog, QTextEdit, QCheckBox,
    QStyledItemDelegate, QGroupBox, QRadioButton, QAbstractScrollArea, QAbstractItemView,
    QButtonGroup
)
from PySide6.QtCore import Qt, QSize, QDate, QTimer
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QPainterPath, QDoubleValidator
from modules.database import Database
from modules.utils import create_styled_message_box, show_message
import os
from shutil import copyfile
from modules.setting import UpdateClinicInfoDialog

class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setMinimumSize(1200, 800)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #012547;
                border: none;
            }
            QPushButton {
                text-align: left;
                padding: 15px;
                border: none;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #023d6d;
            }
            QPushButton:checked {
                background-color: #023d6d;
                border-left: 4px solid #FED766;
            }
            #logoutButton {
                margin-top: auto;
                background-color: #dc3545;
                color: white;
                text-align: center;
                padding: 15px;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            #logoutButton:hover {
                background-color: #c82333;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Logo/Title
        title = QLabel("PetMedix Admin")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 20px;
                background-color: #001e3d;
            }
        """)
        sidebar_layout.addWidget(title)

        # Navigation buttons
        self.dashboard_btn = QPushButton("Dashboard")
        self.dashboard_btn.setCheckable(True)
        self.dashboard_btn.setChecked(True)
        self.dashboard_btn.clicked.connect(lambda: self.show_page("dashboard"))

        self.users_btn = QPushButton("Users")
        self.users_btn.setCheckable(True)
        self.users_btn.clicked.connect(lambda: self.show_page("users"))

        sidebar_layout.addWidget(self.dashboard_btn)
        sidebar_layout.addWidget(self.users_btn)
        sidebar_layout.addStretch()

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("logoutButton")
        logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_btn)

        # Content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)

        # Add widgets to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_area)

        # Initialize pages
        self.setup_dashboard_page()
        self.setup_users_page()

        # Show dashboard by default
        self.show_page("dashboard")

    def setup_dashboard_page(self):
        self.dashboard_page = QWidget()
        layout = QVBoxLayout(self.dashboard_page)

        # Header
        header = QLabel("Dashboard Overview")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header)

        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total Users Card
        self.users_card_value = QLabel("0")
        users_card = self.create_stat_card("Total Users", self.users_card_value)
        stats_layout.addWidget(users_card)

        # Total Vets Card
        self.vets_card_value = QLabel("0")
        vets_card = self.create_stat_card("Veterinarians", self.vets_card_value)
        stats_layout.addWidget(vets_card)

        # Total Receptionists Card
        self.receptionists_card_value = QLabel("0")
        receptionists_card = self.create_stat_card("Receptionists", self.receptionists_card_value)
        stats_layout.addWidget(receptionists_card)

        layout.addLayout(stats_layout)
        
        # Add spacing between stat cards and clinic info
        layout.addSpacing(30)  # Add 30 pixels of vertical spacing

        # --- Clinic Information Section ---
        clinic_section = QFrame()
        clinic_section.setStyleSheet("background-color: white; border-radius: 5px;")
        clinic_layout = QVBoxLayout(clinic_section)
        clinic_layout.setContentsMargins(10, 10, 30, 10)
        clinic_layout.setSpacing(25)
        
        clinic_header = QLabel("VET CLINIC INFORMATION")
        clinic_header.setStyleSheet("font-weight: bold; font-size: 16px;")
        clinic_layout.addWidget(clinic_header)
        clinic_content = QHBoxLayout()
        clinic_content.setSpacing(25)
        clinic_picture_column = QVBoxLayout()
        clinic_picture_column.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        clinic_logo = QLabel()
        clinic_logo.setFixedSize(200, 200)
        clinic_logo.setAlignment(Qt.AlignCenter)
        clinic_logo.setText("Clinic\nLogo")
        clinic_upload_btn = QPushButton("Upload Photo")
        clinic_upload_btn.setStyleSheet("""
            background-color: #dfe4ea;
            color: #000;
            font-size: 12px;
            padding: 8px;
            border-radius: 10px;
            margin-left:45px;
        """)
        clinic_upload_btn.setFixedWidth(170)
        clinic_picture_column.addWidget(clinic_logo)
        clinic_picture_column.addWidget(clinic_upload_btn)
        clinic_picture_column.addStretch()
        clinic_info_column = QGridLayout()
        clinic_info_column.setVerticalSpacing(10)
        clinic_info_column.setHorizontalSpacing(10)
        clinic_labels = {}
        def update_clinic_info_ui():
            db = Database()
            try:
                db.cursor.execute("SELECT name, address, contact_number, email, employees_count, logo_path, vet_license FROM clinic_info LIMIT 1")
                clinic_row = db.cursor.fetchone()
                if clinic_row:
                    clinic_data = {
                        "name": clinic_row[0],
                        "address": clinic_row[1],
                        "contact": clinic_row[2],
                        "email": clinic_row[3],
                        "employees": str(clinic_row[4]),
                        "logo_path": clinic_row[5] or "",
                        "vet_license": clinic_row[6] or "VET-214"
                    }
                else:
                    clinic_data = {"name": "", "address": "", "contact": "", "email": "", "employees": "", "logo_path": "", "vet_license": "VET-214"}
            except Exception as e:
                print(f"❌ Error loading clinic data: {e}")
                clinic_data = {"name": "", "address": "", "contact": "", "email": "", "employees": "", "logo_path": "", "vet_license": "VET-214"}
            # Update logo
            if clinic_data.get("logo_path") and os.path.exists(clinic_data["logo_path"]):
                original_pixmap = QPixmap(clinic_data["logo_path"])
                size = clinic_logo.size()
                rounded_pixmap = QPixmap(size)
                rounded_pixmap.fill(Qt.transparent)
                painter = QPainter(rounded_pixmap)
                painter.setRenderHint(QPainter.Antialiasing)
                path = QPainterPath()
                path.addEllipse(0, 0, size.width(), size.height())
                painter.setClipPath(path)
                scaled_pixmap = original_pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                painter.drawPixmap(0, 0, scaled_pixmap)
                painter.end()
                clinic_logo.setPixmap(rounded_pixmap)
                clinic_logo.setText("")
            else:
                clinic_logo.setText("Clinic\nLogo")
            # Update info fields
            clinic_fields = {
                "Name:": clinic_data.get("name", ""),
                "Vet License Number:": clinic_data.get("vet_license", "VET-214"),
                "Email Address:": clinic_data.get("email", ""),
                "Address:": clinic_data.get("address", ""),
                "Contact Number:": clinic_data.get("contact", ""),
                "No. of Employees:": clinic_data.get("employees", "")
            }
            # Clear previous widgets if any
            for i in reversed(range(clinic_info_column.count())):
                item = clinic_info_column.itemAt(i)
                if item:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            clinic_labels.clear()
            row = 0
            for label_text, value_text in clinic_fields.items():
                label = QLabel(label_text)
                label.setStyleSheet("font-weight: bold; color: #222f3e;")
                value = QLabel(value_text)
                value.setStyleSheet("color: #222f3e;")
                clinic_info_column.addWidget(label, row, 0)
                clinic_info_column.addWidget(value, row, 1)
                clinic_labels[label_text.replace(":", "")] = value
                row += 1
            db.close_connection()
        update_clinic_info_ui()
        def upload_logo():
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Clinic Logo", "", "Images (*.png *.jpg *.jpeg)")
            if file_path:
                logo_dir = os.path.join("assets", "clinic_logos")
                os.makedirs(logo_dir, exist_ok=True)
                filename = "clinic_logo.jpg"
                new_path = os.path.join(logo_dir, filename)
                copyfile(file_path, new_path)
                db = Database()
                db.save_clinic_info(
                    clinic_labels["Name"].text(),
                    clinic_labels["Address"].text(),
                    clinic_labels["Contact Number"].text(),
                    clinic_labels["Email Address"].text(),
                    clinic_labels["No. of Employees"].text(),
                    vet_license=clinic_labels["Vet License Number"].text(),
                    logo_path=new_path
                )
                db.close_connection()
                update_clinic_info_ui()
        clinic_upload_btn.clicked.connect(upload_logo)
        clinic_button_column = QVBoxLayout()
        clinic_button_column.setAlignment(Qt.AlignTop)
        update_clinic_btn = QPushButton("Update Info")
        update_clinic_btn.setIcon(QIcon("edit_icon.png"))
        update_clinic_btn.setIconSize(QSize(10, 10))
        update_clinic_btn.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 10px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #01315d;
            }
        """)
        update_clinic_btn.setFixedWidth(120)
        
        def open_update_clinic_dialog():
            db = Database()
            db.cursor.execute("SELECT name, address, contact_number, email, employees_count, logo_path, vet_license FROM clinic_info LIMIT 1")
            clinic_row = db.cursor.fetchone()
            if clinic_row:
                clinic_data = {
                    "name": clinic_row[0],
                    "address": clinic_row[1],
                    "contact": clinic_row[2],
                    "email": clinic_row[3],
                    "employees": str(clinic_row[4]),
                    "logo_path": clinic_row[5] or "",
                    "vet_license": clinic_row[6] or "VET-214"
                }
            else:
                clinic_data = {"name": "", "address": "", "contact": "", "email": "", "employees": "", "logo_path": "", "vet_license": "VET-214"}
            db.close_connection()
            dialog = UpdateClinicInfoDialog(clinic_data)
            if dialog.exec():
                updated_data = dialog.get_updated_data()
                db = Database()
                db.save_clinic_info(
                    updated_data["name"],
                    updated_data["address"],
                    updated_data["contact"],
                    updated_data["email"],
                    int(updated_data["employees"]),
                    vet_license=updated_data["vet_license"],
                    logo_path=clinic_data.get("logo_path")
                )
                db.close_connection()
                update_clinic_info_ui()
        update_clinic_btn.clicked.connect(open_update_clinic_dialog)
        clinic_button_column.addWidget(update_clinic_btn)
        clinic_button_column.addStretch()
        clinic_content.addLayout(clinic_picture_column)
        clinic_content.addSpacing(40)
        clinic_content.addLayout(clinic_info_column, 1)
        clinic_content.addLayout(clinic_button_column)
        clinic_layout.addLayout(clinic_content)
        layout.addWidget(clinic_section)
        layout.addStretch()

    def create_stat_card(self, title, value_label):
        card = QFrame()
        
        # Set different colors based on card title
        if title == "Total Users":
            bg_color = "#FF0000"  # Light blue
            text_color = "#fff"  # Dark blue
        elif title == "Veterinarians":
            bg_color = "#008000"  # Light green
            text_color = "#fff"  # Dark green
        elif title == "Receptionists":
            bg_color = "#012547"  # Light orange
            text_color = "#fff"  # Dark orange
        else:
            bg_color = "white"
            text_color = "#012547"
            
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        card.setFixedHeight(150)

        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 16px; color: {text_color};")
        
        value_label.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {text_color};")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        return card

    def setup_users_page(self):
        self.users_page = QWidget()
        layout = QVBoxLayout(self.users_page)

        # Header with Add User button and action buttons
        header_layout = QHBoxLayout()
        header = QLabel("User Management")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        # Action buttons container
        self.action_buttons = QWidget()
        action_buttons_layout = QHBoxLayout(self.action_buttons)
        action_buttons_layout.setSpacing(10)
        
        # Edit button
        self.edit_btn = QPushButton()
        self.edit_btn.setIcon(QIcon("assets/edit client button.png"))
        self.edit_btn.setIconSize(QSize(24, 24))
        self.edit_btn.setToolTip("Edit User")
        self.edit_btn.setFixedSize(44, 44)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 22px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.edit_btn.clicked.connect(self.edit_selected_user)
        self.edit_btn.setVisible(False)
        
        # Verify button
        self.verify_btn = QPushButton("Verify")
        self.verify_btn.setIcon(QIcon("assets/check-circle-solid-24.png"))
        self.verify_btn.setIconSize(QSize(24, 24))
        self.verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.verify_btn.clicked.connect(self.verify_selected_user)
        self.verify_btn.setVisible(False)
        
        # Unverify button
        self.unverify_btn = QPushButton("Unverify")
        self.unverify_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
        """)
        self.unverify_btn.clicked.connect(self.unverify_selected_user)
        self.unverify_btn.setVisible(False)
        
        # Delete button
        self.delete_btn = QPushButton()
        self.delete_btn.setIcon(QIcon("assets/trash-can.png"))
        self.delete_btn.setIconSize(QSize(24, 24))
        self.delete_btn.setToolTip("Delete User")
        self.delete_btn.setFixedSize(44, 44)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 22px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_selected_user)
        self.delete_btn.setVisible(False)
        
        # Add User button
        add_user_btn = QPushButton("Add User")
        add_user_btn.setIcon(QIcon("assets/userlogo.png"))
        add_user_btn.setIconSize(QSize(24, 24))
        add_user_btn.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #023d6d;
            }
        """)
        add_user_btn.clicked.connect(self.show_add_user_dialog)

        action_buttons_layout.addWidget(self.edit_btn)
        action_buttons_layout.addWidget(self.verify_btn)
        action_buttons_layout.addWidget(self.unverify_btn)
        action_buttons_layout.addWidget(self.delete_btn)
        action_buttons_layout.addWidget(add_user_btn)

        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(self.action_buttons)
        layout.addLayout(header_layout)

        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(7)
        self.users_table.setHorizontalHeaderLabels([
            "User ID", "Name", "Email", "Role", "Status", "License Number", "Created Date"
        ])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #012547;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 16px;
            }
            QTableWidget::item:selected {
                background-color: rgba(227, 242, 253, 0.5);
                color: #012547;
            }
        """)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setSelectionMode(QTableWidget.SingleSelection)
        self.users_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.users_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.users_table.verticalHeader().setVisible(False)
        self.users_table.setShowGrid(True)
        self.users_table.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(self.users_table)

        # Load initial data
        self.load_users()

    def show_page(self, page):
        # Reset all buttons
        self.dashboard_btn.setChecked(False)
        self.users_btn.setChecked(False)

        # Clear content area
        for i in reversed(range(self.content_layout.count())): 
            self.content_layout.itemAt(i).widget().setParent(None)

        # Show selected page
        if page == "dashboard":
            self.dashboard_btn.setChecked(True)
            self.content_layout.addWidget(self.dashboard_page)
            self.update_dashboard_stats()
        elif page == "users":
            self.users_btn.setChecked(True)
            self.content_layout.addWidget(self.users_page)
            self.load_users()

    def update_dashboard_stats(self):
        db = Database()
        try:
            # Get total verified users count
            db.cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'Verified'")
            total_users = db.cursor.fetchone()[0]

            # Get verified vets count
            db.cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Veterinarian' AND status = 'Verified'")
            total_vets = db.cursor.fetchone()[0]

            # Get verified receptionists count
            db.cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Receptionist' AND status = 'Verified'")
            total_receptionists = db.cursor.fetchone()[0]

            # Update the stat cards
            self.users_card_value.setText(str(total_users))
            self.vets_card_value.setText(str(total_vets))
            self.receptionists_card_value.setText(str(total_receptionists))

        except Exception as e:
            print(f"❌ Error updating dashboard stats: {e}")
        finally:
            db.close_connection()

    def load_users(self):
        db = Database()
        try:
            db.cursor.execute("""
                SELECT user_id, name, email, role, status, license_number, created_date
                FROM users
                WHERE role IN ('Veterinarian', 'Receptionist')
                ORDER BY created_date DESC
            """)
            users = db.cursor.fetchall()

            self.users_table.setRowCount(len(users))
            for row, user in enumerate(users):
                # Add user data
                for col, value in enumerate(user):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    
                    # Set background color based on status
                    if col == 4:  # Status column
                        if value == 'Pending':
                            item.setBackground(QColor('#FFF9C4'))  # Light yellow for pending
                            item.setForeground(QColor('#856404'))  # Dark yellow text
                        elif value == 'Verified':
                            item.setBackground(QColor('#C8E6C9'))  # Light green for verified
                            item.setForeground(QColor('#1B5E20'))  # Dark green text
                    
                    self.users_table.setItem(row, col, item)

        except Exception as e:
            print(f"❌ Error loading users: {e}")
        finally:
            db.close_connection()

    def show_add_user_dialog(self):
        dialog = AddUserDialog(self)
        if dialog.exec():
            self.load_users()

    def verify_selected_user(self):
        selected_items = self.users_table.selectedIndexes()
        if selected_items:
            row = selected_items[0].row()
            user_id = self.users_table.item(row, 0).text()
            self.verify_user(row)

    def delete_selected_user(self):
        selected_items = self.users_table.selectedIndexes()
        if selected_items:
            row = selected_items[0].row()
            self.delete_user(row)

    def verify_user(self, row):
        user_id = self.users_table.item(row, 0).text()
        
        # Create confirmation message box
        confirm = create_styled_message_box(
            QMessageBox.Question,
            "Verify User",
            f"Are you sure you want to verify user {user_id}?"
        )
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if confirm.exec() == QMessageBox.Yes:
            db = Database()
            try:
                db.cursor.execute("""
                    UPDATE users
                    SET status = 'Verified'
                    WHERE user_id = ?
                """, (user_id,))
                db.conn.commit()
                
                # Show success message
                success_msg = create_styled_message_box(
                    QMessageBox.Information,
                    "Success",
                    f"""
                    <div style='font-size: 14px; color: #012547;'>
                        <p style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>User Verified Successfully!</p>
                        <p>The user has been verified and can now access the system.</p>
                    </div>
                    """
                )
                success_msg.setStandardButtons(QMessageBox.Ok)
                success_msg.exec()
                
                self.load_users()
                # Update dashboard stats after verifying user
                self.update_dashboard_stats()
            except Exception as e:
                print(f"Error verifying user: {e}")
                db.conn.rollback()
                # Show error message
                error_msg = create_styled_message_box(
                    QMessageBox.Critical,
                    "Error",
                    "An error occurred while verifying the user. Please try again."
                )
                error_msg.setStandardButtons(QMessageBox.Ok)
                error_msg.exec()

    def delete_user(self, row):
        user_id = self.users_table.item(row, 0).text()
        
        # Create confirmation message box
        confirm = create_styled_message_box(
            QMessageBox.Question,
            "Delete User",
            f"Are you sure you want to delete user {user_id}?"
        )
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        
        if confirm.exec() == QMessageBox.Yes:
            db = Database()
            try:
                db.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                db.conn.commit()
                
                # Show success message
                success_msg = create_styled_message_box(
                    QMessageBox.Information,
                    "Success",
                    f"""
                    <div style='font-size: 14px; color: #012547;'>
                        <p style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>User Deleted Successfully!</p>
                        <p>The user has been removed from the system.</p>
                    </div>
                    """
                )
                success_msg.setStandardButtons(QMessageBox.Ok)
                success_msg.exec()
                
                self.load_users()
                # Update dashboard stats after deleting user
                self.update_dashboard_stats()
            except Exception as e:
                print(f"Error deleting user: {e}")
                db.conn.rollback()
                # Show error message
                error_msg = create_styled_message_box(
                    QMessageBox.Critical,
                    "Error",
                    "An error occurred while deleting the user. Please try again."
                )
                error_msg.setStandardButtons(QMessageBox.Ok)
                error_msg.exec()
            finally:
                db.close_connection()

    def logout(self):
        """Handle logout action."""
        # Create confirmation dialog
        confirm = create_styled_message_box(
            QMessageBox.Question,
            "Confirm Logout",
            """
            <div style='font-size: 14px; color: #012547;'>
                <p style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>Are you sure you want to logout?</p>
                <p>You will be redirected to the login page.</p>
            </div>
            """
        )
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        
        if confirm.exec() == QMessageBox.Yes:
            from modules.login import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.showMaximized()
            self.close()

    def on_selection_changed(self):
        selected_items = self.users_table.selectedIndexes()
        if selected_items:
            row = selected_items[0].row()
            status = self.users_table.item(row, 4).text()  # Status column
            
            # Show delete and edit buttons for any selected user
            self.delete_btn.setVisible(True)
            self.edit_btn.setVisible(True)
            
            # Show verify/unverify buttons based on current status
            self.verify_btn.setVisible(status != 'Verified')
            self.unverify_btn.setVisible(status == 'Verified')
        else:
            # Hide all action buttons if no row is selected
            self.verify_btn.setVisible(False)
            self.unverify_btn.setVisible(False)
            self.delete_btn.setVisible(False)
            self.edit_btn.setVisible(False)

    def unverify_selected_user(self):
        selected_items = self.users_table.selectedIndexes()
        if selected_items:
            row = selected_items[0].row()
            user_id = self.users_table.item(row, 0).text()
            
            # Create confirmation message box
            confirm = create_styled_message_box(
                QMessageBox.Question,
                "Unverify User",
                f"Are you sure you want to unverify user {user_id}?"
            )
            confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            
            if confirm.exec() == QMessageBox.Yes:
                db = Database()
                try:
                    db.cursor.execute("""
                        UPDATE users
                        SET status = 'Pending'
                        WHERE user_id = ?
                    """, (user_id,))
                    db.conn.commit()
                    
                    # Show success message
                    success_msg = create_styled_message_box(
                        QMessageBox.Information,
                        "Success",
                        f"""
                        <div style='font-size: 14px; color: #012547;'>
                            <p style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>User Unverified Successfully!</p>
                            <p>The user's status has been changed to Pending.</p>
                        </div>
                        """
                    )
                    success_msg.setStandardButtons(QMessageBox.Ok)
                    success_msg.exec()
                    
                    self.load_users()
                    # Update dashboard stats after unverifying user
                    self.update_dashboard_stats()
                except Exception as e:
                    print(f"Error unverifying user: {e}")
                    db.conn.rollback()
                    # Show error message
                    error_msg = create_styled_message_box(
                        QMessageBox.Critical,
                        "Error",
                        "An error occurred while unverifying the user. Please try again."
                    )
                    error_msg.setStandardButtons(QMessageBox.Ok)
                    error_msg.exec()

    def edit_selected_user(self):
        selected_items = self.users_table.selectedIndexes()
        if selected_items:
            row = selected_items[0].row()
            user_id = self.users_table.item(row, 0).text()
            name = self.users_table.item(row, 1).text()
            email = self.users_table.item(row, 2).text()
            role = self.users_table.item(row, 3).text()
            
            # Create and show edit dialog
            dialog = EditUserDialog(self, user_id, name, email, role)
            if dialog.exec():
                self.load_users()
                self.update_dashboard_stats()

class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New User")
        self.setFixedSize(600, 650)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet("background-color: #012547;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 30, 30, 30)
        title_label = QLabel("Add New User")
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        header_layout.addWidget(title_label)
        layout.addWidget(header)

        # Main form area
        form_area = QWidget()
        form_layout = QVBoxLayout(form_area)
        form_layout.setContentsMargins(40, 30, 40, 10)
        form_layout.setSpacing(5)

        # First Name and Last Name
        name_label = QLabel("Name")
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 2px;")
        form_layout.addWidget(name_label)
        name_row = QHBoxLayout()
        name_row.setSpacing(20)
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setMinimumHeight(40)
        self.first_name_input.setStyleSheet(self.input_style())
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setMinimumHeight(40)
        self.last_name_input.setStyleSheet(self.input_style())
        name_row.addWidget(self.first_name_input)
        name_row.addWidget(self.last_name_input)
        form_layout.addLayout(name_row)

        # Email
        email_label = QLabel("Email")
        email_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 2px;")
        form_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email (@petmedix.med)")
        self.email_input.setMinimumHeight(40)
        self.email_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.email_input)

        # Password
        password_label = QLabel("Password")
        password_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 2px;")
        form_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.password_input)

        # Role
        role_label = QLabel("Role")
        role_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 2px;")
        form_layout.addWidget(role_label)
        self.role_combo = QComboBox()
        self.role_combo.addItems(['Veterinarian', 'Receptionist'])
        self.role_combo.setMinimumHeight(40)
        self.role_combo.setStyleSheet(self.input_style(combo=True))
        form_layout.addWidget(self.role_combo)

        # License Number
        license_label = QLabel("License Number")
        license_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 2px;")
        form_layout.addWidget(license_label)
        self.license_number_input = QLineEdit()
        self.license_number_input.setPlaceholderText("Enter license number")
        self.license_number_input.setMinimumHeight(40)
        self.license_number_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.license_number_input)

        # Connect role change to show/hide license number
        self.role_combo.currentTextChanged.connect(self.on_role_changed)
        self.on_role_changed(self.role_combo.currentText())

        layout.addWidget(form_area)
        layout.addStretch()

        # Buttons
        button_row = QHBoxLayout()
        button_row.setContentsMargins(0, 0, 35, 50)
        button_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(140, 50)
        cancel_btn.setStyleSheet(self.cancel_button_style())
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Save")
        save_btn.setFixedSize(140, 50)
        save_btn.setStyleSheet(self.save_button_style())
        save_btn.clicked.connect(self.save_user)
        button_row.addWidget(cancel_btn)
        button_row.addWidget(save_btn)
        layout.addLayout(button_row)

    def input_style(self, combo=False):
        if combo:
            return """
                QComboBox {
                    font-family: 'Lato';
                    padding: 8px;
                    background-color: #fff;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    font-size: 16px;
                }
                QComboBox::drop-down {
                    width: 30px;
                    border: none;
                }
                QComboBox QAbstractItemView {
                    font-family: 'Lato';
                    font-size: 16px;
                }
            """
        return """
            QLineEdit {
                font-family: 'Lato';
                padding: 8px;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 10px;
                font-size: 16px;
            }
        """

    def save_button_style(self):
        return """
            QPushButton {
                background-color: #012547;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                color: white;
                font-family: Lato;
            }
            QPushButton:hover {
                background-color: #01315d;
            }
        """

    def cancel_button_style(self):
        return """
            QPushButton {
                background-color: #f5f5f5;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                color: #012547;
                font-family: Lato;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """

    def on_role_changed(self, role):
        self.license_number_input.setVisible(role == 'Veterinarian')
        if role != 'Veterinarian':
            self.license_number_input.clear()

    def save_user(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()
        license_number = self.license_number_input.text() if role == 'Veterinarian' else None

        if not all([first_name, last_name, email, password, role]):
            show_message(self, "Please fill in all fields", QMessageBox.Warning)
            return

        if not email.endswith("@petmedix.med"):
            show_message(self, "Email must end with @petmedix.med", QMessageBox.Warning)
            return

        if role == 'Veterinarian' and not license_number:
            show_message(self, "License number is required for veterinarians", QMessageBox.Warning)
            return

        db = Database()
        try:
            db.cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
            if db.cursor.fetchone():
                show_message(self, "Email already exists", QMessageBox.Warning)
                return
            full_name = f"{first_name} {last_name}"
            user_id = db.create_user(full_name, "", email, password, role, status='Verified', license_number=license_number)
            if user_id:
                show_message(self, "User created successfully!")
                self.parent().update_dashboard_stats()
                self.accept()
            else:
                show_message(self, "Failed to create user", QMessageBox.Critical)
        except Exception as e:
            show_message(self, f"Error creating user: {str(e)}", QMessageBox.Critical)
        finally:
            db.close_connection()

class EditUserDialog(QDialog):
    def __init__(self, parent=None, user_id=None, name=None, email=None, role=None):
        super().__init__(parent)
        self.setWindowTitle("Edit User")
        self.setFixedSize(600, 550)
        self.user_id = user_id
        self.setup_ui(name, email, role)

    def setup_ui(self, name, email, role):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet("background-color: #012547;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 30, 30, 30)
        title_label = QLabel("Edit User")
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        header_layout.addWidget(title_label)
        layout.addWidget(header)

        # Main form area
        form_area = QWidget()
        form_layout = QVBoxLayout(form_area)
        form_layout.setContentsMargins(40, 10, 40, 0)
        form_layout.setSpacing(5)

        # Name
        name_label = QLabel("Name")
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 2px;")
        form_layout.addWidget(name_label)
        name_row = QHBoxLayout()
        name_row.setSpacing(20)
        self.name_input = QLineEdit()
        self.name_input.setText(name)
        self.name_input.setMinimumHeight(40)
        self.name_input.setStyleSheet(self.input_style())
        name_row.addWidget(self.name_input)
        form_layout.addLayout(name_row)

        # Email
        email_field_layout = QVBoxLayout()
        email_field_layout.setSpacing(2)
        email_label = QLabel("Email")
        email_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 2px;")
        email_field_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setText(email)
        self.email_input.setMinimumHeight(40)
        self.email_input.setStyleSheet(self.input_style())
        email_field_layout.addWidget(self.email_input)
        form_layout.addLayout(email_field_layout)

        # Role
        role_field_layout = QVBoxLayout()
        role_field_layout.setSpacing(2)
        role_label = QLabel("Role")
        role_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 2px;")
        role_field_layout.addWidget(role_label)
        self.role_combo = QComboBox()
        self.role_combo.addItems(['Veterinarian', 'Receptionist'])
        self.role_combo.setCurrentText(role)
        self.role_combo.setMinimumHeight(40)
        self.role_combo.setStyleSheet(self.input_style(combo=True))
        role_field_layout.addWidget(self.role_combo)
        form_layout.addLayout(role_field_layout)

        # License Number
        license_field_layout = QVBoxLayout()
        license_field_layout.setSpacing(2)
        license_label = QLabel("License Number")
        license_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 2px;")
        license_field_layout.addWidget(license_label)
        self.license_number_input = QLineEdit()
        self.license_number_input.setMinimumHeight(40)
        self.license_number_input.setStyleSheet(self.input_style())
        # Load existing license number if available
        db = Database()
        try:
            db.cursor.execute("SELECT license_number FROM users WHERE user_id = ?", (self.user_id,))
            result = db.cursor.fetchone()
            if result and result[0]:
                self.license_number_input.setText(result[0])
        except Exception as e:
            print(f"Error loading license number: {e}")
        finally:
            db.close_connection()
        license_field_layout.addWidget(self.license_number_input)
        form_layout.addLayout(license_field_layout)

        # Connect role change to show/hide license number
        self.role_combo.currentTextChanged.connect(self.on_role_changed)
        self.on_role_changed(self.role_combo.currentText())

        layout.addWidget(form_area)
        layout.addStretch()

        # Buttons
        button_row = QHBoxLayout()
        button_row.setContentsMargins(0, 10, 35, 10)
        button_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedSize(140, 50)
        cancel_btn.setStyleSheet(self.cancel_button_style())
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Save")
        save_btn.setFixedSize(140, 50)
        save_btn.setStyleSheet(self.save_button_style())
        save_btn.clicked.connect(self.save_changes)
        button_row.addWidget(cancel_btn)
        button_row.addWidget(save_btn)
        layout.addLayout(button_row)

    def input_style(self, combo=False):
        if combo:
            return """
                QComboBox {
                    font-family: 'Lato';
                    padding: 8px;
                    background-color: #fff;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    font-size: 16px;
                }
                QComboBox::drop-down {
                    width: 30px;
                    border: none;
                }
                QComboBox QAbstractItemView {
                    font-family: 'Lato';
                    font-size: 16px;
                }
            """
        return """
            QLineEdit {
                font-family: 'Lato';
                padding: 8px;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 10px;
                font-size: 16px;
            }
        """

    def save_button_style(self):
        return """
            QPushButton {
                background-color: #012547;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                color: white;
                font-family: Lato;
            }
            QPushButton:hover {
                background-color: #01315d;
            }
        """

    def cancel_button_style(self):
        return """
            QPushButton {
                background-color: #f5f5f5;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                color: #012547;
                font-family: Lato;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """

    def on_role_changed(self, role):
        self.license_number_input.setVisible(role == 'Veterinarian')
        if role != 'Veterinarian':
            self.license_number_input.clear()

    def save_changes(self):
        name = self.name_input.text()
        email = self.email_input.text()
        role = self.role_combo.currentText()
        license_number = self.license_number_input.text() if role == 'Veterinarian' else None

        if not all([name, email, role]):
            show_message(self, "Please fill in all fields", QMessageBox.Warning)
            return

        if not email.endswith("@petmedix.med"):
            show_message(self, "Email must end with @petmedix.med", QMessageBox.Warning)
            return

        if role == 'Veterinarian' and not license_number:
            show_message(self, "License number is required for veterinarians", QMessageBox.Warning)
            return

        db = Database()
        try:
            db.cursor.execute("SELECT 1 FROM users WHERE email = ? AND user_id != ?", (email, self.user_id))
            if db.cursor.fetchone():
                show_message(self, "Email already exists", QMessageBox.Warning)
                return
            db.cursor.execute("""
                UPDATE users 
                SET name = ?, email = ?, role = ?, license_number = ?
                WHERE user_id = ?
            """, (name, email, role, license_number, self.user_id))
            db.conn.commit()
            show_message(self, "User updated successfully!")
            self.accept()
        except Exception as e:
            show_message(self, f"Error updating user: {str(e)}", QMessageBox.Critical)
        finally:
            db.close_connection() 