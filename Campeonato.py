from datetime import datetime
from Luta import *
from Jogador import *
from LutaDAO import *
from JogadorDAO import *

class Campeonato(object):

    def __init__(self, nome, inicio, quantidadeRounds, pontuacaoVitoria, pontuacaoEmpate, pontuacaoDerrota, pontuacaoPerfect, pontuacaoGreat, pontuacaoDoubleKO, pontuacaoRndGanho, pontuacaoTimeOut, pontuacaoRndPerdido, pontuacaoPerfectContra, pontuacaoGreatContra):

        self.nome = nome

        '''
        .date() retorna apenas ano-mes-dia
        .strptime() converte string para o estilo da data
        '''

        dataInicio = datetime.strptime(inicio, "%d/%m/%Y").date() # CONVERTO STRING PARA DATETIME. O .date() CONVERTE DATETIME PARA DATE


        self.inicio = dataInicio
        self.status = 'INICIADO'
        self.quantidadeRounds = quantidadeRounds
        self.vitoria = pontuacaoVitoria
        self.empate = pontuacaoEmpate
        self.derrota = pontuacaoDerrota
        self.perfect = pontuacaoPerfect
        self.great = pontuacaoGreat
        self.doubleKO = pontuacaoDoubleKO
        self.roundGanho = pontuacaoRndGanho
        self.timeOut = pontuacaoTimeOut
        self.roundPerdido = pontuacaoRndPerdido
        self.perfectContra = pontuacaoPerfectContra
        self.greatContra = pontuacaoGreatContra
        self.temRingOut = False
        self.ringOut = 0

    def adicionarRingOut(self, pontuacaoRingOut):
        self.temRingOut = True
        self.ringOut = pontuacaoRingOut

    def adicionarInformacoes(self, teraFase2, primeiroNaFinal,  quantosNaFase2, ultimoEliminado):
        self.teraFase2 = teraFase2
        self.primeiroNaFinal = primeiroNaFinal
        self.quantosNaFase2 = quantosNaFase2
        self.ultimoEliminado = ultimoEliminado

    def gerarRodadas(self, times):

        """
            @times:parameter

        Recebe como parâmetro uma tupla de times (1, 2, 3...) e o método converte-os para listas [1, 2, 3,...]
        para que gere as partidas no sistema de Round Robin


        """
        ListaDeLutas = []
        temp = []
        qtdTimes = len(times)
        #output = open("outputRodadas.txt", "w")

        if qtdTimes % 2 == 0:
            rodadas = qtdTimes - 1
            jogosPorRodada = int((len(times)/ 2))
        else:
            rodadas = qtdTimes
            times.append(0) #time falso
            jogosPorRodada = int((len(times)/ 2)) - 1

        if len(times) > 1:
            for i in range(1, rodadas + 1):
                if i > 1:
                    # AQUI SERÁ FEITA A MOVIMENTAÇÃO DOS TIMES NO SENTIDO HORÁRIO (ROUND ROBIN)
                    for positivo in range(1, len(times)):
                        temp.append(times[positivo])
                    times[1:] = []
                    fim = len(temp) - 1
                    qtdTemp = len(temp)
                    while len(temp) > 0:
                        if len(temp) == qtdTemp:
                            times.append(temp.pop(fim)) # O ultimo time é passado para a frente
                        else:
                            times.append(temp.pop(0)) # Os demais times avançam uma posição

                #print("\nRodada " + str(i))

                '''if i > 1:
                    output.write("\nRodada " + str(i) + "\n")
                else:
                    output.write("Rodada " + str(i) + "\n")'''

                if qtdTimes % 2 == 0:
                    for j in range(0, jogosPorRodada):
                        luta = Luta(jogador1=times[j], jogador2=times[-(j + 1)], rodada=i)
                        ListaDeLutas.append(luta)
                else:
                    j = 0
                    while j <= jogosPorRodada:
                        if times[j] != 0 and times[-(j + 1)] != 0:
                            luta = Luta(jogador1=times[j], jogador2=times[-(j + 1)], rodada=i)
                            ListaDeLutas.append(luta)
                        j += 1

        return ListaDeLutas

    def acabarLuta(self, Luta):


        """

        Este método faz o processamento de uma luta através do resultado informado (atributo da classe Luta); computa a pontuação conquistada pelos
        jogadores na partida e atualiza o status do objeto da classe Luta para "Finalizada"

        :param Luta: Recebe o objeto da classe Luta como parâmetro
        :return:
        """

        roundP1 = 0
        roundP2 = 0


        # PROCESSANDO OS ROUNDS
        for index in range(len(Luta.resultadoJogador1)):
            if roundP1 == self.quantidadeRounds: #casos de digitar VVV x DDD numa luta de 2 rounds
                break
            if Luta.resultadoJogador1[index] == 'P':
                Luta.jogador1.incrementarPerfect()
                roundP1 += 1
                Luta.jogador2.incrementarPerfectContra()
                #Luta.jogador2.incrementarRoundPerdido()
            elif Luta.resultadoJogador1[index] == 'G':
                Luta.jogador1.incrementarGreats()
                roundP1 += 1
                Luta.jogador2.incrementarGreatsContra()
                #Luta.jogador2.incrementarRoundPerdido()
            elif Luta.resultadoJogador1[index] == 'K':
                Luta.jogador1.incrementarDoubleKO()
                Luta.jogador2.incrementarDoubleKO()
                roundP1 += 1
                roundP2 += 1
            elif Luta.resultadoJogador1[index] == 'V':
                Luta.jogador1.incrementarRoundsSimples()
                roundP1 += 1
                Luta.jogador2.incrementarRoundPerdido()
            elif Luta.resultadoJogador1[index] == 'T':
                Luta.jogador1.incrementarTimeOut()
                roundP1 += 1
                Luta.jogador2.incrementarRoundPerdido()
            elif Luta.resultadoJogador1[index] == 'R':
                Luta.jogador1.incrementarRingOut()
                roundP1 += 1
                Luta.jogador2.incrementarRoundPerdido()
            elif Luta.resultadoJogador1[index] == 'D':
                if roundP2 == self.quantidadeRounds or Luta.jogador1.derrota + Luta.jogador1.perfectsContra + Luta.jogador1.greatsContra == self.quantidadeRounds: #casos de digitar DDD x VVV numa luta de 2 rounds e computar 3 derrotas pro P1
                    break
                roundP2 += 1
                if Luta.resultadoJogador2[index] == 'P':
                    Luta.jogador2.incrementarPerfect()
                    Luta.jogador1.incrementarPerfectContra()
                elif Luta.resultadoJogador2[index] == 'G':
                    Luta.jogador2.incrementarGreats()
                    Luta.jogador1.incrementarGreatsContra()
                elif Luta.resultadoJogador2[index] == 'V':
                    Luta.jogador2.incrementarRoundsSimples()
                    Luta.jogador1.incrementarRoundPerdido()
                elif Luta.resultadoJogador2[index] == 'T':
                    Luta.jogador2.incrementarTimeOut()
                    Luta.jogador1.incrementarRoundPerdido()
                elif Luta.resultadoJogador2[index] == 'R':
                    Luta.jogador2.incrementarRingOut()
                    Luta.jogador1.incrementarRoundPerdido()

        # DEFINIR O VENCEDOR DA LUTA
        if roundP1 == self.quantidadeRounds:
            if roundP2 == roundP1: # 2 x 2 numa luta de 2 rounds
                Luta.jogador1.incrementarEmpate()
                Luta.jogador2.incrementarEmpate()
            else: # 2 x 0 ou 2 x 1  numa luta de 2 rounds
                Luta.jogador1.incrementarVitoria()
                Luta.jogador2.incrementarDerrota()
        elif roundP2 == self.quantidadeRounds: #1 x 2 numa luta de 2 rounds
            Luta.jogador2.incrementarVitoria()
            Luta.jogador1.incrementarDerrota()
        else: # 1 x 1 numa luta de 2 rounds.
            print("O resultado é inválido")
            return 0

        # CALCULAR A PONTUAÇÃO DA LUTA DOS JOGADORES
        Luta.jogador1.pontos = (self.vitoria * Luta.jogador1.vitoria) + (self.empate * Luta.jogador1.empate) + (self.perfect * Luta.jogador1.perfects) + (self.great * Luta.jogador1.greats) + (self.doubleKO * Luta.jogador1.doubleKO) + (self.roundGanho * Luta.jogador1.roundsimples) + (self.timeOut * Luta.jogador1.timeout) + (self.ringOut * Luta.jogador1.ringout) - (self.roundPerdido * Luta.jogador1.roundPerdido) - (self.perfectContra * Luta.jogador1.perfectsContra) - (self.greatContra * Luta.jogador1.greatsContra) - (self.derrota * Luta.jogador1.derrota)
        Luta.jogador2.pontos = (self.vitoria * Luta.jogador2.vitoria) + (self.empate * Luta.jogador2.empate) + (self.perfect * Luta.jogador2.perfects) + (self.great * Luta.jogador2.greats) + (self.doubleKO * Luta.jogador2.doubleKO) + (self.roundGanho * Luta.jogador2.roundsimples) + (self.timeOut * Luta.jogador2.timeout) + (self.ringOut * Luta.jogador2.ringout) - (self.roundPerdido * Luta.jogador2.roundPerdido) - (self.perfectContra * Luta.jogador2.perfectsContra) - (self.greatContra * Luta.jogador2.greatsContra) - (self.derrota * Luta.jogador2.derrota)
        Luta.jogador1.atualizarSaldoRounds()
        Luta.jogador2.atualizarSaldoRounds()

        # FINALIZAR LUTA
        Luta.finalizada = True;
        return 1


'''
if __name__ == "__main__":

    # SIMULAÇÃO DE UMA LUTA
    tekken = Campeonato("Teste2", "18/06/2017", 2, 3, 1, 0, 2.5, 2, 1.5, 1, 0.5, 0.5, 3, 0.25)
    heihachi = Jogador("Heihachi", "Japão")
    asuka = Jogador("Asuka", "Japão")
    partida = Luta(heihachi, asuka, 1)
    # teste 1 - resultado invalido: TESTE OK
    #partida.preencherResultadoLuta("VV", "DV")

    #teste 2 - resultado valido
    partida.preencherResultadoLuta("PDG", "DVD")
    tekken.acabarLuta(partida)'''