from CampeonatoDAO import CampeonatoDAO
from Luta import Luta
from LutaDAO import LutaDAO
from JogadorDAO import jogadorDAO
from TekkenNovoCampeonato import Ui_CadastrarCampeonato
from Jogador import Jogador
from CampeonatoDAO import CampeonatoDAO
from Campeonato import Campeonato
import os
import getpass

def alterarPontuacaoTotal(jogPontAtual, jogadorLutaPontuacaoAntiga, jogadorLutaPontuacaoNova): #três objetos do tipo jogador
    jogPontAtual.pontos = jogPontAtual.pontos - jogadorLutaPontuacaoAntiga.pontos + jogadorLutaPontuacaoNova.pontos
    jogPontAtual.vitoria = jogPontAtual.vitoria - jogadorLutaPontuacaoAntiga.vitoria + jogadorLutaPontuacaoNova.vitoria
    jogPontAtual.empate = jogPontAtual.empate - jogadorLutaPontuacaoAntiga.empate + jogadorLutaPontuacaoNova.empate
    jogPontAtual.derrota = jogPontAtual.derrota - jogadorLutaPontuacaoAntiga.derrota + jogadorLutaPontuacaoNova.derrota
    jogPontAtual.perfects = jogPontAtual.perfects - jogadorLutaPontuacaoAntiga.perfects + jogadorLutaPontuacaoNova.perfects
    jogPontAtual.greats = jogPontAtual.greats - jogadorLutaPontuacaoAntiga.greats + jogadorLutaPontuacaoNova.greats
    jogPontAtual.doubleKO = jogPontAtual.doubleKO - jogadorLutaPontuacaoAntiga.doubleKO + jogadorLutaPontuacaoNova.doubleKO
    jogPontAtual.roundsimples = jogPontAtual.roundsimples - jogadorLutaPontuacaoAntiga.roundsimples + jogadorLutaPontuacaoNova.roundsimples
    jogPontAtual.timeout = jogPontAtual.timeout - jogadorLutaPontuacaoAntiga.timeout + jogadorLutaPontuacaoNova.timeout
    jogPontAtual.ringout = jogPontAtual.ringout - jogadorLutaPontuacaoAntiga.ringout + jogadorLutaPontuacaoNova.ringout
    jogPontAtual.roundPerdido = jogPontAtual.roundPerdido - jogadorLutaPontuacaoAntiga.roundPerdido + jogadorLutaPontuacaoNova.roundPerdido
    jogPontAtual.perfectsContra = jogPontAtual.perfectsContra - jogadorLutaPontuacaoAntiga.perfectsContra + jogadorLutaPontuacaoNova.perfectsContra
    jogPontAtual.greatsContra = jogPontAtual.greatsContra - jogadorLutaPontuacaoAntiga.greatsContra + jogadorLutaPontuacaoNova.greatsContra
    jogPontAtual.atualizarSaldoRounds()




