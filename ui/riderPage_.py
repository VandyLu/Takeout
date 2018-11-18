# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 17:50:04 2018

@author: Joshua_yxh
"""

import riderPage
import cv2
import numpy as np
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
		self.update() # flush
		self.updateRiderInfo() # not flush

		self.acceptOrder.clicked.connect(self.accpet_clicked)
		self.rejectOrder.clicked.connect(self.reject_clicked)

		self.saveChange.clicked.connect(self.saveChange_clicked)
		self.abandonChange.clicked.connect(self.updateRiderInfo)

		self.timer = QTimer()
		self.timer.timeout.connect(self.update) 
		self.timer.start(100000)

		

	def get_rider_info(self):
		self.rider_account = gl.get_value('account')
		cmd = 'select riderID, riderName, riderTel from rider where rider.accountID={}'.format(self.rider_account)
		count = self.cursor.execute(cmd)
		result = self.cursor.fetchone()

		self.riderID = result[0]
		self.riderName = result[1]
		self.riderTel = result[2]

		# create view for this rider
		cmd = 'create or replace view tmp_order as (select OrderID, UserID, LocIdx, RestID, OrderTime, State from orders where (riderID is NULL or riderID={}) and restID in (select restID from restrider \
				where riderID={}));'.format(self.riderID, self.riderID)
		count = self.cursor.execute(cmd)


	def blockSignals(self, TF):
		pass

	def update(self):
		self.blockSignals(True)

		cmd = 'select UserName, UserTel, RestName, OrderID from tmp_order join users on tmp_order.userID=users.userID \
				join rest on tmp_order.restID=rest.restID where tmp_order.state=1'
		count = self.cursor.execute(cmd)
		results = self.cursor.fetchall()
		self.waitingOrder = results
		self.updateOrderTable(results)

		cmd = 'select UserName, UserTel, LocString, OrderTime, RestName, OrderID from tmp_order join users on tmp_order.userID=users.userID \
				join rest on tmp_order.restID=rest.restID \
				join Loc on Loc.userID=tmp_order.userID and Loc.LocIdx=tmp_order.LocIdx \
				where tmp_order.state=2'
		count = self.cursor.execute(cmd)
		results = self.cursor.fetchall()
		self.deliveringOrder = results
		self.updateDeliverTable(results)

		# page 2
		self.updateMap()
		# page 3
		self.updateRiderInfo()

		self.blockSignals(False)

	def updateOrderTable(self, results):
		count = len(results)
		self.tableWidget_order.setRowCount(count)
		for i in range(count):
			self.tableWidget_order.setItem(i, 0, QtWidgets.QTableWidgetItem(results[i][0]))
			self.tableWidget_order.setItem(i, 1, QtWidgets.QTableWidgetItem(results[i][1]))
			self.tableWidget_order.setItem(i, 2, QtWidgets.QTableWidgetItem(results[i][2]))
			self.tableWidget_order.setItem(i, 3, QtWidgets.QTableWidgetItem('waiting for rider'))

	def updateDeliverTable(self, results):
		count = len(results)
		self.tableWidget_deliver.setRowCount(count)
		for i in range(count):
			self.tableWidget_deliver.setItem(i, 0, QtWidgets.QTableWidgetItem(results[i][0]))
			self.tableWidget_deliver.setItem(i, 1, QtWidgets.QTableWidgetItem(results[i][1]))
			self.tableWidget_deliver.setItem(i, 2, QtWidgets.QTableWidgetItem(results[i][2]))
			self.tableWidget_deliver.setItem(i, 3, QtWidgets.QTableWidgetItem(str(results[i][3])))
			self.tableWidget_deliver.setItem(i, 4, QtWidgets.QTableWidgetItem(results[i][4]))
			self.tableWidget_deliver.setItem(i, 5, QtWidgets.QTableWidgetItem(str('delivering')))


	def accpet_clicked(self):
		currentRow = self.tableWidget_order.currentRow()
		if currentRow >= 0:
			orderID = self.waitingOrder[currentRow][-1]

			cmd = 'update orders set RiderID={} where OrderID={}'.format(self.riderID, orderID)
			self.cursor.execute(cmd)

		self.update()

	def reject_clicked(self):
		pass

	def saveChange_clicked(self):
		newRiderName = self.lineEdit_riderName.text()
		newRiderTel = self.lineEdit_riderTel.text()
		cmd = 'update Rider set RiderName="{}", RiderTel="{}" where RiderID={};'.format(newRiderName, newRiderTel, self.riderID)
		self.cursor.execute(cmd)
		self.db.commit()


	def updateRiderInfo(self):
		cmd = 'select RiderName, RiderTel from rider where riderID={}'.format(self.riderID)
		count = self.cursor.execute(cmd)
		results = self.cursor.fetchone()

		self.label_riderID.setText(str(self.riderID))
		self.lineEdit_riderName.setText(results[0])
		self.lineEdit_riderTel.setText(results[1])

	def updateMap(self):
		# user is red point
		# rest is blue point

		def draw_point(img, xy, type):
			if type=='rest':
				color = (255, 0, 0)
			else:
				color = (0, 0, 255)
			cv2.circle(img, xy, 10, color, -1)
			return img


		height, width = 400, 600
		img = np.ones((height, width, 3), dtype=np.uint8) * 255
		# prepare data
		count = len(self.deliveringOrder)
		records = np.zeros((count, 4), dtype=np.float32) #(userX, userY, restX, restY)
		for i in range(count):
			orderID = self.deliveringOrder[i][-1]
			cmd = 'select locX, locY from orders join loc on loc.userID=orders.userID and loc.locIdx=orders.locIdx \
					where orders.orderID={}'.format(orderID)
			count = self.cursor.execute(cmd)
			userX, userY = self.cursor.fetchone()
			cmd = 'select locX, locY from orders join rest on orders.restID=rest.restID \
					where orderID={}'.format(orderID)
			count = self.cursor.execute(cmd)
			restX, restY = self.cursor.fetchone()
			records[i,:] = (userX, userY, restX, restY)

		# scale, map to 0.9 of the entire image
		scale = 0.9 
		minX = np.min(records[:, (0, 2)])
		maxX = np.max(records[:, (0, 2)])
		minY = np.min(records[:, (1, 3)])
		maxY = np.max(records[:, (1, 3)])

		records[:, (0, 2)] = ((records[:, (0, 2)] - minX) / (maxX-minX) * scale + (1.0-scale)/2.0) * width
		records[:, (1, 3)] = ((records[:, (1, 3)] - minY) / (maxY-minY) * scale + (1.0-scale)/2.0) * height

		# start drawing
		for x1, y1, x0, y0 in records:
			img = draw_point(img, (x0, y0), 'rest')
			img = draw_point(img, (x1, y1), 'user')

		# end drawing
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
		self.graphicsView_map.setScene(scene)


	def __del__(self):
		self.cursor.execute('drop view tmp_order;')
		self.db.close()