# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 23:37:07 2018

@author: Joshua_yxh
"""

'''
	bug:
		1. when log out and wanna make another log in, the rollback() raise an interface error
		2. __del__ sometimes occurs exception and let the kernel die
	shortage:
		1. use Qmessagebox to create a message box to inform
'''

import sys
import global_ as gl
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
import pymysql


class sqlConnector():

	def __init__(self, user="visitor", passwd="123456"):
		self.db = pymysql.connect(host="localhost", port=3306,
								  user=user, passwd=passwd,
								  db="Takeout", charset="utf8")
		print("login to mysql")
		self.cursor = self.db.cursor()
		self.userID = -1
		self.state = False # True after login

	def login(self, account, password, type):
		user_check, password_check = self.__check_password(account, password, type)
		if not user_check:
			print('User not exist.')
		elif not password_check:
			print('Password wrong.')
		else:
			gl.set_login_state()
			gl.set_value('account', account)
			gl.set_value('type', type)
			print('login done')

	def __check_password(self, account, password, type):
		'''
			Return: AcountCheck, PasswordCheck
 		'''
		try:
			queryStr = "SELECT AccountPassword, AccountType FROM Account WHERE AccountID = {0};".format(account)
			count = self.cursor.execute(queryStr)
			result = self.cursor.fetchone()

			if count > 0:
				# Check Password
				if not result[1] == type:
					return False, False
				elif result[0] == password:
					return True, True
				else:
					return True, False
			else:
				return False, False
		except:
			self.db.rollback()
			return False, False

	def register(self, account, passwd, type):
		# return Success
		try:
			# check same account
			exist, right = self.__check_password(account, passwd, type)
			if exist:
				print('User already exists.')
				return False
			else:
				cmd = "INSERT INTO Account (AccountID, AccountPassword, AccountType) \
					   VALUES({}, '{}', '{}')".format(account, passwd, type)
				#print(cmd)
				self.cursor.execute(cmd)
				self.db.commit() # important
				gl.set_login_state()
				gl.set_value('account', account)
				gl.set_value('type', type)
				return True
		except:
			self.db.rollback()
			return False

	def test(self):
		self.login(1, "123456", 'User') # should be OK
		self.login(1, "111111", 'User') # Password worng
		self.login(1, "123456", 'Rest') # User not exist
		print('Register: {}'.format(self.register(1, '123456', 'User')))
		print('Register: {}'.format(self.register(60, '123456', 'User')))

		print(self.show_all_rest_names())
		print(self.query_rest_menu('KFC'))

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

	def __del__(self):
		self.db.close()

if __name__ == '__main__':

	#db = pymysql.connect("localhost", "user2", '123456', "takeout", charset="utf8")
	#cursor = db.cursor()
	#print(query_menu(cursor, 'KFC'))
	gl._init()

	app = sqlConnector()
	app.test()