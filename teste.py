import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QVBoxLayout, QWidget, QPushButton, QToolBar,QLineEdit,QFormLayout, QDialog, QLabel
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor


pen = QPen(QColor(128, 0, 128))  # Black color
pen.setWidth(2)  # Set pen w


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
        self.scene().addEllipse(x, y, 2, 2, pen)

    def draw_line(self, coordinates):
        x1, y1, x2, y2 = coordinates
        self.scene().addLine(x1, y1, x2, y2, pen)

    def draw_wireframe(self, coordinates):
        if len(coordinates) < 6:  # Precisa de pelo menos 3 pontos (6 coordenadas) para formar um wireframe
            return
        # Desenha linhas entre pontos sequenciais
        for i in range(0, len(coordinates) - 2, 2):
            self.scene().addLine(coordinates[i], coordinates[i+1], coordinates[i+2], coordinates[i+3], pen)
        # Fecha o polígono conectando o último ponto ao primeiro
        self.scene().addLine(coordinates[-2], coordinates[-1], coordinates[0], coordinates[1], pen)


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
        form_window = FormWindow("point")
        form_window.exec()

        listPoints = form_window.readlist()
        if listPoints and isinstance(listPoints[0], tuple) and len(listPoints[0]) == 2:
            # Garante que o ponto seja desenhado corretamente.
            ponto = DisplayFileItem("ponto", "point", listPoints[0])
            self.display_file.add_item(ponto)
            self.viewport.draw_items(self.display_file)
        else:
            print("Input is not a valid point.")

    def draw_line(self):
        form_window = FormWindow("line")
        form_window.exec()

        listPoints = form_window.readlist()
        print(listPoints)

        # if len(listPoints) >= 4:  # Verifica se tem coordenadas suficientes para uma linha
        linha = DisplayFileItem("linha", "line", listPoints[0])  # Pega as primeiras 4 coordenadas
        self.display_file.add_item(linha)
        self.viewport.draw_items(self.display_file)
        # else:
        #     print("Not enough arguments")

    def draw_wireframe(self):
        form_window = FormWindow("wireframe")
        form_window.exec()

        listPoints = form_window.readlist()
        if len(listPoints) >= 6:  # Verifica se tem coordenadas suficientes para um wireframe
            wireframe = DisplayFileItem("wireframe", "wireframe", tuple(listPoints))
            self.display_file.add_item(wireframe)
            self.viewport.draw_items(self.display_file)



    def on_submit(self):
        text = self.input_box.text()
        self.result_label.setText(f"Input received: {text}")


class FormWindow(QDialog):
    def __init__(self, item_type):
        super().__init__()
        self.item_type = item_type
        self.setWindowTitle("Enter Coordinates")
        layout = QVBoxLayout()

        self.coords_label = QLabel("Coordinates:")
        self.coords_input = QLineEdit()
        layout.addWidget(self.coords_label)
        layout.addWidget(self.coords_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_form(self):
        coords_str = self.coords_input.text()
        try:
            # Tenta interpretar a entrada como uma lista de tuplas
            # Por exemplo: "(10, 20)"
            points = eval(coords_str)
            if isinstance(points, tuple):
                self.listReturn = [points]  # Coloca o ponto em uma lista
            else:
                self.listReturn = []
                print("Entered coordinates do not match the format for a point.")
        except:
            self.listReturn = []
            print("Error parsing coordinates")
        self.close()

    def readlist(self):  # Corrigido a indentação aqui
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