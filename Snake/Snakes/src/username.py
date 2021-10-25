import winsound
import game

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QWidget, QMessageBox, QLabel, QDesktopWidget, QLineEdit, QPushButton, QCheckBox, QSlider

from helpers import load_res


class Username2Window(QWidget):

    def __init__(self, speed: int):
        super(Username2Window, self).__init__()
        self.usernames = []
        self.game_speed = speed
        self.num_of_food = 2
        self.multiple_snakes = True
        self.game_window = None

        self.setGeometry(100, 100, 960, 720)
        self.setWindowTitle('2Players')
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon(load_res('icon.png')))

        image = QImage(load_res('wp2409705.jpg'))
        scale_image = image.scaled(QSize(960, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scale_image))
        self.setFixedSize(self.size())

        font = "Spongeboy Me Bob"

        self.usernameLabel1 = QLabel('PLAYER 1: ', self)
        font_label = self.usernameLabel1.font()
        font_label.setPointSize(20)
        font_label.setFamily(font)
        self.usernameLabel1.setFont(font_label)
        self.usernameLabel1.setFixedSize(250, 150)
        self.usernameLabel1.move(80, 100)

        self.usernameEdit1 = QLineEdit(self, )
        font_edit = self.usernameEdit1.font()
        font_edit.setPointSize(22)
        font_edit.setFamily(font)
        self.usernameEdit1.setFont(font_edit)
        self.usernameEdit1.setFixedSize(400, 70)
        self.usernameEdit1.move(80, 200)

        self.usernameLabel2 = QLabel('PLAYER 2: ', self)
        font_label = self.usernameLabel2.font()
        font_label.setPointSize(20)
        font_label.setFamily(font)
        self.usernameLabel2.setFont(font_label)
        self.usernameLabel2.setFixedSize(250, 150)
        self.usernameLabel2.move(80, 300)

        self.usernameEdit2 = QLineEdit(self, )
        font_edit = self.usernameEdit2.font()
        font_edit.setPointSize(22)
        font_edit.setFamily(font)
        self.usernameEdit2.setFont(font_edit)
        self.usernameEdit2.setFixedSize(400, 70)
        self.usernameEdit2.move(80, 400)

        self.cb = QCheckBox('Multiple snakes', self)
        self.cb.setFont(QFont(font))
        self.cb.setStyleSheet("color: black; font-size:30px")
        self.cb.setMinimumSize(150, 70)
        self.cb.move(350, 620)
        self.cb.toggle()
        self.cb.stateChanged.connect(self.change_checkbox)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimumSize(300, 40)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setRange(2, 20)
        self.slider.setSingleStep(1)
        self.slider.move(150, 530)
        self.slider.valueChanged[int].connect(self.changeValue)

        self.apple_box = QLineEdit(self, )
        font_edit = self.apple_box.font()
        font_edit.setPointSize(14)
        font_edit.setFamily(font)
        self.apple_box.setFont(font_edit)
        self.apple_box.setReadOnly(True)
        self.apple_box.setText("2")
        self.apple_box.setFixedSize(70, 60)
        self.apple_box.move(470, 520)

        self.apple_label = QLabel(self, )
        font_edit = self.apple_label.font()
        font_edit.setPointSize(15)
        font_edit.setFamily(font)
        self.apple_label.setFont(font_edit)
        self.apple_label.setText("Food Count")
        self.apple_label.setFixedSize(150, 60)
        self.apple_label.move(550, 520)

        self.start_button = QPushButton(self)
        self.start_button.setText("Start")
        self.start_button.setFont(QFont(font))
        self.start_button.setStyleSheet("color: black; font-size:46px; background-color: green")
        self.start_button.setToolTip("Start the game")
        self.start_button.clicked.connect(self.start_button_pressed)
        self.start_button.resize(self.start_button.sizeHint())
        self.start_button.setMinimumSize(150, 100)
        self.start_button.move(150, 600)

        self.setPalette(palette)

    def changeValue(self, value):
        self.num_of_food = value
        if self.num_of_food < 2:
            self.num_of_food = 2
        self.apple_box.setText(str(self.num_of_food))

    def change_checkbox(self, state):
        if state == Qt.Checked:
            self.multiple_snakes = True
        else:
            self.multiple_snakes = False

    def validate(self, usernameEdit1=None, usernameEdit2=None):
        if (usernameEdit1 != "") & (usernameEdit2 != ""):
            return True
        else:
            return False

    def start_button_pressed(self):
        if self.validate(self.usernameEdit1.text(), self.usernameEdit2.text()):
            self.hide()
            self.usernames.append(self.usernameEdit1.text())
            self.usernames.append(self.usernameEdit2.text())

            winsound.PlaySound(load_res('kaerMorhen.wav'), winsound.SND_ASYNC + winsound.SND_LOOP)

            self.game_window = game.SnakeGame(self.usernames, self.game_speed, self.multiple_snakes, self.num_of_food)
            self.game_window.show()
        else:
            QMessageBox.warning(self, 'Warning', "Validation fault. Username required.", QMessageBox.Ok)
            pass


