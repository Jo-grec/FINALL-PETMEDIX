from PySide6.QtWidgets import QMessageBox

def create_styled_message_box(icon, title, text):
    """Create a styled QMessageBox."""
    message_box = QMessageBox()
    message_box.setIcon(icon)
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setStyleSheet("""
        QMessageBox { 
            background-color: #FED766; 
            border: 2px solid #012547; 
            border-radius: 10px; 
        }
        QMessageBox QLabel { 
            color: #012547; 
            font-size: 14px; 
            font-weight: bold; 
        }
        QMessageBox QPushButton { 
            background-color: #012547; 
            color: white; 
            border-radius: 5px; 
            padding: 5px 10px; 
        }
        QMessageBox QPushButton:hover { 
            background-color: #014A7F; 
        }
    """)
    return message_box