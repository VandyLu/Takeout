# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 01:13:59 2018

@author: Joshua_yxh
"""

import userPage
import connector
import global_ as gl
from PyQt5 import QtCore, QtGui, QtWidgets

class myuserPage(userPage.Ui_MainPage):
	def __init__(self, MainPage):
		self.UserPage = MainPage
		self.setupUi(MainPage)

		self.sqlvisitor = connector.sqlConnector()
		self.restName = self.sqlvisitor.show_all_rest_names()
#		self.restNameChosen
		self.courseName = []
		self.fillListRest()

		'''---interface---'''
		self.listWidget_rest.currentRowChanged.connect(self.restClicked)

	def fillListRest(self):
		self.listWidget_rest.addItems(self.restName)

	def fillListCourse(self):
		self.listWidget_course.addItems(self.courseName)

	def restClicked(self, index):
		restChosen = self.restName[index]
		if self.courseName:
			for item in self.courseName:
				self.listWidget_course.removeItemWidget(item)
		self.courseName.clear()
		self.courseName = self.sqlvisitor.query_rest_menu(restChosen)
		self.fillListCourse()