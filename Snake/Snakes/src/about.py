from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDesktopWidget

from helpers import load_res


class AboutWindow(QWidget):
    def __init__(self):
        super(AboutWindow, self).__init__()

        self.setGeometry(100, 100, 960, 640)
        self.setWindowTitle('About')
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon(load_res('icon.png')))

        self.layout = QVBoxLayout()
        self.label = QLabel(
            "<br> How to play: <br><br>• Two to four players plan a snake movement strategy. Each player has one or "
            "more snakes <br> with which they can execute the strategy. <br><br> • The player's goal is to capture "
            "rival snakes. <br><br> • Every player has 10, 12 or 15 seconds to finish a move, depending on the choice. <br><br>"
            "• A snake dies if it hits its head against a wall or the body of another snake. "
            "<br><br> • A snake has the length and number of steps per stroke that it can extend by gathering food. "
            "<br><br> • Players can choose the extent to which the food will appear, which further affects the difficulty of the game."
            "<br><br> • Food moves in a straight line from 1 to 3 steps per move."
            "<br><br> • When a player consumes at least 5 apples, he gains the ability to create a new snake whose length is five. "
            "The current snake's length will"
            "<br> shrink by the same amount."
            "<br><br>• From time to time an unexpected force appears."
            "<br> The player has two seconds to approach the force or escape from it (the force acts on an area of 5 squares in all directions)."
            "<br> If a player joins a positive force - he will be rewarded, or damaged if he does not manage to escape from the negative force."
            "<br><br>Good luck! :) <br><br><br><br><br><br><br><br><br><br>")

        font = self.label.font()
        font.setPointSize(11)
        font.setFamily('Spongeboy Me Bob')

        image = QImage(load_res('wp2409705.jpg'))
        scale_image = image.scaled(QSize(960, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scale_image))

        self.setPalette(palette)
        self.label.setFont(font)
        self.layout.addWidget(self.label)
        self.setWindowTitle("Turn Snake")
        self.setLayout(self.layout)
        self.setFixedSize(1280, 720)