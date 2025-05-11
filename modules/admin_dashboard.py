from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QLineEdit,
    QComboBox, QHeaderView, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QColor
from modules.database import Database
from modules.utils import show_message
import os

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
        users_card = self.create_stat_card("Total Users", "0", "users")
        stats_layout.addWidget(users_card)

        # Total Vets Card
        vets_card = self.create_stat_card("Veterinarians", "0", "vets")
        stats_layout.addWidget(vets_card)

        # Total Receptionists Card
        receptionists_card = self.create_stat_card("Receptionists", "0", "receptionists")
        stats_layout.addWidget(receptionists_card)

        layout.addLayout(stats_layout)
        layout.addStretch()

    def create_stat_card(self, title, value, icon):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        card.setMinimumHeight(150)

        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; color: #666;")
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #012547;")
        
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
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels([
            "User ID", "Name", "Email", "Role", "Status", "Created Date"
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
            # Get total users count
            db.cursor.execute("SELECT COUNT(*) FROM users")
            total_users = db.cursor.fetchone()[0]

            # Get vets count
            db.cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Veterinarian'")
            total_vets = db.cursor.fetchone()[0]

            # Get receptionists count
            db.cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Receptionist'")
            total_receptionists = db.cursor.fetchone()[0]

            # Update the stat cards
            for i in range(self.dashboard_page.layout().count()):
                widget = self.dashboard_page.layout().itemAt(i).widget()
                if isinstance(widget, QFrame):
                    value_label = widget.findChild(QLabel, "", Qt.FindChildrenRecursively)[1]
                    if "Total Users" in widget.findChildren(QLabel)[0].text():
                        value_label.setText(str(total_users))
                    elif "Veterinarians" in widget.findChildren(QLabel)[0].text():
                        value_label.setText(str(total_vets))
                    elif "Receptionists" in widget.findChildren(QLabel)[0].text():
                        value_label.setText(str(total_receptionists))

        except Exception as e:
            print(f"❌ Error updating dashboard stats: {e}")
        finally:
            db.close_connection()

    def load_users(self):
        db = Database()
        try:
            db.cursor.execute("""
                SELECT user_id, name, email, role, status, created_date
                FROM users
                WHERE role IN ('Veterinarian', 'Receptionist')
                ORDER BY created_date DESC
            """)
            users = db.cursor.fetchall()

            self.users_table.setRowCount(len(users))
            for row, user in enumerate(users):
                # Add user data
                for col, value in enumerate(user):
                    item = QTableWidgetItem(str(value))
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
        name = self.users_table.item(row, 1).text()
        email = self.users_table.item(row, 2).text()
        role = self.users_table.item(row, 3).text()
        
        # Create confirmation dialog
        confirm = QMessageBox()
        confirm.setWindowTitle("Confirm User Verification")
        confirm.setIconPixmap(QPixmap("assets/authentication 1.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Create custom message with styling
        message = f"""
        <div style='font-size: 14px; color: #012547; margin-bottom: 15px;'>
            <p style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>Please confirm the following user details:</p>
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;'>
                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> {email}</p>
                <p><b>Role:</b> {role}</p>
            </div>
            <p style='margin-top: 15px;'>Do you want to verify this user?</p>
        </div>
        """
        confirm.setText(message)
        
        # Style the buttons
        confirm.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QPushButton {
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton#qt_msgbox_yesbutton {
                background-color: #012547;
                color: white;
                border: none;
            }
            QPushButton#qt_msgbox_yesbutton:hover {
                background-color: #023d6d;
            }
            QPushButton#qt_msgbox_yesbutton:pressed {
                background-color: #001e3d;
            }
            QPushButton#qt_msgbox_nobutton {
                background-color: #012547;
                color: white;
                border: none;
            }
            QPushButton#qt_msgbox_nobutton:hover {
                background-color: #023d6d;
            }
            QPushButton#qt_msgbox_nobutton:pressed {
                background-color: #001e3d;
            }
        """)
        
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
                
                # Show success message with styling
                success_msg = QMessageBox()
                success_msg.setWindowTitle("Success")
                success_msg.setIconPixmap(QPixmap("assets/authentication 1.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                success_msg.setText(f"""
                    <div style='font-size: 14px; color: #012547;'>
                        <p style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>User Verified Successfully!</p>
                        <p>The user has been verified and can now access the system.</p>
                    </div>
                """)
                success_msg.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                    }
                    QPushButton {
                        padding: 8px 20px;
                        border-radius: 5px;
                        font-weight: bold;
                        min-width: 80px;
                        background-color: #012547;
                        color: white;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #023d6d;
                    }
                    QPushButton:pressed {
                        background-color: #001e3d;
                    }
                """)
                success_msg.setStandardButtons(QMessageBox.Ok)
                success_msg.exec()
                
                self.load_users()
                # Update dashboard stats after verifying user
                self.update_dashboard_stats()
            except Exception as e:
                show_message(self, f"Error verifying user: {str(e)}", QMessageBox.Critical)
            finally:
                db.close_connection()

    def delete_user(self, row):
        user_id = self.users_table.item(row, 0).text()
        confirm = QMessageBox()
        confirm.setIcon(QMessageBox.Question)
        confirm.setText("Are you sure you want to delete this user?")
        confirm.setWindowTitle("Confirm Deletion")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if confirm.exec() == QMessageBox.Yes:
            db = Database()
            try:
                db.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                db.conn.commit()
                show_message(self, "User deleted successfully!")
                self.load_users()
                # Update dashboard stats after deleting user
                self.update_dashboard_stats()
            except Exception as e:
                show_message(self, f"Error deleting user: {str(e)}", QMessageBox.Critical)
            finally:
                db.close_connection()

    def logout(self):
        """Handle logout action."""
        # Create confirmation dialog
        confirm = QMessageBox()
        confirm.setWindowTitle("Confirm Logout")
        confirm.setIconPixmap(QPixmap("assets/authentication 1.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Create custom message with styling
        message = """
        <div style='font-size: 14px; color: #012547; margin-bottom: 15px;'>
            <p style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>Are you sure you want to logout?</p>
            <p>You will be redirected to the login page.</p>
        </div>
        """
        confirm.setText(message)
        
        # Style the buttons
        confirm.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QPushButton {
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton#qt_msgbox_yesbutton {
                background-color: #012547;
                color: white;
                border: none;
            }
            QPushButton#qt_msgbox_yesbutton:hover {
                background-color: #023d6d;
            }
            QPushButton#qt_msgbox_yesbutton:pressed {
                background-color: #001e3d;
            }
            QPushButton#qt_msgbox_nobutton {
                background-color: #012547;
                color: white;
                border: none;
            }
            QPushButton#qt_msgbox_nobutton:hover {
                background-color: #023d6d;
            }
            QPushButton#qt_msgbox_nobutton:pressed {
                background-color: #001e3d;
            }
        """)
        
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
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
            name = self.users_table.item(row, 1).text()
            email = self.users_table.item(row, 2).text()
            role = self.users_table.item(row, 3).text()
            
            # Create confirmation dialog
            confirm = QMessageBox()
            confirm.setWindowTitle("Confirm User Unverification")
            confirm.setIconPixmap(QPixmap("assets/authentication 1.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            # Create custom message with styling
            message = f"""
            <div style='font-size: 14px; color: #012547; margin-bottom: 15px;'>
                <p style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>Please confirm the following user details:</p>
                <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;'>
                    <p><b>Name:</b> {name}</p>
                    <p><b>Email:</b> {email}</p>
                    <p><b>Role:</b> {role}</p>
                </div>
                <p style='margin-top: 15px;'>Do you want to unverify this user?</p>
            </div>
            """
            confirm.setText(message)
            
            # Style the buttons
            confirm.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QPushButton {
                    padding: 8px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton#qt_msgbox_yesbutton {
                    background-color: #012547;
                    color: white;
                    border: none;
                }
                QPushButton#qt_msgbox_yesbutton:hover {
                    background-color: #023d6d;
                }
                QPushButton#qt_msgbox_yesbutton:pressed {
                    background-color: #001e3d;
                }
                QPushButton#qt_msgbox_nobutton {
                    background-color: #012547;
                    color: white;
                    border: none;
                }
                QPushButton#qt_msgbox_nobutton:hover {
                    background-color: #023d6d;
                }
                QPushButton#qt_msgbox_nobutton:pressed {
                    background-color: #001e3d;
                }
            """)
            
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
                    
                    # Show success message with styling
                    success_msg = QMessageBox()
                    success_msg.setWindowTitle("Success")
                    success_msg.setIconPixmap(QPixmap("assets/authentication 1.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    success_msg.setText(f"""
                        <div style='font-size: 14px; color: #012547;'>
                            <p style='font-weight: bold; font-size: 16px; margin-bottom: 10px;'>User Unverified Successfully!</p>
                            <p>The user's status has been changed to Pending.</p>
                        </div>
                    """)
                    success_msg.setStyleSheet("""
                        QMessageBox {
                            background-color: white;
                        }
                        QPushButton {
                            padding: 8px 20px;
                            border-radius: 5px;
                            font-weight: bold;
                            min-width: 80px;
                            background-color: #012547;
                            color: white;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #023d6d;
                        }
                        QPushButton:pressed {
                            background-color: #001e3d;
                        }
                    """)
                    success_msg.setStandardButtons(QMessageBox.Ok)
                    success_msg.exec()
                    
                    self.load_users()
                    # Update dashboard stats after unverifying user
                    self.update_dashboard_stats()
                except Exception as e:
                    show_message(self, f"Error unverifying user: {str(e)}", QMessageBox.Critical)
                finally:
                    db.close_connection()

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
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 14px;
                color: #012547;
                font-weight: bold;
                margin-bottom: 2px;
            }
            QLabel#sectionLabel {
                font-size: 16px;
                color: #012547;
                font-weight: bold;
                margin: 0px;
                padding: 0px;
            }
            QLabel#sectionLabel#personalInfo {
                margin-bottom: 0px;
            }
            QLabel#sectionLabel#accountInfo, QLabel#sectionLabel#roleInfo {
                margin-bottom: 15px;
            }
            QLineEdit, QComboBox {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                font-size: 13px;
                min-height: 20px;
                margin: 0px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #012547;
            }
            QComboBox {
                padding-right: 30px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(assets/dropdown.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #f0f0f0;
                selection-color: #012547;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 30px;
                padding: 5px 10px;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Form container
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 15px;
            }
            QLabel#sectionLabel {
                font-size: 16px;
                color: #012547;
                font-weight: bold;
                margin: 0px;
                padding: 0px;
            }
            QLabel#sectionLabel#personalInfo {
                margin-bottom: 0px;
            }
            QLabel#sectionLabel#accountInfo, QLabel#sectionLabel#roleInfo {
                margin-bottom: 15px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(15, 15, 15, 15)

        # Form fields
        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(0)

        # Name fields container
        name_container = QHBoxLayout()
        name_container.setSpacing(10)

        # First Name field
        first_name_container = QVBoxLayout()
        first_name_label = QLabel("First Name")
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter first name")
        first_name_container.addWidget(first_name_label)
        first_name_container.addWidget(self.first_name_input)
        first_name_container.setContentsMargins(0, 0, 0, 0)
        first_name_container.setSpacing(2)
        name_container.addLayout(first_name_container)

        # Last Name field
        last_name_container = QVBoxLayout()
        last_name_label = QLabel("Last Name")
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter last name")
        last_name_container.addWidget(last_name_label)
        last_name_container.addWidget(self.last_name_input)
        last_name_container.setContentsMargins(0, 0, 0, 0)
        last_name_container.setSpacing(2)
        name_container.addLayout(last_name_container)

        fields_layout.addLayout(name_container)

        # Email field
        email_container = QVBoxLayout()
        email_label = QLabel("Email Address")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@petmedix.med")
        email_container.addWidget(email_label)
        email_container.addWidget(self.email_input)
        email_container.setContentsMargins(0, 0, 0, 0)
        email_container.setSpacing(2)
        fields_layout.addLayout(email_container)

        # Password field
        password_container = QVBoxLayout()
        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter secure password")
        password_container.addWidget(password_label)
        password_container.addWidget(self.password_input)
        password_container.setContentsMargins(0, 0, 0, 0)
        password_container.setSpacing(2)
        fields_layout.addLayout(password_container)

        # Role field
        role_container = QVBoxLayout()
        role_label = QLabel("Role")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Veterinarian", "Receptionist"])
        
        # Add icons to combo box items
        vet_icon = QIcon(os.path.join("assets", "medical.png"))
        receptionist_icon = QIcon(os.path.join("assets", "client.png"))
        
        self.role_combo.setItemIcon(0, vet_icon)
        self.role_combo.setItemIcon(1, receptionist_icon)
        self.role_combo.setIconSize(QSize(20, 20))
        
        role_container.addWidget(role_label)
        role_container.addWidget(self.role_combo)
        role_container.setContentsMargins(0, 0, 0, 0)
        role_container.setSpacing(2)
        fields_layout.addLayout(role_container)

        form_layout.addLayout(fields_layout)
        main_layout.addWidget(form_container)

        # Buttons container
        buttons_container = QFrame()
        buttons_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(15, 15, 15, 15)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Create User")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #023d6d;
            }
        """)
        save_btn.clicked.connect(self.save_user)

        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)

        main_layout.addWidget(buttons_container)

    def save_user(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        role = self.role_combo.currentText()

        if not all([first_name, last_name, email, password, role]):
            show_message(self, "Please fill in all fields", QMessageBox.Warning)
            return

        # Validate email domain
        if not email.endswith("@petmedix.med"):
            show_message(self, "Email must end with @petmedix.med", QMessageBox.Warning)
            return

        db = Database()
        try:
            # Check if email already exists
            db.cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
            if db.cursor.fetchone():
                show_message(self, "Email already exists", QMessageBox.Warning)
                return

            # Create new user with full name
            full_name = f"{first_name} {last_name}"
            user_id = db.create_user(full_name, "", email, password, role)
            if user_id:
                show_message(self, "User created successfully!")
                # Update dashboard stats after creating new user
                self.parent().update_dashboard_stats()
                self.accept()
            else:
                show_message(self, "Failed to create user", QMessageBox.Critical)

        except Exception as e:
            show_message(self, f"Error creating user: {str(e)}", QMessageBox.Critical)
        finally:
            db.close_connection()

class EditUserDialog(QDialog):
    def __init__(self, parent=None, user_id=None, name="", email="", role=""):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("Edit User")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)  # Reduced height
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 14px;
                color: #012547;
                font-weight: bold;
                margin-bottom: 2px;
            }
            QLineEdit, QComboBox {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                font-size: 13px;
                min-height: 20px;
                margin: 0px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #012547;
            }
            QComboBox {
                padding-right: 30px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(assets/dropdown.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #f0f0f0;
                selection-color: #012547;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 30px;
                padding: 5px 10px;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
        """)
        self.setup_ui(name, email, role)

    def setup_ui(self, name, email, role):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Form container
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(8)
        form_layout.setContentsMargins(15, 15, 15, 15)

        # Form fields
        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(10)

        # Name fields container
        name_container = QHBoxLayout()
        name_container.setSpacing(10)

        # Split name into first and last name
        name_parts = name.split()
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        # First Name field
        first_name_container = QVBoxLayout()
        first_name_label = QLabel("First Name")
        self.first_name_input = QLineEdit()
        self.first_name_input.setText(first_name)
        self.first_name_input.setPlaceholderText("Enter first name")
        first_name_container.addWidget(first_name_label)
        first_name_container.addWidget(self.first_name_input)
        first_name_container.setContentsMargins(0, 0, 0, 0)
        first_name_container.setSpacing(2)
        name_container.addLayout(first_name_container)

        # Last Name field
        last_name_container = QVBoxLayout()
        last_name_label = QLabel("Last Name")
        self.last_name_input = QLineEdit()
        self.last_name_input.setText(last_name)
        self.last_name_input.setPlaceholderText("Enter last name")
        last_name_container.addWidget(last_name_label)
        last_name_container.addWidget(self.last_name_input)
        last_name_container.setContentsMargins(0, 0, 0, 0)
        last_name_container.setSpacing(2)
        name_container.addLayout(last_name_container)

        fields_layout.addLayout(name_container)

        # Email field
        email_container = QVBoxLayout()
        email_label = QLabel("Email Address")
        self.email_input = QLineEdit()
        self.email_input.setText(email)
        self.email_input.setPlaceholderText("example@petmedix.med")
        email_container.addWidget(email_label)
        email_container.addWidget(self.email_input)
        email_container.setContentsMargins(0, 0, 0, 0)
        email_container.setSpacing(2)
        fields_layout.addLayout(email_container)

        # Role field
        role_container = QVBoxLayout()
        role_label = QLabel("Role")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Veterinarian", "Receptionist"])
        
        # Add icons to combo box items
        vet_icon = QIcon(os.path.join("assets", "medical.png"))
        receptionist_icon = QIcon(os.path.join("assets", "client.png"))
        
        self.role_combo.setItemIcon(0, vet_icon)
        self.role_combo.setItemIcon(1, receptionist_icon)
        self.role_combo.setIconSize(QSize(20, 20))
        
        # Set current role
        index = self.role_combo.findText(role)
        if index >= 0:
            self.role_combo.setCurrentIndex(index)
        
        role_container.addWidget(role_label)
        role_container.addWidget(self.role_combo)
        role_container.setContentsMargins(0, 0, 0, 0)
        role_container.setSpacing(2)
        fields_layout.addLayout(role_container)

        form_layout.addLayout(fields_layout)
        main_layout.addWidget(form_container)

        # Buttons container
        buttons_container = QFrame()
        buttons_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(15, 15, 15, 15)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: none;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #012547;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #023d6d;
            }
        """)
        save_btn.clicked.connect(self.save_changes)

        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)

        main_layout.addWidget(buttons_container)

    def save_changes(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        email = self.email_input.text()
        role = self.role_combo.currentText()

        if not all([first_name, last_name, email, role]):
            show_message(self, "Please fill in all fields", QMessageBox.Warning)
            return

        # Validate email domain
        if not email.endswith("@petmedix.med"):
            show_message(self, "Email must end with @petmedix.med", QMessageBox.Warning)
            return

        db = Database()
        try:
            # Check if email already exists for other users
            db.cursor.execute("SELECT 1 FROM users WHERE email = ? AND user_id != ?", (email, self.user_id))
            if db.cursor.fetchone():
                show_message(self, "Email already exists", QMessageBox.Warning)
                return

            # Update user
            full_name = f"{first_name} {last_name}"
            db.cursor.execute("""
                UPDATE users
                SET name = ?, email = ?, role = ?
                WHERE user_id = ?
            """, (full_name, email, role, self.user_id))
            db.conn.commit()
            
            show_message(self, "User updated successfully!")
            self.accept()

        except Exception as e:
            show_message(self, f"Error updating user: {str(e)}", QMessageBox.Critical)
        finally:
            db.close_connection() 