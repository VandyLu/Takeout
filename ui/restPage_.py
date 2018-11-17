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

		# page1
		self.get_rest_info()
		self.update()

		self.tableWidget_course.currentCellChanged.connect(self.courseTableCell_changed)
		self.addCourse.clicked.connect(self.add_clicked)
		self.saveCourse.clicked.connect(self.save_clicked)
		self.deleteCourse.clicked.connect(self.delete_clicked)

		# page2
		

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

	def update(self):
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

	def courseTableCell_changed(self, cur_r, cur_c, pre_r, pre_c):
		self.update()


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
			


