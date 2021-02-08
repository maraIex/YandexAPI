import sys
import os
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton

from PyQt5.QtWidgets import QApplication, QWidget


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Карта')
        self.map_type = "map"
        # self.draw_map()
        self.initUI()

    def change_type(self):
        if self.map_type == "map":
            self.map_type = "sat"
        elif self.map_type == "sat":
            self.map_type = "sat,skl"
        elif self.map_type == "sat,skl":
            self.map_type = "map"

    def draw_map(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l={self.map_type}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        if self.map_type == 'map':
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
            self.pixmap = QPixmap('map.png')
            # Отображаем содержимое QPixmap в объекте QLabel
            self.image.setPixmap(self.pixmap)
            os.remove("map.png")
        else:
            map_file = "map.jpeg"
            with open(map_file, "wb") as file:
                file.write(response.content)
            self.pixmap = QPixmap('map.jpeg')
            # Отображаем содержимое QPixmap в объекте QLabel
            self.image.setPixmap(self.pixmap)
            os.remove("map.jpeg")

    def initUI(self):
        self.image = QLabel(self)
        self.image.resize(300, 300)
        self.draw_btn = QPushButton('Нарисовать \n карту', self)
        self.draw_btn.resize(70, 50)
        self.draw_btn.move(5, 55)
        self.draw_btn.clicked.connect(self.draw_map)
        self.btn = QPushButton('Сменить \n вид', self)
        self.btn.resize(70, 50)
        self.btn.move(5, 5)
        self.btn.clicked.connect(self.change_type)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())