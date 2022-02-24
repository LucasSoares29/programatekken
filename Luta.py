from TekkenNovoCampeonato import *

class Luta(object):

    combinacoes_validas_um_round = ["PD", "GD", "VD", "TD", "RD", "KK", "DT", "DV", "DG", "DR", "DP"]

    def __init__(self, jogador1, jogador2, rodada):
        self.jogador1 = jogador1 #string ou objeto Jogador
        self.jogador2 = jogador2 #string ou objeto Jogador
        self.rodada = rodada
        self.finalizada = 0

    def preencherResultadoLuta(self, resultadoJogador1, resultadoJogador2):

        # VERIFICAR VALIDADE DAS DUAS STRINGS
        for i in range(len(resultadoJogador1)):
            combinacao = str(resultadoJogador1[i]) + str(resultadoJogador2[i])
            if not(combinacao in self.combinacoes_validas_um_round):
                texto = "A combinação de resultados no " + str(i + 1) + "º round não é válida!"
                Ui_CadastrarCampeonato.gerarAviso(3, "Erro", texto)
                return 0

        self.resultadoJogador1 = resultadoJogador1
        self.resultadoJogador2 = resultadoJogador2
        return 1




    '''
    def calcularPontuacaoJogadorLuta(self, Campeonato, Jogador):
        Jogador.pontos = ((Campeonato.vitoria * Jogador.vitoria) + (Campeonato.empate * Jogador.empate) + (Campeonato.perfect * Jogador.perfect) + (Campeonato.great * Jogador.great) + (Campeonato.doubleKO * Jogador.doubleKO) + (Campeonato.roundGanho * Jogador.roundGanho) + (Campeonato.timeOut * Jogador.timeout)) - ((Campeonato.roundPerdido * Jogador.roundPerdido) + (Campeonato.perfectContra * Jogador.perfectsContra) + (Campeonato.greatContra * Jogador.greatsContra) + (Campeonato.derrota * Jogador.derrota))
    '''






