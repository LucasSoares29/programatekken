## 🕹️ Sobre o projeto `programatekken`

Este foi meu **primeiro projeto em Python**, desenvolvido entre 2017 e 2018, no início da minha jornada de aprendizado em programação.

O objetivo do projeto é registrar os resultados de um campeonato do jogo **Tekken** em formato **round-robin** — ou seja, todos os jogadores se enfrentam, em um estilo semelhante ao de torneios como a **Copa do Mundo** ou o **Campeonato Brasileiro**.

---

### 🧱 Estrutura do Projeto

A aplicação utiliza **PyQt** como frontend e armazena os dados em um banco de dados **MySQL**.

#### Principais componentes:

- `CampeonatoDAO.py`, `LutaDAO.py`, `JogadorDAO.py`: Responsáveis pela lógica de acesso ao banco de dados (CRUD), manipulando informações de campeonatos, lutas e jogadores.
  
- `TekkenNovoCampeonato_2.py`: Script para **configuração de um novo campeonato**, permitindo definir o regulamento e cadastrar os jogadores participantes.

![tekken-tela-1](https://github.com/user-attachments/assets/e29bd621-8964-4168-99ac-a2e36c24c46b)

- `RodadaTekken.py` e `RodadaTekken_4k.py`: São as **janelas principais da aplicação**, onde é possível:
  - Registrar os resultados das lutas
  - Sortear os personagens para cada jogador
  - Visualizar resultados anteriores
  - Acompanhar a tabela de pontuação em tempo real


![tekken-tela-2](https://github.com/user-attachments/assets/96b26f9f-28c8-42e0-b079-b00aebcd3e71)
![tekken-tela-3](https://github.com/user-attachments/assets/4c58fdea-d00c-4494-95e2-3df0c232bba9)
![tekken-tela-4](https://github.com/user-attachments/assets/1df0ed2a-3b83-460e-86de-d341276bd916)
![tekken-tela-5](https://github.com/user-attachments/assets/7c8fd266-55ae-4c10-8b54-7f57caeba262)


- `AlterarResultadoTekken.py`: Permite **alterar resultados já registrados** mediante autenticação por senha.

![tekken-tela-6](https://github.com/user-attachments/assets/ef02d5d1-3ce7-4a56-8cba-494c89b982f9)


- `Tekken.SQL`: Script para **criação do banco de dados MySQL** com as tabelas necessárias para o funcionamento da aplicação.

## Esquema Relacional do Banco de Dados `tekken`

```plaintext
+----------------+          +----------------+          +------------------+
|   jogador      |          |    torneio     |          |   pontuacao      |
+----------------+          +----------------+          +------------------+
| idjogador (PK) |          | idtorneio (PK) |<-----+   | idpontuacao (PK) |
| nome           |                                   |   | idtorneio (FK)  |
| nacionalidade  |                                   |   | vitória         |
+----------------+                                   |   | empate          |
                                                    |   | derrota         |
                                                    |   | ...             |
                                                    |   +------------------+
                                                    |
+----------------+          +----------------+       |
|     luta       |          |    tabela      |       |
+----------------+          +----------------+       |
| idluta (PK)    |          | idtabela (PK)  |       |
| idtorneio (FK) +--------->| idtorneio (FK) |<------+
| idjogador1     |          | idjogador (FK) |
| idjogador2     |          | pontos         |
| resultadojogador1 |       | rodadas        |
| resultadojogador2 |       | ...            |
| rodada         |          +----------------+
| finalizada     |
+----------------+
``` 



### ⚙️ Pré-requisitos

Antes de executar o projeto, certifique-se de:

1. Ter o **WampServer** instalado e configurado — ele é responsável por disponibilizar a porta para o servidor MySQL.
2. Instalar as dependências do projeto com:

```
pip install -r requirements.txt
```  
