# Form implementation generated from reading ui file 'D:\Sophomores (2nd semester)\Programming Techniques\matrix-operations\Bonus\MainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(772, 250)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonbrowser = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonbrowser.setGeometry(QtCore.QRect(650, 31, 111, 41))
        self.pushButtonbrowser.setStyleSheet("")
        self.pushButtonbrowser.setObjectName("pushButtonbrowser")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(150, 30, 491, 41))
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButtonopen = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonopen.setGeometry(QtCore.QRect(200, 90, 171, 51))
        self.pushButtonopen.setStyleSheet("")
        self.pushButtonopen.setObjectName("pushButtonopen")
        self.pushButtonsave = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButtonsave.setGeometry(QtCore.QRect(410, 90, 161, 51))
        self.pushButtonsave.setStyleSheet("")
        self.pushButtonsave.setObjectName("pushButtonsave")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 111, 31))
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 772, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MyHoa_K234111389"))
        self.pushButtonbrowser.setText(_translate("MainWindow", "browser"))
        self.pushButtonopen.setText(_translate("MainWindow", "Open Chart in Browser"))
        self.pushButtonsave.setText(_translate("MainWindow", "Save Chart to HTML File"))
        self.label.setText(_translate("MainWindow", "Choose File:"))
