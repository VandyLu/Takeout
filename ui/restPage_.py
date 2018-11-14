# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 17:44:31 2018

@author: Joshua_yxh
"""

import restPage
import connector
from PyQt5 import QtCore, QtGui, QtWidgets

class myrestPage(restPage.Ui_RestPage):
	def __init__(self, RestPage):
		self.setupUi(RestPage)
		self.sqlvisitor = connector.sqlConnector()