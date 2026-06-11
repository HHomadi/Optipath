import sys
import os
import math
import pickle
import random
import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QLineEdit, QLabel,
    QInputDialog, QVBoxLayout, QWidget, QHBoxLayout, QAction, QMessageBox, QMenu, QTableWidget, QTableWidgetItem,
    QTabWidget, QColorDialog, QGraphicsObject, QGridLayout, QGraphicsLineItem,
    QGraphicsPolygonItem, QTextBrowser, QScrollArea,
)
from PyQt5.QtCore import Qt, QUrl, QThread, QTimer, QPointF
from PyQt5.QtGui import QPen, QBrush, QPolygonF, QTransform
from PyQt5.QtWebEngineWidgets import QWebEngineView

from config import IMAGES_DIR, GRAPHS_DIR, FLASK_URL
from database import Database
from algorithms import ALGORITHMS

logfile = open("logfile.txt", "w")
logfile2 = open("logfile2.txt", "w")


def custom_print(*args, **kwargs):
    output = " ".join(map(str, args))
    sys.stdout.write(output + "\n")
    logfile.write(output + "\n")
    logfile.flush()
    logfile2.flush()

built_in_print = print
print = custom_print

class GraphVisualiser(QMainWindow):

    def __init__(self):
        super().__init__()
        self.nodes = {}
        self.edges = []
        self.initUI()
        self.auto_label_mode = False
        self.label_counter = 65  # ASCII value of 'A'
        self.graph_list = []
        self.random_graph_label_counter = 0
        self.max_random_edges = 10
        self.adjacency_matrix = None
        self.node_colour = Qt.blue
        self.label_counter_number = 1

    def get_current_user_id(self):
        if __name__ == "__main__":
            return "defaultUser"
        try:
            db = Database()
            user_id = db.get_logged_in_user_id()
            return user_id
        except Exception:
            return 1

    def initUI(self) -> None:
        self.setWindowTitle("Graph Visualisation")
        self.setGeometry(0, 0, 1920, 1080)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.horizontal_layout = QHBoxLayout()
        self.central_widget.setLayout(self.horizontal_layout)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 960, 880)

        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.horizontal_layout.addWidget(self.view)

        self.tab_widget = QTabWidget()
        self.horizontal_layout.addWidget(self.tab_widget)

        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab2, "Edge Plotter")

        self.tab2_layout = QVBoxLayout()

        self.label_start = QLabel('Start Node:', self.tab2)
        self.label_start.setAlignment(Qt.AlignCenter)
        self.label_start.setStyleSheet('font-weight: bold')

        self.entry_start = QLineEdit(self.tab2)
        self.entry_start.setAlignment(Qt.AlignCenter)

        self.label_end = QLabel('End Node:', self.tab2)
        self.label_end.setAlignment(Qt.AlignCenter)
        self.label_end.setStyleSheet('font-weight: bold')

        self.entry_end = QLineEdit(self.tab2)
        self.entry_end.setAlignment(Qt.AlignCenter)

        self.label_weight = QLabel('Weight:', self.tab2)
        self.label_weight.setAlignment(Qt.AlignCenter)
        self.label_weight.setStyleSheet('font-weight: bold')

        self.entry_weight = QLineEdit(self.tab2)
        self.entry_weight.setAlignment(Qt.AlignCenter)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.label_start, 0, 0)
        grid_layout.addWidget(self.entry_start, 0, 1)
        grid_layout.addWidget(self.label_end, 1, 0)
        grid_layout.addWidget(self.entry_end, 1, 1)
        grid_layout.addWidget(self.label_weight, 2, 0)
        grid_layout.addWidget(self.entry_weight, 2, 1)

        self.tab2_layout.addLayout(grid_layout)

        self.add_edge_button = QPushButton('Add Edge', self.tab2)
        self.add_edge_button.clicked.connect(self.add_edge)
        self.tab2_layout.addWidget(self.add_edge_button)

        self.toggle_label_button = QPushButton('Toggle Auto Label Mode', self.tab2)
        self.toggle_label_button.clicked.connect(self.toggle_auto_label_mode)
        self.tab2_layout.addWidget(self.toggle_label_button)

        self.clear_graph_button = QPushButton('Clear Graph', self.tab2)
        self.clear_graph_button.clicked.connect(self.clear_graph)
        self.tab2_layout.addWidget(self.clear_graph_button)

        self.generate_random_graph_button = QPushButton('Generate Random Graph', self.tab2)
        self.generate_random_graph_button.clicked.connect(self.generate_random_graph_dialog)
        self.tab2_layout.addWidget(self.generate_random_graph_button)

        self.tab2.setLayout(self.tab2_layout)

        # tab 1 visually: Adjacency Matrix (named tab1 in code but rendered third)
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1, "Adjacency Matrix")

        self.adjacency_matrix_table = QTableWidget(self.tab1)
        self.adjacency_matrix_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.tab1_layout = QVBoxLayout()
        self.tab1_layout.addWidget(self.adjacency_matrix_table)
        self.tab1.setLayout(self.tab1_layout)

        self.tab3 = QWidget()
        self.tab_widget.addTab(self.tab3, "Save/Load")

        self.tab3_layout = QVBoxLayout()

        self.save_button = QPushButton('Save Graph', self.tab3)
        self.save_button.clicked.connect(self.save_graph)

        self.load_button = QPushButton('Load Graph', self.tab3)
        self.load_button.clicked.connect(self.load_graph)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)

        self.tab3_layout.addLayout(button_layout)

        self.tab3.setLayout(self.tab3_layout)

        self.tab4 = QWidget()
        self.tab_widget.addTab(self.tab4, "Graph Visualiser")
        self.tab4_layout = QVBoxLayout()

        self.change_background_button = QPushButton('Change Background', self.tab2)
        self.change_background_button.clicked.connect(self.change_background)
        self.tab4_layout.addWidget(self.change_background_button)

        self.change_node_colour_button = QPushButton('Change Node Color', self.tab4)
        self.change_node_colour_button.clicked.connect(self.change_node_colour)
        self.tab4_layout.addWidget(self.change_node_colour_button)

        self.tab4.setLayout(self.tab4_layout)

        self.tab5 = QWidget()
        self.tab_widget.addTab(self.tab5, "Algorithms")
        self.tab5_layout = QVBoxLayout()

        for display_name, solver_class in ALGORITHMS:
            btn = QPushButton(display_name, self.tab5)
            if display_name == "Brute Force":
                btn.clicked.connect(self.run_brute_force)
            else:
                btn.clicked.connect(lambda checked, c=solver_class, n=display_name: self.run_algorithm(n, c))  # c= and n= capture current loop values, without this all buttons use the last iteration's values
            self.tab5_layout.addWidget(btn)

        self.tab5.setLayout(self.tab5_layout)

        self.tab6 = QWidget()
        self.tab_widget.addTab(self.tab6, "Embedded Website")

        tab6_layout = QVBoxLayout(self.tab6)
        webview = QWebEngineView()

        try:
            webview.setUrl(QUrl(FLASK_URL))
        except Exception as e:
            raise RuntimeError("Error loading URL: {}".format(e))

        tab6_layout.addWidget(webview)
        self.tab6.setLayout(tab6_layout)

        logTab1 = FileViewer('logfile.txt')
        logTab2 = FileViewer('logfile2.txt')

        clear_button1 = QPushButton('Clear logfile.txt')
        clear_button2 = QPushButton('Clear logfile2.txt')

        clear_button1.clicked.connect(lambda: self.clear_log_file(0))
        clear_button2.clicked.connect(lambda: self.clear_log_file(1))

        tab7_layout = QWidget()
        tab7 = QGridLayout()
        tab7.addWidget(clear_button1, 0, 0)
        tab7.addWidget(clear_button2, 0, 1)
        tab7.addWidget(logTab1, 1, 0)
        tab7.addWidget(logTab2, 1, 1)

        tab7_layout.setLayout(tab7)
        self.tab_widget.addTab(tab7_layout, 'Log ')

        self.view.mousePressEvent = self.add_node

    def clear_log_file(self, tab: int) -> None:
        file_path = "logfile.txt" if tab == 0 else "logfile2.txt"
        with open(file_path, 'w'):
            pass

    def convert_list(self, tour: list) -> list:
        sorted_names = sorted(self.nodes.keys())
        return [sorted_names[i] for i in tour]

    def get_start_node(self) -> list:
        start_node, ok = QInputDialog.getText(self, 'Start Node', 'Enter the start node')

        if not ok:
            return -1

        if start_node.upper() not in list(self.nodes):
            QMessageBox.warning(self,"Error!","Start node does not exist")
            return -1
        elif ok:
            return list(self.nodes.keys()).index(start_node.upper())

    def full_graph(self, adjacency_matrix) -> bool:
        num_nodes = len(adjacency_matrix)

        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j and adjacency_matrix[i, j] == 0:
                    QMessageBox.warning(self, "Error!", "Every pair of nodes needs an edge")
                    return False

        return True

    def run_algorithm(self, display_name: str, solver_class, **solver_kwargs) -> None:
        start_node = self.get_start_node()
        if start_node == -1:
            return
        self.update_scene()
        if not self.full_graph(self.adjacency_matrix):
            return
        solver = solver_class(self.adjacency_matrix, **solver_kwargs)
        tour, length, elapsed = solver.solve(start_node)
        self.highlight_tour_edges(tour)
        print("{}:".format(display_name))
        print("Best Tour:", self.convert_list(tour))
        print("Tour Length:", length)
        print("Time Taken:", elapsed, "seconds")
        print("")

    def run_brute_force(self) -> None:
        if len(self.nodes) > 10:
            if QMessageBox.warning(
                self, "Warning",
                "Running Brute Force may take a while. Are you sure you want to continue?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            ) != QMessageBox.Yes:
                return
        print_iterations = (
            QMessageBox.question(
                self, "Print Iterations",
                "Do you want to print the iterations? (Will take longer)",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            ) == QMessageBox.Yes
        )
        from algorithms import BruteForce
        self.run_algorithm("Brute Force", BruteForce, print_iterations=print_iterations)

    def highlight_tour_edges(self, tour: list) -> None:
        nodeList = list(self.nodes.values())

        for i in range(len(tour) - 1):
            start_node_index = tour[i]
            end_node_index = tour[i + 1]
            start_x, start_y = nodeList[start_node_index]
            end_x, end_y = nodeList[end_node_index]

            # draw the red line for this edge of the tour
            line_item = QGraphicsLineItem(start_x, start_y, end_x, end_y)
            line_item.setPen(QPen(Qt.red, 2))
            self.scene.addItem(line_item)

            # work out the angle of the line so the arrowhead points the right way
            angle = math.atan2(end_y - start_y, end_x - start_x)
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            arrow_length = 10

            # arrowhead is a triangle pointing to the right, then we rotate it to match the line
            arrowhead = QPolygonF([
                QPointF(0, 0),
                QPointF(-arrow_length, -arrow_length / 2),
                QPointF(-arrow_length, arrow_length / 2),
            ])

            rotation = QTransform()
            rotation.rotate(math.degrees(angle))
            arrowhead = rotation.map(arrowhead)

            # move the arrowhead to sit at the midpoint of the line
            translation = QTransform()
            translation.translate(mid_x, mid_y)
            arrowhead = translation.map(arrowhead)

            arrowhead_item = QGraphicsPolygonItem(arrowhead)
            arrowhead_item.setBrush(Qt.black)
            self.scene.addItem(arrowhead_item)

            QApplication.processEvents()
            QThread.msleep(100)  # 100ms per edge so you can watch the tour draw

    def change_background(self):
        colour_dialog = QColorDialog(self)
        colour = colour_dialog.getColor()
        if colour.isValid():
            self.view.setBackgroundBrush(QBrush(colour))

    def change_node_colour(self):
        colour_dialog = QColorDialog(self)
        colour = colour_dialog.getColor()
        self.node_colour = colour
        if len(self.nodes) != 0:
            self.update_scene()

    def generate_random_graph(self, n: int) -> list:
        nodes = [chr(ord('A') + i) for i in range(n)]
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                weight = random.randint(1, 10)
                edges.append((nodes[i], nodes[j], weight))
        return edges

    def generate_random_graph_dialog(self) -> None:
        n, ok = QInputDialog.getInt(self, 'Random Graph Size', 'Enter the size of the random graph:')
        if ok:
            random_graph = self.generate_random_graph(n)
            self.clear_graph()
            self.update_scene_with_random_graph(random_graph)
    def update_adjacency_matrix_random(self, random_graph: list) -> None:
        self.edges = random_graph
        sorted_node_names = sorted(self.nodes.keys())
        num_nodes = len(sorted_node_names)

        adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        self.adjacency_matrix = adjacency_matrix

        node_to_index = {node: i for i, node in enumerate(sorted_node_names)}

        for start_node, end_node, weight in random_graph:
            i, j = node_to_index[start_node], node_to_index[end_node]
            weight = int(weight)
            adjacency_matrix[i][j] = weight
            adjacency_matrix[j][i] = weight

        self.adjacency_matrix_table.setRowCount(num_nodes)
        self.adjacency_matrix_table.setColumnCount(num_nodes)

        for i, node in enumerate(sorted_node_names):
            self.adjacency_matrix_table.setHorizontalHeaderItem(i, QTableWidgetItem(node))
            self.adjacency_matrix_table.setVerticalHeaderItem(i, QTableWidgetItem(node))

        for i in range(num_nodes):
            for j in range(num_nodes):
                self.adjacency_matrix_table.setItem(i, j, QTableWidgetItem(str(adjacency_matrix[i][j])))

        self.adjacency_matrix_table.resizeColumnsToContents()
        self.adjacency_matrix_table.resizeRowsToContents()

    def update_scene_with_random_graph(self, random_graph: list) -> None:
        self.scene.clear()
        self.edges = random_graph
        self.nodes = {}

        def generate_non_overlapping_coords() -> int:
            # tries up to 10 times to find a spot that isn't too close to existing nodes otherwise just gives up and returns null
            for i in range(1, 10):
                x, y = random.randint(20, 940), random.randint(20, 860)
                if all(
                    ((x - x1) ** 2 + (y - y1) ** 2) >= (min_gap ** 2)
                    and abs(x - x1) >= 5 and abs(y - y1) >= 5
                    for x1, y1 in self.nodes.values()
                ):
                    return x, y
            return -1, -1

        for start_node, end_node, weight in random_graph:
            # scale gap down as more nodes are placed so they still fit
            min_gap = 800 / max(1, len(self.nodes))  # max(1, ...) avoids div by zero on first node

            if start_node not in self.nodes:
                x, y = generate_non_overlapping_coords()
                if x == -1:
                    return self.update_scene_with_random_graph(self.edges)
                self.nodes[start_node] = (x, y)
                node_item = self.scene.addEllipse(x - 10, y - 10, 20, 20, QPen(), Qt.blue)
                node_item.setFlag(QGraphicsObject.ItemIsMovable)
                node_item.setFlag(QGraphicsObject.ItemSendsGeometryChanges)
                text_item = self.scene.addText(start_node)
                text_item.setPos(x - 10, y - 30)

            if end_node not in self.nodes:
                x, y = generate_non_overlapping_coords()
                if x == -1:
                    return self.update_scene_with_random_graph(self.edges)
                self.nodes[end_node] = (x, y)
                node_item = self.scene.addEllipse(x - 10, y - 10, 20, 20, QPen(), Qt.blue)
                node_item.setFlag(QGraphicsObject.ItemIsMovable)
                node_item.setFlag(QGraphicsObject.ItemSendsGeometryChanges)
                text_item = self.scene.addText(end_node)
                text_item.setPos(x - 10, y - 30)

            start_x, start_y = self.nodes[start_node]
            end_x, end_y = self.nodes[end_node]

            self.scene.addLine(start_x, start_y, end_x, end_y, QPen(Qt.black))
            text_item = self.scene.addText(str(weight))
            text_item.setPos((start_x + end_x) / 2, (start_y + end_y) / 2)

        self.update_adjacency_matrix_random(random_graph)

    def toggle_auto_label_mode(self) -> None:
        self.auto_label_mode = not self.auto_label_mode
        if self.auto_label_mode:
            QMessageBox.information(self, "Auto Label Mode", "Auto label mode is enabled. Nodes will be labeled A-Z then numerical values.")
        else:
            QMessageBox.information(self, "Auto Label Mode", "Auto label mode is abled. You can manually enter labels.")

    def add_node(self, event) -> None:
        node_label = ""

        if self.auto_label_mode:
            # 65 = 'A', 90 = 'Z', so label A-Z then switch to numbers after Z
            if self.label_counter <= 90:
                node_label = chr(self.label_counter)
                self.label_counter += 1
            else:
                node_label = str(self.label_counter_number)
                self.label_counter_number += 1
        else:
            node_label, ok = QInputDialog.getText(self, 'Node Label', 'Enter node label:')
            node_label = node_label.upper()
            if not ok:
                return

        if node_label in self.nodes:
            QMessageBox.warning(self, "Error", "Node name must be unique.")
            return

        if len(node_label.strip()) == 0:
            QMessageBox.warning(self, "Error", "Node name must not be blank")
            return

        # mapToScene gives position relative to the viewport not the full scene,
        # so add the scroll offset to land the node in the right spot
        h_scroll_value = self.view.horizontalScrollBar().value()

        cursor_pos = event.pos()
        scene_pos = self.view.mapToScene(cursor_pos)

        x = scene_pos.x() + h_scroll_value
        y = scene_pos.y()

        node_item = self.scene.addEllipse(x - 10, y - 10, 20, 20, QPen(), self.node_colour)
        node_item.setFlag(QGraphicsObject.ItemIsMovable)
        node_item.setFlag(QGraphicsObject.ItemSendsGeometryChanges)

        text_item = self.scene.addText(node_label)
        text_item.setPos(x - 10, y - 30)

        self.nodes[node_label] = (x, y)
        self.update_adjacency_matrix()

    def add_edge(self) -> None:
        start_node = self.entry_start.text().upper()
        end_node = self.entry_end.text().upper()
        weight = self.entry_weight.text()

        if start_node == end_node:
            QMessageBox.warning(self, "Error", "Nodes cannot have the same name.")
            return

        if start_node not in self.nodes or end_node not in self.nodes:
            QMessageBox.warning(self, "Error", "Start and end nodes must exist.")
            return

        try:
            weight = int(weight)
        except ValueError:
            QMessageBox.warning(self, "Error", "Edge weight must be a valid integer.")
            return

        for i, (node1, node2, _) in enumerate(self.edges):
            if (start_node == node1 and end_node == node2) or (start_node == node2 and end_node == node1):
                reply = QMessageBox.question(self, "Edge Exists", "An edge between these nodes already exists. Do you want to overwrite it?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.edges[i] = (start_node, end_node, weight)
                    self.update_scene()
                    self.update_adjacency_matrix()
                    self.entry_start.clear()
                    self.entry_end.clear()
                    self.entry_weight.clear()
                return

        start_x, start_y = self.nodes[start_node]
        end_x, end_y = self.nodes[end_node]

        self.scene.addLine(start_x, start_y, end_x, end_y, QPen(Qt.black))
        text_item = self.scene.addText(str(weight))
        text_item.setPos((start_x + end_x) / 2, (start_y + end_y) / 2)

        self.edges.append((start_node, end_node, weight))

        self.entry_start.clear()
        self.entry_end.clear()
        self.entry_weight.clear()

        self.update_adjacency_matrix()

    def update_adjacency_matrix(self) -> None:
        sorted_node_names = sorted(self.nodes.keys())
        num_nodes = len(sorted_node_names)

        adjacency_matrix = np.zeros((num_nodes, num_nodes), dtype=int)
        self.adjacency_matrix = adjacency_matrix

        node_to_index = {node: i for i, node in enumerate(sorted_node_names)}

        for start_node, end_node, weight in self.edges:
            i, j = node_to_index[start_node], node_to_index[end_node]
            weight = int(weight)
            adjacency_matrix[i][j] = weight
            adjacency_matrix[j][i] = weight

        self.adjacency_matrix_table.setRowCount(num_nodes)
        self.adjacency_matrix_table.setColumnCount(num_nodes)

        for i, node in enumerate(sorted_node_names):
            self.adjacency_matrix_table.setHorizontalHeaderItem(i, QTableWidgetItem(node))
            self.adjacency_matrix_table.setVerticalHeaderItem(i, QTableWidgetItem(node))

        for i in range(num_nodes):
            for j in range(num_nodes):
                self.adjacency_matrix_table.setItem(i, j, QTableWidgetItem(str(adjacency_matrix[i][j])))

        self.adjacency_matrix_table.resizeColumnsToContents()
        self.adjacency_matrix_table.resizeRowsToContents()

    def save_graph(self) -> None:
        def isempty(n): return not(bool(n))
        
        graph_name, ok = QInputDialog.getText(self, 'Graph Name', 'Enter a name for the graph:')
        if not ok:
            return

        user_id = self.get_current_user_id()

        if user_id:
            user_folder = os.path.join(str(GRAPHS_DIR), str(user_id))
            os.makedirs(user_folder, exist_ok=True)
            file_name = os.path.join(user_folder, f"{graph_name}.graph")

            graph_data = {
                'nodes': self.nodes,
                'edges': self.edges,
            }

            if isempty(self.nodes):
                QMessageBox.warning(self, "Error", "Graph is empty, cannot be saved.")
                return

            if isempty(self.edges):
                QMessageBox.warning(self, "Error", "No edges between nodes, cannot be saved.")
                return

            elif graph_name == "":
                QMessageBox.warning(self, "Error", "Graph name cannot be empty.")
                return

            for i in os.listdir(os.path.join(str(GRAPHS_DIR), str(user_id))):
                self.graph_list.append(i.split(".")[0])

            if graph_name in self.graph_list:
                reply = QMessageBox.question(self, "Warning", f"Graph name '{graph_name}' already exists. Do you want to overwrite it?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply != QMessageBox.Yes:
                    return

            try:
                with open(file_name, 'wb') as file:
                    pickle.dump(graph_data, file)
                    QMessageBox.information(self, "Success", "Graph saved successfully.")

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error saving graph: {str(e)}")

    def populate_graph_list(self) -> None:
        self.load_graph_dropdown.clear()
        self.load_graph_dropdown.addItem("Select a Graph")

        user_id = self.get_current_user_id()
        if user_id:
            user_folder = os.path.join(str(GRAPHS_DIR), str(user_id))
            if os.path.exists(user_folder):
                graph_files = [file for file in os.listdir(user_folder) if file.endswith(".graph")]
                if graph_files:
                    self.load_graph_dropdown.addItems(graph_files)

    def update_scene(self) -> None:
        self.scene.clear()

        for node_label, (x, y) in self.nodes.items():
            self.scene.addEllipse(x - 10, y - 10, 20, 20, QPen(), self.node_colour)
            text_item = self.scene.addText(node_label)
            text_item.setPos(x - 10, y - 30)

        for start_node, end_node, weight in self.edges:
            start_x, start_y = self.nodes[start_node]
            end_x, end_y = self.nodes[end_node]
            self.scene.addLine(start_x, start_y, end_x, end_y, QPen(Qt.black))
            weight = str(weight)
            text_item = self.scene.addText(weight)
            text_item.setPos((start_x + end_x) / 2, (start_y + end_y) / 2)

        self.update_adjacency_matrix()

    def load_graph(self) -> None:
        load_menu = QMenu(self)

        user_id = self.get_current_user_id()
        if user_id:
            user_folder = os.path.join(str(GRAPHS_DIR), str(user_id))
            if os.path.exists(user_folder):
                graph_files = [file for file in os.listdir(user_folder) if file.endswith(".graph")]
                if graph_files:
                    for graph_file in graph_files:
                        action = QAction(graph_file, self)
                        action.triggered.connect(lambda checked, file=graph_file: self.load_selected_graph(file))
                        load_menu.addAction(action)

        load_menu.exec_(self.load_button.mapToGlobal(self.load_button.rect().bottomLeft()))

    def load_selected_graph(self, selected_graph) -> None:
        try:
            user_id = self.get_current_user_id()
            if user_id:
                user_folder = os.path.join(str(GRAPHS_DIR), str(user_id))
                file_path = os.path.join(user_folder, selected_graph)

                with open(file_path, 'rb') as file:
                    graph_data = pickle.load(file)
                    self.nodes = graph_data['nodes']
                    self.edges = graph_data['edges']
                    self.update_scene()
                    QMessageBox.information(self, "Success", "Graph loaded successfully.")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading graph: {str(e)}")

    def clear_graph(self) -> None:
        self.nodes = {}
        self.edges = []
        self.scene.clear()
        self.adjacency_matrix_table.clearContents()
        self.adjacency_matrix_table.setRowCount(0)
        self.adjacency_matrix_table.setColumnCount(0)
        self.entry_start.clear()
        self.entry_end.clear()
        self.entry_weight.clear()
        self.label_counter = 65  # ASCII value of 'A'
        self.label_counter_number = 1

class FileViewer(QScrollArea):
    """Displays a log file in a scrollable text view, refreshing every second."""

    def __init__(self, file_path, parent=None):
        super(FileViewer, self).__init__(parent)
        self.inner_widget = QTextBrowser(self)
        self.inner_widget.setOpenExternalLinks(True)
        self.setWidgetResizable(True)
        self.setWidget(self.inner_widget)
        self.file_path = file_path
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_contents)
        self.timer.start(1000)
        self.current_scroll_position = 0
        self.update_contents()

    def update_contents(self):
        current_scroll_value = self.inner_widget.verticalScrollBar().value()
        try:
            with open(self.file_path, 'r') as file:
                contents = file.read()
                self.inner_widget.setPlainText(contents)
        except FileNotFoundError:
            self.inner_widget.setPlainText("File not found.")
        self.inner_widget.verticalScrollBar().setValue(current_scroll_value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GraphVisualiser()
    ex.show()
    sys.exit(app.exec_())