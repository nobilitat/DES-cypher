from PySide6 import QtGui, QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.resize(600, 400)
        self.setWindowTitle('Криптографическая программа DES')

