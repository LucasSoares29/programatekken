# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TekkenNovoCampeonato.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
from Campeonato import *
from Jogador import *
from CampeonatoDAO import *
from JogadorDAO import *
from LutaDAO import *

class Ui_CadastrarCampeonato(object):

    @staticmethod
    def gerarAviso(icone, titulo, msg):
        erro = QtWidgets.QMessageBox()
        erro.setWindowTitle(titulo)
        erro.setIcon(icone) # 0 - sem ícone, 1 - Informação, 2 - Cuidado, 3 - Erro crítico
        erro.setText(msg)
        erro.exec_()

    #OK
    def carregarJogadoresCadastrados(self):
        if self.listWidget_2.count() > 0:
            for i in range(self.listWidget_2.count()):
                self.listWidget_2.takeItem(0)

        jogadoresCadastrados = jogadorDAO().listaDeJogadores()

        for cadajogador in jogadoresCadastrados:
            item = QtWidgets.QListWidgetItem(cadajogador)
            self.listWidget_2.addItem(item)

    #OK
    def incluir(self):
        nome = self.campoNome_2.text()
        nacionalidade = self.campoNacionalidade.text()
        texto = nome + ' (' + nacionalidade + ')'

        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.text() == texto:
                self.gerarAviso(2, titulo="Atenção", msg="Este jogador já foi incluido")
                return

        for i in range(self.listWidget_2.count()):
            item = self.listWidget_2.item(i)
            if item.text() == texto:
                self.gerarAviso(2, titulo="Atenção", msg="Este jogador já está cadastrado no banco")
                return

        item = QtWidgets.QListWidgetItem(texto);
        self.listWidget.addItem(item)

    #OK
    def removerSelecionado(self):
        itemSelecionado = self.listWidget.currentItem()

        if itemSelecionado is None:
            self.gerarAviso(2, titulo="Atenção", msg="Não há jogador selecionado. Por favor, escolha um jogador ao clicar com o botão esquerdo do mouse no seu nome listado a esquerda")
            return

        # verificando se o jogador não está no banco. Se estiver no banco, coloco ele na listagem de jogadores cadastrados
        textoDoItem = itemSelecionado.text()
        nacionalidade = self.extrairNacionalidadeDoTexto(textoDoItem)
        nome = textoDoItem.rsplit(' (' + nacionalidade + ')')
        if int(jogadorDAO().recuperarID(nome[0])) > 0:
            self.listWidget_2.addItem(QtWidgets.QListWidgetItem(textoDoItem))
        index = self.listWidget.row(itemSelecionado)
        self.listWidget.takeItem(index)

    #OK
    def removerTodos(self):
        qtdItens = self.listWidget.count()
        for i in range(qtdItens):
            self.listWidget.takeItem(0)
        self.carregarJogadoresCadastrados()

    #OK
    def apagarTudo(self):
        self.campoNome.setText('')
        self.campoNome_2.setText('')
        self.spinBox.setProperty("value", 2)
        self.calendarWidget.setSelectedDate(QtCore.QDate(datetime.now().year, datetime.now().month, datetime.now().day)) #o calendarWidget retorna QDate
        self.campoPerfect.setText('')
        self.campoGreat.setText('')
        self.campoVitoria.setText('')
        self.campoEmpate.setText('')
        self.campoDerrota.setText('')
        self.campoDoubleKO.setText('')
        self.campoRoundGanho.setText('')
        self.campoTimeOut.setText('')
        self.campoRndMenos.setText('')
        self.campoPerfectTomado.setText('')
        self.campoGreatTomado.setText('')
        self.removerTodos()
        self.progressBar.setValue(0)
        self.campoStatus.setPlainText('')

    #OK
    def extrairNacionalidadeDoTexto(self, string, inicio='(', fim=')'):
        return string[string.index(inicio)+1:string.index(fim)]

    # OK
    def incluirJogadorCadastrado(self):
        qtdItens = self.listWidget_2.count()
        if qtdItens == 0:
            self.gerarAviso(2, titulo="Atenção", msg="Não há jogadores para excluir. Insira um jogador na lista da esquerda ao clicar com o botão esquerdo do mouse")
            return
        itemSelecionado = self.listWidget_2.currentItem()
        if itemSelecionado is None:
            self.gerarAviso(2, titulo="Atenção", msg="Não há jogador selecionado. Por favor, escolha um jogador na lista da direita ao clicar com o botão esquerdo do mouse no seu nome antes de excluir")
            return
        index = self.listWidget_2.row(itemSelecionado)
        self.listWidget_2.takeItem(index)
        self.listWidget.addItem(itemSelecionado)

    # OK
    def iniciarCampeonato(self):
        if self.listWidget.count() == 0:
            self.gerarAviso(3, "Atenção", "Não há jogadores cadastrados no campeonato")
            return

        nomeTorneio = self.campoNome.text()
        qtdRounds = self.spinBox.text()
        dataInicio = str(self.calendarWidget.selectedDate().day()) + '/' + str(self.calendarWidget.selectedDate().month()) + '/' + str(self.calendarWidget.selectedDate().year())
        pontVit = self.campoVitoria.text()
        pontEmp = self.campoEmpate.text()
        pontDer = self.campoDerrota.text()
        pontPerf = self.campoPerfect.text()
        pontGreat = self.campoGreat.text()
        pontDoubleKO = self.campoDoubleKO.text()
        pontRndG = self.campoRoundGanho.text()
        pontTO = self.campoTimeOut.text()
        pontRndP = self.campoRndMenos.text()
        pontPerfC = self.campoPerfectTomado.text()
        pontGreatC = self.campoGreatTomado.text()

        cdao = CampeonatoDAO()
        ldao = LutaDAO()

        novoCampeonato = Campeonato(nomeTorneio, dataInicio, qtdRounds, pontVit, pontEmp, pontDer, pontPerf, pontGreat, pontDoubleKO, pontRndG, pontTO, pontRndP, pontPerfC, pontGreatC)




        cdao.cadastrarCampeonato(novoCampeonato)
        index = 0

        plainText = "Campeonato " + nomeTorneio + " cadastrado com sucesso\n"
        self.campoStatus.insertPlainText(plainText)
        self.progressBar.setValue(25)

        porcentagem = 25 / self.listWidget.count();



        #adicionando jogadores
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            textoDoItem = item.text()
            nacionalidade = self.extrairNacionalidadeDoTexto(textoDoItem)
            nome = textoDoItem.rsplit(' (' + nacionalidade + ')')
            jogador = Jogador(nome[0], nacionalidade)
            if jogadorDAO().recuperarID(nome[0]) == 0:
                jogadorDAO().cadastrarJogador(jogador) # OK
            cdao.cadastrarNovoJogador(novoCampeonato, jogador) #inserir pontuação inicial na tabela OK
            plainText = str(nome[0]) + " cadastrado no campeonato com sucesso\n"
            self.campoStatus.appendPlainText(plainText)
            if index == 0:
                progresso = 25 + porcentagem
            else:
                progresso = progresso + porcentagem
            self.progressBar.setValue(progresso)


        #gerando as rodadas

        idjogadores = cdao.recuperarIDJogadoresNoCampeonato(novoCampeonato)
        rodadas = novoCampeonato.gerarRodadas(idjogadores)
        idCampeonato = cdao.recuperarID(novoCampeonato.nome)
        for lutas in rodadas:
            ldao.inserirLuta(idCampeonato, lutas)  # OK COM NUMERO PAR E IMPAR DE JOGADORES.
        cdao = CampeonatoDAO()
        plainText = "Rodadas geradas com sucesso\n"
        self.campoStatus.appendPlainText(plainText)
        progresso += 25
        self.progressBar.setValue(progresso)

        #imprimindo txt com as rodadas
        plainText = "Imprimindo lutas do campeonato...\n"
        self.campoStatus.appendPlainText(plainText)
        cdao.imprimirRodadas(idCampeonato)
        input = open("outputRodadas.txt", "r")
        while True:
            linha = input.readline().strip("\n")
            if linha == "FIM DO ARQUIVO":
                break
            self.campoStatus.appendPlainText(linha)
        input.close()
        progresso = 100
        self.progressBar.setValue(progresso)

        self.gerarAviso(1, "Tekken Novo Campeonato", "Novo campeonato foi criado com sucesso")


        self.apagarTudo()
        self.carregarJogadoresCadastrados()


    def setupUi(self, CadastrarCampeonato):
        CadastrarCampeonato.setObjectName("CadastrarCampeonato")
        CadastrarCampeonato.setWindowModality(QtCore.Qt.ApplicationModal)
        CadastrarCampeonato.resize(1280, 720)
        CadastrarCampeonato.setSizeIncrement(QtCore.QSize(0, 0))
        CadastrarCampeonato.setBaseSize(QtCore.QSize(1280, 720))
        self.centralwidget = QtWidgets.QWidget(CadastrarCampeonato)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 1261, 701))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(30, 30, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.campoNome = QtWidgets.QLineEdit(self.frame)
        self.campoNome.setGeometry(QtCore.QRect(100, 26, 381, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoNome.setFont(font)
        self.campoNome.setObjectName("campoNome")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(29, 76, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.spinBox = QtWidgets.QSpinBox(self.frame)
        self.spinBox.setGeometry(QtCore.QRect(270, 80, 42, 26))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox.setFont(font)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(5)
        self.spinBox.setProperty("value", 2)
        self.spinBox.setObjectName("spinBox")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.frame)
        self.calendarWidget.setGeometry(QtCore.QRect(30, 170, 312, 183))
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.SingleLetterDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setDateEditAcceptDelay(1500)
        self.calendarWidget.setObjectName("calendarWidget")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(520, 20, 661, 441))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(20, 50, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.campoNome_2 = QtWidgets.QLineEdit(self.frame_2)
        self.campoNome_2.setGeometry(QtCore.QRect(90, 46, 461, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoNome_2.setFont(font)
        self.campoNome_2.setObjectName("campoNome_2")
        self.campoNacionalidade = QtWidgets.QLineEdit(self.frame_2)
        self.campoNacionalidade.setGeometry(QtCore.QRect(170, 86, 381, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoNacionalidade.setFont(font)
        self.campoNacionalidade.setObjectName("campoNacionalidade")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(20, 90, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.listWidget = QtWidgets.QListWidget(self.frame_2)
        self.listWidget.setGeometry(QtCore.QRect(20, 210, 271, 131))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setObjectName("listWidget")

        self.listWidget_2 = QtWidgets.QListWidget(self.frame_2)
        self.listWidget_2.setGeometry(QtCore.QRect(320, 210, 271, 131))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.listWidget.setFont(font)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setObjectName("listWidget_2")

        self.botaoIncluir = QtWidgets.QPushButton(self.frame_2)
        self.botaoIncluir.setGeometry(QtCore.QRect(20, 130, 351, 31))
        self.botaoIncluir.clicked.connect(self.incluir)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.botaoIncluir.setFont(font)
        self.botaoIncluir.setObjectName("botaoIncluir")

        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(20, 170, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.label_20 = QtWidgets.QLabel(self.frame_2)
        self.label_20.setGeometry(QtCore.QRect(330, 170, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")

        self.botaoRemoverSelecionado = QtWidgets.QPushButton(self.frame_2)
        self.botaoRemoverSelecionado.setGeometry(QtCore.QRect(20, 350, 231, 31))
        self.botaoRemoverSelecionado.clicked.connect(self.removerSelecionado)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.botaoRemoverSelecionado.setFont(font)
        self.botaoRemoverSelecionado.setObjectName("botaoRemoverSelecionado")

        self.botaoIncluirJogadorCadastrado = QtWidgets.QPushButton(self.frame_2)
        self.botaoIncluirJogadorCadastrado.setGeometry(QtCore.QRect(340, 350, 231, 31))
        self.botaoIncluirJogadorCadastrado.clicked.connect(self.incluirJogadorCadastrado)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.botaoIncluirJogadorCadastrado.setFont(font)
        self.botaoIncluirJogadorCadastrado.setObjectName("botaoIncluirJogadorCadastrado")


        self.botaoRemoverTodos = QtWidgets.QPushButton(self.frame_2)
        self.botaoRemoverTodos.setGeometry(QtCore.QRect(20, 390, 231, 31))
        self.botaoRemoverTodos.clicked.connect(self.removerTodos)

        font = QtGui.QFont()
        font.setPointSize(16)

        self.botaoRemoverTodos.setFont(font)
        self.botaoRemoverTodos.setObjectName("botaoRemoverTodos")

        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(30, 370, 471, 321))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_3.setObjectName("frame_3")
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(20, 10, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setGeometry(QtCore.QRect(20, 50, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.campoVitoria = QtWidgets.QLineEdit(self.frame_3)
        self.campoVitoria.setGeometry(QtCore.QRect(110, 46, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoVitoria.setFont(font)
        self.campoVitoria.setText("")
        self.campoVitoria.setMaxLength(4)
        self.campoVitoria.setObjectName("campoVitoria")
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setGeometry(QtCore.QRect(20, 82, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.campoEmpate = QtWidgets.QLineEdit(self.frame_3)
        self.campoEmpate.setGeometry(QtCore.QRect(110, 83, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoEmpate.setFont(font)
        self.campoEmpate.setText("")
        self.campoEmpate.setMaxLength(4)
        self.campoEmpate.setObjectName("campoEmpate")
        self.campoDerrota = QtWidgets.QLineEdit(self.frame_3)
        self.campoDerrota.setGeometry(QtCore.QRect(110, 120, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoDerrota.setFont(font)
        self.campoDerrota.setText("")
        self.campoDerrota.setMaxLength(4)
        self.campoDerrota.setObjectName("campoDerrota")
        self.label_11 = QtWidgets.QLabel(self.frame_3)
        self.label_11.setGeometry(QtCore.QRect(20, 120, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.frame_3)
        self.label_12.setGeometry(QtCore.QRect(20, 154, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.campoPerfect = QtWidgets.QLineEdit(self.frame_3)
        self.campoPerfect.setGeometry(QtCore.QRect(110, 156, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoPerfect.setFont(font)
        self.campoPerfect.setText("")
        self.campoPerfect.setMaxLength(4)
        self.campoPerfect.setObjectName("campoPerfect")
        self.campoGreat = QtWidgets.QLineEdit(self.frame_3)
        self.campoGreat.setGeometry(QtCore.QRect(110, 192, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoGreat.setFont(font)
        self.campoGreat.setText("")
        self.campoGreat.setMaxLength(4)
        self.campoGreat.setObjectName("campoGreat")
        self.label_13 = QtWidgets.QLabel(self.frame_3)
        self.label_13.setGeometry(QtCore.QRect(20, 190, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.frame_3)
        self.label_14.setGeometry(QtCore.QRect(10, 260, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.campoDoubleKO = QtWidgets.QLineEdit(self.frame_3)
        self.campoDoubleKO.setGeometry(QtCore.QRect(110, 226, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoDoubleKO.setFont(font)
        self.campoDoubleKO.setText("")
        self.campoDoubleKO.setMaxLength(4)
        self.campoDoubleKO.setObjectName("campoDoubleKO")
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        self.label_15.setGeometry(QtCore.QRect(20, 226, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.campoRoundGanho = QtWidgets.QLineEdit(self.frame_3)
        self.campoRoundGanho.setGeometry(QtCore.QRect(110, 262, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoRoundGanho.setFont(font)
        self.campoRoundGanho.setText("")
        self.campoRoundGanho.setMaxLength(4)
        self.campoRoundGanho.setObjectName("campoRoundGanho")
        self.campoTimeOut = QtWidgets.QLineEdit(self.frame_3)
        self.campoTimeOut.setGeometry(QtCore.QRect(350, 46, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoTimeOut.setFont(font)
        self.campoTimeOut.setText("")
        self.campoTimeOut.setMaxLength(4)
        self.campoTimeOut.setObjectName("campoTimeOut")
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        self.label_16.setGeometry(QtCore.QRect(250, 44, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.frame_3)
        self.label_17.setGeometry(QtCore.QRect(250, 81, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.campoRndMenos = QtWidgets.QLineEdit(self.frame_3)
        self.campoRndMenos.setGeometry(QtCore.QRect(350, 83, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoRndMenos.setFont(font)
        self.campoRndMenos.setText("")
        self.campoRndMenos.setMaxLength(4)
        self.campoRndMenos.setObjectName("campoRndMenos")
        self.label_18 = QtWidgets.QLabel(self.frame_3)
        self.label_18.setGeometry(QtCore.QRect(170, 118, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.campoPerfectTomado = QtWidgets.QLineEdit(self.frame_3)
        self.campoPerfectTomado.setGeometry(QtCore.QRect(350, 120, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoPerfectTomado.setFont(font)
        self.campoPerfectTomado.setText("")
        self.campoPerfectTomado.setMaxLength(4)
        self.campoPerfectTomado.setObjectName("campoPerfectTomado")
        self.label_19 = QtWidgets.QLabel(self.frame_3)
        self.label_19.setGeometry(QtCore.QRect(180, 154, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.campoGreatTomado = QtWidgets.QLineEdit(self.frame_3)
        self.campoGreatTomado.setGeometry(QtCore.QRect(350, 156, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoGreatTomado.setFont(font)
        self.campoGreatTomado.setText("")
        self.campoGreatTomado.setMaxLength(4)
        self.campoGreatTomado.setObjectName("campoGreatTomado")
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setGeometry(QtCore.QRect(550, 660, 651, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.campoStatus = QtWidgets.QPlainTextEdit(self.frame)
        self.campoStatus.setGeometry(QtCore.QRect(550, 520, 641, 131))
        self.campoStatus.setFocusPolicy(QtCore.Qt.NoFocus)
        self.campoStatus.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.campoStatus.setReadOnly(True)
        self.campoStatus.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.campoStatus.setObjectName("campoStatus")

        self.botaoApagar = QtWidgets.QPushButton(self.frame)
        self.botaoApagar.setGeometry(QtCore.QRect(560, 470, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(16)

        self.botaoApagar.setFont(font)
        self.botaoApagar.setObjectName("botaoApagar")
        self.botaoApagar.clicked.connect(self.apagarTudo)

        self.botaoIniciarCampeonato = QtWidgets.QPushButton(self.frame)
        self.botaoIniciarCampeonato.setGeometry(QtCore.QRect(800, 470, 231, 41))
        self.botaoIniciarCampeonato.clicked.connect(self.iniciarCampeonato)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.botaoIniciarCampeonato.setFont(font)
        self.botaoIniciarCampeonato.setObjectName("botaoIniciarCampeonato")
        CadastrarCampeonato.setCentralWidget(self.centralwidget)

        self.carregarJogadoresCadastrados()

        self.retranslateUi(CadastrarCampeonato)
        QtCore.QMetaObject.connectSlotsByName(CadastrarCampeonato)

    def retranslateUi(self, CadastrarCampeonato):
        _translate = QtCore.QCoreApplication.translate
        CadastrarCampeonato.setWindowTitle(_translate("CadastrarCampeonato", "Tekken Novo Campeonato"))
        self.label.setText(_translate("CadastrarCampeonato", "Nome"))
        self.label_2.setText(_translate("CadastrarCampeonato", "Quantidade de rounds"))
        self.label_3.setText(_translate("CadastrarCampeonato", "Data de Inicio"))
        self.calendarWidget.setToolTip(_translate("CadastrarCampeonato", "Inserir a data do inicio do campeonato"))
        self.label_4.setText(_translate("CadastrarCampeonato", "Participantes"))
        self.label_5.setText(_translate("CadastrarCampeonato", "Nome"))
        self.label_6.setText(_translate("CadastrarCampeonato", "Nacionalidade"))
        self.botaoIncluir.setText(_translate("CadastrarCampeonato", "Cadastrar novo participante"))
        self.label_7.setText(_translate("CadastrarCampeonato", "Participantes do torneio:"))
        self.botaoRemoverSelecionado.setText(_translate("CadastrarCampeonato", "Remover selecionado"))
        self.botaoIncluirJogadorCadastrado.setText(_translate("CadastrarCampeonato", "Incluir jogador cadastrado"))
        self.botaoRemoverTodos.setText(_translate("CadastrarCampeonato", "Remover todos"))
        self.label_8.setText(_translate("CadastrarCampeonato", "Pontuação:"))
        self.label_9.setText(_translate("CadastrarCampeonato", "Vitória"))
        self.label_10.setText(_translate("CadastrarCampeonato", "Empate"))
        self.label_11.setText(_translate("CadastrarCampeonato", "Derrota"))
        self.label_12.setText(_translate("CadastrarCampeonato", "Perfect"))
        self.label_13.setText(_translate("CadastrarCampeonato", "Great"))
        self.label_14.setText(_translate("CadastrarCampeonato", "Round ganho"))
        self.label_15.setText(_translate("CadastrarCampeonato", "Double KO"))
        self.label_16.setText(_translate("CadastrarCampeonato", "Time Out"))
        self.label_17.setText(_translate("CadastrarCampeonato", "Round perdido"))
        self.label_18.setText(_translate("CadastrarCampeonato", "Round perdido por perfect"))
        self.label_19.setText(_translate("CadastrarCampeonato", "Round perdido por great"))
        self.label_20.setText(_translate("CadastrarCampeonato", "Jogadores cadastrados no banco"))
        self.botaoApagar.setText(_translate("CadastrarCampeonato", "Apagar tudo"))
        self.botaoIniciarCampeonato.setText(_translate("CadastrarCampeonato", "Iniciar Campeonato"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_CadastrarCampeonato()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())