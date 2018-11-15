# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 17:20:31 2018

@author: Joshua_yxh
"""

import loginPage
import userPage_
import restPage_
import riderPage_
import connector
import global_ as gl
from PyQt5 import QtCore, QtGui, QtWidgets


class myloginPage(loginPage.Ui_LoginPage):
	def __init__(self, LoginPage):

		self.LoginPage = LoginPage
		self.setupUi(LoginPage)

		self.sqlvisitor = connector.sqlConnector()
		self.lineEdit_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
		self.lineEdit_passwd_.setEchoMode(QtWidgets.QLineEdit.Password)

		# for debug
		self.lineEdit_ID.setText('1')
		self.lineEdit_passwd.setText('123456')

		'''---interface---'''
		self.Login.clicked.connect(self.login)
		self.Register.clicked.connect(self.register)



	def login(self):
		if self.radioButton_user.isChecked():
			type_ = self.radioButton_user.text()
		elif self.radioButton_rest.isChecked():
			type_ = self.radioButton_rest.text()
		elif self.radioButton_rider.isChecked():
			type_ = self.radioButton_rider.text()

		self.sqlvisitor.login(int(self.lineEdit_ID.text()), self.lineEdit_passwd.text(), type_)
		if gl.get_login_state():
			print("%d: %s" % (gl.get_value('account'), gl.get_value('type')))
			self.jump_page()

	def register(self):
		print('button pushed')
		if self.radioButton_user_.isChecked():
			type_ = self.radioButton_user_.text()
		elif self.radioButton_rest_.isChecked():
			type_ = self.radioButton_rest_.text()
		elif self.radioButton_rider_.isChecked():
			type_ = self.radioButton_rider_.text()

		self.sqlvisitor.register(int(self.lineEdit_ID_.text()), self.lineEdit_passwd_.text(), type_)
		if gl.get_login_state():
			print("%d: %s" % (gl.get_value('account'), gl.get_value('type')))
			self.jump_page()

	def delete_all_input(self):
		self.lineEdit_ID.clear()
		self.lineEdit_passwd.clear()
		self.lineEdit_ID_.clear()
		self.lineEdit_passwd_.clear()

	def jump_page(self):
		self.LoginPage.close()
		self.sqlvisitor.db.close()

		if gl.get_value('type') == 'User':
			dialog_ = QtWidgets.QDialog()
			ui_ = userPage_.myuserPage(dialog_)
		elif gl.get_value('type') == 'Rest':
			dialog_ = QtWidgets.QDialog()
			ui_ = restPage_.myrestPage(dialog_)
		elif gl.get_value('type') == 'Rider':
			dialog_ = QtWidgets.QDialog()
			ui_ = riderPage_.myriderPage(dialog_)

		dialog_.show()
		dialog_.exec_()
		gl.reset_state()
		self.delete_all_input()
		self.LoginPage.show()