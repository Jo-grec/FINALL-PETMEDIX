import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from modules.login import LoginWindow

app = QApplication(sys.argv)

app.setWindowIcon(QIcon("assets/logo.ico"))

window = LoginWindow()

screen = app.primaryScreen()
size = screen.size()
screen_width = size.width()
screen_height = size.height()

window.resize(int(screen_width * 0.8), int(screen_height * 0.8))

# Show the window maximized (not full-screen)
window.showMaximized()

sys.exit(app.exec())                    