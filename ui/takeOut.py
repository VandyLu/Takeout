# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 22:34:16 2018

@author: Joshua_yxh
"""

import sys
import loginPage_
import global_ as gl
from PyQt5 import QtCore, QtGui, QtWidgets

def main():
	''' ---init--- '''
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QDialog()
	gl._init()
	ui = loginPage_.myloginPage(dialog)

	dialog.show()

	sys.exit(app.exec_())


if __name__ == '__main__':
	main()