# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 01:13:59 2018

@author: Joshua_yxh
"""

import cv2
import pymysql
import userPage
import connector
import global_ as gl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QGraphicsScene, QGraphicsPixmapItem,
							 QAbstractItemView, QTableWidgetItem)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class myuserPage(userPage.Ui_MainPage):
	def __init__(self, MainPage):
		self.UserPage = MainPage
		self.setupUi(MainPage)

		self.db = pymysql.connect(host="localhost", port=3306,
								  user="visitor", passwd="123456",
								  db="Takeout", charset="utf8")
		self.cursor = self.db.cursor()

		#self.sqlvisitor = connector.sqlConnector()
		self.restName = self.show_all_rest_names()
		self.restName_ = ''
		self.courseName = []
		self.orders = []
		self.orderID = None
		self.fillListRest()

#		self.axWidget.setControl("{8856F961-340A-11D0-A96B-00C04FD705A2}")
#		self.axWidget.setObjectName("webWidget")
#		self.axWidget.setFocusPolicy(Qt.StrongFocus)
#		self.axWidget.setProperty("DisplayAlerts",False)
#		self.axWidget.setProperty("DisplayScrollBars",True)
#		webstr = "www.baidu.com"
#		self.axWidget.dynamicCall("Navigate(const QString&)",webstr)

		'''---user info---'''
		self.accountID = gl.get_value('account')
		self.addLoginTime()
		self.userID_, self.userName_, self.userTel_ = self.query_user_info()
		print("{}: {}, {}".format(self.userID_, self.userName_, self.userTel_))
		self.locNum = 0
		self.locTitles = ['Address', 'Longitude', 'Latitude']
		self.locTitles_ = []
		self.LocRowClicked = None
		self.changeRecord = None
		self.locs = ()
		self.initTableLoc()
		self.showinfo()

		'''---interface---'''
		self.listWidget_rest.currentRowChanged.connect(self.restClicked)
		self.listWidget_course.currentRowChanged.connect(self.courseClicked)
		self.checkBox.stateChanged.connect(self.selectClicked)
		self.spinBox.valueChanged.connect(self.numChanged)
		self.placeOrder.clicked.connect(self.commitOrder)
		self.pushButton_confirmReceipt.clicked.connect(self.confirmReceipt)
		self.addAddress.clicked.connect(self.add_address)
		self.deleteAddress.clicked.connect(self.delete_address)
		self.modifyAddress.clicked.connect(self.modify_address)
		self.saveChange.clicked.connect(self.saveInfoChange)
		self.abandonChange.clicked.connect(self.abandonInfoChange)

		'''---init history orders state---'''
		self.cursor.execute("select orderID,state from Orders where UserID={} and state<3;".format(self.userID_))
		self.historyIncompleteOrder = self.cursor.fetchall()
		if self.historyIncompleteOrder:
			tmp = self.historyIncompleteOrder[0][0]
			state = self.historyIncompleteOrder[0][1]
			print("Incomplete orderID: {}, state:{}".format(tmp,state))
			if state == 0:
				self.label_deliverState.setText("Waiting for being accepted by restaurant")
			elif state == 1:
				self.label_deliverState.setText("Order accepted by restaurant")
			elif state == 2:
				self.label_deliverState.setText("Order delivering")
		else:
			self.label_deliverState.setText("No Order")

		'''---init table of orders and Loc---'''
		self.recordNum = 0
		self.recordTitles = []
		self.titles=['Course', 'RestName', 'RiderName', 'State', 'Timestamp', 'Score_Rest', 'Score_Rider', 'Comment']
		self.historyOrders = () # (orderID(hide), restID, riderID, state, "course", timestamp, score1, score2, "comment")
		self.initTableOrder()
		self.recordRowClicked = None
		self.doubleSpinBox_rest.setRange(0, 5)
		self.doubleSpinBox_rider.setRange(0, 5)
		self.commit_comment.clicked.connect(self.commitComment)

	def commitOrder(self):
		# get userID, restName, orders
		# not finished
#		button = QMessageBox.question("place order","Are you sure to place this order?",
#									  QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)
#
#		if button == QMessageBox.Ok:
		print("\tpresent order:")
		for r in self.orders:
			print("\t{} * {};".format(r[0], r[1]))
		restID_ = self.query_rest_ID(self.restName_)
		print('restID:{}'.format(restID_))
		self.insert_order(self.userID_,restID_)
		self.resetShoppingCart()
		self.updateTableOrder(False)

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
			self.courseInOrders = [r[0] for r in self.orders]
			numInOrders = [r[1] for r in self.orders]

			priceTable = {}
			restName = self.listWidget_rest.currentItem().text()
			for courseName in self.courseName:
				price, score, photo = self.query_course_info(restName, courseName)
				priceTable[courseName] = float(price)

			totalPrice = 0.0
			for i, name in enumerate(self.courseInOrders):
				totalPrice = totalPrice + priceTable[self.courseInOrders[i]] * numInOrders[i]

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
			if reply == QMessageBox.Yes:
				self.shoppingCart.clear()
				self.listWidget_course.setCurrentRow(-1)


		if index >= 0:
			self.restName_ = self.restName[index]
			self.listWidget_course.clear()

			self.courseName.clear()
			self.courseName = self.query_rest_menu(self.restName[index])
			self.fillListCourse()

		self.updateTotal()

	def resetShoppingCart(self):
		self.checkBox.setCheckState(Qt.Unchecked)
		self.spinBox.clear()
		self.total.clear()
		self.orders.clear()
		self.updateShoppingCart()

	def courseClicked(self, index):
		courseName = self.listWidget_course.currentItem().text()
		if index >= 0:
			courseChosen = self.courseName[index]
			price, score, imagePath = self.query_course_info(self.restName[self.listWidget_rest.currentRow()], courseChosen)
			self.price.setText(str(price))
			scoreStr = "{}/5".format(score)
			print(scoreStr)
			self.score.setText(scoreStr)
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

			'''---read image---'''
			if not imagePath is None:
				print(imagePath)
				img = cv2.imread(imagePath)
				height, width, bytesPerComponent = img.shape
				bytesPerLine = 3 * width
				cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
				Qimg = QImage(img.data, width, height, bytesPerLine,QImage.Format_RGB888)
				self.zoomscale=350/max(height, width)
				pix = QPixmap.fromImage(Qimg)
				self.item=QGraphicsPixmapItem(pix)
				self.item.setScale(self.zoomscale)
				self.scene=QGraphicsScene()
				self.scene.addItem(self.item)
				self.graphicsView.setScene(self.scene)


		else:
			self.price.setText('')
			self.score.setText('')

		self.updateTotal()

	'''---init table setting---'''
	def initTableOrder(self):
		cmd = "select count(*) from orders where UserID={};".format(self.userID_)
		self.cursor.execute(cmd)
		self.recordNum = self.cursor.fetchall()[0][0]
		for i in range(1, self.recordNum+1):
			self.recordTitles.append(str(i))

		self.tableWidget_orders.setColumnCount(8)
		self.tableWidget_orders.setRowCount(self.recordNum)
		self.tableWidget_orders.horizontalHeader().setDefaultSectionSize(100)
		self.tableWidget_orders.horizontalHeader().resizeSection(0,250)
		self.tableWidget_orders.horizontalHeader().resizeSection(3,60)
		self.tableWidget_orders.horizontalHeader().resizeSection(4,180)
		self.tableWidget_orders.horizontalHeader().resizeSection(5,120)
		self.tableWidget_orders.horizontalHeader().resizeSection(6,120)
		self.tableWidget_orders.horizontalHeader().resizeSection(7,500)
		self.tableWidget_orders.horizontalHeader().setFixedHeight(40)
		self.tableWidget_orders.horizontalHeader().setHighlightSections(False)
		self.tableWidget_orders.setHorizontalHeaderLabels(self.titles)
		self.tableWidget_orders.verticalHeader().setDefaultSectionSize(40)
		self.tableWidget_orders.verticalHeader().setFixedWidth(50)
		self.tableWidget_orders.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tableWidget_orders.setVerticalHeaderLabels(self.recordTitles)

		self.tableWidget_orders.itemClicked.connect(self.orderRowClicked)

		self.updateTableOrder(True)

	def initTableLoc(self):
		cmd = "select count(*) from Loc where UserID={};".format(self.userID_)
		self.cursor.execute(cmd)
		self.locNum = self.cursor.fetchall()[0][0]
		for i in range(1, self.locNum+1):
			self.locTitles_.append(str(i))

		self.tableWidget_Loc.setColumnCount(3)
		self.tableWidget_Loc.setRowCount(self.locNum)
		self.tableWidget_Loc.horizontalHeader().setDefaultSectionSize(100)
		self.tableWidget_Loc.horizontalHeader().resizeSection(0,300)
		self.tableWidget_Loc.horizontalHeader().setFixedHeight(40)
		self.tableWidget_Loc.horizontalHeader().setHighlightSections(False)
		self.tableWidget_Loc.setHorizontalHeaderLabels(self.locTitles)
		self.tableWidget_Loc.verticalHeader().setDefaultSectionSize(40)
		self.tableWidget_Loc.verticalHeader().setFixedWidth(50)
		self.tableWidget_Loc.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tableWidget_Loc.setVerticalHeaderLabels(self.locTitles_)

		self.tableWidget_Loc.itemClicked.connect(self.locRowClicked)

		self.updateTableLoc()

	'''---insert records into tables---'''
	def updateTableOrder(self, flag):# flag=true:the init state, flag=false:new order insertion
		if flag:
			cmd = "select OrderID,RestName,RiderName,state,OrderTime,ScoreRest,ScoreRider,CommentTxt \
				   from (Orders Left Join Rest on Orders.RestID=Rest.RestID) Left Join Rider on Orders.RiderID=Rider.RiderID \
				   where Orders.UserID={} order by OrderID;".format(self.userID_)
			self.cursor.execute(cmd)
			self.historyOrders = self.cursor.fetchall()
			row = 0
			for record in self.historyOrders:
				'''---add course at the first column---'''
				cmd_ = "select CourseID, Num from OrderCourse where OrderID={};".format(record[0])
				self.cursor.execute(cmd_)
				tmp = self.cursor.fetchall()
				course = ''
				for item in tmp:
					_cmd_ = "select CourseName from Course where CourseID={};".format(item[0])
					self.cursor.execute(_cmd_)
					courseName_ = self.cursor.fetchall()[0][0]
					course = course + courseName_ + '*' + str(item[1]) + ';'
				self.tableWidget_orders.setItem(row, 0, QTableWidgetItem(course))
				'''---add other info---'''
				self.tableWidget_orders.setItem(row, 1, QTableWidgetItem(str(record[1])))
				self.tableWidget_orders.setItem(row, 2, QTableWidgetItem(str(record[2])))
				self.tableWidget_orders.setItem(row, 3, QTableWidgetItem(str(record[3])))
				self.tableWidget_orders.setItem(row, 4, QTableWidgetItem(str(record[4])))
				self.tableWidget_orders.setItem(row, 5, QTableWidgetItem(str(record[5])))
				self.tableWidget_orders.setItem(row, 6, QTableWidgetItem(str(record[6])))
				self.tableWidget_orders.setItem(row, 7, QTableWidgetItem(record[7]))

				row = row + 1
		else:
			'''---add a row into table of orders---'''
			cmd = "select OrderID,RestName,RiderName,state,OrderTime,ScoreRest,ScoreRider,CommentTxt \
				   from (Orders Left Join Rest on Orders.RestID=Rest.RestID) Left Join Rider on Orders.RiderID=Rider.RiderID \
				   where Orders.UserID={} order by OrderID;".format(self.userID_)
			self.cursor.execute(cmd)
			self.historyOrders = self.cursor.fetchall()
			if len(self.historyOrders) > self.recordNum:
				self.recordNum = len(self.historyOrders)
				self.tableWidget_orders.setRowCount(self.recordNum)
				self.recordTitles.append(str(self.recordNum))
				self.tableWidget_orders.setVerticalHeaderLabels(self.recordTitles)
				'''---add course at the first column---'''
				record = self.historyOrders[self.recordNum-1]
				cmd_ = "select CourseID, Num from OrderCourse where OrderID={};".format(record[0])
				self.cursor.execute(cmd_)
				tmp = self.cursor.fetchall()
				course = ''
				row = self.recordNum - 1
				for item in tmp:
					_cmd_ = "select CourseName from Course where CourseID={};".format(item[0])
					self.cursor.execute(_cmd_)
					courseName_ = self.cursor.fetchall()[0][0]
					course = course + courseName_ + '*' + str(item[1]) + ';'
				self.tableWidget_orders.setItem(row, 0, QTableWidgetItem(course))
				'''---add other info---'''
				self.tableWidget_orders.setItem(row, 1, QTableWidgetItem(str(record[1])))
				self.tableWidget_orders.setItem(row, 2, QTableWidgetItem(str(record[2])))
				self.tableWidget_orders.setItem(row, 3, QTableWidgetItem(str(record[3])))
				self.tableWidget_orders.setItem(row, 4, QTableWidgetItem(str(record[4])))
				self.tableWidget_orders.setItem(row, 5, QTableWidgetItem(str(record[5])))
				self.tableWidget_orders.setItem(row, 6, QTableWidgetItem(str(record[6])))
				if record[7]:
					self.tableWidget_orders.setItem(row, 7, QTableWidgetItem(record[7]))
				else:
					self.tableWidget_orders.setItem(row, 7, QTableWidgetItem(str(record[7])))


	def updateTableLoc(self, flag=0):# 0: show all Loc, >0:add one row, <0: delete one row;
		if flag == 0:
			self.tableWidget_Loc.setRowCount(self.locNum)
			self.tableWidget_Loc.setVerticalHeaderLabels(self.locTitles_)
			cmd = "select LocString,LocX,LocY from Loc where UserID={} order by LocIdx;".format(self.userID_)
			self.cursor.execute(cmd)
			self.locs = self.cursor.fetchall()
			row = 0
			for record in self.locs:
				self.tableWidget_Loc.setItem(row, 0, QTableWidgetItem(record[0]))
				self.tableWidget_Loc.setItem(row, 1, QTableWidgetItem(str(record[1])))
				self.tableWidget_Loc.setItem(row, 2, QTableWidgetItem(str(record[2])))
				row = row + 1
		elif flag > 0:
			self.tableWidget_Loc.setRowCount(self.locNum+1)
			self.locTitles_.append(str(self.locNum+1))
			self.tableWidget_Loc.setVerticalHeaderLabels(self.locTitles_)
			self.locTitles_.pop()
			cmd = "select LocString,LocX,LocY from Loc where UserID={} order by LocIdx;".format(self.userID_)
			self.cursor.execute(cmd)
			self.locs = self.cursor.fetchall()
			row = 0
			for record in self.locs:
				self.tableWidget_Loc.setItem(row, 0, QTableWidgetItem(record[0]))
				self.tableWidget_Loc.setItem(row, 1, QTableWidgetItem(str(record[1])))
				self.tableWidget_Loc.setItem(row, 2, QTableWidgetItem(str(record[2])))
				row = row + 1
		elif flag < 0:
			if self.locNum == 1:
				pass # cant delete when there is only one address
			else:
				self.tableWidget_Loc.setRowCount(self.locNum-1)
				self.locTitles_.pop()
				self.tableWidget_Loc.setVerticalHeaderLabels(self.locTitles_)
				self.locTitles_.append(str(self.locNum))
				cmd = "select LocString,LocX,LocY from Loc where UserID={} order by LocIdx;".format(self.userID_)
				self.cursor.execute(cmd)
				self.locs = self.cursor.fetchall()
				row = 0
				for record in self.locs:
					if row < self.LocRowClicked:
						self.tableWidget_Loc.setItem(row, 0, QTableWidgetItem(record[0]))
						self.tableWidget_Loc.setItem(row, 1, QTableWidgetItem(str(record[1])))
						self.tableWidget_Loc.setItem(row, 2, QTableWidgetItem(str(record[2])))
					elif row > self.LocRowClicked:
						self.tableWidget_Loc.setItem(row-1, 0, QTableWidgetItem(record[0]))
						self.tableWidget_Loc.setItem(row-1, 1, QTableWidgetItem(str(record[1])))
						self.tableWidget_Loc.setItem(row-1, 2, QTableWidgetItem(str(record[2])))
					row = row + 1


	def orderRowClicked(self, item=None):
		if item:
			self.recordRowClicked = item.row()
			record = self.historyOrders[self.recordRowClicked]
			if record[5]:
				self.doubleSpinBox_rest.setValue(record[5])
			else:
				self.doubleSpinBox_rest.setValue(4)
			if record[6]:
				self.doubleSpinBox_rider.setValue(record[6])
			else:
				self.doubleSpinBox_rider.setValue(4)
			if record[7]:
				self.commentTxt.setText(record[7])
			else:
				self.commentTxt.clear()
		else:
			print("None")

	def locRowClicked(self, item=None):
		if item:
			self.LocRowClicked = item.row()
			record = self.locs[self.LocRowClicked]
			if record[0]:
				self.Address.setText(record[0])
			else:
				self.Address.clear()
			if record[1]:
				self.lineEdit_longitude.setText(str(record[1]))
			else:
				self.lineEdit_longitude.clear()
			if record[2]:
				self.lineEdit_latitude.setText(str(record[2]))
			else:
				self.lineEdit_latitude.clear()
		else:
			self.Address.clear()
			self.lineEdit_longitude.clear()
			self.lineEdit_latitude.clear()
			print("None")

	def commitComment(self):
		row = self.recordRowClicked
		orderID = self.historyOrders[row][0]
		score1 = self.doubleSpinBox_rest.value()
		score2 = self.doubleSpinBox_rider.value()
		txt = self.commentTxt.toPlainText()
		cmd = "update Orders set ScoreRest={},ScoreRider={},CommentTxt='{}' where OrderID={};"\
			  .format(score1, score2, txt, orderID)
		try:
			self.cursor.execute(cmd)
			self.db.commit()
			self.updateTableOrder(True)

			'''---recalculate the scores---'''
			restname = self.historyOrders[row][1]
			cmd = "select RestID from Rest where RestName='{}';".format(restname)
			self.cursor.execute(cmd)
			restID = self.cursor.fetchall()[0][0]
			cmd = "update Rest set Score=(select AVG(ScoreRest) \
				   from Orders where RestID={}) where RestID={};".format(restID, restID)
			self.cursor.execute(cmd)
			self.db.commit()

			ridername = self.historyOrders[row][2]
			cmd = "select RiderID from Rider where RiderName='{}';".format(ridername)
			self.cursor.execute(cmd)
			riderID = self.cursor.fetchall()[0][0]
			cmd = "update Rider set Score=(select AVG(ScoreRider) \
				   from Orders where RiderID={}) where RiderID={};".format(riderID, riderID)
			self.cursor.execute(cmd)
			self.db.commit()

			cmd = "select CourseID from OrderCourse where OrderID={};".format(orderID)
			self.cursor.execute(cmd)
			courseID_ = self.cursor.fetchall()
			for course in courseID_:
				courseID = course[0]
				print(courseID)
				cmd = "update Course set Score=\
					   (select AVG(ScoreRest) From OrderCourse Left Join Orders \
					   ON OrderCourse.OrderID=Orders.OrderID\
					   where OrderCourse.CourseID={}) where CourseID={};".format(courseID,courseID)
				print(cmd)
				self.cursor.execute(cmd)
				self.db.commit()
		except:
			print("update wrong")
			self.db.rollback()

	def confirmReceipt(self):
		if self.historyIncompleteOrder:
			state = self.historyIncompleteOrder[0][1]
			if state == 2:
				try:
					cmd = "update Orders set State=3 where UserID={} and State=2;".format(self.userID_)
					self.cursor.execute(cmd)
					self.db.commit()
					self.updateTableOrder(True)
				except:
					self.db.rollback()
					print("confirm receipt wrong!")

	def showinfo(self):
		self.userID.setText(str(self.userID_))
		self.lineEdit_userName.setText(self.userName_)
		self.lineEdit_userTel.setText(self.userTel_)

	def add_address(self):
		self.updateTableLoc(1)
		self.changeRecord = 1

	def delete_address(self):
		if self.LocRowClicked:
			self.updateTableLoc(-1)
			self.changeRecord = 2


	def modify_address(self):
		self.changeRecord = 3
		pass

	def saveInfoChange(self):
		'''---insert and renew self info---'''
		if self.lineEdit_userName.text() != self.userName_:
			try:
				cmd = "update Users set UserName='{}' where UserID={};".format(self.lineEdit_userName.text(), self.userID_)
				self.cursor.execute(cmd)
				self.db.commit()
				self.userName_ = self.lineEdit_userName.text()
			except:
				self.rollback()
				print("insert name wrong")
		if self.lineEdit_userTel.text() != self.userTel_:
			try:
				cmd = "update Users set UserTel='{}' where UserID={};".format(self.lineEdit_userTel.text(), self.userID_)
				self.cursor.execute(cmd)
				self.db.commit()
				self.userTel_ = self.lineEdit_userTel.text()
			except:
				self.db.rollback()
				print("insert tel wrong")
		'''---insert loc info---'''
		if self.changeRecord == 1:
			try:
				cmd = "insert into Loc (UserID, LocString, LocX, LocY) Values ({}, '{}', {}, {});"\
					  .format(self.userID_, self.Address.toPlainText(), self.lineEdit_longitude.text(),\
					  self.lineEdit_latitude.text())
				self.cursor.execute(cmd)
				self.db.commit()
				self.locNum = self.locNum + 1
				self.locTitles_.append(str(self.locNum))
			except:
				self.db.rollback()
				print("insertion wrong")
		elif self.changeRecord == 2:
			try:
				record = self.locs[self.LocRowClicked]
				cmd = "delete from Loc where UserID={} and LocString='{}';"\
					  .format(self.userID_, record[0])
				self.cursor.execute(cmd)
				self.db.commit()
				self.locNum = self.locNum - 1
				self.locTitles_.pop()
			except:
				self.db.rollback()
				print("delete loc wrong")
		elif self.changeRecord == 3:
			try:
				record = self.locs[self.LocRowClicked]
				cmd = "update Loc set LocString='{}',LocX={},LocY={} where UserID={} and LocString='{}';"\
					   .format(self.Address.toPlainText(), self.lineEdit_longitude.text(), \
							   self.lineEdit_latitude.text(), self.userID_, record[0])
				print(cmd)
				self.cursor.execute(cmd)
				self.db.commit()
			except:
				self.db.rollback()
				print("modify loc wrong")
		self.LocRowClicked = None
		self.changeRecord = None
		self.locs = ()

		self.showinfo()
		self.updateTableLoc()
		self.Address.clear()
		self.lineEdit_longitude.clear()
		self.lineEdit_latitude.clear()

	def abandonInfoChange(self):
		self.LocRowClicked = None
		self.changeRecord = None
		self.locs = ()

		self.showinfo()
		self.updateTableLoc()
		self.Address.clear()
		self.lineEdit_longitude.clear()
		self.lineEdit_latitude.clear()

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

	def query_rest_ID(self, restname):
		cmd = "select restID from rest where RestName='{}';".format(restname)
		self.cursor.execute(cmd)
		result = self.cursor.fetchall()[0][0]
		return result

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

	def query_user_info(self):
		self.cursor.execute("select userID,userName,userTel \
							 from users where AccountID={};".format(self.accountID))
		result = self.cursor.fetchall()[0]
		return result[0], result[1], result[2]

	def insert_order(self, userID, restID):
		cmd1 = "insert into orders (UserID, RestID) values ({}, {});".format(userID,restID)
		try:
			self.cursor.execute(cmd1)
			self.db.commit()
		except:
			self.db.rollback()

		cmd2 = "insert into OrderCourse (OrderID, CourseID, Num) values "
		self.cursor.execute("select OrderID from orders where state=0 and userID={} and restID={};".format(userID,restID))
		self.orderID = self.cursor.fetchone()[0]
		print("orderID:{};".format(self.orderID))
		for r in self.orders:
			self.cursor.execute("select courseID from Course where RestID={} and CourseName='{}';".format(restID,r[0]))
			courseID = self.cursor.fetchone()[0]
			cmd2 = cmd2 + "({}, {}, {}),".format(self.orderID, courseID, r[1])
		cmd2 = cmd2[:-1] + ";"
		print(cmd2)
		try:
			self.cursor.execute(cmd2)
			self.db.commit()
		except:
			self.db.rollback()

		self.label_deliverState.setText("Waiting for being accepted by restaurant")


	def addLoginTime(self):
		self.cursor.execute("select UserLoginTime from users;")
		time = int(self.cursor.fetchone()[0]) + 1
		print("logintimes: {}".format(int(time)))
		try:
			cmd = "UPDATE users SET UserLoginTime={} WHERE UserID={};".format(time, self.accountID)
			print(cmd)
			self.cursor.execute(cmd)
			self.db.commit()
		except:
			self.db.rollback()
#######################################################################################################
	def __del__(self):
		self.db.close()