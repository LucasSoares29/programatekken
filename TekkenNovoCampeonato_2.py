# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TekkenNovoCampeonato.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
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

    def ativarSpinBox2(self):
        if self.checkBox_2fase.isChecked():
            self.spinBox_2.setEnabled(True)
            self.checkBox_primeiroLugarFinal.setEnabled(True)
        else:
            self.spinBox_2.setEnabled(False)
            self.checkBox_primeiroLugarFinal.setEnabled(False)

    def ativarPontuacaoRingOut(self):
        if self.checkBox_RingOut.isChecked():
            self.campoRingOut.setEnabled(True)
        else:
            self.campoRingOut.setEnabled(False)

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
        self.campoRingOut.setText('')
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

        if self.checkBox_2fase.isChecked() and (self.listWidget.count() < int(self.spinBox_2.text())):
            self.gerarAviso(3, "Atenção", "Há mais jogadores classificados do que inscritos no campeonato")
            return

        nomeTorneio = self.campoNome.text()
        qtdRounds = self.spinBox.text()
        dataInicio = str(self.calendarWidget.selectedDate().day()) + '/' + str(self.calendarWidget.selectedDate().month()) + '/' + str(self.calendarWidget.selectedDate().year())

        teraRingOut = self.checkBox_RingOut.isChecked();
        teraSegundaFase = self.checkBox_2fase.isChecked();
        if teraSegundaFase is True:
            primeiroNaFinal = self.checkBox_primeiroLugarFinal.isChecked();
            quantidadeNaFase2 = self.spinBox_2.text();
        else:
            primeiroNaFinal = False
            quantidadeNaFase2 = 0
        ultimoEliminado = self.checkBox_ultimo.isChecked();

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
        novoCampeonato.adicionarInformacoes(teraSegundaFase, primeiroNaFinal, quantidadeNaFase2, ultimoEliminado)

        #adiciona pontuação de ringout, se estiver sido checado
        if self.checkBox_RingOut.isChecked():
            pontRingOut = self.campoRingOut.text()
            novoCampeonato.adicionarRingOut(pontRingOut)

        #cadastro no banco
        if cdao.cadastrarCampeonato(novoCampeonato) == 0:
            return

        index = 0

        plainText = "Campeonato " + nomeTorneio + " cadastrado com sucesso\n"
        self.campoStatus.insertPlainText(plainText)
        self.progressBar.setValue(25)

        porcentagem = 25 / self.listWidget.count();



        #adicionando jogadores
        try:
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
                self.campoStatus.append(plainText)
                if index == 0:
                    progresso = 25 + round(porcentagem)
                else:
                    progresso = progresso + round(porcentagem)
                self.progressBar.setValue(progresso)
        except Exception as e:
            print(e)
            print(type(e))
            return

        #gerando as rodadas
        try:
            idjogadores = cdao.recuperarIDJogadoresNoCampeonato(novoCampeonato)
            rodadas = novoCampeonato.gerarRodadas(idjogadores)
            idCampeonato = cdao.recuperarID(novoCampeonato.nome)
            for lutas in rodadas:
                ldao.inserirLuta(idCampeonato, lutas)  # OK COM NUMERO PAR E IMPAR DE JOGADORES.
            cdao = CampeonatoDAO()
            plainText = "Rodadas geradas com sucesso\n"
            self.campoStatus.append(plainText)
            progresso += 25
            self.progressBar.setValue(progresso)
        except Exception as e:
           print(e)
           print(type(e))
           return

        #imprimindo txt com as rodadas
        try:
            plainText = "Imprimindo lutas do campeonato...\n"
            self.campoStatus.append(plainText)
            cdao.imprimirRodadas(idCampeonato)
            input = open("outputRodadas.txt", "r")
            while True:
                linha = input.readline().strip("\n")
                if linha == "FIM DO ARQUIVO":
                    break
                self.campoStatus.append(plainText)
            input.close()
            progresso = 100
            self.progressBar.setValue(progresso)
        except Exception as e:
           print(e)
           print(type(e))
           return

        self.gerarAviso(1, "Tekken Novo Campeonato", "Novo campeonato foi criado com sucesso")


        self.apagarTudo()
        self.carregarJogadoresCadastrados()

    def setupUi(self, CadastrarCampeonato):
        CadastrarCampeonato.setObjectName("CadastrarCampeonato")
        CadastrarCampeonato.setWindowModality(QtCore.Qt.ApplicationModal)
        CadastrarCampeonato.resize(1280, 881)
        CadastrarCampeonato.setSizeIncrement(QtCore.QSize(1, 1))
        CadastrarCampeonato.setBaseSize(QtCore.QSize(1280, 720))

        self.centralwidget = QtWidgets.QWidget(CadastrarCampeonato)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 1280, 851))
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setMaximumSize(QtCore.QSize(3840, 2160))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(30, 30, 90, 25))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.campoNome = QtWidgets.QLineEdit(self.frame)
        self.campoNome.setGeometry(QtCore.QRect(100, 30, 381, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoNome.setFont(font)
        self.campoNome.setObjectName("campoNome")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 300, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.spinBox = QtWidgets.QSpinBox(self.frame)
        self.spinBox.setGeometry(QtCore.QRect(260, 70, 42, 26))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox.setFont(font)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(5)
        self.spinBox.setProperty("value", 2)
        self.spinBox.setObjectName("spinBox")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(30, 110, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.frame)
        self.calendarWidget.setGeometry(QtCore.QRect(30, 150, 351, 211))
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.SingleLetterDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setDateEditAcceptDelay(1500)
        self.calendarWidget.setObjectName("calendarWidget")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(530, 30, 661, 441))
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
        font.setPointSize(15)
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
        font.setPointSize(13)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.botaoIncluir = QtWidgets.QPushButton(self.frame_2)
        self.botaoIncluir.setGeometry(QtCore.QRect(20, 130, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.botaoIncluir.setFont(font)
        self.botaoIncluir.setObjectName("botaoIncluir")
        self.botaoIncluir.clicked.connect(self.incluir)


        self.listWidget = QtWidgets.QListWidget(self.frame_2)
        self.listWidget.setGeometry(QtCore.QRect(20, 210, 271, 131))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setObjectName("listWidget")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(20, 170, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.botaoRemoverSelecionado = QtWidgets.QPushButton(self.frame_2)
        self.botaoRemoverSelecionado.setGeometry(QtCore.QRect(20, 350, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.botaoRemoverSelecionado.setFont(font)
        self.botaoRemoverSelecionado.setObjectName("botaoRemoverSelecionado")
        self.botaoRemoverSelecionado.clicked.connect(self.removerSelecionado)


        self.botaoRemoverTodos = QtWidgets.QPushButton(self.frame_2)
        self.botaoRemoverTodos.setGeometry(QtCore.QRect(20, 390, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.botaoRemoverTodos.setFont(font)
        self.botaoRemoverTodos.setObjectName("botaoRemoverTodos")
        self.botaoRemoverTodos.clicked.connect(self.removerTodos)

        self.listWidget_2 = QtWidgets.QListWidget(self.frame_2)
        self.listWidget_2.setGeometry(QtCore.QRect(320, 210, 271, 131))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget_2.setFont(font)
        self.listWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget_2.setObjectName("listWidget_2")

        self.botaoIncluirJogadorCadastrado = QtWidgets.QPushButton(self.frame_2)
        self.botaoIncluirJogadorCadastrado.setGeometry(QtCore.QRect(320, 350, 280, 31))
        self.botaoIncluirJogadorCadastrado.clicked.connect(self.incluirJogadorCadastrado)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.botaoIncluirJogadorCadastrado.setFont(font)
        self.botaoIncluirJogadorCadastrado.setObjectName("botaoIncluirJogadorCadastrado")


        self.label_20 = QtWidgets.QLabel(self.frame_2)
        self.label_20.setGeometry(QtCore.QRect(330, 170, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(20, 550, 471, 281))
        self.frame_3.setMinimumSize(QtCore.QSize(0, 0))
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
        self.label_14.setGeometry(QtCore.QRect(280, 40, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.campoDoubleKO = QtWidgets.QLineEdit(self.frame_3)
        self.campoDoubleKO.setGeometry(QtCore.QRect(110, 230, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoDoubleKO.setFont(font)
        self.campoDoubleKO.setText("")
        self.campoDoubleKO.setMaxLength(4)
        self.campoDoubleKO.setObjectName("campoDoubleKO")
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        self.label_15.setGeometry(QtCore.QRect(0, 230, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.campoRoundGanho = QtWidgets.QLineEdit(self.frame_3)
        self.campoRoundGanho.setGeometry(QtCore.QRect(400, 40, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoRoundGanho.setFont(font)
        self.campoRoundGanho.setText("")
        self.campoRoundGanho.setMaxLength(4)
        self.campoRoundGanho.setObjectName("campoRoundGanho")
        self.campoTimeOut = QtWidgets.QLineEdit(self.frame_3)
        self.campoTimeOut.setGeometry(QtCore.QRect(400, 80, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoTimeOut.setFont(font)
        self.campoTimeOut.setText("")
        self.campoTimeOut.setMaxLength(4)
        self.campoTimeOut.setObjectName("campoTimeOut")
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        self.label_16.setGeometry(QtCore.QRect(300, 78, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.frame_3)
        self.label_17.setGeometry(QtCore.QRect(270, 120, 120, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.campoRndMenos = QtWidgets.QLineEdit(self.frame_3)
        self.campoRndMenos.setGeometry(QtCore.QRect(400, 117, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoRndMenos.setFont(font)
        self.campoRndMenos.setText("")
        self.campoRndMenos.setMaxLength(4)
        self.campoRndMenos.setObjectName("campoRndMenos")
        self.label_18 = QtWidgets.QLabel(self.frame_3)
        self.label_18.setGeometry(QtCore.QRect(190, 190, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.campoPerfectTomado = QtWidgets.QLineEdit(self.frame_3)
        self.campoPerfectTomado.setGeometry(QtCore.QRect(400, 192, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoPerfectTomado.setFont(font)
        self.campoPerfectTomado.setText("")
        self.campoPerfectTomado.setMaxLength(4)
        self.campoPerfectTomado.setObjectName("campoPerfectTomado")
        self.label_19 = QtWidgets.QLabel(self.frame_3)
        self.label_19.setGeometry(QtCore.QRect(190, 230, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.campoGreatTomado = QtWidgets.QLineEdit(self.frame_3)
        self.campoGreatTomado.setGeometry(QtCore.QRect(400, 228, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoGreatTomado.setFont(font)
        self.campoGreatTomado.setText("")
        self.campoGreatTomado.setMaxLength(4)
        self.campoGreatTomado.setObjectName("campoGreatTomado")

        self.campoRingOut = QtWidgets.QLineEdit(self.frame_3)
        self.campoRingOut.setGeometry(QtCore.QRect(400, 152, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.campoRingOut.setFont(font)
        self.campoRingOut.setText("")
        self.campoRingOut.setMaxLength(4)
        self.campoRingOut.setObjectName("campoRingOut")
        self.campoRingOut.setEnabled(False)

        self.label_21 = QtWidgets.QLabel(self.frame_3)
        self.label_21.setGeometry(QtCore.QRect(220, 150, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")

        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setGeometry(QtCore.QRect(540, 800, 651, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.campoStatus = QtWidgets.QTextEdit(self.frame)
        self.campoStatus.setGeometry(QtCore.QRect(540, 660, 641, 131))
        self.campoStatus.setFocusPolicy(QtCore.Qt.NoFocus)
        self.campoStatus.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.campoStatus.setReadOnly(True)
        self.campoStatus.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.campoStatus.setObjectName("campoStatus")

        self.botaoApagar = QtWidgets.QPushButton(self.frame)
        self.botaoApagar.setGeometry(QtCore.QRect(710, 610, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.botaoApagar.setFont(font)
        self.botaoApagar.setObjectName("botaoApagar")
        self.botaoApagar.clicked.connect(self.apagarTudo)



        self.botaoIniciarCampeonato = QtWidgets.QPushButton(self.frame)
        self.botaoIniciarCampeonato.setGeometry(QtCore.QRect(950, 610, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.botaoIniciarCampeonato.setFont(font)
        self.botaoIniciarCampeonato.setObjectName("botaoIniciarCampeonato")
        self.botaoIniciarCampeonato.clicked.connect(self.iniciarCampeonato)

        self.label_24 = QtWidgets.QLabel(self.frame)
        self.label_24.setGeometry(QtCore.QRect(30, 460, 411, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")

        self.checkBox_primeiroLugarFinal = QtWidgets.QCheckBox(self.frame)
        self.checkBox_primeiroLugarFinal.setGeometry(QtCore.QRect(30, 430, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_primeiroLugarFinal.setFont(font)
        self.checkBox_primeiroLugarFinal.setObjectName("checkBox_primeiroLugarFinal")
        self.checkBox_primeiroLugarFinal.setEnabled(False)


        self.checkBox_2fase = QtWidgets.QCheckBox(self.frame)
        self.checkBox_2fase.setGeometry(QtCore.QRect(30, 390, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_2fase.setFont(font)
        self.checkBox_2fase.setObjectName("checkBox_2fase")
        self.checkBox_2fase.clicked.connect(self.ativarSpinBox2)

        self.spinBox_2 = QtWidgets.QSpinBox(self.frame)
        self.spinBox_2.setGeometry(QtCore.QRect(450, 460, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.spinBox_2.setFont(font)
        self.spinBox_2.setMinimum(2)
        self.spinBox_2.setMaximum(16)
        self.spinBox_2.setSingleStep(1)
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_2.setEnabled(False)

        self.checkBox_ultimo = QtWidgets.QCheckBox(self.frame)
        self.checkBox_ultimo.setGeometry(QtCore.QRect(30, 500, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_ultimo.setFont(font)
        self.checkBox_ultimo.setObjectName("checkBox_ultimo")

        self.checkBox_RingOut = QtWidgets.QCheckBox(self.frame)
        self.checkBox_RingOut.setGeometry(QtCore.QRect(30, 363, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.checkBox_RingOut.setFont(font)
        self.checkBox_RingOut.setObjectName("checkBox_RingOut")
        self.checkBox_RingOut.clicked.connect(self.ativarPontuacaoRingOut)

        CadastrarCampeonato.setCentralWidget(self.centralwidget)

        self.carregarJogadoresCadastrados()

        self.retranslateUi(CadastrarCampeonato)
        QtCore.QMetaObject.connectSlotsByName(CadastrarCampeonato)

    def retranslateUi(self, CadastrarCampeonato):
        _translate = QtCore.QCoreApplication.translate
        CadastrarCampeonato.setWindowTitle(_translate("CadastrarCampeonato", "MainWindow"))
        self.label.setText(_translate("CadastrarCampeonato", "Nome"))
        self.label_2.setText(_translate("CadastrarCampeonato", "Quantidade de rounds"))
        self.label_3.setText(_translate("CadastrarCampeonato", "Data de Inicio"))
        self.calendarWidget.setToolTip(_translate("CadastrarCampeonato", "Inserir a data do inicio do campeonato"))
        self.label_4.setText(_translate("CadastrarCampeonato", "Participantes"))
        self.label_5.setText(_translate("CadastrarCampeonato", "Nome"))
        self.label_6.setText(_translate("CadastrarCampeonato", "Nacionalidade"))
        self.botaoIncluir.setText(_translate("CadastrarCampeonato", "Incluir novo participante"))
        self.label_7.setText(_translate("CadastrarCampeonato", "Novos participantes:"))
        self.botaoRemoverSelecionado.setText(_translate("CadastrarCampeonato", "Remover selecionado"))
        self.botaoRemoverTodos.setText(_translate("CadastrarCampeonato", "Remover todos"))
        self.botaoIncluirJogadorCadastrado.setText(_translate("CadastrarCampeonato", "Incluir jogador cadastrado"))
        self.label_20.setText(_translate("CadastrarCampeonato", "Jogadores cadastrados no banco:"))
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
        self.label_21.setText(_translate("CadastrarCampeonato", "Ring out"))
        self.botaoApagar.setText(_translate("CadastrarCampeonato", "Apagar tudo"))
        self.botaoIniciarCampeonato.setText(_translate("CadastrarCampeonato", "Iniciar Campeonato"))
        self.label_24.setText(_translate("CadastrarCampeonato", "Quantidade de classificados para 2ª fase"))
        self.checkBox_primeiroLugarFinal.setText(_translate("CadastrarCampeonato", "1º lugar na final"))
        self.checkBox_2fase.setText(_translate("CadastrarCampeonato", "Terá segunda fase"))
        self.checkBox_ultimo.setText(_translate("CadastrarCampeonato", "Ultimo será eliminado"))
        self.checkBox_RingOut.setText(_translate("CadastrarCampeonato", "Ring Out válidos"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_CadastrarCampeonato()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())