if __name__ == "__main__":

    #logar
    print("Insira a senha abaixo\n")
    senha = getpass.getpass()
    print(senha)
    if senha == "heihachirei":

       #carregar campeonato salvos
       os.system('cls') #limpa prompt
       listaCampeonatos = CampeonatoDAO().listarCampeonatos()
       print("Campeonatos salvos no banco:\n")
       i = 1
       print("{:<8} {:<15} ".format('ID', 'Nome'))  #isto já formata em tabela
       for cadaCampeonato in listaCampeonatos:
           print("{:<8} {:<15} ".format(i, cadaCampeonato))
           i += 1

       teste = True;
       while teste:
            id = input("\nQual campeonato você deseja carregar?\n")
            if int(id) > 0 and int(id) <= i - 1 :
                teste = False

       #escolher campeonato
       i = 1
       for cadaCampeonato in listaCampeonatos:
           if i == int(id):
               idtorneio = CampeonatoDAO().recuperarID(cadaCampeonato)
           i += 1

        #carregar sistema de pontuação
       campeonatoSelecionado = CampeonatoDAO().carregarInformacoesCampeonato(idtorneio) #cria um objeto do Tipo Campeonato.

        #perguntar a rodada
       teste = True;
       while teste:
           rodada = input("\nQual rodada você deseja alterar o resultado [1-" + str(LutaDAO().totalDeRodadas(idtorneio)) + "]?\n")
           if int(rodada) > 0 and int(rodada) <= LutaDAO().totalDeRodadas(idtorneio):
               teste = False


       lutasRealizadas = LutaDAO().carregarLutasRealizadas(idtorneio, rodada, rodada)
       if len(lutasRealizadas) > 0:
           i = 1
           print("\n{:<5} {:<8} {:<20} {:<10} {:<10} {:<20}".format('ID', 'Rodada', 'Jogador 1', 'Resultado', 'vs Resultado', 'Jogador 2'))
           for cadaLuta in lutasRealizadas:
                print("{:<5} {:<8} {:<20} {:<10} {:<10} {:<20}".format(i, cadaLuta[0], cadaLuta[1], cadaLuta[2], cadaLuta[3], cadaLuta[4] ))
                i += 1

           #perguntar a luta que quer alterar
           teste = True;
           while teste:
               luta = input("\nQual luta você deseja alterar?\n")
               if int(luta) > 0 and int(luta) <= i - 1:
                   teste = False;

            #carregar as informações da luta desejada
           i = 1
           for cadaLuta in lutasRealizadas:
               if i == int(luta):
                    nomeJogador1 = cadaLuta[1]
                    resultadoJogador1 = cadaLuta[2]
                    resultadoJogador2 = cadaLuta[3]
                    nomeJogador2 = cadaLuta[4]
                    break
               i += 1

            #carregar a pontuação dos jogadores
           idjogador1 = jogadorDAO().recuperarID(nomeJogador1)
           idjogador2 = jogadorDAO().recuperarID(nomeJogador2)
           idluta = LutaDAO().recuperarIDLuta(idtorneio, idjogador1, idjogador2)

           pontuacaoAtualJogador1 = jogadorDAO().pontuacaoAtualJogador(idjogador1, idtorneio)
           pontuacaoAtualJogador1.nome = nomeJogador1 #a função pontuacaoAtualJogador nao registra o nome. O objeto Jogador é criado sem o nome do jogador
           pontuacaoAtualJogador2 = jogadorDAO().pontuacaoAtualJogador(idjogador2, idtorneio)
           pontuacaoAtualJogador2.nome = nomeJogador2

           opcao = input("\nDeseja ver a pontuação atual dos jogadores? [Y/N]\n")
           if opcao.upper() == 'Y':
               pontuacaoAtualJogador1.exibirPontuacao() #tipo Jogador
               pontuacaoAtualJogador2.exibirPontuacao()

            #carregar a pontuação que estes jogadores marcaram nesta luta
           jog01 = Jogador(nomeJogador1, None) #crio objeto do tipo Jogador com pontuação zerada para poder calcular a pontuação do jogador naquela luta especifica
           jog02 = Jogador(nomeJogador2, None)
           lutaAtual = Luta(jog01, jog02, rodada) #crio um objeto do tipo Luta
           lutaAtual.preencherResultadoLuta(resultadoJogador1, resultadoJogador2) #valida o resultado da luta
           campeonatoSelecionado.acabarLuta(lutaAtual) #Computa a pontuação conquistada pelos jogadores
           opcao = input("\nDeseja ver a pontuação que os jogadores conquistaram naquela luta? [Y/N]\n")
           if opcao.upper() == 'Y':
               jog01.exibirPontuacao()
               jog02.exibirPontuacao()

            #perguntar se deseja inserir o resultado novo
           resultadoNovoJogador1 = input("\nInsira o novo resultado do jogador " + nomeJogador1 + "?\n")
           resultadoNovoJogador2 = input("\nInsira o novo resultado do jogador " + nomeJogador2 + "?\n")

            #validar as novas alterações (validar se o novo resultado respeita o numero de rounds)
           jogNovo01 = Jogador(nomeJogador1, None)  # crio objeto do tipo Jogador com pontuação zerada para poder calcular a pontuação do jogador naquela luta especifica
           jogNovo02 = Jogador(nomeJogador2, None)
           lutaNovoAtual = Luta(jogNovo01, jogNovo02, rodada)  # crio um objeto do tipo Luta
           lutaNovoAtual.preencherResultadoLuta(resultadoNovoJogador1, resultadoNovoJogador2)  # valida o resultado da luta
           campeonatoSelecionado.acabarLuta(lutaNovoAtual)  # Computa a pontuação conquistada pelos jogadores
           opcao = input("\nDeseja ver a nova pontuação que os jogadores conquistaram naquela luta após as alterações? [Y/N]\n")
           if opcao.upper() == 'Y':
               jogNovo01.exibirPontuacao()
               jogNovo02.exibirPontuacao()

            #atualizar a pontuação total
           alterarPontuacaoTotal(pontuacaoAtualJogador1, jog01, jogNovo01)
           alterarPontuacaoTotal(pontuacaoAtualJogador2, jog02, jogNovo02)
           opcao = input("\nDeseja ver a nova pontuação total dos jogadores após as alterações? [Y/N]\n")
           if opcao.upper() == 'Y':
               pontuacaoAtualJogador1.exibirPontuacao()  # tipo Jogador
               pontuacaoAtualJogador2.exibirPontuacao()

           opcao = input("\nDeseja salvar as alterações? [Y/N]\n")
           if opcao.upper() == 'Y':
               #salvar resultado alterado no banco de dados
               LutaDAO().terminarLuta(idluta, lutaNovoAtual)
               #subtraindo a pontuação antiga conquistada por esses jogadores
               jogadorDAO().subtrairPontuacao(idjogador1, idtorneio, jog01)
               jogadorDAO().subtrairPontuacao(idjogador2, idtorneio, jog02)
               # atualizando a pontuação nova conquistada por esses jogadores
               jogadorDAO().atualizarPontuacao(idjogador1, idtorneio, jogNovo01)
               jogadorDAO().atualizarPontuacao(idjogador2, idtorneio, jogNovo02)
               print("Atualização feita com sucesso!")

           opcao = input("\n\nAperte qualquer botão para fechar o prompt\n")
           os.system("cls")

       else:
           print("\nNão há lutas nesta rodada")
           opcao = input("\n\nAperte qualquer botão para fechar o prompt\n")
           os.system("cls")

    else:
        print("Senha incorreta. Acesso não autorizado!")
        opcao = input("\n\nAperte qualquer botão para fechar o prompt\n")
        os.system("cls")


