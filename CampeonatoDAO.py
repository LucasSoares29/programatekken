import pymysql
from Campeonato import *
from Jogador import *
from JogadorDAO import jogadorDAO
from datetime import datetime

class CampeonatoDAO(object):

    host = 'localhost'
    port=3308

    def recuperarID(self, nome):
        try:
            conexao = pymysql.connect(host=self.host, user='root', db='tekken', port=self.port)
            cursor = conexao.cursor()
            sql = "select idtorneio from torneio where nome like %s;"
            cursor.execute(sql, (nome,))
            id = cursor.fetchone()[0]
            cursor.close()
            conexao.close()
            return id
        except Exception as e:
                print(type(e))

    def listarCampeonatos(self):

        nomeDosCampeonatos = []
        try:
            conexao = pymysql.connect(host=self.host, user='root', db='tekken', port=self.port)
            cursor = conexao.cursor()
            sql = "select nome from torneio where status = 'INICIADO'"
            cursor.execute(sql)
            for row in cursor.fetchall():
                nomeDosCampeonatos.append(str(row[0]))
            cursor.close()
            conexao.close()
            return nomeDosCampeonatos
        except Exception as e:
                print(type(e))

    #ok
    def recuperarIDJogadoresNoCampeonato(self, Campeonato):

        """
            Retorna uma lista de ids de jogadores no campeonato
        """
        try:
            conexao = pymysql.connect(host=self.host, user='root', db='tekken', port=self.port)
            cursor = conexao.cursor()
            ids = []
            idCampeonato = str(self.recuperarID(Campeonato.nome))
            sql = "select idjogador from tabela where idtorneio = %s;"
            cursor.execute(sql, (idCampeonato,))
            for row in cursor.fetchall():
                ids.append(row[0])
            cursor.close()
            conexao.close()
            return ids
        except Exception as e:
                print(type(e))

    def cadastrarCampeonato(self, Campeonato):
        try:
            conexao = pymysql.connect(host=self.host, user='root', db='tekken', port=self.port)
            cursor = conexao.cursor()
            sql = "insert into torneio(nome, inicio, status, qtdrounds, TemRingOut, PrimeiroNaFinal, TeraFase2, QtdJogadoresFase2, UltimoEliminado) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (Campeonato.nome, str(Campeonato.inicio), Campeonato.status, str(Campeonato.quantidadeRounds), int(Campeonato.temRingOut), int(Campeonato.primeiroNaFinal), int(Campeonato.teraFase2), str(Campeonato.quantosNaFase2), int(Campeonato.ultimoEliminado)))
            sql2 = "insert into pontuacao(idtorneio, vitória, empate, derrota, perfect, great, doubleko, roundganho, timeout, ringout, roundperdido, perfectcontra, greatcontra) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql2, (str(self.recuperarID(Campeonato.nome)), Campeonato.vitoria, Campeonato.empate, Campeonato.derrota,Campeonato.perfect, Campeonato.great, Campeonato.doubleKO, Campeonato.roundGanho, Campeonato.timeOut, Campeonato.ringOut, Campeonato.roundPerdido, Campeonato.perfectContra, Campeonato.greatContra))
            conexao.commit()
            return 1
        except pymysql.err.IntegrityError:
            print("Já há este nome do campeonato no banco de dados. Mude o nome")
            return 0
        except Exception as e:
            print(e)
            print(type(e))
            return 0
        finally:
            conexao.close()

    def cadastrarNovoJogador(self, Campeonato, Jogador):
        try:
            conexao = pymysql.connect(host=self.host, user='root', db='tekken', port=self.port)
            cursor = conexao.cursor()
            idTorneio = str(self.recuperarID(Campeonato.nome))
            idJogador = str(jogadorDAO().recuperarID(Jogador.nome))

            sql = "insert into tabela(idtorneio, idjogador, pontos, rodadas, vitorias, empates, derrotas, perfect, great, doubleko, roundganho, timeout, ringout, roundperdido, saldorounds, perfectcontra, greatcontra) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (idTorneio, idJogador, Jogador.pontos, Jogador.rodadas, Jogador.vitoria, Jogador.empate, Jogador.derrota, Jogador.perfects, Jogador.greats, Jogador.doubleKO, Jogador.roundsimples, Jogador.timeout, Jogador.ringout, Jogador.roundPerdido, Jogador.saldoRounds, Jogador.perfectsContra, Jogador.greatsContra,))
            conexao.commit()
            cursor.close()
            conexao.close()
        except Exception as e:
                print(type(e))

    def imprimirRodadas(self, idcampeonato):
        #apagando o que estiver escrito nele
        try:
            output = open("outputRodadas.txt", "w")
            output.close()

            conexao = pymysql.connect(host=self.host, user='root',  db='tekken', port=self.port)
            cursor = conexao.cursor()
            output = open("outputRodadas.txt", "w")
            sql = "select count(*) from luta where idtorneio = %s group by rodada limit 1"
            cursor.execute(sql, (idcampeonato,))
            lutasPorRodada = int(cursor.fetchone()[0])

            sql = ''' select idtorneio, rodada, A.nome, B.nome from luta, jogador as A, jogador as B
            where idjogador1 = A.idjogador and
            idjogador2 = B.idjogador
            and idtorneio = %s
            order by 1, idluta, 2; '''
            cursor.execute(sql, (idcampeonato,))

            index = 1 # controla quantas linhas devo pular pra colocar o "Rodada X" no texto

            for row in cursor.fetchall():
                if index % lutasPorRodada == 1:
                    linha = "\nRodada " + str(row[1]) + "\n\n"
                    output.write(linha)
                linha = str(row[2]) + " vs " + str(row[3]) + "\n"
                output.write(linha)
                index += 1

            output.write("\n\nFIM DO ARQUIVO")
            output.close()
            cursor.close()
            conexao.close()
        except Exception as e:
                print(type(e))

    def carregarInformacoesCampeonato(self, idCampeonato):
        sql = '''select * from tekken.torneio join tekken.pontuacao using(idtorneio)
        where idtorneio = %s;'''

        try:
            conexao = pymysql.connect(host=self.host, user='root', db='tekken', port=self.port)
            cursor = conexao.cursor()
            cursor.execute(sql, idCampeonato)
            row = cursor.fetchone()
            data = row[2].strftime('%d/%m/%Y') # CONVERTO DATE PARA STRING
            #dataInicio = datetime.strptime(data, "%d/%m/%Y")
            c = Campeonato(nome=row[1], inicio=data, quantidadeRounds=row[4], pontuacaoVitoria=row[11], pontuacaoEmpate=row[12],
                           pontuacaoDerrota=row[13], pontuacaoPerfect=row[14], pontuacaoGreat=row[15], pontuacaoDoubleKO=row[16],
                           pontuacaoRndGanho=row[17], pontuacaoTimeOut=row[18], pontuacaoRndPerdido=row[20],
                           pontuacaoGreatContra=row[22], pontuacaoPerfectContra=row[21])

            if row[5] == 0:
                c.temRingOut = False
            else:
                c.temRingOut = True
            c.ringOut = row[19]

            if row[6] == 0:
                c.primeiroNaFinal = False
            else:
                c.primeiroNaFinal = True

            if row[7] == 0:
                c.teraFase2 = False
            else:
                c.teraFase2 = True

            c.quantosNaFase2 = row[8]

            if row[9] == 0:
                c.ultimoEliminado = False
            else:
                c.ultimoEliminado = True

            return c
        except Exception as e:
            print(type(e))

    def gerarTabelaPontuacao(self, idCampeonato, Campeonato):
        try:
            if Campeonato.temRingOut is True:
                sql = ''' select A.nome, pontos, rodadas, vitorias, empates, derrotas, perfect, great, doubleko, roundganho, timeout, ringout,
                   roundperdido, saldorounds, perfectcontra, greatcontra
                   from tekken.tabela join tekken.jogador as A using(idjogador)
                   where idtorneio = %s and rodadas > 0
                   order by 2 desc, 3, 4 desc, 5 desc, 6, 7 desc, 8 desc, 9 desc, 11 desc, 12 desc, 14 desc, 1'''
            else:
                sql = ''' select A.nome, pontos, rodadas, vitorias, empates, derrotas, perfect, great, doubleko, roundganho, timeout,
                   roundperdido, saldorounds, perfectcontra, greatcontra
                   from tekken.tabela join tekken.jogador as A using(idjogador)
                   where idtorneio = %s and rodadas > 0
                   order by 2 desc, 3, 4 desc, 5 desc, 6, 7 desc, 8 desc, 9 desc, 11 desc, 13 desc, 1'''

            conexao = pymysql.connect(host=self.host, user='root', db='tekken', port=self.port)
            cursor = conexao.cursor()
            cursor.execute(sql, idCampeonato)
            tabela = list(cursor.fetchall())
            conexao.commit()
            cursor.close()
            conexao.close()
            return tabela
        except Exception as e:
                print(type(e))

    def qtdJogadoresTorneio(self, idCampeonato):

        """
        Esta função retorna a quantidade de jogadores cadastrados no campeonato, ou seja, a posição máxima de posição possivel
        no torneio.
        :param idCampeonato:
        :return: A quantidade de jogadores cadastrados no campeonato informado
        """

        try:
           conexao = pymysql.connect(host=self.host, user='root', db='tekken', port=self.port)
           cursor = conexao.cursor()
           sql = "select count(*) from tekken.tabela where idtorneio = %s;"
           cursor.execute(sql, (idCampeonato,))
           qtdJogadores = int(cursor.fetchone()[0])
           return qtdJogadores
        except Exception as e:
            print(type(e))

'''
if __name__ == "__main__":
    tekken = Campeonato("Teste2", "18/06/2017", 2, 3, 1, 0, 2.5, 2, 1.5, 1, 0.5, 0.5, 3, 0.25)
    bd = CampeonatoDAO()
    bd.cadastrarCampeonato(tekken)
    bd.encerrar()'''