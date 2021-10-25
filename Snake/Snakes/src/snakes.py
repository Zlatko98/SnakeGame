
import splash

from PyQt5.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    ex = splash.SplashScreen()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
