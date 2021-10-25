import re
import winsound

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFontDatabase, QFont, QImage, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QGridLayout, QComboBox, QDesktopWidget, QMessageBox)

import about
import game
from helpers import load_res, init_button
from username import Username2Window, Username3Window, Username4Window


class SplashScreen(QMainWindow):

    def __init__(self):
        super().__init__()
        self.game_window = None
        self.classic = None
        self.combo_speeds = QComboBox()
        self.about_window = about.AboutWindow()
        self.central_widget = QWidget()

        font_db = QFontDatabase()

        font_db.addApplicationFont(load_res('Spongeboy Me Bob.ttf'))

        self.setWindowIcon(QIcon(load_res('icon.png')))

        combo_speeds_list = [' Speed 1x ', ' Speed 2x ', ' Speed 3x ']
        self.combo_speeds.addItems(combo_speeds_list)
        self.combo_speeds.setFixedSize(210, 70)
        font_cbs = self.combo_speeds.font()
        font_cbs.setPointSize(20)
        font_cbs.setFamily('Spongeboy Me Bob')
        self.combo_speeds.setFont(font_cbs)
        combo_players_list = [' 2 players ', ' 3 players ', ' 4 players ', ' Classic snake ']
        self.combo_players = QComboBox(self)
        self.combo_players.addItems(combo_players_list)
        self.combo_players.setFixedSize(270, 70)
        font_cb = self.combo_players.font()
        font_cb.setPointSize(20)
        font_cb.setFamily('Spongeboy Me Bob')

        self.combo_players.setFont(font_cb)
        self.combo_players.setStyleSheet("color: orange; background-color: transparent;"
                                         "selection-background-color: transparent;"
                                         "selection-color: orange")
        self.combo_speeds.setStyleSheet("color: orange; background-color: transparent;"
                                        "selection-background-color: transparent;"
                                        "selection-color: orange")

        font = QFont("Spongeboy Me Bob")

        btn_start = init_button('Start')
        btn_start.setFont(font)
        btn_start.clicked.connect(self.on_btn_start_pressed)
        btn_start.setStyleSheet("color: orange; font-size:40px; background-color: transparent")

        btn_close = init_button('Exit')
        btn_close.setFont(font)

        btn_close.clicked.connect(QApplication.instance().quit)
        btn_close.setStyleSheet("color: red; font-size:40px; background-color: transparent")

        btn_about = init_button('About')

        btn_about.clicked.connect(self.about_info)
        btn_about.setFont(font)
        btn_about.setStyleSheet("color: orange; font-size:30px; background-color: transparent")

        self.setCentralWidget(self.central_widget)
        grid = QGridLayout()
        grid.setSpacing(150)
        grid.addWidget(btn_start, 1, 1, 2, 1)
        grid.addWidget(btn_close, 1, 3, 2, 1)
        grid.addWidget(self.combo_speeds, 1, 1)
        grid.addWidget(self.combo_players, 1, 2)
        grid.addWidget(btn_about, 1, 3)

        image = QImage(load_res('splash.png'))
        scale_image = image.scaled(QSize(960, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scale_image))

        self.setPalette(palette)
        self.setGeometry(100, 100, 960, 640)
        self.setFixedSize(self.size())
        self.centralWidget().setLayout(grid)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowTitle('Welcome to Snakes!')
        self.show()
        winsound.PlaySound(load_res('rattlesnake.wav'), winsound.SND_ASYNC)


    def get_players(self):
        cmb_text = str(self.combo_players.currentText())
        if cmb_text == ' Classic snake ':
            final = '1'
        else:
            final = re.sub('\D', '', cmb_text)
        print(final)
        return int(final)

    def on_btn_start_pressed(self):
        self.hide()

        num_of_players = self.get_players()
        game_speed = self.get_speed()
        if num_of_players == 1:
            self.classic = game.ClassicSnake()
            self.classic.show()
            self.classic.sboard.start(self.get_speed())
            winsound.PlaySound(load_res('kaerMorhen.wav'), winsound.SND_ASYNC + winsound.SND_LOOP)

        if num_of_players == 2:
            self.username_window = Username2Window(game_speed)
            self.username_window.show()
        elif num_of_players == 3:
            self.username_window = Username3Window(game_speed)
            self.username_window.show()
        elif num_of_players == 4:
            self.username_window = Username4Window(game_speed)
            self.username_window.show()

    def about_info(self):
        self.about_window.show()

    def get_speed(self):
        cmb_text = str(self.combo_speeds.currentText())
        cmb_speed = cmb_text.replace(' Speed ', ' ')
        final_speed = cmb_speed.replace('x', ' ')
        return int(final_speed)

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Really?',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
