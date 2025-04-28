from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, 
    QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class CorrelationView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор корреляций")
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout1 = QVBoxLayout(self.main_widget)

        self.create_controls()
        self.create_table()
        self.create_plot()

    def create_controls(self):
        '''Панель управления'''
        control_layout = QHBoxLayout()

        self.load_btn = QPushButton("Загрузить CSV")
        self.clear_btn = QPushButton("Очистить")
        self.calc_btn = QPushButton("Рассчитать")

        control_layout.addWidget(self.load_btn)
        control_layout.addWidget(self.clear_btn)
        control_layout.addWidget(self.calc_btn)

        self.layout1.addLayout(control_layout)

    def create_table(self):
        """Таблица данных"""
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["X", "Y"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)

        self.layout1.addWidget(self.table) 

    def create_plot(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.layout1.addWidget(self.canvas)

        self.results_label = QLabel("Результаты:")
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout1.addWidget(self.results_label)

    def update_table(self, x_data, y_data):
        self.table.blockSignals(True)
        self.table.setRowCount(len(x_data))

        for i in range(len(x_data)):
            self.table.setItem(i, 0, QTableWidgetItem(str(x_data[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(y_data[i])))

        self.table.blockSignals(False)

    def update_plot(self, x_data, y_data, correlation_line = None):
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        ax.scatter(x_data, y_data, color='blue', marker='o')

        if correlation_line is not None:
            x_range, y_range = correlation_line
            ax.plot(x_range, y_range, color='red', label="Линия регрессии")

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title('Диаграмма рассеяния X и Y')
        ax.legend()
        ax.grid(True)    

        self.canvas.draw()

    def update_results(self, results):
        """Обновление результатов"""
        text = (
            f"Корреляция Пирсона: {results['pearson'][0]:.4f} (p-value: {results['pearson'][1]:.4f})\n"
            f"Корреляция Спирмена: {results['spearman'][0]:.4f} (p-value: {results['spearman'][1]:.4f})\n"
            f"Корреляция Кендалла: {results['kendall'][0]:.4f} (p-value: {results['kendall'][1]:.4f})"
        )
        self.results_label.setText(text)


    def show_error(self, message):
        """Показ ошибки"""
        self.results_label.setText(f"Ошибка: {message}")    