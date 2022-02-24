
from Luta import *
from CampeonatoDAO import *
from JogadorDAO import *
import pymysql


class LutaDAO(object):
    
    
        host = '192.168.0.101'
        port = 3308

        # testar recuperarIDLuta()
        def recuperarIDLuta(self, idtorneio, idjogador1, idjogador2):
            try:
                conexao2 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao2.cursor()
                sql = "select idluta from luta where idtorneio = %s and (idjogador1 = %s or idjogador1 = %s)  and (idjogador2 = %s or idjogador2 = %s);"
                cursor.execute(sql, (idtorneio, idjogador1, idjogador2, idjogador1, idjogador2))
                return cursor.fetchone()[0]
            except TypeError:
                return 0
            except Exception as e:
                print(type(e))
                print("Erro de conexão")
            finally:
                cursor.close()
                conexao2.close()

        # OK
        def inserirLuta(self, idCampeonato, Luta):
            try:
                conexao2 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao2.cursor()
                sql = "insert into luta(idtorneio, idjogador1, idjogador2, rodada, finalizada) values (%s, %s, %s, %s, %s);"
                cursor.execute(sql, (str(idCampeonato), str(Luta.jogador1), str(Luta.jogador2), str(Luta.rodada), str(Luta.finalizada)))
                conexao2.commit()
                cursor.close()
                conexao2.close()
            except Exception as e:
                print(type(e))

        # TESTAR terminarLuta()
        def terminarLuta(self, idLuta, Luta):

            """
            Atualiza os dados da Luta no banco de dados
            :param idLuta: parâmetro do tipo inteiro ou string
            :param Luta: objeto da classe Luta
            :return:
            """
            try:
                conexao2 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao2.cursor()
                sql = "update luta set resultadojogador1 = %s, resultadojogador2 = %s, finalizada = %s where idluta = %s;"
                cursor.execute(sql, (Luta.resultadoJogador1, Luta.resultadoJogador2, Luta.finalizada, idLuta))
                # atualizar pontuação do jogador
                conexao2.commit()
                cursor.close()
                conexao2.close()
            except Exception as e:
                print(type(e))

        # OK
        def carregarLutasNaoFinalizadas(self, idCampeonato):
            try:
                sql = '''select tekken.jogador.nome, B.nome, rodada from tekken.luta
                join tekken.jogador on(idjogador1 = idjogador)
                join tekken.jogador as B on (idjogador2 = B.idjogador)
                where idtorneio = %s
                and finalizada = 0
                order by idluta;'''

                conexao2 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao2.cursor()
                cursor.execute(sql, idCampeonato)
                listaLutas = list(cursor.fetchall())
                conexao2.commit()
                cursor.close()
                conexao2.close()
            except TypeError:
                return []
            except Exception as e:
                print(type(e))

            return listaLutas


        def carregarLutasRealizadas(self, idCampeonato, rodadaInicial, rodadaFinal):
            try:
                sql = '''select rodada, tekken.jogador.nome, resultadojogador1, resultadojogador2,  B.nome from tekken.luta
                join tekken.jogador on(idjogador1 = idjogador)
                join tekken.jogador as B on (idjogador2 = B.idjogador)
                where idtorneio = %s
                and finalizada = 1
                and rodada >= %s
                and rodada <= %s
                order by idluta;'''

                conexao2 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao2.cursor()
                cursor.execute(sql, (idCampeonato, rodadaInicial, rodadaFinal))
                listaLutas = list(cursor.fetchall())
                conexao2.commit()
                cursor.close()
                conexao2.close()
            except TypeError:
                return []
            except Exception as e:
                print(type(e))

            return listaLutas

        def carregarLutasRealizadasJogador(self, idCampeonato, rodadaInicial, rodadaFinal, jogador):

            jogador = jogador + '%'

            try:
                sql = '''select rodada, tekken.jogador.nome, resultadojogador1, resultadojogador2,  B.nome from tekken.luta
                join tekken.jogador on(idjogador1 = idjogador)
                join tekken.jogador as B on (idjogador2 = B.idjogador)
                where idtorneio = %s
                and finalizada = 1
                and rodada >= %s
                and rodada <= %s
                and (tekken.jogador.nome like %s or B.nome like %s)
                order by idluta;'''

                conexao2 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao2.cursor()
                cursor.execute(sql, (idCampeonato, rodadaInicial, rodadaFinal, jogador, jogador))
                listaLutas = list(cursor.fetchall())
                conexao2.commit()
                cursor.close()
                conexao2.close()
            except TypeError:
                return []
            except Exception as e:
                print(type(e))

            return listaLutas

        def totalDeRodadas(self, idCampeonato):
            try:
                sql = '''select max(rodada) from tekken.luta
                where idtorneio = %s'''

                conexao2 = pymysql.connect(host=self.host, user='root', password='root', db='tekken', port=self.port)
                cursor = conexao2.cursor()
                cursor.execute(sql, idCampeonato)
                rodadas = int(cursor.fetchone()[0])
                conexao2.commit()
                cursor.close()
                conexao2.close()
            except TypeError:
                return 0
            except Exception as e:
                print(type(e))

            return rodadas

