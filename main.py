import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from modules.login import LoginWindow
from modules.petmedix import PetMedix

# Import development configuration
try:
    from dev_config import DEVELOPMENT_MODE, DEV_USER
except ImportError:
    # Fallback if dev_config.py doesn't exist
    DEVELOPMENT_MODE = False
    DEV_USER = {
        "user_id": "DEV001",
        "role": "Admin",
        "last_name": "Developer", 
        "first_name": "Test"
    }

app = QApplication(sys.argv)

app.setWindowIcon(QIcon("assets/logo.ico"))

if DEVELOPMENT_MODE:
    # Development mode: directly open main application
    print(f"🚀 Development mode enabled - Logging in as {DEV_USER['role']}")
    window = PetMedix(
        user_id=DEV_USER["user_id"], 
        role=DEV_USER["role"],
        last_name=DEV_USER["last_name"], 
        first_name=DEV_USER["first_name"]
    )
else:
    # Production mode: start with login
    print("🔐 Production mode - Starting with login")
    window = LoginWindow()

screen = app.primaryScreen()
size = screen.size()
screen_width = size.width()
screen_height = size.height()

window.resize(int(screen_width * 0.8), int(screen_height * 0.8))

# Show the window maximized (not full-screen)
window.showMaximized()

sys.exit(app.exec())                    