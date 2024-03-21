import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow

class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create widgets
        self.label = QLabel("Hello, PyQt!")
        self.button = QPushButton("Click me!")
        
        # Connect button click event to function
        self.button.clicked.connect(self.change_text)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
    
    def change_text(self):
        self.label.setText("Button clicked!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Basic Interface")
        
        # Set central widget
        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 200)  # Set initial window size
    window.show()
    sys.exit(app.exec())

    