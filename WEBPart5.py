import sys
import os
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QInputDialog

from PyQt5.QtWidgets import QApplication, QWidget


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.spn_levels = [0.005, 0.01, 0.015, 0.025, 0.045, 0.06]
        self.spni = 0
        self.spn = self.spn_levels[self.spni]
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Карта')
        self.map_type = "map"
        self.ll = [37.530887, 55.703118]
        # self.draw_map()
        self.initUI()
        self.draw_map()

    def change_type(self):
        if self.map_type == "map":
            self.map_type = "sat"
        elif self.map_type == "sat":
            self.map_type = "sat,skl"
        elif self.map_type == "sat,skl":
            self.map_type = "map"

    def draw_map(self, request=None):
        if not request:
            l1 = self.ll[0]
            l2 = self.ll[1]
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={l1},{l2}&spn={str(self.spn)},{str(self.spn)}&l={self.map_type}"
            response = requests.get(map_request)
        else:
            map_request = f"http://static-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={request}&spn={str(self.spn)},{str(self.spn)}&l={self.map_type}"
            response = requests.get(map_request)
            print(response.url)
            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]
            self.ll = ''.split(toponym["Point"]["pos"])

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

    def input_request(self):
        name, ok_pressed = QInputDialog.getText(self, "Введите запрос",
                                                "Город, улица, ваше любимое кафе или станция метро."
                                                " Постараемся найти!")
        if ok_pressed:
            self.draw_map(name)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_C:
            self.change_type()
            self.draw_map()
        elif event.key() == Qt.Key_D:
            self.draw_map()
        elif event.key() == Qt.Key_R:
            self.input_request()
        elif event.key() == Qt.Key_PageUp:
            if self.spni < 4:
                self.spni = self.spni + 1
            self.spn = self.spn_levels[self.spni]
            self.draw_map()
        elif event.key() == Qt.Key_PageDown:
            if self.spni > 0:
                self.spni = self.spni - 1
            self.spn = self.spn_levels[self.spni]
            self.draw_map()
        elif event.key() == Qt.Key_Up:
            if self.ll[1] + self.spn < 90:
                self.ll[1] = self.ll[1] + self.spn
            self.draw_map()
        elif event.key() == Qt.Key_Down:
            if self.ll[1] - self.spn > -90:
                self.ll[1] = self.ll[1] - self.spn
            self.draw_map()
        elif event.key() == Qt.Key_Left:
            if self.ll[0] - self.spn > -180:
                self.ll[0] = self.ll[0] - self.spn
            self.draw_map()
        elif event.key() == Qt.Key_Right:
            if self.ll[0] + self.spn < 180:
                self.ll[0] = self.ll[0] + self.spn
            self.draw_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
