# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RodadaTekken.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from CampeonatoDAO import CampeonatoDAO
from Luta import Luta
from LutaDAO import LutaDAO
from JogadorDAO import jogadorDAO
from TekkenNovoCampeonato import Ui_CadastrarCampeonato
from Jogador import Jogador
from RodadaTekkenTabela import Ui_FormPontuacao
from RodadaTekkenResultadosAnteriores import Ui_FormRodadasFinalizadas
from RodadaTekkenComecar import Ui_Form
import os

class Ui_RodadaTekken(object):

    idCampeonato = 0
    luta = 0
    rodada = 0
    resultados = ["Selecione um resultado", "Perfect", "Great", "Double KO", "Vitória", "Time Out", "Derrota"]
    lutaAtual = Luta(None, None, None)
    partidasNaoFinalizadas = []
    campeonatoSelecionado = None
    segundaLuta = False # Botão ativado quando há clico no próxima luta uma vez no mesmo campeonato

    # OK
    def carregarCampeonatosEmAndamento(self):
        listaCampeonatos = CampeonatoDAO().listarCampeonatos()
        self.comboBoxCampeonato.addItem("Selecione um campeonato para começar...")
        for nomeCampeonato in listaCampeonatos:
            self.comboBoxCampeonato.addItem(nomeCampeonato)

    def mudarCorPosicao(self, Campeonato, posicaoP1, posicaoP2, idCampeonato):
        posicaoVerde = int(Campeonato.quantosNaFase2) #posições da área que se classifica
        if int(posicaoP1) == 0:
            self.posicaoAtual_1.setStyleSheet("background-color: rgb(255,255,255);\ncolor: rgb(0,0,0)"); #branco com letras pretas
        if int(posicaoP2) == 0:
            self.posicaoAtual_2.setStyleSheet("background-color: rgb(255,255,255);\ncolor: rgb(0,0,0)"); #branco com letras pretas

        if int(posicaoP1) > 0 and int(posicaoP2) > 0:
            #posição player 1
            try:
                if Campeonato.primeiroNaFinal is True:
                    if int(posicaoP1) == 1:
                        self.posicaoAtual_1.setStyleSheet("background-color: rgb(255,255,0);\ncolor: rgb(0,0,0)"); #amarelo com letras pretas
                    elif int(posicaoP1) > 1 and int(posicaoP1) <= posicaoVerde + 1:
                        self.posicaoAtual_1.setStyleSheet("background-color: rgb(0,255,127);\ncolor: rgb(0,0,0)") #verde com letras pretas
                    else:
                        if int(posicaoP1) == CampeonatoDAO().qtdJogadoresTorneio(idCampeonato) and Campeonato.ultimoEliminado is True:
                           self.posicaoAtual_1.setStyleSheet("background-color: rgb(0,0,0);\ncolor: rgb(255,255,255)"); #preto com letras brancas
                        else:
                           self.posicaoAtual_1.setStyleSheet("background-color: rgb(255,0,0);\ncolor: rgb(255,255,255)"); #vermelho com letras pretas
                else:
                    if int(posicaoP1) <= posicaoVerde:
                        self.posicaoAtual_1.setStyleSheet("background-color: rgb(0,255,127);\ncolor: rgb(0,0,0)")
                    else:
                        if int(posicaoP1) == CampeonatoDAO().qtdJogadoresTorneio(idCampeonato) and Campeonato.ultimoEliminado is True:
                           self.posicaoAtual_1.setStyleSheet("background-color: rgb(0,0,0);\ncolor: rgb(255,255,255)");
                        else:
                           self.posicaoAtual_1.setStyleSheet("background-color: rgb(255,0,0);\ncolor: rgb(255,255,255)");

                #posição player 2
                if Campeonato.primeiroNaFinal is True:
                    if int(posicaoP2) == 1:
                        self.posicaoAtual_2.setStyleSheet("background-color: rgb(255,255,0);\ncolor: rgb(0,0,0)"); #amarelo com letras pretas
                    elif int(posicaoP2) > 1 and int(posicaoP2) <= posicaoVerde:
                        self.posicaoAtual_2.setStyleSheet("background-color: rgb(0,255,127);\ncolor: rgb(0,0,0)") #verde com letras pretas
                    else:
                        if int(posicaoP2) == CampeonatoDAO().qtdJogadoresTorneio(idCampeonato) and Campeonato.ultimoEliminado is True:
                           self.posicaoAtual_2.setStyleSheet("background-color: rgb(0,0,0);\ncolor: rgb(255,255,255)"); #preto com letras brancas
                        else:
                           self.posicaoAtual_2.setStyleSheet("background-color: rgb(255,0,0);\ncolor: rgb(255,255,255)"); #vermelho com letras pretas
                else:
                    posicaoVerde = int(Campeonato.quantosNaFase2)
                    if int(posicaoP2) <= posicaoVerde:
                        self.posicaoAtual_2.setStyleSheet("background-color: rgb(0,255,127);\ncolor: rgb(0,0,0)")
                    else:
                        if int(posicaoP2) == CampeonatoDAO().qtdJogadoresTorneio(idCampeonato) and Campeonato.ultimoEliminado is True:
                           self.posicaoAtual_2.setStyleSheet("background-color: rgb(0,0,0);\ncolor: rgb(255,255,255)");
                        else:
                           self.posicaoAtual_2.setStyleSheet("background-color: rgb(255,0,0);\ncolor: rgb(255,255,255)");
            except Exception as e:
                print(e)
                print(type(e))



    # OK, TESTAR DENTRO DA FUNÇÃO PROXIMA LUTA
    def carregarLuta(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)

        if self.comboBoxCampeonato.currentIndex() > 0:
            #carregar o campeonato
            idCampeonato = int(CampeonatoDAO().recuperarID(self.comboBoxCampeonato.currentText()))
            if idCampeonato == self.idCampeonato:
                self.luta += 1
            else:
                self.segundaLuta = False
                self.luta = 1
            self.idCampeonato = idCampeonato
            self.campeonatoSelecionado = CampeonatoDAO().carregarInformacoesCampeonato(self.idCampeonato)

            #carregar a opção de Ring Out nos comboboxes
            if self.campeonatoSelecionado.temRingOut is True:
                self.resultados = ["Selecione um resultado", "Perfect", "Great", "Double KO", "Vitória", "Time Out", "Ring Out", "Derrota"]

            else:
                self.resultados = ["Selecione um resultado", "Perfect", "Great", "Double KO", "Vitória", "Time Out", "Derrota"]
                # removendo e readicionando os itens dos comboboxes
            self.comboBoxR1P1.clear()
            self.comboBoxR1P1.addItems(self.resultados)
            self.comboBoxR2P1.clear()
            self.comboBoxR2P1.addItems(self.resultados)
            self.comboBoxR3P1.clear()
            self.comboBoxR3P1.addItems(self.resultados)
            self.comboBoxR4P1.clear()
            self.comboBoxR4P1.addItems(self.resultados)
            self.comboBoxR5P1.clear()
            self.comboBoxR5P1.addItems(self.resultados)
            self.comboBoxR6P1.clear()
            self.comboBoxR6P1.addItems(self.resultados)
            self.comboBoxR7P1.clear()
            self.comboBoxR7P1.addItems(self.resultados)
            self.comboBoxR8P1.clear()
            self.comboBoxR8P1.addItems(self.resultados)
            self.comboBoxR9P1.clear()
            self.comboBoxR9P1.addItems(self.resultados)
            self.comboBoxR1P2.clear()
            self.comboBoxR1P2.addItems(self.resultados)
            self.comboBoxR2P2.clear()
            self.comboBoxR2P2.addItems(self.resultados)
            self.comboBoxR3P2.clear()
            self.comboBoxR3P2.addItems(self.resultados)
            self.comboBoxR4P2.clear()
            self.comboBoxR4P2.addItems(self.resultados)
            self.comboBoxR5P2.clear()
            self.comboBoxR5P2.addItems(self.resultados)
            self.comboBoxR6P2.clear()
            self.comboBoxR6P2.addItems(self.resultados)
            self.comboBoxR7P2.clear()
            self.comboBoxR7P2.addItems(self.resultados)
            self.comboBoxR8P2.clear()
            self.comboBoxR8P2.addItems(self.resultados)
            self.comboBoxR9P2.clear()
            self.comboBoxR9P2.addItems(self.resultados)


            if self.luta == 1:
                #carregar partidas não finalizadas
                self.partidasNaoFinalizadas = LutaDAO().carregarLutasNaoFinalizadas(self.idCampeonato)
                if len(self.partidasNaoFinalizadas) == 0: #caso após a última rodada
                    Ui_CadastrarCampeonato().gerarAviso(2, "Rodada Tekken", "O campeonato já foi finalizado")
                    #resetar interface
                    self.pushButton_2.setEnabled(False)
                    self.label_jogador1.setText("Nome do jogador")
                    self.label_jogador2.setText("Nome do jogador")
                    self.posicaoAtual_1.setVisible(False)
                    self.posicaoAtual_2.setVisible(False)
                    self.resultadoP1.setText('')
                    self.resultadoP2.setText('')
                    self.statusP1.setText('')
                    self.statusP2.setText('')
                    self.posicaoAtual_1.setText('1')
                    self.posicaoAtual_2.setText('1')
                    self.posicaoAtual_1.setStyleSheet("background-color: rgb(255,0,0);\ncolor: rgb(255,255,255)");
                    self.posicaoAtual_2.setStyleSheet("background-color: rgb(255,0,0);\ncolor: rgb(255,255,255)");
                    self.luta = 0
                    self.rodada = 0
                    self.segundaLuta = False
                    return

            #carregar a luta
            if self.luta <= len(self.partidasNaoFinalizadas):
                p1 = Jogador(str(self.partidasNaoFinalizadas[self.luta - 1][0]), None)
                p2 = Jogador(str(self.partidasNaoFinalizadas[self.luta - 1][1]), None)
                self.lutaAtual = Luta(p1, p2, str(self.partidasNaoFinalizadas[self.luta - 1][2]))
                self.rodada = self.lutaAtual.rodada
            else:
                Ui_CadastrarCampeonato().gerarAviso(2, "Rodada Tekken", "Não há mais partidas para serem realizadas")
                self.label_jogador1.setText("Nome do jogador")
                self.label_jogador2.setText("Nome do jogador")
                self.resultadoP1.setText('')
                self.resultadoP2.setText('')
                self.statusP1.setText('')
                self.statusP2.setText('')
                self.posicaoAtual_1.setText('1')
                self.posicaoAtual_2.setText('1')
                self.posicaoAtual_1.setStyleSheet("background-color: rgb(255,0,0);\ncolor: rgb(255,255,255)");
                self.posicaoAtual_2.setStyleSheet("background-color: rgb(255,0,0);\ncolor: rgb(255,255,255)");
                self.luta = 0
                self.rodada = 0
                self.segundaLuta = False
                self.pushButton_2.setEnabled(False)
                return

            #carregar a posição atual de cada jogador
            self.tabela = CampeonatoDAO().gerarTabelaPontuacao(self.idCampeonato, self.campeonatoSelecionado)
            posicaoP1 = str(jogadorDAO().posicaoAtual(self.lutaAtual.jogador1.nome, self.tabela))
            posicaoP2 = str(jogadorDAO().posicaoAtual(self.lutaAtual.jogador2.nome, self.tabela))
            if int(posicaoP1) > 0 and int(posicaoP2) > 0:
                self.posicaoAtual_1.setText(posicaoP1)
                self.posicaoAtual_2.setText(posicaoP2)
                self.posicaoAtual_1.setVisible(True)
                self.posicaoAtual_2.setVisible(True)
            else:
                if int(posicaoP1) == 0:
                    self.posicaoAtual_1.setVisible(False)
                if int(posicaoP2) == 0:
                    self.posicaoAtual_2.setVisible(False)

            ## MUDANDO A COR DO QUADRADO DEPENDENDO DA POSIÇÃO
            self.mudarCorPosicao(self.campeonatoSelecionado, posicaoP1, posicaoP2, self.idCampeonato)

            #atualizar labels do titulo rodada e luta
            self.label_rodada.setText("RODADA " + str(self.rodada))
            self.label_luta.setText("Luta " + str(self.luta))

            #carregar nome dos jogadores
            self.label_jogador1.setText(self.lutaAtual.jogador1.nome.strip("\n"))
            self.label_jogador2.setText(self.lutaAtual.jogador2.nome.strip("\n"))

            #carregar ComboBoxes que inserirei os resultados
            self.carregarComboBoxes()

            #resetar campo de resultado e status (vitória/derrota/empate)
            self.resultadoP1.setText('')
            self.resultadoP2.setText('')
            self.statusP1.setText('')
            self.statusP2.setText('')
        else:
            #RESETAREI EXIBIÇÃO E CONTEUDO DOS COMBOBOXES E O TEXTO DOS LABELS
            #COMBOBOXES
            self.label_R1.setEnabled(True)
            self.comboBoxR1P1.setEnabled(True)
            self.comboBoxR1P2.setEnabled(True)
            self.comboBoxR1P1.setCurrentIndex(0)
            self.comboBoxR1P2.setCurrentIndex(0)
            self.label_R2.setEnabled(True)
            self.comboBoxR2P1.setEnabled(True)
            self.comboBoxR2P2.setEnabled(True)
            self.comboBoxR2P1.setCurrentIndex(0)
            self.comboBoxR2P2.setCurrentIndex(0)
            self.label_R3.setEnabled(True)
            self.comboBoxR3P1.setEnabled(True)
            self.comboBoxR3P2.setEnabled(True)
            self.comboBoxR3P1.setCurrentIndex(0)
            self.comboBoxR3P2.setCurrentIndex(0)
            self.label_R4.setEnabled(True)
            self.comboBoxR4P1.setEnabled(True)
            self.comboBoxR4P2.setEnabled(True)
            self.comboBoxR4P1.setCurrentIndex(0)
            self.comboBoxR4P2.setCurrentIndex(0)
            self.label_R5.setEnabled(True)
            self.comboBoxR5P1.setEnabled(True)
            self.comboBoxR5P2.setEnabled(True)
            self.comboBoxR5P1.setCurrentIndex(0)
            self.comboBoxR5P2.setCurrentIndex(0)
            self.label_R6.setEnabled(True)
            self.comboBoxR6P1.setEnabled(True)
            self.comboBoxR6P2.setEnabled(True)
            self.comboBoxR6P1.setCurrentIndex(0)
            self.comboBoxR6P2.setCurrentIndex(0)
            self.label_R7.setEnabled(True)
            self.comboBoxR7P1.setEnabled(True)
            self.comboBoxR7P2.setEnabled(True)
            self.comboBoxR7P1.setCurrentIndex(0)
            self.comboBoxR7P2.setCurrentIndex(0)
            self.label_R8.setEnabled(True)
            self.comboBoxR8P1.setEnabled(True)
            self.comboBoxR8P2.setEnabled(True)
            self.comboBoxR8P1.setCurrentIndex(0)
            self.comboBoxR8P2.setCurrentIndex(0)
            self.label_R9.setEnabled(True)
            self.comboBoxR9P1.setEnabled(True)
            self.comboBoxR9P2.setEnabled(True)
            self.comboBoxR9P1.setCurrentIndex(0)
            self.comboBoxR9P2.setCurrentIndex(0)

            #labels
            self.label_jogador1.setText("Nome do jogador")
            self.label_jogador2.setText("Nome do jogador")
            self.label_rodada.setText("RODADA 1 ")
            self.label_luta.setText("Luta 1")
            self.resultadoP1.setText('')
            self.resultadoP2.setText('')
            self.statusP1.setText('')
            self.statusP2.setText('')
            self.posicaoAtual_1.setText('1')
            self.posicaoAtual_2.setText('1')
            self.posicaoAtual_1.setStyleSheet("background-color: rgb(255,0,0);\ncolor: rgb(255,255,255)");
            self.posicaoAtual_2.setStyleSheet("background-color: rgb(255,0,0);\ncolor: rgb(255,255,255)");

            #resetar variaveis luta e rodada
            self.luta = 0
            self.rodada = 0

            #desabilitar botão de próxima luta
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)

    def carregarComboBoxes(self):
        if self.campeonatoSelecionado.quantidadeRounds == 1:
            self.label_R1.setEnabled(True)
            self.comboBoxR1P1.setEnabled(True)
            self.comboBoxR1P2.setEnabled(True)
            self.label_R2.setEnabled(False)
            self.comboBoxR2P1.setEnabled(False)
            self.comboBoxR2P2.setEnabled(False)
            self.label_R3.setEnabled(False)
            self.comboBoxR3P1.setEnabled(False)
            self.comboBoxR3P2.setEnabled(False)
            self.label_R4.setEnabled(False)
            self.comboBoxR4P1.setEnabled(False)
            self.comboBoxR4P2.setEnabled(False)
            self.label_R5.setEnabled(False)
            self.comboBoxR5P1.setEnabled(False)
            self.comboBoxR5P2.setEnabled(False)
            self.label_R6.setEnabled(False)
            self.comboBoxR6P1.setEnabled(False)
            self.comboBoxR6P2.setEnabled(False)
            self.label_R7.setEnabled(False)
            self.comboBoxR7P1.setEnabled(False)
            self.comboBoxR7P2.setEnabled(False)
            self.label_R8.setEnabled(False)
            self.comboBoxR8P1.setEnabled(False)
            self.comboBoxR8P2.setEnabled(False)
            self.label_R9.setEnabled(False)
            self.comboBoxR9P1.setEnabled(False)
            self.comboBoxR9P2.setEnabled(False)
        elif self.campeonatoSelecionado.quantidadeRounds == 2:
            self.label_R1.setEnabled(True)
            self.comboBoxR1P1.setEnabled(True)
            self.comboBoxR1P2.setEnabled(True)
            self.label_R2.setEnabled(True)
            self.comboBoxR2P1.setEnabled(True)
            self.comboBoxR2P2.setEnabled(True)
            self.label_R3.setEnabled(True)
            self.comboBoxR3P1.setEnabled(True)
            self.comboBoxR3P2.setEnabled(True)
            self.label_R4.setEnabled(False)
            self.comboBoxR4P1.setEnabled(False)
            self.comboBoxR4P2.setEnabled(False)
            self.label_R5.setEnabled(False)
            self.comboBoxR5P1.setEnabled(False)
            self.comboBoxR5P2.setEnabled(False)
            self.label_R6.setEnabled(False)
            self.comboBoxR6P1.setEnabled(False)
            self.comboBoxR6P2.setEnabled(False)
            self.label_R7.setEnabled(False)
            self.comboBoxR7P1.setEnabled(False)
            self.comboBoxR7P2.setEnabled(False)
            self.label_R8.setEnabled(False)
            self.comboBoxR8P1.setEnabled(False)
            self.comboBoxR8P2.setEnabled(False)
            self.label_R9.setEnabled(False)
            self.comboBoxR9P1.setEnabled(False)
            self.comboBoxR9P2.setEnabled(False)
        elif self.campeonatoSelecionado.quantidadeRounds == 3:
            self.label_R1.setEnabled(True)
            self.comboBoxR1P1.setEnabled(True)
            self.comboBoxR1P2.setEnabled(True)
            self.label_R2.setEnabled(True)
            self.comboBoxR2P1.setEnabled(True)
            self.comboBoxR2P2.setEnabled(True)
            self.label_R3.setEnabled(True)
            self.comboBoxR3P1.setEnabled(True)
            self.comboBoxR3P2.setEnabled(True)
            self.label_R4.setEnabled(True)
            self.comboBoxR4P1.setEnabled(True)
            self.comboBoxR4P2.setEnabled(True)
            self.label_R5.setEnabled(True)
            self.comboBoxR5P1.setEnabled(True)
            self.comboBoxR5P2.setEnabled(True)
            self.label_R6.setEnabled(False)
            self.comboBoxR6P1.setEnabled(False)
            self.comboBoxR6P2.setEnabled(False)
            self.label_R7.setEnabled(False)
            self.comboBoxR7P1.setEnabled(False)
            self.comboBoxR7P2.setEnabled(False)
            self.label_R8.setEnabled(False)
            self.comboBoxR8P1.setEnabled(False)
            self.comboBoxR8P2.setEnabled(False)
            self.label_R9.setEnabled(False)
            self.comboBoxR9P1.setEnabled(False)
            self.comboBoxR9P2.setEnabled(False)
        elif self.campeonatoSelecionado.quantidadeRounds == 4:
            self.label_R1.setEnabled(True)
            self.comboBoxR1P1.setEnabled(True)
            self.comboBoxR1P2.setEnabled(True)
            self.label_R2.setEnabled(True)
            self.comboBoxR2P1.setEnabled(True)
            self.comboBoxR2P2.setEnabled(True)
            self.label_R3.setEnabled(True)
            self.comboBoxR3P1.setEnabled(True)
            self.comboBoxR3P2.setEnabled(True)
            self.label_R4.setEnabled(True)
            self.comboBoxR4P1.setEnabled(True)
            self.comboBoxR4P2.setEnabled(True)
            self.label_R5.setEnabled(True)
            self.comboBoxR5P1.setEnabled(True)
            self.comboBoxR5P2.setEnabled(True)
            self.label_R6.setEnabled(True)
            self.comboBoxR6P1.setEnabled(True)
            self.comboBoxR6P2.setEnabled(True)
            self.label_R7.setEnabled(True)
            self.comboBoxR7P1.setEnabled(True)
            self.comboBoxR7P2.setEnabled(True)
            self.label_R8.setEnabled(False)
            self.comboBoxR8P1.setEnabled(False)
            self.comboBoxR8P2.setEnabled(False)
            self.label_R9.setEnabled(False)
            self.comboBoxR9P1.setEnabled(False)
            self.comboBoxR9P2.setEnabled(False)
        else:
            self.label_R1.setEnabled(True)
            self.comboBoxR1P1.setEnabled(True)
            self.comboBoxR1P2.setEnabled(True)
            self.label_R2.setEnabled(True)
            self.comboBoxR2P1.setEnabled(True)
            self.comboBoxR2P2.setEnabled(True)
            self.label_R3.setEnabled(True)
            self.comboBoxR3P1.setEnabled(True)
            self.comboBoxR3P2.setEnabled(True)
            self.label_R4.setEnabled(True)
            self.comboBoxR4P1.setEnabled(True)
            self.comboBoxR4P2.setEnabled(True)
            self.label_R5.setEnabled(True)
            self.comboBoxR5P1.setEnabled(True)
            self.comboBoxR5P2.setEnabled(True)
            self.label_R6.setEnabled(True)
            self.comboBoxR6P1.setEnabled(True)
            self.comboBoxR6P2.setEnabled(True)
            self.label_R7.setEnabled(True)
            self.comboBoxR7P1.setEnabled(True)
            self.comboBoxR7P2.setEnabled(True)
            self.label_R8.setEnabled(True)
            self.comboBoxR8P1.setEnabled(True)
            self.comboBoxR8P2.setEnabled(True)
            self.label_R9.setEnabled(True)
            self.comboBoxR9P1.setEnabled(True)
            self.comboBoxR9P2.setEnabled(True)

    def proximaLuta(self):
        self.segundaLuta = True

        # DIGITAR O RESULTADO
        comboBoxesP1 = [self.comboBoxR1P1, self.comboBoxR2P1, self.comboBoxR3P1, self.comboBoxR4P1, self.comboBoxR5P1, self.comboBoxR6P1, self.comboBoxR7P1, self.comboBoxR8P1, self.comboBoxR9P1]
        comboBoxesP2 = [self.comboBoxR1P2, self.comboBoxR2P2, self.comboBoxR3P2, self.comboBoxR4P2, self.comboBoxR5P2, self.comboBoxR6P2, self.comboBoxR7P2, self.comboBoxR8P2, self.comboBoxR9P2]

        if self.campeonatoSelecionado.quantidadeRounds == 1:
            verificarAteComboBox = 1
        elif self.campeonatoSelecionado.quantidadeRounds == 2:
            verificarAteComboBox = 3
        elif self.campeonatoSelecionado.quantidadeRounds == 3:
            verificarAteComboBox = 5
        elif self.campeonatoSelecionado.quantidadeRounds == 4:
            verificarAteComboBox = 7
        else:
            verificarAteComboBox = len(comboBoxesP1)

        resultadoP1 = ''
        for i in range(verificarAteComboBox):
            if comboBoxesP1[i].currentIndex() > 0:
                if comboBoxesP1[i].currentIndex() == 3:
                    resultadoP1 += 'K'
                else:
                    resultadoP1 += comboBoxesP1[i].currentText()[0]
            '''elif comboBoxesP1[i].currentIndex() == 0 and i + 1 < verificarAteComboBox:
                texto = "Resultado não selecionado no round " + str(i + 1) + " do jogador 1. Insira um resultado válido."
                Ui_CadastrarCampeonato.gerarAviso(3, "Erro", texto)
                return'''

        resultadoP2 = ''
        for i in range(verificarAteComboBox):
            if comboBoxesP2[i].currentIndex() > 0:
                if comboBoxesP2[i].currentIndex() == 3:
                    resultadoP2 += 'K'
                else:
                    resultadoP2 += comboBoxesP2[i].currentText()[0]
            '''elif comboBoxesP1[i].currentIndex() == 0 and i + 1 < verificarAteComboBox:
                texto = "Resultado não selecionado no round " + str(i + 1) + " do jogador 2. Insira um resultado válido."
                Ui_CadastrarCampeonato.gerarAviso(3, "Erro", texto)
                return #evita processamentos de resultados incompletos (ex: VD_ x DVV)'''


        # OK

        if self.lutaAtual.preencherResultadoLuta(resultadoP1, resultadoP2) == 1: #se o processamento do resultado for bem sucedido, gravar o resultado da luta no banco
            if self.campeonatoSelecionado.acabarLuta(self.lutaAtual) == 1: # se a computagem dos pontos foi bem sucedida
                # preencher campo resultado e status
                self.resultadoP1.setText(self.lutaAtual.resultadoJogador1)
                self.resultadoP2.setText(self.lutaAtual.resultadoJogador2)
                if self.lutaAtual.jogador1.vitoria == 1:
                    self.statusP1.setText("Vitória")
                    self.statusP2.setText("Derrota")
                elif self.lutaAtual.jogador1.empate == 1:
                    self.statusP1.setText("Empate")
                    self.statusP2.setText("Empate")
                else:
                    self.statusP1.setText("Derrota")
                    self.statusP2.setText("Vitória")

                #preencher o resultado das lutas no banco
                idP1 = str(jogadorDAO().recuperarID(self.lutaAtual.jogador1.nome))
                idP2 = str(jogadorDAO().recuperarID(self.lutaAtual.jogador2.nome))
                idluta = LutaDAO().recuperarIDLuta(self.idCampeonato, idP1, idP2)
                LutaDAO().terminarLuta(idluta, self.lutaAtual)

                # atualizar a pontuação dos jogadores no banco
                jogadorDAO().atualizarPontuacao(idP1, str(self.idCampeonato), self.lutaAtual.jogador1) # erro no commit
                jogadorDAO().atualizarPontuacao(idP2, str(self.idCampeonato), self.lutaAtual.jogador2)
                Ui_CadastrarCampeonato.gerarAviso(1, "Rodada Tekken", "Luta foi salva e finalizada com sucesso")

                #resetar index dos comboboxes selecionados
                for i in range(verificarAteComboBox):
                    comboBoxesP1[i].setCurrentIndex(0)
                    comboBoxesP2[i].setCurrentIndex(0)

                #carregar nova luta
                self.carregarLuta()

            else:
                Ui_CadastrarCampeonato.gerarAviso(3, "Erro", "Resultado inválido. Verifique novamente se não esqueceu de inserir algum resultado em algum round")

    def mostrarTabela(self):
        arquivoPath = open("id.txt", "w")
        arquivoPath.write(str(self.idCampeonato))
        arquivoPath.close()
        #os.system('RodadaTekkenTabela.py')
        form = QtWidgets.QDialog()
        ui2 = Ui_FormPontuacao()
        ui2.setupUi(form)
        form.exec_()

    def mostrarResultados(self):
        arquivoPath = open("id.txt", "w")
        arquivoPath.write(str(self.idCampeonato))
        arquivoPath.close()
        form = QtWidgets.QDialog()
        ui3 = Ui_FormRodadasFinalizadas()
        ui3.setupUi(form)
        form.exec_()

    def alterarResultados(self):
        os.system("cls")
        path = os.getcwd() #peguei o caminho atual
        #path += "\\AlterarResultadoTekken.py" #arquivo python que altera o resultado
        if os.path.exists(path): #se o caminho existe
            if path[0].upper() != 'C': #se nao estiver no C, o prompt do windows vai até o disco que estiver o arquivo atual RodadaTekken.py
                os.system(path[0] + ":")
                os.system("cd " + path)
                if os.path.isfile(path + "\\AlterarResultadoTekken.py"):
                    os.system("AlterarResultadoTekken.py")
            else:
                path += "\\AlterarResultadoTekken.py"
                path = path.replace("\\", "/")
                os.system(path)

        else:
            print("Arquivo não disponível")


    def quemComeca(self):
        form = QtWidgets.QDialog()
        ui4 = Ui_Form()
        ui4.setupUi(form)
        form.exec_()

    def teste(self):
        #selecionando o lado do Player 1 primeiro:
        if self.comboBoxR1P1.currentText() == "Perfect" or self.comboBoxR1P1.currentText() == "Great" or self.comboBoxR1P1.currentText() == "Vitória" or self.comboBoxR1P1.currentText() == "Time Out" or self.comboBoxR1P1.currentText() == "Ring Out":
            self.comboBoxR1P2.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR1P1.currentText() == "Double KO":
            self.comboBoxR1P2.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR2P1.currentText() == "Perfect" or self.comboBoxR2P1.currentText() == "Great" or self.comboBoxR2P1.currentText() == "Vitória" or self.comboBoxR2P1.currentText() == "Time Out" or self.comboBoxR1P1.currentText() == "Ring Out":
            self.comboBoxR2P2.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR2P1.currentText() == "Double KO":
            self.comboBoxR2P2.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR3P1.currentText() == "Perfect" or self.comboBoxR3P1.currentText() == "Great" or self.comboBoxR3P1.currentText() == "Vitória" or self.comboBoxR3P1.currentText() == "Time Out" or self.comboBoxR3P1.currentText() == "Ring Out":
            self.comboBoxR3P2.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR3P1.currentText() == "Double KO":
            self.comboBoxR3P2.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR4P1.currentText() == "Perfect" or self.comboBoxR4P1.currentText() == "Great" or self.comboBoxR4P1.currentText() == "Vitória" or self.comboBoxR4P1.currentText() == "Time Out" or self.comboBoxR4P1.currentText() == "Ring Out":
            self.comboBoxR4P2.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR4P1.currentText() == "Double KO":
            self.comboBoxR4P2.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR5P1.currentText() == "Perfect" or self.comboBoxR5P1.currentText() == "Great" or self.comboBoxR5P1.currentText() == "Vitória" or self.comboBoxR5P1.currentText() == "Time Out" or self.comboBoxR5P1.currentText() == "Ring Out":
            self.comboBoxR5P2.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR5P1.currentText() == "Double KO":
            self.comboBoxR5P2.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR6P1.currentText() == "Perfect" or self.comboBoxR6P1.currentText() == "Great" or self.comboBoxR6P1.currentText() == "Vitória" or self.comboBoxR6P1.currentText() == "Time Out" or self.comboBoxR6P1.currentText() == "Ring Out":
            self.comboBoxR6P2.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR6P1.currentText() == "Double KO":
            self.comboBoxR6P2.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR7P1.currentText() == "Perfect" or self.comboBoxR7P1.currentText() == "Great" or self.comboBoxR7P1.currentText() == "Vitória" or self.comboBoxR7P1.currentText() == "Time Out" or self.comboBoxR7P1.currentText() == "Ring Out":
            self.comboBoxR7P2.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR7P1.currentText() == "Double KO":
            self.comboBoxR7P2.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR8P1.currentText() == "Perfect" or self.comboBoxR8P1.currentText() == "Great" or self.comboBoxR8P1.currentText() == "Vitória" or self.comboBoxR8P1.currentText() == "Time Out" or self.comboBoxR8P1.currentText() == "Ring Out":
            self.comboBoxR8P2.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR8P1.currentText() == "Double KO":
            self.comboBoxR8P2.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR9P1.currentText() == "Perfect" or self.comboBoxR9P1.currentText() == "Great" or self.comboBoxR9P1.currentText() == "Vitória" or self.comboBoxR9P1.currentText() == "Time Out" or self.comboBoxR9P1.currentText() == "Ring Out":
            self.comboBoxR9P2.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR9P1.currentText() == "Double KO":
            self.comboBoxR9P2.setCurrentIndex(self.resultados.index('Double KO'))

        #selecionando o lado do Player 2 primeiro:
        if self.comboBoxR1P2.currentText() == "Perfect" or self.comboBoxR1P2.currentText() == "Great" or self.comboBoxR1P2.currentText() == "Vitória" or self.comboBoxR1P2.currentText() == "Time Out" or self.comboBoxR1P2.currentText() == "Ring Out":
            self.comboBoxR1P1.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR1P2.currentText() == "Double KO":
            self.comboBoxR1P1.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR2P2.currentText() == "Perfect" or self.comboBoxR2P2.currentText() == "Great" or self.comboBoxR2P2.currentText() == "Vitória" or self.comboBoxR2P2.currentText() == "Time Out" or self.comboBoxR1P2.currentText() == "Ring Out":
            self.comboBoxR2P1.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR2P2.currentText() == "Double KO":
            self.comboBoxR2P1.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR3P2.currentText() == "Perfect" or self.comboBoxR3P2.currentText() == "Great" or self.comboBoxR3P2.currentText() == "Vitória" or self.comboBoxR3P2.currentText() == "Time Out" or self.comboBoxR3P2.currentText() == "Ring Out":
            self.comboBoxR3P1.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR3P2.currentText() == "Double KO":
            self.comboBoxR3P1.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR4P2.currentText() == "Perfect" or self.comboBoxR4P2.currentText() == "Great" or self.comboBoxR4P2.currentText() == "Vitória" or self.comboBoxR4P2.currentText() == "Time Out" or self.comboBoxR4P2.currentText() == "Ring Out":
            self.comboBoxR4P1.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR4P2.currentText() == "Double KO":
            self.comboBoxR4P1.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR5P2.currentText() == "Perfect" or self.comboBoxR5P2.currentText() == "Great" or self.comboBoxR5P2.currentText() == "Vitória" or self.comboBoxR5P2.currentText() == "Time Out" or self.comboBoxR5P2.currentText() == "Ring Out":
            self.comboBoxR5P1.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR5P2.currentText() == "Double KO":
            self.comboBoxR5P1.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR6P2.currentText() == "Perfect" or self.comboBoxR6P2.currentText() == "Great" or self.comboBoxR6P2.currentText() == "Vitória" or self.comboBoxR6P2.currentText() == "Time Out" or self.comboBoxR6P2.currentText() == "Ring Out":
            self.comboBoxR6P1.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR6P2.currentText() == "Double KO":
            self.comboBoxR6P1.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR7P2.currentText() == "Perfect" or self.comboBoxR7P2.currentText() == "Great" or self.comboBoxR7P2.currentText() == "Vitória" or self.comboBoxR7P2.currentText() == "Time Out" or self.comboBoxR7P2.currentText() == "Ring Out":
            self.comboBoxR7P1.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR7P2.currentText() == "Double KO":
            self.comboBoxR7P1.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR8P2.currentText() == "Perfect" or self.comboBoxR8P2.currentText() == "Great" or self.comboBoxR8P2.currentText() == "Vitória" or self.comboBoxR8P2.currentText() == "Time Out" or self.comboBoxR8P2.currentText() == "Ring Out":
            self.comboBoxR8P1.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR8P2.currentText() == "Double KO":
            self.comboBoxR8P1.setCurrentIndex(self.resultados.index('Double KO'))

        if self.comboBoxR9P2.currentText() == "Perfect" or self.comboBoxR9P2.currentText() == "Great" or self.comboBoxR9P2.currentText() == "Vitória" or self.comboBoxR9P2.currentText() == "Time Out" or self.comboBoxR9P2.currentText() == "Ring Out":
            self.comboBoxR9P1.setCurrentIndex(len(self.resultados) - 1)
        elif self.comboBoxR9P2.currentText() == "Double KO":
            self.comboBoxR9P1.setCurrentIndex(self.resultados.index('Double KO'))





    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(16, 20, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")

        self.comboBoxCampeonato = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxCampeonato.setGeometry(QtCore.QRect(390, 25, 541, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBoxCampeonato.setFont(font)
        self.comboBoxCampeonato.setObjectName("comboBoxCampeonato")
        self.carregarCampeonatosEmAndamento()
        self.comboBoxCampeonato.currentIndexChanged.connect(self.carregarLuta)

        self.label_rodada = QtWidgets.QLabel(self.centralwidget)
        self.label_rodada.setGeometry(QtCore.QRect(0, 70, 1280, 41))
        self.label_rodada.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_rodada.setFont(font)
        self.label_rodada.setAutoFillBackground(False)
        self.label_rodada.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0.492, y2:0, stop:0 rgba(0, 39, 255, 255), stop:0.994318 rgba(164, 196, 255, 255));\n"
"color: rgb(0, 0, 0);")
        self.label_rodada.setFrameShape(QtWidgets.QFrame.Box)
        self.label_rodada.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_rodada.setScaledContents(False)
        self.label_rodada.setAlignment(QtCore.Qt.AlignCenter)
        self.label_rodada.setObjectName("label_rodada")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(40, 120, 811, 571))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.posicaoAtual_1 = QtWidgets.QLabel(self.frame)
        self.posicaoAtual_1.setGeometry(QtCore.QRect(30, 40, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.posicaoAtual_1.setFont(font)
        self.posicaoAtual_1.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.posicaoAtual_1.setFrameShape(QtWidgets.QFrame.Box)
        self.posicaoAtual_1.setAlignment(QtCore.Qt.AlignCenter)
        self.posicaoAtual_1.setObjectName("posicaoAtual_1")

        self.label_jogador1 = QtWidgets.QLabel(self.frame)
        self.label_jogador1.setGeometry(QtCore.QRect(70, 40, 311, 41))
        font2 = QtGui.QFont()
        font2.setPointSize(12)
        self.label_jogador1.setFont(font2)
        self.label_jogador1.setAutoFillBackground(False)
        self.label_jogador1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.label_jogador1.setFrameShape(QtWidgets.QFrame.Box)
        self.label_jogador1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_jogador1.setObjectName("label_jogador1")

        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(390, 50, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_jogador2 = QtWidgets.QLabel(self.frame)
        self.label_jogador2.setGeometry(QtCore.QRect(420, 40, 311, 41))
        self.label_jogador2.setFont(font2)
        self.label_jogador2.setAutoFillBackground(False)
        self.label_jogador2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.label_jogador2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_jogador2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_jogador2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_jogador2.setObjectName("label_jogador2")

        self.posicaoAtual_2 = QtWidgets.QLabel(self.frame)
        self.posicaoAtual_2.setGeometry(QtCore.QRect(730, 40, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.posicaoAtual_2.setFont(font)
        self.posicaoAtual_2.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.posicaoAtual_2.setFrameShape(QtWidgets.QFrame.Box)
        self.posicaoAtual_2.setAlignment(QtCore.Qt.AlignCenter)
        self.posicaoAtual_2.setObjectName("posicaoAtual_2")
        self.label_R1 = QtWidgets.QLabel(self.frame)
        self.label_R1.setGeometry(QtCore.QRect(370, 230, 54, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_R1.setFont(font)
        self.label_R1.setObjectName("label_R1")
        self.label_R2 = QtWidgets.QLabel(self.frame)
        self.label_R2.setGeometry(QtCore.QRect(370, 260, 54, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_R2.setFont(font)
        self.label_R2.setObjectName("label_R2")
        self.label_R3 = QtWidgets.QLabel(self.frame)
        self.label_R3.setGeometry(QtCore.QRect(370, 290, 54, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_R3.setFont(font)
        self.label_R3.setObjectName("label_R3")
        self.label_R4 = QtWidgets.QLabel(self.frame)
        self.label_R4.setGeometry(QtCore.QRect(370, 320, 54, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_R4.setFont(font)
        self.label_R4.setObjectName("label_R4")
        self.label_R5 = QtWidgets.QLabel(self.frame)
        self.label_R5.setGeometry(QtCore.QRect(370, 350, 54, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_R5.setFont(font)
        self.label_R5.setObjectName("label_R5")
        self.label_R6 = QtWidgets.QLabel(self.frame)
        self.label_R6.setGeometry(QtCore.QRect(370, 380, 54, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_R6.setFont(font)
        self.label_R6.setObjectName("label_R6")
        self.label_R7 = QtWidgets.QLabel(self.frame)
        self.label_R7.setGeometry(QtCore.QRect(370, 410, 54, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_R7.setFont(font)
        self.label_R7.setObjectName("label_R7")
        self.label_R8 = QtWidgets.QLabel(self.frame)
        self.label_R8.setGeometry(QtCore.QRect(370, 440, 54, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_R8.setFont(font)
        self.label_R8.setObjectName("label_R8")
        self.label_R9 = QtWidgets.QLabel(self.frame)
        self.label_R9.setGeometry(QtCore.QRect(370, 470, 54, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_R9.setFont(font)
        self.label_R9.setObjectName("label_R9")

        self.comboBoxR1P1 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR1P1.setGeometry(QtCore.QRect(38, 230, 321, 22))
        self.comboBoxR1P1.setCurrentText("")
        self.comboBoxR1P1.setObjectName("comboBoxR1P1")
        self.comboBoxR1P1.addItems(self.resultados)

        self.comboBoxR2P1 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR2P1.setGeometry(QtCore.QRect(38, 260, 321, 22))
        self.comboBoxR2P1.setCurrentText("")
        self.comboBoxR2P1.setObjectName("comboBoxR2P1")
        self.comboBoxR2P1.addItems(self.resultados)

        self.comboBoxR3P1 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR3P1.setGeometry(QtCore.QRect(38, 290, 321, 22))
        self.comboBoxR3P1.setCurrentText("")
        self.comboBoxR3P1.setObjectName("comboBoxR3P1")
        self.comboBoxR3P1.addItems(self.resultados)

        self.comboBoxR4P1 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR4P1.setGeometry(QtCore.QRect(38, 320, 321, 22))
        self.comboBoxR4P1.setCurrentText("")
        self.comboBoxR4P1.setObjectName("comboBoxR4P1")
        self.comboBoxR4P1.addItems(self.resultados)

        self.comboBoxR5P1 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR5P1.setGeometry(QtCore.QRect(38, 350, 321, 22))
        self.comboBoxR5P1.setCurrentText("")
        self.comboBoxR5P1.setObjectName("comboBoxR5P1")
        self.comboBoxR5P1.addItems(self.resultados)

        self.comboBoxR6P1 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR6P1.setGeometry(QtCore.QRect(38, 380, 321, 22))
        self.comboBoxR6P1.setCurrentText("")
        self.comboBoxR6P1.setObjectName("comboBoxR6P1")
        self.comboBoxR6P1.addItems(self.resultados)

        self.comboBoxR7P1 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR7P1.setGeometry(QtCore.QRect(38, 410, 321, 22))
        self.comboBoxR7P1.setCurrentText("")
        self.comboBoxR7P1.setObjectName("comboBoxR7P1")
        self.comboBoxR7P1.addItems(self.resultados)

        self.comboBoxR8P1 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR8P1.setGeometry(QtCore.QRect(38, 440, 321, 22))
        self.comboBoxR8P1.setCurrentText("")
        self.comboBoxR8P1.setObjectName("comboBoxR8P1")
        self.comboBoxR8P1.addItems(self.resultados)

        self.comboBoxR9P1 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR9P1.setGeometry(QtCore.QRect(40, 470, 321, 22))
        self.comboBoxR9P1.setCurrentText("")
        self.comboBoxR9P1.setObjectName("comboBoxR9P1")
        self.comboBoxR9P1.addItems(self.resultados)

        self.comboBoxR2P2 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR2P2.setGeometry(QtCore.QRect(430, 260, 321, 22))
        self.comboBoxR2P2.setCurrentText("")
        self.comboBoxR2P2.setObjectName("comboBoxR2P2")
        self.comboBoxR2P2.addItems(self.resultados)

        self.comboBoxR3P2 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR3P2.setGeometry(QtCore.QRect(430, 290, 321, 22))
        self.comboBoxR3P2.setCurrentText("")
        self.comboBoxR3P2.setObjectName("comboBoxR3P2")
        self.comboBoxR3P2.addItems(self.resultados)

        self.comboBoxR5P2 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR5P2.setGeometry(QtCore.QRect(430, 350, 321, 22))
        self.comboBoxR5P2.setCurrentText("")
        self.comboBoxR5P2.setObjectName("comboBoxR5P2")
        self.comboBoxR5P2.addItems(self.resultados)

        self.comboBoxR4P2 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR4P2.setGeometry(QtCore.QRect(430, 320, 321, 22))
        self.comboBoxR4P2.setCurrentText("")
        self.comboBoxR4P2.setObjectName("comboBoxR4P2")
        self.comboBoxR4P2.addItems(self.resultados)

        self.comboBoxR9P2 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR9P2.setGeometry(QtCore.QRect(430, 470, 321, 22))
        self.comboBoxR9P2.setCurrentText("")
        self.comboBoxR9P2.setObjectName("comboBoxR9P2")
        self.comboBoxR9P2.addItems(self.resultados)

        self.comboBoxR8P2 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR8P2.setGeometry(QtCore.QRect(430, 440, 321, 22))
        self.comboBoxR8P2.setCurrentText("")
        self.comboBoxR8P2.setObjectName("comboBoxR8P2")
        self.comboBoxR8P2.addItems(self.resultados)

        self.comboBoxR6P2 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR6P2.setGeometry(QtCore.QRect(430, 380, 321, 22))
        self.comboBoxR6P2.setCurrentText("")
        self.comboBoxR6P2.setObjectName("comboBoxR6P2")
        self.comboBoxR6P2.addItems(self.resultados)

        self.comboBoxR7P2 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR7P2.setGeometry(QtCore.QRect(430, 410, 321, 22))
        self.comboBoxR7P2.setCurrentText("")
        self.comboBoxR7P2.setObjectName("comboBoxR7P2")
        self.comboBoxR7P2.addItems(self.resultados)

        self.comboBoxR1P2 = QtWidgets.QComboBox(self.frame)
        self.comboBoxR1P2.setGeometry(QtCore.QRect(430, 230, 321, 22))
        self.comboBoxR1P2.setCurrentText("")
        self.comboBoxR1P2.setObjectName("comboBoxR1P2")
        self.comboBoxR1P2.addItems(self.resultados)

        self.comboBoxR1P1.currentIndexChanged.connect(self.teste)
        self.comboBoxR2P1.currentIndexChanged.connect(self.teste)
        self.comboBoxR3P1.currentIndexChanged.connect(self.teste)
        self.comboBoxR4P1.currentIndexChanged.connect(self.teste)
        self.comboBoxR5P1.currentIndexChanged.connect(self.teste)
        self.comboBoxR6P1.currentIndexChanged.connect(self.teste)
        self.comboBoxR7P1.currentIndexChanged.connect(self.teste)
        self.comboBoxR8P1.currentIndexChanged.connect(self.teste)
        self.comboBoxR9P1.currentIndexChanged.connect(self.teste)
        self.comboBoxR1P2.currentIndexChanged.connect(self.teste)
        self.comboBoxR2P2.currentIndexChanged.connect(self.teste)
        self.comboBoxR3P2.currentIndexChanged.connect(self.teste)
        self.comboBoxR4P2.currentIndexChanged.connect(self.teste)
        self.comboBoxR5P2.currentIndexChanged.connect(self.teste)
        self.comboBoxR6P2.currentIndexChanged.connect(self.teste)
        self.comboBoxR7P2.currentIndexChanged.connect(self.teste)
        self.comboBoxR8P2.currentIndexChanged.connect(self.teste)
        self.comboBoxR9P2.currentIndexChanged.connect(self.teste)

        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(40, 510, 52, 13))
        self.label_3.setObjectName("label_3")
        self.resultadoP1 = QtWidgets.QLineEdit(self.frame)
        self.resultadoP1.setGeometry(QtCore.QRect(100, 507, 261, 20))
        self.resultadoP1.setReadOnly(True)
        self.resultadoP1.setObjectName("resultadoP1")
        self.resultadoP2 = QtWidgets.QLineEdit(self.frame)
        self.resultadoP2.setGeometry(QtCore.QRect(430, 507, 261, 20))
        self.resultadoP2.setReadOnly(True)
        self.resultadoP2.setObjectName("resultadoP2")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(40, 533, 52, 13))
        self.label_4.setObjectName("label_4")
        self.statusP1 = QtWidgets.QLineEdit(self.frame)
        self.statusP1.setGeometry(QtCore.QRect(100, 530, 261, 20))
        self.statusP1.setReadOnly(True)
        self.statusP1.setObjectName("statusP1")
        self.statusP2 = QtWidgets.QLineEdit(self.frame)
        self.statusP2.setGeometry(QtCore.QRect(430, 530, 261, 20))
        self.statusP2.setReadOnly(True)
        self.statusP2.setObjectName("statusP2")

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(700, 505, 101, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.proximaLuta)
        self.pushButton.setEnabled(False)

        self.label_luta = QtWidgets.QLabel(self.frame)
        self.label_luta.setGeometry(QtCore.QRect(380, 15, 60, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_luta.setFont(font)
        self.label_luta.setObjectName("label_luta")
        self.label_jogador1.raise_()
        self.label_2.raise_()
        self.label_jogador2.raise_()
        self.posicaoAtual_2.raise_()
        self.posicaoAtual_1.raise_()
        self.label_R1.raise_()
        self.label_R2.raise_()
        self.label_R3.raise_()
        self.label_R4.raise_()
        self.label_R5.raise_()
        self.label_R6.raise_()
        self.label_R7.raise_()
        self.label_R8.raise_()
        self.label_R9.raise_()
        self.comboBoxR1P1.raise_()
        self.comboBoxR2P1.raise_()
        self.comboBoxR3P1.raise_()
        self.comboBoxR4P1.raise_()
        self.comboBoxR5P1.raise_()
        self.comboBoxR6P1.raise_()
        self.comboBoxR7P1.raise_()
        self.comboBoxR8P1.raise_()
        self.comboBoxR9P1.raise_()
        self.comboBoxR2P2.raise_()
        self.comboBoxR3P2.raise_()
        self.comboBoxR5P2.raise_()
        self.comboBoxR4P2.raise_()
        self.comboBoxR9P2.raise_()
        self.comboBoxR8P2.raise_()
        self.comboBoxR6P2.raise_()
        self.comboBoxR7P2.raise_()
        self.comboBoxR1P2.raise_()
        self.label_3.raise_()
        self.resultadoP1.raise_()
        self.resultadoP2.raise_()
        self.label_4.raise_()
        self.statusP1.raise_()
        self.statusP2.raise_()
        self.pushButton.raise_()
        self.label_luta.raise_()

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(870, 120, 341, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.quemComeca)
        self.pushButton_2.setEnabled(False)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(870, 300, 341, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.mostrarTabela)
        self.pushButton_3.setEnabled(False)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(870, 210, 341, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.mostrarResultados)
        self.pushButton_4.setEnabled(False)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(870, 400, 341, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.alterarResultados)
        self.pushButton_5.setEnabled(False)

        self.frame.raise_()
        self.label.raise_()
        self.comboBoxCampeonato.raise_()
        self.label_rodada.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.pushButton_5.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rodada Tekken"))
        self.label.setText(_translate("MainWindow", "Selecione o campeonato"))
        self.label_rodada.setText(_translate("MainWindow", "RODADA 1"))
        self.posicaoAtual_1.setText(_translate("MainWindow", "01"))
        self.label_jogador1.setText(_translate("MainWindow", "Nome do jogador"))
        self.label_2.setText(_translate("MainWindow", "VS"))
        self.label_jogador2.setText(_translate("MainWindow", "Nome do jogador"))
        self.posicaoAtual_2.setText(_translate("MainWindow", "01"))
        self.label_R1.setText(_translate("MainWindow", "Round 1"))
        self.label_R2.setText(_translate("MainWindow", "Round 2"))
        self.label_R3.setText(_translate("MainWindow", "Round 3"))
        self.label_R4.setText(_translate("MainWindow", "Round 4"))
        self.label_R5.setText(_translate("MainWindow", "Round 5"))
        self.label_R6.setText(_translate("MainWindow", "Round 6"))
        self.label_R7.setText(_translate("MainWindow", "Round 7"))
        self.label_R8.setText(_translate("MainWindow", "Round 8"))
        self.label_R9.setText(_translate("MainWindow", "Round 9"))
        self.label_3.setText(_translate("MainWindow", "Resultado:"))
        self.label_4.setText(_translate("MainWindow", "Status:"))
        self.pushButton.setText(_translate("MainWindow", "Próxima\n"
"Luta"))
        self.label_luta.setText(_translate("MainWindow", "Luta 1"))
        self.pushButton_2.setText(_translate("MainWindow", "Quem é o lutador\nda esquerda?"))
        self.pushButton_3.setText(_translate("MainWindow", "Consultar tabela\n"
" do campeonato"))
        self.pushButton_4.setText(_translate("MainWindow", "Consultar resultados\n"
"anteriores"))
        self.pushButton_5.setText(_translate("MainWindow", "Alterar resultado"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_RodadaTekken()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())