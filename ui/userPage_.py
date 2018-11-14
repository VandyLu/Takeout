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
		self.currentRestIndex = -1

		'''---interface---'''
		self.listWidget_rest.currentRowChanged.connect(self.restClicked)
		self.listWidget_course.currentRowChanged.connect(self.courseClicked)

	def fillListRest(self):
		self.listWidget_rest.addItems(self.restName)

	def fillListCourse(self):
		self.listWidget_course.addItems(self.courseName)

	def restClicked(self, index):
		self.currentRestIndex = index
		self.currentRestName = self.restName[index]
		restChosen = self.currentRestName
		if self.courseName:
			self.listWidget_course.clear()
			
		self.courseName.clear()
		self.courseName = self.sqlvisitor.query_rest_menu(restChosen)
		self.fillListCourse()

	def courseClicked(self, index):
		courseChosen = self.courseName[index]
		price, score, photo = self.sqlvisitor.query_course_info(self.currentRestName, courseChosen)
		self.price.setText(str(price))