class Username3Window(QWidget):
    def __init__(self, speed: int):
        super(Username3Window, self).__init__()
        self.game_window = None
        self.usernames = []
        self.num_of_food = 2
        self.multiple_snakes = True
        self.game_speed = speed

        self.setGeometry(100, 100, 960, 720)
        self.setWindowTitle('3Players')
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon(load_res('icon.png')))

        image = QImage(load_res('wp2409705.jpg'))
        scale_image = image.scaled(QSize(960, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scale_image))
        self.setFixedSize(self.size())

        font = "Spongeboy Me Bob"

        self.usernameLabel1 = QLabel('PLAYER 1: ', self)
        font_label = self.usernameLabel1.font()
        font_label.setPointSize(20)
        font_label.setFamily(font)
        self.usernameLabel1.setFont(font_label)
        self.usernameLabel1.setFixedSize(250, 150)
        self.usernameLabel1.move(50, 100)

        self.usernameEdit1 = QLineEdit(self, )
        font_edit = self.usernameEdit1.font()
        font_edit.setPointSize(22)
        font_edit.setFamily(font)
        self.usernameEdit1.setFont(font_edit)
        self.usernameEdit1.setFixedSize(400, 70)
        self.usernameEdit1.move(50, 200)

        self.usernameLabel2 = QLabel('PLAYER 2: ', self)
        font_label = self.usernameLabel2.font()
        font_label.setPointSize(20)
        font_label.setFamily(font)
        self.usernameLabel2.setFont(font_label)
        self.usernameLabel2.setFixedSize(250, 150)
        self.usernameLabel2.move(50, 300)

        self.usernameEdit2 = QLineEdit(self, )
        font_edit = self.usernameEdit2.font()
        font_edit.setPointSize(22)
        font_edit.setFamily(font)
        self.usernameEdit2.setFont(font_edit)
        self.usernameEdit2.setFixedSize(400, 70)
        self.usernameEdit2.move(50, 400)

        self.usernameLabel3 = QLabel('PLAYER 3: ', self)
        font_label = self.usernameLabel3.font()
        font_label.setPointSize(20)
        font_label.setFamily(font)
        self.usernameLabel3.setFont(font_label)
        self.usernameLabel3.setFixedSize(250, 150)
        self.usernameLabel3.move(500, 100)

        self.usernameEdit3 = QLineEdit(self, )
        font_edit = self.usernameEdit3.font()
        font_edit.setPointSize(22)
        font_edit.setFamily(font)
        self.usernameEdit3.setFont(font_edit)
        self.usernameEdit3.setFixedSize(400, 70)
        self.usernameEdit3.move(500, 200)

        self.cb = QCheckBox('Multiple snakes', self)
        self.cb.setFont(QFont(font))
        self.cb.setStyleSheet("color: black; font-size:30px")
        self.cb.setMinimumSize(150, 70)
        self.cb.move(350, 620)
        self.cb.toggle()
        self.cb.stateChanged.connect(self.change_checkbox)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimumSize(300, 40)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setRange(2, 20)
        self.slider.setSingleStep(1)
        self.slider.move(150, 530)
        self.slider.valueChanged[int].connect(self.changeValue)

        self.apple_box = QLineEdit(self, )
        font_edit = self.apple_box.font()
        font_edit.setPointSize(14)
        font_edit.setFamily(font)
        self.apple_box.setFont(font_edit)
        self.apple_box.setReadOnly(True)
        self.apple_box.setText("2")
        self.apple_box.setFixedSize(70, 60)
        self.apple_box.move(470, 520)

        self.apple_label = QLabel(self, )
        font_edit = self.apple_label.font()
        font_edit.setPointSize(15)
        font_edit.setFamily(font)
        self.apple_label.setFont(font_edit)
        self.apple_label.setText("Food Count")
        self.apple_label.setFixedSize(150, 60)
        self.apple_label.move(550, 520)

        self.start_button = QPushButton(self)
        self.start_button.setText("Start")
        self.start_button.setFont(QFont(font))
        self.start_button.setStyleSheet("color: black; font-size:46px; background-color: green")
        self.start_button.setToolTip("Start the game")
        self.start_button.clicked.connect(self.start_button_pressed)
        self.start_button.resize(self.start_button.sizeHint())
        self.start_button.setMinimumSize(150, 100)
        self.start_button.move(150, 600)

        self.setPalette(palette)

    def changeValue(self, value):
        self.num_of_food = value
        if self.num_of_food < 2:
            self.num_of_food = 2
        self.apple_box.setText(str(self.num_of_food))

    def change_checkbox(self, state):
        if state == Qt.Checked:
            self.multiple_snakes = True
        else:
            self.multiple_snakes = False

    def validate(self, usernameEdit1=None, usernameEdit2=None, usernameEdit3=None):
        if (usernameEdit1 != "") & (usernameEdit2 != "") & (usernameEdit3 != ""):
            return True
        else:
            return False

    def start_button_pressed(self):
        if self.validate(self.usernameEdit1.text(), self.usernameEdit2.text(), self.usernameEdit3.text()):
            self.hide()

            self.usernames.append(self.usernameEdit1.text())
            self.usernames.append(self.usernameEdit2.text())
            self.usernames.append(self.usernameEdit3.text())
            winsound.PlaySound(load_res('kaerMorhen.wav'), winsound.SND_ASYNC + winsound.SND_LOOP)
            self.game_window = game.SnakeGame(self.usernames, self.game_speed, self.multiple_snakes, self.num_of_food)
            self.game_window.show()
        else:
            QMessageBox.warning(self, 'Warning', "Validation fault. Username required.", QMessageBox.Ok)
            pass


