# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demoTest3.ui'
#
# Created: Wed Dec 19 11:08:09 2018
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(780, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonAddVaga = QtWidgets.QPushButton(self.tab)
        self.pushButtonAddVaga.setObjectName(_fromUtf8("pushButtonAddVaga"))
        self.gridLayout.addWidget(self.pushButtonAddVaga, 2, 4, 1, 1)
        self.pushButtonRmVaga = QtWidgets.QPushButton(self.tab)
        self.pushButtonRmVaga.setObjectName(_fromUtf8("pushButtonRmVaga"))
        self.gridLayout.addWidget(self.pushButtonRmVaga, 3, 4, 1, 1)
        self.pushButtonRstVaga = QtWidgets.QPushButton(self.tab)
        self.pushButtonRstVaga.setObjectName(_fromUtf8("pushButtonRstVaga"))
        self.gridLayout.addWidget(self.pushButtonRstVaga, 4, 4, 1, 1)
        self.labelEstadoVagas = QtWidgets.QLabel(self.tab)
        self.labelEstadoVagas.setObjectName(_fromUtf8("labelEstadoVagas"))
        self.gridLayout.addWidget(self.labelEstadoVagas, 0, 4, 1, 1)
        self.listWidgetEstadoVagas = QtWidgets.QListWidget(self.tab)
        self.listWidgetEstadoVagas.setObjectName(_fromUtf8("listWidgetEstadoVagas"))
        self.gridLayout.addWidget(self.listWidgetEstadoVagas, 1, 4, 1, 1)
        self.pushButtonSaveVaga = QtWidgets.QPushButton(self.tab)
        self.pushButtonSaveVaga.setObjectName(_fromUtf8("pushButtonSaveVaga"))
        self.gridLayout.addWidget(self.pushButtonSaveVaga, 5, 4, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.labelImage = QtWidgets.QLabel(self.tab)
        self.labelImage.setText(_fromUtf8(""))
        self.labelImage.setObjectName(_fromUtf8("labelImage"))
        self.horizontalLayout_5.addWidget(self.labelImage)
        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 3, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 780, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuArquivo = QtWidgets.QMenu(self.menubar)
        self.menuArquivo.setObjectName(_fromUtf8("menuArquivo"))
        self.menuAjuda = QtWidgets.QMenu(self.menubar)
        self.menuAjuda.setObjectName(_fromUtf8("menuAjuda"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSalvar_Vagas = QtWidgets.QAction(MainWindow)
        self.actionSalvar_Vagas.setObjectName(_fromUtf8("actionSalvar_Vagas"))
        self.actionAbrir_Camera = QtWidgets.QAction(MainWindow)
        self.actionAbrir_Camera.setObjectName(_fromUtf8("actionAbrir_Camera"))
        self.menuArquivo.addAction(self.actionSalvar_Vagas)
        self.menuArquivo.addAction(self.actionAbrir_Camera)
        self.menubar.addAction(self.menuArquivo.menuAction())
        self.menubar.addAction(self.menuAjuda.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButtonAddVaga.setText(_translate("MainWindow", "Adicionar vaga", None))
        self.pushButtonRmVaga.setText(_translate("MainWindow", "Remover Vaga", None))
        self.pushButtonRstVaga.setText(_translate("MainWindow", "Resetar Vagas", None))
        self.labelEstadoVagas.setText(_translate("MainWindow", "Estado das Vagas", None))
        self.pushButtonSaveVaga.setText(_translate("MainWindow", "Salvar Vagas", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Câmera 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Câmera 2", None))
        self.menuArquivo.setTitle(_translate("MainWindow", "Arquivo", None))
        self.menuAjuda.setTitle(_translate("MainWindow", "Ajuda", None))
        self.actionSalvar_Vagas.setText(_translate("MainWindow", "Salvar Vagas", None))
        self.actionAbrir_Camera.setText(_translate("MainWindow", "Abrir Câmera", None))

