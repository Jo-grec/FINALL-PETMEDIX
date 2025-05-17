from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QHeaderView, QTableWidget, QTableWidgetItem, QAbstractItemView, QScrollBar, QSizePolicy
from PySide6.QtGui import QPixmap, QIcon, QColor
from PySide6.QtCore import Qt
from modules.database import Database  # Import the Database class
from datetime import datetime

def get_home_widget():
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
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
        layout.setSpacing(0)  # Ensure no spacing between main layout items

        # Create container for title and table
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container.setStyleSheet("QWidget { margin: 0; padding: 0; }")

        # Create title label
        title_label = QLabel("Recent Reports")
        title_label.setStyleSheet("""
            background-color: #012547;
            color: white;
            font-size: 16px;
            font-weight: bold;
            font-family: Poppins;
            padding: 8px;
            padding-bottom: 0;
            margin: 0;
            border: none;
        """)
        title_label.setFixedHeight(40)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        container_layout.addWidget(title_label)

        # Create the table for Recent Reports
        table_widget = QTableWidget()
        table_widget.setContentsMargins(0, 0, 0, 0)
        table_widget.setObjectName("RecentReportsTable")
        table_widget.setStyleSheet("""
            QTableWidget {
                margin: 0;
                padding: 0;
                border: none;
            }
            QHeaderView::section {
                margin: 0;
                padding: 8px;
                border: none;
                background-color: #012547;
            }
            QHeaderView {
                margin: 0;
                padding: 0;
                border: none;
            }
        """)
        table_widget.setColumnCount(5)

        # Set column headers
        table_widget.setHorizontalHeaderLabels([
            "Consultation Date", 
            "Type",
            "Pet", 
            "Owner/Client", 
            "Veterinarian/Staff in Charge"
        ])
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table_widget.horizontalHeader().setFixedHeight(40)  # Set fixed height for column headers
        table_widget.horizontalHeader().setStyleSheet("""
            QHeaderView::section:horizontal {
                background-color: #012547;
                font-family: Poppins;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 8px;
                margin: 0;
                border: none;
            }
        """)
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
    
        # Column widths - adjusted for 5 columns
        table_widget.setColumnWidth(0, 200)  # Consultation Date
        table_widget.setColumnWidth(1, 250)  # Type
        table_widget.setColumnWidth(2, 250)  # Pet
        table_widget.setColumnWidth(3, 300)  # Owner/Client
        table_widget.setColumnWidth(4, 300)  # Veterinarian

        # Hide vertical header (row numbers)
        table_widget.verticalHeader().setVisible(False)

        # Disable the visible scrollbars but keep scrolling functionality
        table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Allow scrolling with mouse wheel
        table_widget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        table_widget.setShowGrid(True)
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_widget.setFocusPolicy(Qt.NoFocus)

        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        table_widget.setFixedHeight(300)

        # Add table to container
        container_layout.addWidget(table_widget)

        # Add container to main layout
        layout.addWidget(container)

        # Fetch and populate recent reports
        db = Database()
        try:
            print("\n=== Fetching Recent Reports for Home Page ===")
            recent_reports = db.fetch_recent_reports_summary()
            print(f"Received {len(recent_reports)} reports from database")
            
            if len(recent_reports) == 0:
                print("No reports found to display")
                # Add a message to the table
                table_widget.setRowCount(1)
                no_data_item = QTableWidgetItem("No recent reports found")
                no_data_item.setTextAlignment(Qt.AlignCenter)
                table_widget.setSpan(0, 0, 1, 5)  # Merge all columns
                table_widget.setItem(0, 0, no_data_item)
            else:
                # Populate the table
                print("\nPopulating table with data...")
                table_widget.setRowCount(len(recent_reports))
                for row, report in enumerate(recent_reports):
                    try:
                        print(f"\nProcessing row {row}:")
                        print(f"Raw data: {report}")
                        
                        # Format date to dd/MM/yyyy
                        try:
                            date = datetime.strptime(str(report[0]), "%Y-%m-%d").strftime("%d/%m/%Y")
                        except Exception as date_error:
                            print(f"Error formatting date: {date_error}")
                            date = str(report[0])
                        
                        # Get other values, using empty string if None
                        pet_name = str(report[1]) if report[1] is not None else ""
                        client_name = str(report[2]) if report[2] is not None else ""
                        vet_name = str(report[3]) if report[3] is not None else ""
                        report_type = str(report[4]) if report[4] is not None else ""
                        
                        # Add items to table with center alignment
                        for col, value in enumerate([date, report_type, pet_name, client_name, vet_name]):
                            item = QTableWidgetItem(value)
                            item.setTextAlignment(Qt.AlignCenter)
                            
                            # Add background color based on report type
                            if col == 1:  # Type column
                                if value == "Consultation":
                                    item.setBackground(QColor("#E3F2FD"))  # Light Blue
                                elif value == "Vaccination":
                                    item.setBackground(QColor("#E8F5E9"))  # Light Green
                                elif value == "Surgery":
                                    item.setBackground(QColor("#FFEBEE"))  # Light Red
                                elif value == "Grooming":
                                    item.setBackground(QColor("#F3E5F5"))  # Light Purple
                                elif value == "Deworming":
                                    item.setBackground(QColor("#FFF3E0"))  # Light Orange
                                elif value == "Other Treatment":
                                    item.setBackground(QColor("#FAFAFA"))  # Light Gray
                            
                            table_widget.setItem(row, col, item)
                            print(f"Column {col}: {value}")
                            
                    except Exception as row_error:
                        print(f"Error processing row {row}:")
                        print(f"Error type: {type(row_error).__name__}")
                        print(f"Error message: {str(row_error)}")
                        continue
                
                print("\nFinished populating table")
                    
        except Exception as e:
            print(f"\nError fetching recent reports:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            import traceback
            print("Traceback:")
            print(traceback.format_exc())
            
            # Show error message in table
            table_widget.setRowCount(1)
            error_item = QTableWidgetItem("Error loading recent reports")
            error_item.setTextAlignment(Qt.AlignCenter)
            table_widget.setSpan(0, 0, 1, 5)  # Merge all 5 columns
            table_widget.setItem(0, 0, error_item)
        finally:
            db.close_connection()
            print("=== Finished loading recent reports ===\n")
        
        return content

class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PetMedix - Home")
        self.setup_ui()

    def setup_ui(self):
        content = get_home_widget()
        self.setLayout(content)
