import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QVBoxLayout, QWidget, QPushButton, QToolBar,QLineEdit,QFormLayout, QDialog, QLabel
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor

class DisplayFileItem:
    def __init__(self, name, item_type, coordinates):
        self.name = name
        self.item_type = item_type
        self.coordinates = coordinates

class DisplayFile:
    def __init__(self):
        self.items = []

    def add_item(self, item:DisplayFileItem):
        self.items.append(item)

    def clear_items(self):
        self.items = []

class Viewport(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def draw_items(self, display_file):
        self.scene().clear()
        for item in display_file.items:
            if item.item_type == 'point':
                self.draw_point(item.coordinates)
            elif item.item_type == 'line':
                self.draw_line(item.coordinates)
            elif item.item_type == 'wireframe':
                self.draw_wireframe(item.coordinates)

    def draw_point(self, coordinates):
        x, y = coordinates
        self.scene().addEllipse(x, y, 2, 2, QPen())

    def draw_line(self, coordinates):
        x1, y1, x2, y2 = coordinates
        self.scene().addLine(x1, y1, x2, y2, QPen())

    def draw_wireframe(self, coordinates):
        x1, y1, x2, y2,x3,y3 = coordinates
        self.scene().addLine(x1, y1, x2, y2, QPen())
        self.scene().addLine(x2, y2, x3, y3, QPen())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window")
        self.display_file = DisplayFile()
        self.viewport = Viewport()
        self.setCentralWidget(self.viewport)

        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        pan_button = QPushButton("Pan")
        pan_button.clicked.connect(self.pan)
        toolbar.addWidget(pan_button)

        zoom_in_button = QPushButton("Zoom In")
        zoom_in_button.clicked.connect(self.zoom_in)
        toolbar.addWidget(zoom_in_button)

        zoom_out_button = QPushButton("Zoom Out")
        zoom_out_button.clicked.connect(self.zoom_out)
        toolbar.addWidget(zoom_out_button)

        draw_line_button = QPushButton("Draw Line")
        draw_line_button.clicked.connect(self.draw_line)
        toolbar.addWidget(draw_line_button)

        draw_point_button = QPushButton("Draw point")
        draw_point_button.clicked.connect(self.draw_point)
        toolbar.addWidget(draw_point_button)

        draw_wireframe_button = QPushButton("Draw wireframe")
        draw_wireframe_button.clicked.connect(self.draw_wireframe)
        toolbar.addWidget(draw_wireframe_button)

    def pan(self):
        self.viewport.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.viewport.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def zoom_in(self):
        self.viewport.scale(1.2, 1.2)

    def zoom_out(self):
        self.viewport.scale(0.8, 0.8)

    def draw_point(self):

        form_window = FormWindow()
        form_window.exec()

        listPoints = form_window.readlist()
        ponto = DisplayFileItem("ponto", "point", (int(listPoints[0]),int(listPoints[1])))
        self.display_file.add_item(ponto)
        print(self.display_file.items)
        self.viewport.draw_point(self.display_file)

    def draw_line(self):
        linha = DisplayFileItem("linha1", "line", (10,20,30,40))
        self.display_file.add_item(linha)
        self.viewport.draw_items(self.display_file)

    def draw_wireframe(self):
        wireframe = DisplayFileItem("wireframe1", "wireframe", (70,20,30,40,50,60))
        self.display_file.add_item(wireframe)
        self.viewport.draw_items(self.display_file)


    def on_submit(self):
        text = self.input_box.text()
        self.result_label.setText(f"Input received: {text}")


class FormWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.listReturn = []
        self.setWindowTitle("Form Window")

        layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_form(self):
        name = self.name_input.text()
        email = self.email_input.text()
        self.listReturn.append(name)
        self.listReturn.append(email)

        print(self.listReturn)
        print(f"Name: {name}, Email: {email}")
        self.close()

    def readlist(self):
        return self.listReturn

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    #ponto = DisplayFileItem("ponto", "point", (50,20))
    #window.display_file.add_item(ponto)

    #linha = DisplayFileItem("linha1", "line", (10,20,30,40))
    #window.display_file.add_item(linha)
    
    #window.viewport.draw_items(window.display_file)

    window.setGeometry(100, 100, 800, 600)
    window.show()

    sys.exit(app.exec())