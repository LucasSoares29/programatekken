class Jogador(object):

    def __init__(self, nome, nacionalidade):
        self.nome = nome
        self.nacionalidade = nacionalidade
        self.iniciarPontuacaoCampeonato()

    def iniciarPontuacaoCampeonato(self):
        self.pontos = 0.0
        self.rodadas = 0
        self.vitoria = 0
        self.empate = 0
        self.derrota = 0
        self.perfects = 0
        self.greats = 0
        self.doubleKO = 0
        self.roundsimples = 0
        self.timeout = 0
        self.ringout = 0
        self.roundPerdido = 0
        self.saldoRounds = 0
        self.perfectsContra = 0
        self.greatsContra = 0

    '''
    def pontuacaoAtual(self, P, V, E, D, PERF, G, DKO, RS, TO, RP, PC, GC):
        self.pontos = P
        self.vitoria = V
        self.empate = E
        self.derrota = D
        self.perfects = PERF
        self.greats = G
        self.doubleKO = DKO
        self.roundsimples = RS
        self.timeout = TO
        self.roundPerdido = RP
        self.perfectsContra = PC
        self.greatsContra = GC
        self.rodadas = V + E + D
        self.atualizarSaldoRounds()'''

    def incrementarVitoria(self):
        self.vitoria += 1

    def incrementarEmpate(self):
        self.empate += 1

    def incrementarDerrota(self):
        self.derrota += 1

    def incrementarPerfect(self):
        self.perfects += 1

    def incrementarGreats(self):
        self.greats += 1

    def incrementarDoubleKO(self):
        self.doubleKO += 1

    def incrementarRoundsSimples(self):
        self.roundsimples += 1

    def incrementarTimeOut(self):
        self.timeout += 1

    def incrementarRingOut(self):
        self.ringout += 1

    def incrementarRoundPerdido(self):
        self.roundPerdido += 1

    def incrementarPerfectContra(self):
        self.perfectsContra += 1

    def incrementarGreatsContra(self):
        self.greatsContra += 1

    def atualizarSaldoRounds(self):
        self.saldoRounds = (self.perfects + self.greats + self.doubleKO + self.roundsimples + self.timeout + self.ringout) - self.roundPerdido - self.perfectsContra - self.greatsContra

    def exibirPontuacao(self):
        print("Pontuação atual do jogador " + self.nome)
        print("Total de pontos: " + str(self.pontos))
        print("Total de rodadas: " + str(self.vitoria + self.empate + self.derrota))
        print("Total de vitórias: " + str(self.vitoria))
        print("Total de empates: " + str(self.empate))
        print("Total de derrotas: " + str(self.derrota))
        print("Total de perfects: " + str(self.perfects))
        print("Total de greats: " + str(self.greats))
        print("Total de double KO: " + str(self.doubleKO))
        print("Total de rounds ganhos: " + str(self.roundsimples))
        print("Total de timeout: " + str(self.timeout))
        print("Total de ring outs: " + str(self.ringout))
        print("Total de round perdidos: " + str(self.roundPerdido))
        print("Total de perfects tomados: " + str(self.perfectsContra))
        print("Total de greatsContra: " + str(self.greatsContra))
        print("Total de saldo de Rounds: " + str(self.saldoRounds) + "\n")




