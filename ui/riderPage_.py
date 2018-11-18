# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 17:50:04 2018

@author: Joshua_yxh
"""

import riderPage
import cv2
import connector
import pymysql
import global_ as gl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QAbstractItemView, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class myriderPage(riderPage.Ui_RiderPage):
	def __init__(self, RiderPage):
		self.setupUi(RiderPage)

		self.db = pymysql.connect(host="localhost", port=3306,
								  user=gl.get_value('sql_account'), 
								  passwd=gl.get_value('sql_passwd'),
								  db="Takeout", charset="utf8")
		self.cursor = self.db.cursor()

		self.get_rider_info()
		self.update()

		self.timer = QTimer()
		self.timer.timeout.connect(self.update) 
		self.timer.start(5000)

		

	def get_rider_info(self):
		self.rider_account = gl.get_value('account')
		cmd = 'select riderID, riderName, riderTel from rider where rider.accountID={}'.format(self.rider_account)
		count = self.cursor.execute(cmd)
		result = self.cursor.fetchone()

		self.riderID = result[0]
		self.riderName = result[1]
		self.riderTel = result[2]

	def blockSignals(self, TF):
		pass

	def update(self):
		print('update!')
