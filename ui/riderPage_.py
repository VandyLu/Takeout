# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 17:50:04 2018

@author: Joshua_yxh
"""

import riderPage
import connector
from PyQt5 import QtCore, QtGui, QtWidgets

class myriderPage(riderPage.Ui_RiderPage):
	def __init__(self, RiderPage):
		self.setupUi(RiderPage)
		self.sqlvisitor = connector.sqlConnector()