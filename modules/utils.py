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
            border: 1px solid #e0e0e0; 
            border-radius: 8px; 
        }
        QMessageBox QLabel { 
            color: #333333; 
            font-size: 16px; 
            font-weight: normal;
            padding: 10px;
            font-family: Lato;
        }
        QMessageBox QPushButton { 
            background-color: #012547; 
            color: white; 
            border-radius: 4px; 
            padding: 8px 16px;
            font-size: 13px;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover { 
            background-color: #014A7F; 
        }
        QMessageBox QPushButton:pressed {
            background-color: #001e3d;
        }
    """)
    return message_box

def show_message(parent, message, icon=QMessageBox.Information):
    """Show a message box without a title."""
    msg = QMessageBox(parent)
    msg.setIcon(icon)
    msg.setText(message)
    msg.setWindowTitle("")  # Remove title
    msg.setStyleSheet("""
        QMessageBox {
            background-color: white;
        }
        QMessageBox QLabel {
            color: black;
            font-size: 14px;
        }
        QPushButton {
            background-color: #012547;
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 5px;
            min-width: 80px;
            font-family: Poppins;
        }
        QPushButton:hover {
            background-color: #01315d;
        }
    """)
    return msg.exec()
