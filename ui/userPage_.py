# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 01:13:59 2018

@author: Joshua_yxh
"""

import pymysql
import userPage
import connector
import global_ as gl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class myuserPage(userPage.Ui_MainPage):
	def __init__(self, MainPage):
		self.UserPage = MainPage
		self.setupUi(MainPage)

		self.db = pymysql.connect(host="localhost", port=3306,
								  user='root', passwd='lfblfblfb',
								  db="Takeout", charset="utf8")
		self.cursor = self.db.cursor()

		#self.sqlvisitor = connector.sqlConnector()
		self.restName = self.show_all_rest_names()
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
		# not finished
		self.sqlvisitor()

	def fillListRest(self):
		self.listWidget_rest.addItems(self.restName)

	def fillListCourse(self):
		self.listWidget_course.addItems(self.courseName)

	def updateShoppingCart(self):
		str_items = [r[0] +' * '+str(r[1]) for r in self.orders]
		self.shoppingCart.clear()
		self.shoppingCart.addItems(str_items)

	def updateTotal(self):
		if len(self.orders) == 0:
			self.total.setText('0')
		else:
			courseInOrders = [r[0] for r in self.orders]
			numInOrders = [r[1] for r in self.orders]

			priceTable = {}
			restName = self.listWidget_rest.currentItem().text()
			for courseName in self.courseName:
				price, score, photo = self.query_course_info(restName, courseName)
				priceTable[courseName] = float(price)

			totalPrice = 0.0
			for i, name in enumerate(courseInOrders):
				totalPrice = totalPrice + priceTable[courseInOrders[i]] * numInOrders[i]

			self.total.setText(str(totalPrice))


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
		self.updateTotal()
		
		#print('In "numChanged":', self.orders)


	def selectClicked(self, state):
		#print(self.listWidget_course.currentItem().text())

		courseName = self.listWidget_course.currentItem().text()
		in_orders = False
		num = 0
		for r in self.orders:
			if r[0] == courseName:
				in_orders = True
				num = r[1]
				break

		self.spinBox.blockSignals(True)
		if self.checkBox.isChecked() and not in_orders:
			self.spinBox.setValue(1) # num is 1
			self.orders.append((courseName, self.spinBox.value()))
			
		elif not self.checkBox.isChecked() and in_orders:
			#delete from shoppingcart
			self.spinBox.setValue(0)
			self.orders = [r for r in self.orders if r[0] != courseName]
		self.spinBox.blockSignals(False)

		self.updateShoppingCart()
		self.updateTotal()
		#print('In "selectClicked":', in_orders)
		#print('In "selectClicked":', self.orders)
		

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
			self.courseName = self.query_rest_menu(self.restName[index])
			self.fillListCourse()

		self.updateTotal()


	def courseClicked(self, index):
		courseName = self.listWidget_course.currentItem().text()
		if index >= 0:
			courseChosen = self.courseName[index]
			price, score, photo = self.query_course_info(self.restName[self.listWidget_rest.currentRow()], courseChosen)
			self.price.setText(str(price))
			self.score.setText(str(score))
			# check if the course is in the orderings

			self.spinBox.blockSignals(True)
			self.checkBox.blockSignals(True)

			in_orders = False
			self.spinBox.setValue(0)
			for r in self.orders:
				if r[0] == courseName:
					print(r)
					in_orders = True
					self.spinBox.setValue(r[1])
					break

			self.checkBox.setChecked(in_orders)

			self.checkBox.blockSignals(False)
			self.spinBox.blockSignals(False)
			
			
			#print('In "courseClicked":', in_orders)
			#print('In "courseClicked":', self.orders)

		else:
			self.price.setText('')
			self.score.setText('')

		self.updateTotal()


####################################################################################################
# MYSQL
	def show_all_rest_names(self):
		''' return a list of rest names
		'''
		try:
			cmd = "SELECT RestName from Rest"
			count = self.cursor.execute(cmd)
			result =  self.cursor.fetchall()
			return [record[0] for record in result]
		except:
			self.db.rollback()
			return []

	def query_rest_menu(self, restname):
		self.cursor.execute("select CourseName "
					"from Rest natural join Course where Rest.RestName='{}';".format(restname))
		return [r[0] for r in self.cursor.fetchall()]

	def query_course_info(self, restname, coursename):
		self.cursor.execute("select RestID from Rest where restName='{}';".format(restname))
		restID = self.cursor.fetchall()[0][0]
		cmd = "select Price, Score, Photo from Course "\
				"where RestID={} and CourseName='{}';".format(restID, coursename)
		print(cmd)
		self.cursor.execute(cmd)
		result = self.cursor.fetchall()[0]
		return result

	def query_rest_all_prices(self, restname):
		self.cursor.execute("")
#######################################################################################################
	def __del__(self):
		self.db.close()