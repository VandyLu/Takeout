# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainpage.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainPage(object):
    def setupUi(self, MainPage):
        MainPage.setObjectName("MainPage")
        MainPage.resize(800, 600)
        MainPage.setMinimumSize(QtCore.QSize(800, 600))
        MainPage.setMaximumSize(QtCore.QSize(800, 600))
        self.tabWidget = QtWidgets.QTabWidget(MainPage)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.tabWidget.setMinimumSize(QtCore.QSize(800, 600))
        self.tabWidget.setMaximumSize(QtCore.QSize(800, 600))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.listWidget_rest = QtWidgets.QListWidget(self.tab_1)
        self.listWidget_rest.setGeometry(QtCore.QRect(30, 20, 151, 381))
        self.listWidget_rest.setObjectName("listWidget_rest")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tab_1)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(400, 510, 361, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_12 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout.addWidget(self.label_12)
        self.total = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.total.setObjectName("total")
        self.horizontalLayout.addWidget(self.total)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.placeOrder = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.placeOrder.setObjectName("placeOrder")
        self.horizontalLayout.addWidget(self.placeOrder)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.frame = QtWidgets.QFrame(self.tab_1)
        self.frame.setGeometry(QtCore.QRect(400, 20, 361, 481))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 440, 361, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.checkBox = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.spinBox = QtWidgets.QSpinBox(self.horizontalLayoutWidget_2)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_2.addWidget(self.spinBox)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(0, 390, 361, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.price = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.price.setObjectName("price")
        self.horizontalLayout_3.addWidget(self.price)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_3.addWidget(self.label_10)
        self.score = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.score.setObjectName("score")
        self.horizontalLayout_3.addWidget(self.score)
        self.graphicsView = QtWidgets.QGraphicsView(self.frame)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 361, 381))
        self.graphicsView.setObjectName("graphicsView")
        self.listWidget_course = QtWidgets.QListWidget(self.tab_1)
        self.listWidget_course.setGeometry(QtCore.QRect(210, 20, 161, 381))
        self.listWidget_course.setObjectName("listWidget_course")
        self.shoppingCart = QtWidgets.QListWidget(self.tab_1)
        self.shoppingCart.setGeometry(QtCore.QRect(30, 430, 341, 121))
        self.shoppingCart.setObjectName("shoppingCart")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.doubleSpinBox_rider = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_rider.setGeometry(QtCore.QRect(630, 490, 141, 20))
        self.doubleSpinBox_rider.setObjectName("doubleSpinBox_rider")
        self.commentTxt = QtWidgets.QTextEdit(self.tab_2)
        self.commentTxt.setGeometry(QtCore.QRect(30, 420, 571, 131))
        self.commentTxt.setObjectName("commentTxt")
        self.doubleSpinBox_rest = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_rest.setGeometry(QtCore.QRect(630, 440, 141, 21))
        self.doubleSpinBox_rest.setObjectName("doubleSpinBox_rest")
        self.tableWidget_orders = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_orders.setGeometry(QtCore.QRect(30, 20, 741, 381))
        self.tableWidget_orders.setObjectName("tableWidget_orders")
        self.tableWidget_orders.setColumnCount(0)
        self.tableWidget_orders.setRowCount(0)
        self.commit_comment = QtWidgets.QPushButton(self.tab_2)
        self.commit_comment.setGeometry(QtCore.QRect(630, 520, 141, 31))
        self.commit_comment.setObjectName("commit_comment")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(630, 470, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(630, 420, 111, 16))
        self.label_2.setObjectName("label_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.axWidget = QAxContainer.QAxWidget(self.tab_4)
        self.axWidget.setProperty("geometry", QtCore.QRect(10, 10, 771, 501))
        self.axWidget.setObjectName("axWidget")
        self.horizontalLayoutWidget_8 = QtWidgets.QWidget(self.tab_4)
        self.horizontalLayoutWidget_8.setGeometry(QtCore.QRect(10, 520, 771, 41))
        self.horizontalLayoutWidget_8.setObjectName("horizontalLayoutWidget_8")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_8)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.deliver_state = QtWidgets.QLabel(self.horizontalLayoutWidget_8)
        self.deliver_state.setObjectName("deliver_state")
        self.horizontalLayout_10.addWidget(self.deliver_state)
        self.label_deliverState = QtWidgets.QLabel(self.horizontalLayoutWidget_8)
        self.label_deliverState.setText("")
        self.label_deliverState.setObjectName("label_deliverState")
        self.horizontalLayout_10.addWidget(self.label_deliverState)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem8)
        self.pushButton_confirmReceipt = QtWidgets.QPushButton(self.horizontalLayoutWidget_8)
        self.pushButton_confirmReceipt.setObjectName("pushButton_confirmReceipt")
        self.horizontalLayout_10.addWidget(self.pushButton_confirmReceipt)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem9)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.formLayoutWidget = QtWidgets.QWidget(self.tab_5)
        self.formLayoutWidget.setGeometry(QtCore.QRect(50, 20, 691, 96))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.userID = QtWidgets.QLabel(self.formLayoutWidget)
        self.userID.setText("")
        self.userID.setObjectName("userID")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.userID)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.FieldRole, spacerItem10)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_userName = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_userName.setObjectName("lineEdit_userName")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_userName)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(4, QtWidgets.QFormLayout.FieldRole, spacerItem11)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_userTel = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_userTel.setObjectName("lineEdit_userTel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_userTel)
        self.tableWidget_Loc = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget_Loc.setGeometry(QtCore.QRect(50, 130, 691, 191))
        self.tableWidget_Loc.setObjectName("tableWidget_Loc")
        self.tableWidget_Loc.setColumnCount(0)
        self.tableWidget_Loc.setRowCount(0)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.tab_5)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(50, 330, 691, 41))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem12)
        self.addAddress = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        self.addAddress.setObjectName("addAddress")
        self.horizontalLayout_5.addWidget(self.addAddress)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem13)
        self.deleteAddress = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        self.deleteAddress.setObjectName("deleteAddress")
        self.horizontalLayout_5.addWidget(self.deleteAddress)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem14)
        self.modifyAddress = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        self.modifyAddress.setObjectName("modifyAddress")
        self.horizontalLayout_5.addWidget(self.modifyAddress)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem15)
        self.Address = QtWidgets.QTextEdit(self.tab_5)
        self.Address.setGeometry(QtCore.QRect(50, 380, 481, 111))
        self.Address.setObjectName("Address")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.tab_5)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(550, 380, 191, 111))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_11 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.lineEdit_longitude = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_longitude.setObjectName("lineEdit_longitude")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_longitude)
        self.lineEdit_latitude = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_latitude.setObjectName("lineEdit_latitude")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_latitude)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(2, QtWidgets.QFormLayout.LabelRole, spacerItem16)
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(0, QtWidgets.QFormLayout.LabelRole, spacerItem17)
        spacerItem18 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(4, QtWidgets.QFormLayout.LabelRole, spacerItem18)
        self.horizontalLayoutWidget_9 = QtWidgets.QWidget(self.tab_5)
        self.horizontalLayoutWidget_9.setGeometry(QtCore.QRect(50, 510, 691, 41))
        self.horizontalLayoutWidget_9.setObjectName("horizontalLayoutWidget_9")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_9)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem19)
        self.saveChange = QtWidgets.QPushButton(self.horizontalLayoutWidget_9)
        self.saveChange.setObjectName("saveChange")
        self.horizontalLayout_9.addWidget(self.saveChange)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem20)
        self.abandonChange = QtWidgets.QPushButton(self.horizontalLayoutWidget_9)
        self.abandonChange.setObjectName("abandonChange")
        self.horizontalLayout_9.addWidget(self.abandonChange)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem21)
        self.tabWidget.addTab(self.tab_5, "")

        self.retranslateUi(MainPage)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainPage)

    def retranslateUi(self, MainPage):
        _translate = QtCore.QCoreApplication.translate
        MainPage.setWindowTitle(_translate("MainPage", "Dialog"))
        self.label_12.setText(_translate("MainPage", "Total:"))
        self.total.setText(_translate("MainPage", "$"))
        self.placeOrder.setText(_translate("MainPage", "place order"))
        self.checkBox.setText(_translate("MainPage", "select"))
        self.label_3.setText(_translate("MainPage", "price per unit:"))
        self.price.setText(_translate("MainPage", "$"))
        self.label_10.setText(_translate("MainPage", "score:"))
        self.score.setText(_translate("MainPage", "/5"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainPage", "Food and Delights"))
        self.commit_comment.setText(_translate("MainPage", "comment"))
        self.label.setText(_translate("MainPage", "rider:"))
        self.label_2.setText(_translate("MainPage", "restaurant:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainPage", "history orders and add comments"))
        self.deliver_state.setText(_translate("MainPage", "deliver state:"))
        self.pushButton_confirmReceipt.setText(_translate("MainPage", "confirm receipt"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainPage", "deliver state"))
        self.label_5.setText(_translate("MainPage", "user id:       "))
        self.label_4.setText(_translate("MainPage", "user name:    "))
        self.label_6.setText(_translate("MainPage", "user Tel:"))
        self.addAddress.setText(_translate("MainPage", "add"))
        self.deleteAddress.setText(_translate("MainPage", "delete"))
        self.modifyAddress.setText(_translate("MainPage", "modify"))
        self.label_7.setText(_translate("MainPage", "longitude:"))
        self.label_11.setText(_translate("MainPage", "latitude:"))
        self.saveChange.setText(_translate("MainPage", "save change"))
        self.abandonChange.setText(_translate("MainPage", "abandon change"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainPage", "personal information edit"))

from PyQt5 import QAxContainer
