import pymysql
from Jogador import Jogador
from CampeonatoDAO import *

class jogadorDAO(object):

        host = '192.168.0.101'
        port = 3308

        def recuperarID(self, nome):
            try:
                conexao3 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao3.cursor()
                sql = "select idjogador from jogador where nome like %s;"
                cursor.execute(sql, (nome,))
                return cursor.fetchone()[0]
            except TypeError: #se não achar resultado
                return 0
            except Exception as e:
                print(type(e))
                print("Erro de conexão")
            finally:
                cursor.close()
                conexao3.close()

        def cadastrarJogador(self, Jogador):
            try:
                conexao3 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao3.cursor()
                sql = "insert into jogador(nome, nacionalidade) values(%s, %s);"
                cursor.execute(sql, (Jogador.nome, Jogador.nacionalidade,))
                conexao3.commit()
                print("Jogador cadastrado")
            except pymysql.err.IntegrityError:
                print("Já há este nome cadastrado. Mude o nome")
            except Exception:
                print(type(e))
                print("Erro de conexão")
            finally:
                cursor.close()
                conexao3.close()

        def recuperarJogador(self, nome):
            conexao3 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
            cursor = conexao3.cursor()
            sql = "select nome, nacionalidade from jogador where nome like %s;"
            cursor.execute(sql, (nome,))
            row = cursor.fetchone()
            jogador = Jogador(row[0], row[1])
            cursor.close()
            conexao3.close()
            return jogador

        def listaDeJogadores(self):
            conexao3 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
            cursor = conexao3.cursor()
            jogadores = []
            sql = "select nome, nacionalidade from jogador order by 1"
            cursor.execute(sql)
            for row in cursor.fetchall():
                texto = row[0] + ' (' + row[1] + ')'
                jogadores.append(texto)
            cursor.close()
            conexao3.close()
            return jogadores

        def pontuacaoAtualJogador(self, idjogador, idcampeonato):

            j = Jogador(None, None)

            try:
                conexao4 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao4.cursor()
                sql = "select * from tabela where idtorneio = %s and idjogador = %s;"
                cursor.execute(sql, (str(idcampeonato), str(idjogador)))
                dados = list(cursor.fetchone())
                cursor.close()
                conexao4.close()
                j.pontos = dados[3]
                j.vitoria = dados[5]
                j.empate = dados[6]
                j.derrota = dados[7]
                j.perfects = dados[8]
                j.greats = dados[9]
                j.doubleKO = dados[10]
                j.roundsimples = dados[11]
                j.timeout = dados[12]
                j.ringout = dados[13]
                j.roundPerdido = dados[14]
                j.perfectsContra = dados[16]
                j.greatsContra = dados[17]
                j.atualizarSaldoRounds()
                return j
            except Exception as e:
                print(type(e))

        def atualizarPontuacao(self, idJogador, idCampeonato, Jogador):
            """
            Atualizará a pontuação do jogador no campeonato. Recebe como parâmetro a identificação do jogador e do campeonato. Além dos
            dados a atualizar armazenados na classe Jogador.
            :param idJogador:
            :param idCampeonato:
            :param Jogador: objeto da classe Jogador
            :return:
            """

            try:
                conexao3 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao3.cursor()
                 # sql recuperar pontuacao atual do jogador

                jogadorPontuacaoAtual = self.pontuacaoAtualJogador(idJogador, idCampeonato)

                #somar resultado
                jogadorPontuacaoAtual.pontos += Jogador.pontos
                jogadorPontuacaoAtual.vitoria += Jogador.vitoria
                jogadorPontuacaoAtual.empate += Jogador.empate
                jogadorPontuacaoAtual.derrota += Jogador.derrota
                jogadorPontuacaoAtual.rodadas = jogadorPontuacaoAtual.vitoria + jogadorPontuacaoAtual.empate + jogadorPontuacaoAtual.derrota
                jogadorPontuacaoAtual.perfects += Jogador.perfects
                jogadorPontuacaoAtual.greats += Jogador.greats
                jogadorPontuacaoAtual.doubleKO += Jogador.doubleKO
                jogadorPontuacaoAtual.roundsimples += Jogador.roundsimples
                jogadorPontuacaoAtual.timeout += Jogador.timeout
                jogadorPontuacaoAtual.ringout += Jogador.ringout
                jogadorPontuacaoAtual.roundPerdido += Jogador.roundPerdido
                jogadorPontuacaoAtual.perfectsContra += Jogador.perfectsContra
                jogadorPontuacaoAtual.greatsContra += Jogador.greatsContra
                jogadorPontuacaoAtual.atualizarSaldoRounds()

                #atualizar no banco
                sql = "update tabela set pontos = %s, rodadas =  %s, vitorias = %s, empates = %s, derrotas = %s, perfect = %s, great = %s, doubleko = %s, roundganho = %s, timeout = %s, ringout = %s, roundperdido = %s, saldorounds = %s, perfectcontra = %s, greatcontra = %s where idjogador = %s and idtorneio = %s"
                cursor.execute(sql, (jogadorPontuacaoAtual.pontos, str(jogadorPontuacaoAtual.rodadas), str(jogadorPontuacaoAtual.vitoria), str(jogadorPontuacaoAtual.empate), str(jogadorPontuacaoAtual.derrota), str(jogadorPontuacaoAtual.perfects), str(jogadorPontuacaoAtual.greats), str(jogadorPontuacaoAtual.doubleKO), str(jogadorPontuacaoAtual.roundsimples), str(jogadorPontuacaoAtual.timeout), str(jogadorPontuacaoAtual.ringout), str(jogadorPontuacaoAtual.roundPerdido), str(jogadorPontuacaoAtual.saldoRounds), str(jogadorPontuacaoAtual.perfectsContra), str(jogadorPontuacaoAtual.greatsContra), str(idJogador), str(idCampeonato)))
                conexao3.commit()
                cursor.close()
                conexao3.close()
            except Exception as e:
                print(type(e))
                print(e)

        def subtrairPontuacao(self, idJogador, idCampeonato, Jogador):
            """
            Subtrairá a pontuação do jogador no campeonato em caso de alteração dos resultados. Recebe como parâmetro a identificação do jogador e do campeonato. Além dos
            dados a atualizar armazenados na classe Jogador.
            :param idJogador:
            :param idCampeonato:
            :param Jogador: objeto da classe Jogador
            :return:
            """

            try:
                conexao3 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao3.cursor()
                 # sql recuperar pontuacao atual do jogador

                jogadorPontuacaoAtual = self.pontuacaoAtualJogador(idJogador, idCampeonato)

                #somar resultado
                jogadorPontuacaoAtual.pontos -= Jogador.pontos
                jogadorPontuacaoAtual.vitoria -= Jogador.vitoria
                jogadorPontuacaoAtual.empate -= Jogador.empate
                jogadorPontuacaoAtual.derrota -= Jogador.derrota
                jogadorPontuacaoAtual.rodadas = jogadorPontuacaoAtual.vitoria + jogadorPontuacaoAtual.empate + jogadorPontuacaoAtual.derrota
                jogadorPontuacaoAtual.perfects -= Jogador.perfects
                jogadorPontuacaoAtual.greats -= Jogador.greats
                jogadorPontuacaoAtual.doubleKO -= Jogador.doubleKO
                jogadorPontuacaoAtual.roundsimples -= Jogador.roundsimples
                jogadorPontuacaoAtual.timeout -= Jogador.timeout
                jogadorPontuacaoAtual.ringout -= Jogador.ringout
                jogadorPontuacaoAtual.roundPerdido -= Jogador.roundPerdido
                jogadorPontuacaoAtual.perfectsContra -= Jogador.perfectsContra
                jogadorPontuacaoAtual.greatsContra -= Jogador.greatsContra
                jogadorPontuacaoAtual.atualizarSaldoRounds()

                #atualizar no banco
                sql = "update tabela set pontos = %s, rodadas =  %s, vitorias = %s, empates = %s, derrotas = %s, perfect = %s, great = %s, doubleko = %s, roundganho = %s, timeout = %s, ringout = %s, roundperdido = %s, saldorounds = %s, perfectcontra = %s, greatcontra = %s where idjogador = %s and idtorneio = %s"
                cursor.execute(sql, (jogadorPontuacaoAtual.pontos, str(jogadorPontuacaoAtual.rodadas), str(jogadorPontuacaoAtual.vitoria), str(jogadorPontuacaoAtual.empate), str(jogadorPontuacaoAtual.derrota), str(jogadorPontuacaoAtual.perfects), str(jogadorPontuacaoAtual.greats), str(jogadorPontuacaoAtual.doubleKO), str(jogadorPontuacaoAtual.roundsimples), str(jogadorPontuacaoAtual.timeout), str(jogadorPontuacaoAtual.ringout), str(jogadorPontuacaoAtual.roundPerdido), str(jogadorPontuacaoAtual.saldoRounds), str(jogadorPontuacaoAtual.perfectsContra), str(jogadorPontuacaoAtual.greatsContra), str(idJogador), str(idCampeonato)))
                conexao3.commit()
                cursor.close()
                conexao3.close()
            except Exception as e:
                print(type(e))
                print(e)

        def posicaoAtual(self, nomeDoJogador, tabelaCampeonato):
            posicao = 1
            for linha in tabelaCampeonato:
                if linha[0] == nomeDoJogador:
                    return posicao
                else:
                    posicao += 1
            return 0


'''
if __name__ == "__main__":
    #j = Jogador("Lucas", "Brasil")
    #jogadorDAO().cadastrarJogador(j)
    j = jogadorDAO().recuperarJogador("Lucas")
    print(j.nome)
    print(j.nacionalidade)'''