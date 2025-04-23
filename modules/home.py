from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, QScrollBar, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from modules.database import Database  # Import the Database class

def get_home_widget():
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 30)
        layout.setSpacing(0)

        boxes_layout = QHBoxLayout()

        # Connect to the database and fetch counts
        db = Database()
        clients_count, medical_records_count, appointments_count = db.fetch_counts()
        db.close_connection()

        # Box 1: Clients
        box1 = QWidget()
        box1.setStyleSheet("background-color: #012547;")
        box1.setFixedWidth(300)
        box1.setFixedHeight(150)
        box1.setObjectName("Box1")

        icon_label = QLabel(box1)
        icon_label.setObjectName("IconLabel")
        pixmap = QPixmap("assets/client.png")
        icon_label.setPixmap(pixmap)
        icon_label.setFixedWidth(100)
        icon_label.setScaledContents(True)
        icon_label.setAlignment(Qt.AlignCenter)

        number_label = QLabel(str(clients_count), box1)  # Dynamic count
        number_label.setObjectName("NumberLabel")
        number_label.setAlignment(Qt.AlignCenter)

        clients_label = QLabel("clients", box1)
        clients_label.setObjectName("ClientsLabel")
        clients_label.setAlignment(Qt.AlignCenter)
        clients_label.setStyleSheet("color: white; font-size: 14px;")

        icon_and_number_layout = QHBoxLayout()
        icon_and_number_layout.addWidget(icon_label)
        icon_and_number_layout.addWidget(number_label)
        icon_and_number_layout.setAlignment(Qt.AlignCenter)

        box1_layout = QVBoxLayout(box1)
        box1_layout.addLayout(icon_and_number_layout)
        box1_layout.addWidget(clients_label)
        box1_layout.setAlignment(Qt.AlignCenter)

        boxes_layout.addWidget(box1)

        # Box 2: Medical Records
        box2 = QWidget()
        box2.setStyleSheet("background-color: #012547;")
        box2.setFixedWidth(300)
        box2.setFixedHeight(150)
        box2.setObjectName("Box2")

        icon_label2 = QLabel(box2)
        icon_label2.setObjectName("IconLabel2")
        pixmap2 = QPixmap("assets/medical.png")
        icon_label2.setPixmap(pixmap2)
        icon_label2.setFixedWidth(100)
        icon_label2.setScaledContents(True)
        icon_label2.setAlignment(Qt.AlignCenter)

        number_label2 = QLabel(str(medical_records_count), box2)  # Dynamic count
        number_label2.setObjectName("NumberLabel2")
        number_label2.setAlignment(Qt.AlignCenter)

        medical_label = QLabel("medical records", box2)
        medical_label.setObjectName("MedicalLabel")
        medical_label.setAlignment(Qt.AlignCenter)
        medical_label.setStyleSheet("color: white; font-size: 14px;")

        icon_and_number_layout2 = QHBoxLayout()
        icon_and_number_layout2.addWidget(icon_label2)
        icon_and_number_layout2.addWidget(number_label2)
        icon_and_number_layout2.setAlignment(Qt.AlignCenter)

        box2_layout = QVBoxLayout(box2)
        box2_layout.addLayout(icon_and_number_layout2)
        box2_layout.addWidget(medical_label)
        box2_layout.setAlignment(Qt.AlignCenter)

        boxes_layout.addWidget(box2)

        # Box 3: Appointments
        box3 = QWidget()
        box3.setStyleSheet("background-color: #012547;")
        box3.setFixedWidth(300)
        box3.setFixedHeight(150)
        box3.setObjectName("Box3")

        icon_label3 = QLabel(box3)
        icon_label3.setObjectName("IconLabel3")
        pixmap3 = QPixmap("assets/appoint.png")
        icon_label3.setPixmap(pixmap3)
        icon_label3.setFixedWidth(100)
        icon_label3.setScaledContents(True)
        icon_label3.setAlignment(Qt.AlignCenter)

        number_label3 = QLabel(str(appointments_count), box3)  # Dynamic count
        number_label3.setObjectName("NumberLabel3")
        number_label3.setAlignment(Qt.AlignCenter)

        appointments_label = QLabel("appointments", box3)
        appointments_label.setObjectName("AppointmentsLabel")
        appointments_label.setAlignment(Qt.AlignCenter)
        appointments_label.setStyleSheet("color: white; font-size: 14px;")

        icon_and_number_layout3 = QHBoxLayout()
        icon_and_number_layout3.addWidget(icon_label3)
        icon_and_number_layout3.addWidget(number_label3)
        icon_and_number_layout3.setAlignment(Qt.AlignCenter)

        box3_layout = QVBoxLayout(box3)
        box3_layout.addLayout(icon_and_number_layout3)
        box3_layout.addWidget(appointments_label)
        box3_layout.setAlignment(Qt.AlignCenter)

        boxes_layout.addWidget(box3)

        # Add boxes layout to the content layout
        layout.addLayout(boxes_layout)

            # Create the text label "Recent Reports" and align it with the first box
        recent_reports_label = QLabel("Recent Reports")
        recent_reports_label.setMaximumHeight(80)  # Set a maximum height for the label
        recent_reports_label.setStyleSheet("background-color: #012547;")  # Set background color
        recent_reports_label.setAlignment(Qt.AlignLeft)  # Align to the left
        recent_reports_label.setObjectName("RecentReportsLabel")

        # Add the label below the boxes, aligned with the first box
        layout.addWidget(recent_reports_label)
        

        # Create the table for Consultation Data
        table_widget = QTableWidget(20, 4)
        table_widget.setContentsMargins(0, 0, 0, 0)
        table_widget.setObjectName("ConsultationTable")        
        table_widget.setHorizontalHeaderLabels(["Consultation Date", "Pet", "Owner/Client", "Veterinarian/Staff in Charge"])
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
    
            
        header = table_widget.horizontalHeader()
        header.setStyleSheet("""
                background-color: #012547;
                font-family: Poppins;
                color: black;
                font-weight: bold;
                font-size: 16px;
                font-style: normal;
                line-height: 20px;
            """)
            
            # Column widths
        table_widget.setColumnWidth(0, 318)
        table_widget.setColumnWidth(1, 318)
        table_widget.setColumnWidth(2, 318)
        table_widget.setColumnWidth(3, 320)

        # 🛠️ Hide vertical header (row numbers)
        table_widget.verticalHeader().setVisible(False)

        # 🛠️ Disable the visible scrollbars but keep scrolling functionality
        table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # 🛠️ Allow scrolling with mouse wheel
        table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        table_widget.setShowGrid(True)  # Optional: hide cell grid lines
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Optional: make it read-only
        table_widget.setFocusPolicy(Qt.NoFocus)  # Optional: remove ugly blue selection rectangle

        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        table_widget.setFixedHeight(300)

        table_container = QWidget()
        table_container_layout = QHBoxLayout(table_container)
        table_container_layout.setContentsMargins(0, 0, 0, 0)
        table_container_layout.addWidget(table_widget)

        layout.addWidget(table_container)
        
        return content