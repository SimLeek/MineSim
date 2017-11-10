import unittest as ut
from PyQt5 import QtWidgets
import minesim.perspective_window as persp
from .data.perspectiveTesting import setupForTesting

class TestPerspectiveWindow(ut.TestCase):
    def testRuns(self):
        app = QtWidgets.QApplication([])

        win = persp.PerspectiveWindow()
        setupForTesting(win)

        win.move(QtWidgets.QDesktopWidget().rect().center() - win.rect().center())
        win.show()
        app.exec_()