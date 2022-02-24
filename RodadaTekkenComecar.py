# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RodadaTekkenComecar.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import random

class Ui_Form(object):

    def alterarTexto(self, Form):
        x = random.randint(0, 100)
        fotoLucas = QtGui.QPixmap("rodadatekkencomecar_lucas.jpg")
        fotoRenan = QtGui.QPixmap("rodadatekkencomecar_renan.jpg")
        if x % 2 == 0:
            self.label.setPixmap(fotoLucas.scaled(941, 542, QtCore.Qt.KeepAspectRatioByExpanding))
            Form.setWindowTitle("Quem começa a luta? Lucas")
        else:
            self.label.setPixmap(fotoRenan.scaled(941, 542, QtCore.Qt.KeepAspectRatioByExpanding))
            Form.setWindowTitle("Quem começa a luta? Renan")

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(961, 560)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(10, 10, 941, 651))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 941, 542))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        self.alterarTexto(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Quem começa a luta"))
        self.label.setText(_translate("Form", "Foto"))

