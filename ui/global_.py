# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 11:15:25 2018

@author: Joshua_yxh
"""


def _init():
	global _global_account
	_global_account = {}
	set_value('login_state', False)

def get_login_state():
	return _global_account['login_state']

def set_login_state():
	_global_account['login_state'] = True

def set_value(name, value):
	_global_account[name] = value

def get_value(name, defValue=None):
	try:
		return _global_account[name]
	except KeyError:
		return defValue

def reset_state():
	keys = list(_global_account.keys())
	for key in keys:
		if not key == 'login_state':
			del(_global_account[key])
	_global_account['login_state'] = False