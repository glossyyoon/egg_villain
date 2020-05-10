import sys
import os
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from PIL import Image


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        #self.setStyleSheet("background-color: black;")
        self.initUI()

    def read_info(self):
        user_info = []  # 0 = 성별, 1 = 스타일, 2 = 계절
        file = open('user_info.txt', 'r')

        all = file.read()
        file.close()
        user_info = all.split('\n')

        return user_info

    def mens_top(self):
        dir = 'C:/Users/현정/Desktop/semi_final/' # 데이터셋 경로 밑에도 다 고쳐^^

        user_info = self.read_info()
        top_path = dir + "top/" + user_info[1] + "/" + user_info[2]
        filename = random.choice(os.listdir(top_path))
        path = top_path + "/" + filename

        return path

    def womens_dress(self):
        dir = 'C:/Users/현정/Desktop/semi_final/'

        user_info = self.read_info()
        dress_path = dir + "dress/" + user_info[1] + "/" + user_info[2]
        filename = random.choice(os.listdir(dress_path))
        path = dress_path + "/" + filename

        return path

    def mens_pants(self):
        user_info = self.read_info()
        dir = 'C:/Users/현정/Desktop/semi_final/'

        pants_path = dir + "pants/" + user_info[1] + "/" + user_info[2]
        filename = random.choice(os.listdir(pants_path))
        path = pants_path + "/" + filename

        return path

    def womens_skirt(self):
        dir = 'C:/Users/현정/Desktop/semi_final/'

        user_info = self.read_info()
        skirt_path = dir + "skirt/" + user_info[1] + "/" + user_info[2]
        filename = random.choice(os.listdir(skirt_path))
        path = skirt_path + "/" + filename

        return path

    def convert_img(self, path, clothes):
        result = Image.open(path)
        if(clothes == "dress"): result = result.resize((300, 600))
        else: result = result.resize((300, 300))
        filename = clothes + ".png"
        result.save(filename)

    def mens_replay(self):
        top1_path = self.mens_top()
        self.convert_img(top1_path, "top1")
        pixmap = QPixmap("top1.png")
        self.top1.setPixmap(QPixmap(pixmap))

        top2_path = self.mens_top()
        self.convert_img(top2_path, "top2")
        pixmap = QPixmap("top2.png")
        self.top2.setPixmap(QPixmap(pixmap))

        pants1_path = self.mens_pants()
        self.convert_img(pants1_path, "pants1")
        pixmap = QPixmap("pants1.png")
        self.pants1.setPixmap(QPixmap(pixmap))

        pants2_path = self.mens_pants()
        self.convert_img(pants2_path, "pants2")
        pixmap = QPixmap("pants2.png")
        self.pants2.setPixmap(QPixmap(pixmap))

    def womens_replay(self):
        dress_path = self.womens_dress()
        self.convert_img(dress_path, "dress")
        pixmap = QPixmap("dress.png")
        self.dress.setPixmap(QPixmap(pixmap))

        top2_path = self.mens_top()
        self.convert_img(top2_path, "top2")
        pixmap = QPixmap("top2.png")
        self.top2.setPixmap(QPixmap(pixmap))

        skirt_path = self.womens_skirt()
        self.convert_img(skirt_path, "skirt")
        pixmap = QPixmap("skirt.png")
        self.skirt.setPixmap(QPixmap(pixmap))


    def initUI(self):
        user_info = self.read_info()
        if(user_info[0] == "female"): gender = "female"
        else: gender = "male"

        face1 = QLabel(self)
        face1.resize(300, 300)
        pixmap = QPixmap("0.png")
        face1.setPixmap(QPixmap(pixmap))

        face2 = QLabel(self)
        face2.resize(300, 300)
        pixmap = QPixmap("0.png")
        face2.setPixmap(QPixmap(pixmap))

        #상의==================================================
        if(gender == "female"):
            self.dress = QLabel(self)
            self.dress.resize(300, 600)
            dress_path = self.womens_dress()
            self.convert_img(dress_path, "dress")
            pixmap = QPixmap("dress.png")
            self.dress.setPixmap(QPixmap(pixmap))

        else:
            self.top1 = QLabel(self)
            self.top1.resize(300, 300)
            top1_path = self.mens_top()
            self.convert_img(top1_path, "top1")
            pixmap = QPixmap("top1.png")
            self.top1.setPixmap(pixmap)

        self.top2 = QLabel(self)
        self.top2.resize(300, 300)
        top2_path = self.mens_top()
        self.convert_img(top2_path, "top2")
        pixmap = QPixmap("top2.png")
        self.top2.setPixmap(QPixmap(pixmap))

        # 하의==================================================
        if(gender == "female"):
            self.skirt = QLabel(self)
            self.skirt.resize(300, 300)
            skirt_path = self.womens_skirt()
            self.convert_img(skirt_path, "skirt")
            pixmap = QPixmap("skirt.png")
            self.skirt.setPixmap(QPixmap(pixmap))

        else:
            self.pants1 = QLabel(self)
            self.pants1.resize(300, 300)
            pants1_path = self.mens_pants()
            self.convert_img(pants1_path, "pants1")
            pixmap = QPixmap("pants1.png")
            self.pants1.setPixmap(pixmap)

            self.pants2 = QLabel(self)
            self.pants2.resize(300, 300)
            pants2_path = self.mens_pants()
            self.convert_img(pants2_path, "pants2")
            pixmap = QPixmap("pants2.png")
            self.pants2.setPixmap(QPixmap(pixmap))


        # 버튼==================================================
        exit_btn = QPushButton("종료", self)
        exit_btn.clicked.connect(QCoreApplication.instance().quit)

        re_btn = QPushButton("다시", self)
        if(gender == "female"):
            re_btn.clicked.connect(self.womens_replay)
        else:
            re_btn.clicked.connect(self.mens_replay)

        # 레이아웃===============================================
        if(gender == "female"):
            vbox1 = QVBoxLayout()
            vbox1.addWidget(face1)
            vbox1.addWidget(self.dress)

        else:
            vbox1 = QVBoxLayout()
            vbox1.addWidget(face1)
            vbox1.addWidget(self.top1)
            vbox1.addWidget(self.pants1)


        if(gender == "female"):
            vbox2 = QVBoxLayout()
            vbox2.addWidget(face2)
            vbox2.addWidget(self.top2)
            vbox2.addWidget(self.skirt)

        else:
            vbox2 = QVBoxLayout()
            vbox2.addWidget(face2)
            vbox2.addWidget(self.top2)
            vbox2.addWidget(self.pants2)


        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addLayout(vbox1)
        hbox1.addStretch(1)
        hbox1.addLayout(vbox2)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(3)
        hbox2.addWidget(re_btn)
        hbox2.addWidget(exit_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        self.setWindowTitle('오늘의 옷 추천')
        self.setGeometry(400, 100, 800, 800)
        self.show()

        print(gender, "success")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
