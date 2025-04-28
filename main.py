import sys
from PyQt5.QtWidgets import QApplication
from model import CorrelationModel
from view import CorrelationView
from controller import Controller


def main():
    app = QApplication(sys.argv)

    # Инициализация MVC
    model = CorrelationModel()
    view = CorrelationView()
    controller = Controller(model, view)

    # Запуск
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()