class Username4Window(QWidget):
    def __init__(self, speed: int):
        super(Username4Window, self).__init__()
        self.game_window = None
        self.game_speed = speed
        self.num_of_food = 2
        self.multiple_snakes = True
        self.usernames = []

        self.setGeometry(100, 100, 960, 720)
        self.setWindowTitle('4Players')
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon(load_res('icon.png')))

        image = QImage(load_res('wp2409705.jpg'))
        scale_image = image.scaled(QSize(960, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scale_image))
        self.setFixedSize(self.size())

        font = "Spongeboy Me Bob"

        self.usernameLabel1 = QLabel('PLAYER 1: ', self)
        font_label = self.usernameLabel1.font()
        font_label.setPointSize(20)
        font_label.setFamily(font)
        self.usernameLabel1.setFont(font_label)
        self.usernameLabel1.setFixedSize(250, 150)
        self.usernameLabel1.move(50, 100)

        self.usernameEdit1 = QLineEdit(self, )
        font_edit = self.usernameEdit1.font()
        font_edit.setPointSize(22)
        font_edit.setFamily(font)
        self.usernameEdit1.setFont(font_edit)
        self.usernameEdit1.setFixedSize(400, 70)
        self.usernameEdit1.move(50, 200)

        self.usernameLabel2 = QLabel('PLAYER 2: ', self)
        font_label = self.usernameLabel2.font()
        font_label.setPointSize(20)
        font_label.setFamily(font)
        self.usernameLabel2.setFont(font_label)
        self.usernameLabel2.setFixedSize(250, 150)
        self.usernameLabel2.move(50, 300)

        self.usernameEdit2 = QLineEdit(self, )
        font_edit = self.usernameEdit2.font()
        font_edit.setPointSize(22)
        font_edit.setFamily(font)
        self.usernameEdit2.setFont(font_edit)
        self.usernameEdit2.setFixedSize(400, 70)
        self.usernameEdit2.move(50, 400)

        self.usernameLabel3 = QLabel('PLAYER 3: ', self)
        font_label = self.usernameLabel3.font()
        font_label.setPointSize(20)
        font_label.setFamily(font)
        self.usernameLabel3.setFont(font_label)
        self.usernameLabel3.setFixedSize(250, 150)
        self.usernameLabel3.move(500, 100)

        self.usernameEdit3 = QLineEdit(self, )
        font_edit = self.usernameEdit3.font()
        font_edit.setPointSize(22)
        font_edit.setFamily(font)
        self.usernameEdit3.setFont(font_edit)
        self.usernameEdit3.setFixedSize(400, 70)
        self.usernameEdit3.move(500, 200)

        self.usernameLabel4 = QLabel('PLAYER 4: ', self)
        font_label = self.usernameLabel4.font()
        font_label.setPointSize(20)
        font_label.setFamily(font)
        self.usernameLabel4.setFont(font_label)
        self.usernameLabel4.setFixedSize(250, 150)
        self.usernameLabel4.move(500, 300)

        self.usernameEdit4 = QLineEdit(self, )
        font_edit = self.usernameEdit4.font()
        font_edit.setPointSize(22)
        font_edit.setFamily(font)
        self.usernameEdit4.setFont(font_edit)
        self.usernameEdit4.setFixedSize(400, 70)
        self.usernameEdit4.move(500, 400)

        self.cb = QCheckBox('Multiple snakes', self)
        self.cb.setFont(QFont(font))
        self.cb.setStyleSheet("color: black; font-size:30px")
        self.cb.setMinimumSize(150, 70)
        self.cb.move(350, 620)
        self.cb.toggle()
        self.cb.stateChanged.connect(self.change_checkbox)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimumSize(300, 40)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setRange(2, 20)
        self.slider.setSingleStep(1)
        self.slider.move(150, 530)
        self.slider.valueChanged[int].connect(self.changeValue)

        self.apple_box = QLineEdit(self, )
        font_edit = self.apple_box.font()
        font_edit.setPointSize(14)
        font_edit.setFamily(font)
        self.apple_box.setFont(font_edit)
        self.apple_box.setReadOnly(True)
        self.apple_box.setText("2")
        self.apple_box.setFixedSize(70, 60)
        self.apple_box.move(470, 520)

        self.apple_label = QLabel(self, )
        font_edit = self.apple_label.font()
        font_edit.setPointSize(15)
        font_edit.setFamily(font)
        self.apple_label.setFont(font_edit)
        self.apple_label.setText("Food Count")
        self.apple_label.setFixedSize(150, 60)
        self.apple_label.move(550, 520)

        self.start_button = QPushButton(self)
        self.start_button.setText("Start")
        self.start_button.setFont(QFont(font))
        self.start_button.setStyleSheet("color: black; font-size:46px; background-color: green")
        self.start_button.setToolTip("Start the game")
        self.start_button.clicked.connect(self.start_button_pressed)
        self.start_button.resize(self.start_button.sizeHint())
        self.start_button.setMinimumSize(150, 100)
        self.start_button.move(150, 600)

        self.setPalette(palette)

    def changeValue(self, value):
        self.num_of_food = value
        if self.num_of_food < 2:
            self.num_of_food = 2
        self.apple_box.setText(str(self.num_of_food))

    def change_checkbox(self, state):
        if state == Qt.Checked:
            self.multiple_snakes = True
        else:
            self.multiple_snakes = False

    def validate(self, usernameEdit1=None, usernameEdit2=None, usernameEdit3=None, usernameEdit4=None):
        if (usernameEdit1 != "") & (usernameEdit2 != "") & (usernameEdit3 != "") & (usernameEdit4 != ""):
            return True
        else:
            return False

    def start_button_pressed(self):
        if self.validate(self.usernameEdit1.text(), self.usernameEdit2.text(), self.usernameEdit3.text(),
                         self.usernameEdit4.text()):
            self.hide()

            self.usernames.append(self.usernameEdit1.text())
            self.usernames.append(self.usernameEdit2.text())
            self.usernames.append(self.usernameEdit3.text())
            self.usernames.append(self.usernameEdit4.text())
            # winsound.PlaySound(load_res('rattlesnake.wav'), winsound.SND_ASYNC) hocu da kad se klikne START da se cuje taj zvuk zmije jednom
            winsound.PlaySound(load_res('kaerMorhen.wav'), winsound.SND_ASYNC + winsound.SND_LOOP)
            self.game_window = game.SnakeGame(self.usernames, self.game_speed, self.multiple_snakes, self.num_of_food)
            self.game_window.show()
        else:
            QMessageBox.warning(self, 'Warning', "Validation fault. Username required.", QMessageBox.Ok)
            pass
