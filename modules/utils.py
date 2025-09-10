from PySide6.QtWidgets import QMessageBox

def create_styled_message_box(icon, title, text):
    """Create a styled QMessageBox."""
    message_box = QMessageBox()
    message_box.setIcon(icon)
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setStyleSheet("""
        QMessageBox { 
            background-color: white; 
        }
        QMessageBox QLabel { 
            color: #012547; 
            font-size: 14px; 
            font-family: Lato;
            padding: 10px;
        }
        QMessageBox QPushButton { 
            background-color: #012547; 
            color: white; 
            border: none;
            padding: 8px 20px;
            border-radius: 5px;
            font-weight: bold;
            min-width: 80px;
            font-family: Lato;
        }
        QMessageBox QPushButton:hover { 
            background-color: #023d6d; 
        }
        QMessageBox QPushButton:pressed {
            background-color: #001e3d;
        }
    """)
    return message_box

def show_message(parent, message, icon=QMessageBox.Information):
    """Show a message box without a title."""
    msg = create_styled_message_box(icon, "", message)
    return msg.exec()