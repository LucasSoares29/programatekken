# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RodadaTekkenResultadosAnteriores.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from LutaDAO import *

class Ui_FormRodadasFinalizadas(object):

    def __init__(self):
        arquivo = open("id.txt", "r")
        self.id = arquivo.readline().strip("\n")
        arquivo.close()
        self.rodadaMax = LutaDAO().totalDeRodadas(self.id)
        #print(self.rodadaMax)

    def gerarAviso(self, icone, titulo, msg):
        erro = QtWidgets.QMessageBox()
        erro.setWindowTitle(titulo)
        erro.setIcon(icone) # 0 - sem ícone, 1 - Informação, 2 - Cuidado, 3 - Erro crítico
        erro.setText(msg)
        erro.exec_()

    def mostrarTudo(self):
        if self.checkBox.isChecked():
            self.spinBox_Inicial.setValue(1)
            self.spinBox_Final.setValue(self.rodadaMax)

    def buscar(self):
        if self.tabela.rowCount() > 0:
            self.tabela.setRowCount(0)

        if int(self.spinBox_Inicial.text()) <= int(self.spinBox_Final.text()):
            self.botaoExportar.setEnabled(True)

            if self.checkBox2.isChecked():
                tabelaLutas = LutaDAO().carregarLutasRealizadasJogador(self.id, self.spinBox_Inicial.text(), self.spinBox_Final.text(), self.caixaDeTexto.text())
            else:
                tabelaLutas = LutaDAO().carregarLutasRealizadas(self.id, self.spinBox_Inicial.text(), self.spinBox_Final.text())
            if len(tabelaLutas) == 0:
                self.gerarAviso(2, "Atenção", "Nenhuma luta foi realizada neste campeonato")
                self.botaoExportar.setEnabled(False)

            self.tabela.setRowCount(len(tabelaLutas))
            linha = 0
            for luta in tabelaLutas:
                for coluna in range(0, 5):
                    item = QtWidgets.QTableWidgetItem(str(luta[coluna]))
                    if coluna == 2 or coluna == 3:
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tabela.setItem(linha, coluna, item)
                linha += 1

            self.tabela.resizeColumnToContents(0)
            self.tabela.setColumnWidth(1, 350)
            self.tabela.resizeColumnToContents(2)
            self.tabela.resizeColumnToContents(3)
        else:
            self.gerarAviso(3, "Erro", "Valores inválidos. O valor da rodada inicial é maior do que rodada final")
            diferença = int(self.spinBox_Inicial.text()) - int(self.spinBox_Final.text())
            self.spinBox_Inicial.setValue(int(self.spinBox_Final.text()) - diferença)


    def exportar(self):
        tabelaLutas = LutaDAO().carregarLutasRealizadas(self.id, self.spinBox_Inicial.text(),
                                                                 self.spinBox_Final.text())

        arquivoTexto = open("Rodadas Finalizadas.txt", "w")
        rodada = int(self.spinBox_Inicial.text())
        linha = "Rodada " + str(rodada) + "\n"
        arquivoTexto.write(linha)
        for luta in tabelaLutas:
            if int(luta[0]) != int(rodada):
                rodada += 1
                linha = "\nRodada " + str(rodada) + "\n"
                arquivoTexto.write(linha)
            linha = luta[1] + ' ' + luta[2] + ' vs ' + luta[3] + ' ' + luta[4] + "\n"
            arquivoTexto.write(linha)
        arquivoTexto.close()
        self.gerarAviso(2, "Atenção", "Arquivo 'Rodadas Finalizadas.txt' foi gerado com sucesso.")


    def habilitarCampoTexto(self):
        if self.checkBox2.isChecked():
            self.caixaDeTexto.setEnabled(True)
        else:
            self.caixaDeTexto.setEnabled(False)

    def setupUi(self, FormRodadasFinalizadas):
        FormRodadasFinalizadas.setObjectName("FormRodadasFinalizadas")
        FormRodadasFinalizadas.resize(985, 750)
        self.frame = QtWidgets.QFrame(FormRodadasFinalizadas)
        self.frame.setGeometry(QtCore.QRect(10, 10, 961, 720))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.tabela = QtWidgets.QTableWidget(self.frame)
        self.tabela.setGeometry(QtCore.QRect(10, 280, 931, 391))
        self.tabela.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tabela.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tabela.setObjectName("tabela")
        self.tabela.setColumnCount(5)
        self.tabela.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tabela.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabela.setHorizontalHeaderItem(4, item)
        self.tabela.horizontalHeader().setStretchLastSection(True)
        self.tabela.verticalHeader().setVisible(False)

        self.tabela.setColumnWidth(0, 100)
        self.tabela.setColumnWidth(1, 250)
        self.tabela.setColumnWidth(2, 150)
        self.tabela.setColumnWidth(3, 150)


        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(360, 20, 180, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.spinBox_Inicial = QtWidgets.QSpinBox(self.frame)
        self.spinBox_Inicial.setGeometry(QtCore.QRect(550, 20, 42, 22))
        self.spinBox_Inicial.setMinimum(1)
        self.spinBox_Inicial.setObjectName("spinBox_Inicial")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(360, 60, 180, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.spinBox_Final = QtWidgets.QSpinBox(self.frame)
        self.spinBox_Final.setGeometry(QtCore.QRect(550, 60, 42, 22))
        self.spinBox_Final.setMinimum(1)
        self.spinBox_Final.setObjectName("spinBox_Inicial_2")

        self.checkBox = QtWidgets.QCheckBox(self.frame)
        self.checkBox.setGeometry(QtCore.QRect(360, 100, 234, 27))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.clicked.connect(self.mostrarTudo)

        self.botaoBuscar = QtWidgets.QPushButton(self.frame)
        self.botaoBuscar.setGeometry(QtCore.QRect(400, 240, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.botaoBuscar.setFont(font)
        self.botaoBuscar.setObjectName("botaoBuscar")
        self.botaoBuscar.clicked.connect(self.buscar)

        self.checkBox2 = QtWidgets.QCheckBox(self.frame)
        self.checkBox2.setGeometry(QtCore.QRect(360, 140, 234, 27))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox2.setFont(font)
        self.checkBox2.setObjectName("checkBox2")
        self.checkBox2.clicked.connect(self.habilitarCampoTexto)

        self.caixaDeTexto = QtWidgets.QLineEdit(self.frame)
        self.caixaDeTexto.setGeometry(QtCore.QRect(360, 180, 400, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.caixaDeTexto.setFont(font)
        self.caixaDeTexto.setObjectName("caixaDeTexto")
        self.caixaDeTexto.setText("Insira o nome do jogador")
        self.caixaDeTexto.setEnabled(False)

        self.botaoExportar = QtWidgets.QPushButton(self.frame)
        self.botaoExportar.setGeometry(QtCore.QRect(410, 680, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.botaoExportar.setFont(font)
        self.botaoExportar.setObjectName("botaoExportar")
        self.botaoExportar.setEnabled(False)
        self.botaoExportar.clicked.connect(self.exportar)

        self.spinBox_Inicial.setMaximum(self.rodadaMax)
        self.spinBox_Final.setMaximum(self.rodadaMax)

        self.retranslateUi(FormRodadasFinalizadas)
        QtCore.QMetaObject.connectSlotsByName(FormRodadasFinalizadas)

    def retranslateUi(self, FormRodadasFinalizadas):
        _translate = QtCore.QCoreApplication.translate
        FormRodadasFinalizadas.setWindowTitle(_translate("FormRodadasFinalizadas", "Consultar Resultados Anteriores"))
        item = self.tabela.horizontalHeaderItem(0)
        item.setText(_translate("FormRodadasFinalizadas", "Rodada"))
        item = self.tabela.horizontalHeaderItem(1)
        item.setText(_translate("FormRodadasFinalizadas", "Jogador 1"))
        item = self.tabela.horizontalHeaderItem(2)
        item.setText(_translate("FormRodadasFinalizadas", "Resultado"))
        item = self.tabela.horizontalHeaderItem(3)
        item.setText(_translate("FormRodadasFinalizadas", "Resultado"))
        item = self.tabela.horizontalHeaderItem(4)
        item.setText(_translate("FormRodadasFinalizadas", "Jogador 2"))
        self.label.setText(_translate("FormRodadasFinalizadas", "Insira a rodada inicial"))
        self.label_2.setText(_translate("FormRodadasFinalizadas", "Insira a rodada final"))
        self.checkBox.setText(_translate("FormRodadasFinalizadas", "Mostrar todas as rodadas"))
        self.checkBox2.setText(_translate("FormRodadasFinalizadas", "Filtrar por jogador"))
        self.botaoBuscar.setText(_translate("FormRodadasFinalizadas", "Buscar"))
        self.botaoExportar.setText(_translate("FormRodadasFinalizadas", "Exportar"))


