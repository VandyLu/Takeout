# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 01:13:59 2018

@author: Joshua_yxh
"""

import userPage
import connector
import global_ as gl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class myuserPage(userPage.Ui_MainPage):
	def __init__(self, MainPage):
		self.UserPage = MainPage
		self.setupUi(MainPage)

		self.sqlvisitor = connector.sqlConnector()
		self.restName = self.sqlvisitor.show_all_rest_names()
		self.courseName = []
		self.orders = []
		self.fillListRest()

		'''---interface---'''
		self.listWidget_rest.currentRowChanged.connect(self.restClicked)
		self.listWidget_course.currentRowChanged.connect(self.courseClicked)
		self.checkBox.stateChanged.connect(self.selectClicked)
		self.spinBox.valueChanged.connect(self.numChanged)
		self.placeOrder.clicked.connect(self.commitOrder)

	def commitOrder(self):
		# get userID, restName, orders
		self.sqlvisitor()

	def fillListRest(self):
		self.listWidget_rest.addItems(self.restName)

	def fillListCourse(self):
		self.listWidget_course.addItems(self.courseName)

	def updateShoppingCart(self):
		str_items = [r[0] +' * '+str(r[1]) for r in self.orders]
		self.shoppingCart.clear()
		self.shoppingCart.addItems(str_items)


	def numChanged(self, value):
		if self.checkBox.isChecked():
			courseName = self.listWidget_course.currentItem().text()
			new_orders = []
			for record in self.orders:
				if record[0] == courseName:
					new_orders.append((record[0], value)) # update value
				else:
					new_orders.append(record)
			self.orders = new_orders

		self.updateShoppingCart()



	def selectClicked(self, state):
		#print(self.listWidget_course.currentItem().text())

		courseName = self.listWidget_course.currentItem().text()
		in_orders = False
		num = 0
		for r in self.orders:
			if r[0] == courseName:
				in_orders = True
				num = r[1]

		if self.checkBox.isChecked() and not in_orders:
			self.spinBox.setValue(1) # num is 1
			self.orders.append((courseName, self.spinBox.value()))
		elif self.checkBox.isChecked() and in_orders: #when doing 'setCheck' in courseClicked, selectClicked is triggerd.
			self.spinBox.setValue(num)
		elif not self.checkBox.isChecked() and not in_orders:
			self.spinBox.setValue(0)
		elif not self.checkBox.isChecked() and in_orders:
			#delete from shoppingcart
			self.spinBox.setValue(0)
			self.orders = [r for r in self.orders if r[0] != courseName]

		self.updateShoppingCart()
		print(self.orders)

	def restClicked(self, index):	
		if self.shoppingCart.count() > 0:
			# change to a new rest
			reply = QMessageBox.question(self, 'Warning', 'Give up current ordering?', 
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if replay == QMessageBox.Yes:
				self.shoppingCart.clear()
				self.listWidget_course.setCurrentRow(-1)
				

		if index >= 0:
			self.listWidget_course.clear()
			
			self.courseName.clear()
			self.courseName = self.sqlvisitor.query_rest_menu(self.restName[index])
			self.fillListCourse()


	def courseClicked(self, index):
		courseName = self.listWidget_course.currentItem().text()
		if index >= 0:
			courseChosen = self.courseName[index]
			price, score, photo = self.sqlvisitor.query_course_info(self.restName[self.listWidget_rest.currentRow()], courseChosen)
			self.price.setText(str(price))
			# check if the course is in the orderings

			in_orders = False
			self.spinBox.setValue(0)
			for r in self.orders:
				if r[0] == courseName:
					in_orders = True
					self.spinBox.setValue(r[1])
					break
			
			self.checkBox.setChecked(in_orders)
			print(in_orders)

		else:
			self.price.setText('')