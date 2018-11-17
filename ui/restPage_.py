# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 17:44:31 2018

@author: Joshua_yxh
"""

import cv2
import restPage
import connector
import pymysql
import global_ as gl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QAbstractItemView, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


class myrestPage(restPage.Ui_RestPage):
	def __init__(self, RestPage):
		self.setupUi(RestPage)
		self.db = pymysql.connect(host="localhost", port=3306,
								  user=gl.get_value('sql_account'), 
								  passwd=gl.get_value('sql_passwd'),
								  db="Takeout", charset="utf8")
		self.cursor = self.db.cursor()

		self.get_rest_info()
		self.update()

		self.tableWidget_course.currentCellChanged.connect(self.update)
		self.addCourse.clicked.connect(self.add_clicked)
		self.saveCourse.clicked.connect(self.save_clicked)
		self.deleteCourse.clicked.connect(self.delete_clicked)

		self.tableWidget_order.currentCellChanged.connect(self.update)
		self.acceptOrder.clicked.connect(self.accept_clicked)
		self.rejectOrder.clicked.connect(self.reject_clicked)

		self.tableWidget_history.currentCellChanged.connect(self.update)
		self.saveChange.clicked.connect(self.saveChange_clicked)
		self.abandonChange.clicked.connect(self.abandonChange_clicked)

	def get_rest_info(self):
		self.restAccount = gl.get_value('account')
		cmd = 'select RestID, RestName, RestTel, RestScore, LocX, LocY ' +\
			'from rest where AccountID = "{}"'.format(self.restAccount)
		count = self.cursor.execute(cmd)
		if count > 0:
			result = self.cursor.fetchone()
			self.restID = result[0]
			self.restName = result[1]
			self.restTel = result[2]
			self.restScore = result[3]
			self.locX = result[4]
			self.locY = result[5]

	def blockSignals(self, TF):
		self.tableWidget_course.blockSignals(TF)
		self.addCourse.blockSignals(TF)
		self.saveCourse.blockSignals(TF)
		self.deleteCourse.blockSignals(TF)
		self.tableWidget_order.blockSignals(TF)
		self.acceptOrder.blockSignals(TF)
		self.rejectOrder.blockSignals(TF)
		self.tableWidget_history.blockSignals(TF)

	def update(self):
		# page 1
		self.blockSignals(True)
		cmd = 'select CourseName, Price, Photo, CourseID from course where RestID = {}'.format(self.restID)
		count = self.cursor.execute(cmd)
		results = self.cursor.fetchall()
		self.courseTable = results

		currentRow = self.tableWidget_course.currentRow()
		#self.tableWidget_course.currentCellChanged.blocksignal(True)
		if currentRow == -1:
			currentRow = 0
			self.tableWidget_course.setCurrentCell(0, 0)
		#self.tableWidget_course.currentCellChanged.blocksignal(False)

		self.updateCourseTable(results)
		self.updateImage(results[currentRow][2])

		self.courseNameEdit.setText(results[currentRow][0])
		self.coursePriceEdit.setText(str(results[currentRow][1]))
		self.coursePhotoEdit.setText(results[currentRow][2])

		# page 2
		cmd = 'select UserName, OrderTime, State, OrderID from (orders join users on orders.UserID=users.UserID) where RestID={} and State=0;'.format(self.restID)
		count = self.cursor.execute(cmd)
		results = self.cursor.fetchall()
		
		self.orderTable = results
		self.updateOrderTable(results)

		currentOrderRow = self.tableWidget_order.currentRow()
		if currentOrderRow >= 0:
			currentOrderID = results[currentOrderRow][-1]
			cmd = 'select CourseName, Num from (OrderCourse join Course on OrderCourse.CourseID=Course.CourseID) where OrderID={};'.format(currentOrderID)
			count = self.cursor.execute(cmd)
			course_num = self.cursor.fetchall()
			self.updateOrderCourseList(course_num)

		# page 3
		cmd = 'select UserName, RiderName, OrderTime, ScoreRest, CommentTxt from orders join users on orders.UserID=users.UserID join Rider on Rider.RiderID=Orders.RiderID where restid={} and State=3;'.format(self.restID)
		count = self.cursor.execute(cmd)
		results = self.cursor.fetchall()
		self.historyTable = results
		self.updateHistoryTable(results)

		currentHistoyRow = self.tableWidget_history.currentRow()
		if currentHistoyRow >= 0:
			self.comment.setText(self.historyTable[currentHistoyRow][-1])

		# page 4
		cmd = 'select RestName, RestTel, RestAddress, LocX, LocY from Rest where RestID={}'.format(self.restID)
		count = self.cursor.execute(cmd)
		result = self.cursor.fetchone()

		self.label_restID.setText(str(self.restID))
		self.lineEdit_restName.setText(result[0])
		self.lineEdit_restTel.setText(result[1])
		self.Address.setText(result[2])
		self.lineEdit_restLongitude.setText(str(result[3]))
		self.lineEdit_restLatitude.setText(str(result[4]))

		self.blockSignals(False)

	def updateHistoryTable(self, results):
		count = len(results)
		self.tableWidget_history.setRowCount(count)
		for i in range(count):
			self.tableWidget_history.setItem(i, 0, QtWidgets.QTableWidgetItem(results[i][0]))
			self.tableWidget_history.setItem(i, 1, QtWidgets.QTableWidgetItem(results[i][1]))
			self.tableWidget_history.setItem(i, 2, QtWidgets.QTableWidgetItem(str(results[i][2])))
			self.tableWidget_history.setItem(i, 3, QtWidgets.QTableWidgetItem(str(results[i][3])))


	def updateOrderTable(self, results):
		count = len(results)
		self.tableWidget_order.setRowCount(count)
		for i in range(count):
			self.tableWidget_order.setItem(i, 0, QtWidgets.QTableWidgetItem(results[i][0]))
			self.tableWidget_order.setItem(i, 1, QtWidgets.QTableWidgetItem(str(results[i][1])))
			self.tableWidget_order.setItem(i, 2, QtWidgets.QTableWidgetItem(str(results[i][2])))
			self.tableWidget_order.setItem(i, 3, QtWidgets.QTableWidgetItem('NULL'))

	def updateOrderCourseList(self, course_num):
		self.listWidget_orderCourse.clear()
		print('course_num: ', course_num)
		for name, num in course_num:
			show_str = '{} * {}'.format(name, num)
			self.listWidget_orderCourse.addItem(show_str)

	def updateCourseTable(self, results):
		count = len(results)
		self.tableWidget_course.setRowCount(count)
		for i in range(count):
			self.tableWidget_course.setItem(i, 0, QtWidgets.QTableWidgetItem(results[i][0]))
			self.tableWidget_course.setItem(i, 1, QtWidgets.QTableWidgetItem(str(results[i][1])))

	def updateImage(self, imagePath):
		img = cv2.imread(imagePath)
		height, width, bytesPerComponent = img.shape
		bytesPerLine = 3 * width
		cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
		Qimg = QImage(img.data, width, height, bytesPerLine,QImage.Format_RGB888)
		zoomscale=350/max(height, width)
		pix = QPixmap.fromImage(Qimg)
		item=QGraphicsPixmapItem(pix)
		item.setScale(zoomscale)
		scene=QGraphicsScene()
		scene.addItem(item)
		self.graphicsView.setScene(scene)

	#def courseTableCell_changed(self, cur_r, cur_c, pre_r, pre_c):
	#	self.update()


	def add_clicked(self):
		
		newCourseName = self.courseNameEdit.text()
		newCoursePrice = float(self.coursePriceEdit.text())
		newCoursePhoto = self.coursePhotoEdit.text().replace('\\','\\\\')

		cmd = 'insert into course(CourseName, RestID, Price, Score, Photo) ' + \
				  'values("{}", {}, {}, {}, "{}");'.format(newCourseName, self.restID, newCoursePrice, 0.0, newCoursePhoto)
		#print(cmd)
		self.cursor.execute(cmd)
		self.db.commit()

		self.update()

	def save_clicked(self):
		currentRow = self.tableWidget_course.currentRow()
		currentCourseID = self.courseTable[currentRow][-1]

		newCourseName = self.courseNameEdit.text()
		newCoursePrice = float(self.coursePriceEdit.text())
		newCoursePhoto = self.coursePhotoEdit.text().replace('\\','\\\\')

		cmd = 'update Course set CourseName="{}", Price={}, Photo="{}" \
		    where CourseID={};'.format(newCourseName, 
		   								newCoursePrice, 
		   								newCoursePhoto,
		   								currentCourseID)
		print(cmd)
		self.cursor.execute(cmd)
		self.db.commit()
		self.update()		

	def delete_clicked(self):
		currentRow = self.tableWidget_course.currentRow()
		if currentRow >= 0:
			cmd = 'delete from course where courseID = {};'.format(self.courseTable[currentRow][-1])
			self.cursor.execute(cmd)
			self.db.commit()
			self.tableWidget_course.setCurrentCell(0, 0)
			


	def accept_clicked(self):
		currentRow = self.tableWidget_order.currentRow()
		if currentRow >= 0:
			cmd = 'update Orders set state=1 where OrderID={}'.format(self.orderTable[currentRow][-1])
			self.cursor.execute(cmd)
			self.db.commit()

			self.listWidget_orderCourse.clear()
			self.tableWidget_order.setCurrentCell(0, 0)

		self.update()

	def reject_clicked(self):
		currentRow = self.tableWidget_order.currentRow()
		if currentRow >= 0:
			cmd = 'delete from orders where orderID={};'.format(self.orderTable[currentRow][-1])
			self.cursor.execute(cmd)
			cmd = 'delete from ordercourse where orderID={};'.format(self.orderTable[currentRow][-1])
			self.cursor.execute(cmd)
			self.db.commit()

			self.listWidget_orderCourse.clear()
			self.tableWidget_order.setCurrentCell(0, 0)

		self.update()

	def saveChange_clicked(self):
		newRestName = self.lineEdit_restName.text()
		newRestTel = self.lineEdit_restTel.text()
		newRestAddress = self.Address.toPlainText()
		newRestLocX = self.lineEdit_restLongitude.text()
		newRestLocY = self.lineEdit_restLatitude.text()

		cmd = 'update rest set RestName="{}", RestTel="{}", RestAddress="{}", LocX={}, LocY={} where restid={}'.format(newRestName,
		 newRestTel,
		 newRestAddress,
		 newRestLocX,
		 newRestLocY, 
		 self.restID)
		self.cursor.execute(cmd)
		self.db.commit()

	def abandonChange_clicked(self):
		self.update()