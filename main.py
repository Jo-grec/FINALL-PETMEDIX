import sys
from PySide6.QtWidgets import QApplication
from modules.login import LoginWindow
from modules.signup import SignUpWindow

app = QApplication(sys.argv)

window = LoginWindow()
window = SignUpWindow()

screen = app.primaryScreen()
size = screen.size()
screen_width = size.width()
screen_height = size.height()

window.resize(int(screen_width * 0.8), int(screen_height * 0.8))

window.show()

sys.exit(app.exec())
