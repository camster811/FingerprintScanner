import sys
import scanner
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget, QLabel, QLineEdit
)


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        spectrum = self.palette()
        spectrum.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(spectrum)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fingerprint Scanner")

        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()
        layout.addLayout(button_layout)
        layout.addLayout(self.stacklayout)

        self.label1 = QLabel("Bio-Auto Fingerprint Scanner")
        font_size = self.label1.font()
        font_size.setPointSize(15)
        self.label1.setFont(font_size)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.label1)

        button = QPushButton("Read Finger Print")
        button.pressed.connect(self.pass_or_fail)
        button_layout.addWidget(button)
        self.stacklayout.addWidget(Color("red"))

        button = QPushButton("Delete Finger Print")
        button.pressed.connect(self.delete_print)
        button_layout.addWidget(button)
        self.stacklayout.addWidget(Color("green"))

        button = QPushButton("Add Finger Print")
        button.pressed.connect(self.add_print)
        button_layout.addWidget(button)
        self.stacklayout.addWidget(Color("blue"))
        
        button = QPushButton("List stored IDs")
        button.pressed.connect(self.list_ids)
        button_layout.addWidget(button)
        self.stacklayout.addWidget(Color("blue"))

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.stacklayout.setCurrentIndex(2)

    def pass_or_fail(self):
        if scanner.fingerprint_check():
            print("Detected ID #", scanner.scannerLibrary.finger_id, "with confidence", scanner.scannerLibrary.confidence)
            self.stacklayout.setCurrentIndex(1)
        else:
            print("No fingerprint found")
            self.stacklayout.setCurrentIndex(0)

    def delete_print(self):
        scanner.delete_print()
        self.stacklayout.setCurrentIndex(2)

    def add_print(self):
        scanner.store_fingerprint(scanner.get_storage_ID())
        self.stacklayout.setCurrentIndex(2)
        
    def list_ids(self):
        scanner.list_ids()
        
        


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
