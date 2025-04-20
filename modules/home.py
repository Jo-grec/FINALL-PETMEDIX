from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, QScrollBar, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
def get_home_widget():
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 30)
        layout.setSpacing(0)
    
        boxes_layout = QHBoxLayout()

        # Box 1
        box1 = QWidget()
        box1.setStyleSheet("background-color: #012547;")  # Example style for box
        box1.setFixedWidth(300)
        box1.setFixedHeight(150)
        box1.setObjectName("Box1")

        icon_label = QLabel(box1)
        icon_label.setObjectName("IconLabel")  # Set object name for the icon
        pixmap = QPixmap("assets/client.png")  # Path to your box image
        icon_label.setPixmap(pixmap)
        icon_label.setFixedWidth(100)
        icon_label.setScaledContents(True)
        icon_label.setAlignment(Qt.AlignCenter)

        number_label = QLabel("10", box1)
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

        # Box 2
        box2 = QWidget()
        box2.setStyleSheet("background-color: #012547;")  # Example style for box
        box2.setFixedWidth(300)
        box2.setFixedHeight(150)
        box2.setObjectName("Box2")

        # Create a QLabel to hold the image (icon) for box2
        icon_label2 = QLabel(box2)
        icon_label2.setObjectName("IconLabel2")  # Set object name for the icon
        pixmap2 = QPixmap("assets/medical.png")  # Path to your second box image
        icon_label2.setPixmap(pixmap2)

        # Adjust the width of the icon
        icon_label2.setFixedWidth(100)  # Set the desired width for the icon
        icon_label2.setScaledContents(True)  # Ensures the image scales with the widget size
        icon_label2.setAlignment(Qt.AlignCenter)

        # Create a QLabel for the number for box2
        number_label2 = QLabel("30", box2)
        number_label2.setObjectName("NumberLabel2")  # Set object name for the number
        number_label2.setAlignment(Qt.AlignCenter)  # Keep the number centered

        # Create a QLabel for the text "Medical Records"
        medical_label = QLabel("medical records", box2)
        medical_label.setObjectName("MedicalLabel")  # Set object name for the text
        medical_label.setAlignment(Qt.AlignCenter)  # Keep the "Medical Records" text centered
        medical_label.setStyleSheet("color: white; font-size: 14px;")  # Optional styling for "Medical Records" text

        # Create a horizontal layout to align the icon and number for box2
        icon_and_number_layout2 = QHBoxLayout()
        icon_and_number_layout2.addWidget(icon_label2)
        icon_and_number_layout2.addWidget(number_label2)
        icon_and_number_layout2.setAlignment(Qt.AlignCenter)  # Keep icon and number aligned as before

        # Create a vertical layout for the icon, number, and medical label
        box2_layout = QVBoxLayout(box2)
        box2_layout.addLayout(icon_and_number_layout2)  # Add icon and number layout
        box2_layout.addWidget(medical_label)  # Add the "Medical Records" text below the number
        box2_layout.setAlignment(Qt.AlignCenter)  # Align everything to the center

        # Add the second box to the layout
        boxes_layout.addWidget(box2)

        # Box 3
        box3 = QWidget()
        box3.setStyleSheet("background-color: #012547;")  # Example style for box
        box3.setFixedWidth(300)
        box3.setFixedHeight(150)
        box3.setObjectName("Box3")

        # Create a QLabel to hold the image (icon) for box2
        icon_label3 = QLabel(box3)
        icon_label3.setObjectName("IconLabel3")  # Set object name for the icon
        pixmap3 = QPixmap("assets/appoint.png")  # Path to your second box image
        icon_label3.setPixmap(pixmap3)

        # Adjust the width of the icon
        icon_label3.setFixedWidth(100)  # Set the desired width for the icon
        icon_label3.setScaledContents(True)  # Ensures the image scales with the widget size
        icon_label3.setAlignment(Qt.AlignCenter)

        # Create a QLabel for the number for box2
        number_label3 = QLabel("5", box3)
        number_label3.setObjectName("NumberLabel3")  # Set object name for the number
        number_label3.setAlignment(Qt.AlignCenter)  # Keep the number centered

        # Create a QLabel for the text "Appointments"
        appointments_label = QLabel("appointments", box3)
        appointments_label.setObjectName("AppointmentsLabel")  # Set object name for the text
        appointments_label.setAlignment(Qt.AlignCenter)  # Keep the "Appointments" text centered
        appointments_label.setStyleSheet("color: white; font-size: 14px;")  # Optional styling for "Appointments" text

        # Create a horizontal layout to align the icon and number for box2
        icon_and_number_layout3 = QHBoxLayout()
        icon_and_number_layout3.addWidget(icon_label3)
        icon_and_number_layout3.addWidget(number_label3)
        icon_and_number_layout3.setAlignment(Qt.AlignCenter)  # Keep icon and number aligned as before

        # Create a vertical layout for the icon, number, and appointments label
        box3_layout = QVBoxLayout(box3)
        box3_layout.addLayout(icon_and_number_layout3)  # Add icon and number layout
        box3_layout.addWidget(appointments_label)  # Add the "Appointments" text below the number
        box3_layout.setAlignment(Qt.AlignCenter)  # Align everything to the center

        # Add the third box to the layout
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
                color: #fff;
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
