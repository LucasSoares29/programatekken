import os
from pymediainfo import MediaInfo


#tutorial - https://automatetheboringstuff.com/chapter8/
#https://stackabuse.com/python-check-if-string-contains-substring/
#https://stackoverflow.com/questions/54338990/how-can-i-to-run-windows-powershell-commands-from-python
#https://stackoverflow.com/questions/7348505/get-dimensions-of-a-video-file


if __name__ == "__main__":

    pastaExiste = True

    print(os.path.dirname(os.path.abspath(__file__))) #

    path = 'Y:\\NVEncC_4.69'
    os.chdir(path) #change directory
    print("Diretório atual : " + os.getcwd()) #print current directory

    #os.makedirs('Y:\\NVEnc_3.25\\NVEncC\\x64\\converted') #exceçao FileExistsError caso ja tenha sido criado

    #print(os.listdir(path)) #listando arquivos do diretório atual

    arquivos = os.listdir(path)
    arquivosMkv = []
    substring = ".mkv"
    print(arquivos)

    #Filtrando arquivos de video MKV
    for cadaArquivo in arquivos:
        if substring in cadaArquivo:
            arquivosMkv.append(cadaArquivo); #adiciono a lista caso encontre um arquivo mkv

    print(arquivosMkv)
    print("Há " + str(len(arquivosMkv)) + " arquivos de video mkv no diretório " + path);

    #convertendo os videos
    for cadaArquivo in arquivosMkv:
        pathVideo = path + '\\' + cadaArquivo #pega o path do arquivo em mkv
        print("input: " + pathVideo)

        #informacao resolucao
        media_info = MediaInfo.parse(pathVideo)

        for track in media_info.tracks:
            if track.track_type == 'Video':
                #print("O video possui resolução {}x{}".format(track.width, track.height))
                resolucao = int(track.height);
                fps = float(track.frame_rate);
                print("O video está em " + str(resolucao) + "p a " + str(fps) + "fps" )

        #tento criar a pasta dos videos convertidos
        while pastaExiste:
            try:
                os.makedirs(path + '\\converted')
            except FileExistsError:
                pastaExiste = False

        #mudando o codec da saída de video do path
        cadaArquivo = cadaArquivo.replace(".mkv", ".mp4")
        pathSaida = path + '\\converted\\' + cadaArquivo

        print("output: " + pathSaida)


        pathConversor = path + '\\NVEncC64.exe'
        print("conversor: " + pathConversor)



        #chamando conversor

        if resolucao <= 720:
            if fps <= 30:
                os.system(
                    pathConversor + ' -i "' + pathVideo + '" -c hevc --vbrhq 2000 --audio-codec aac --audio-bitrate 192 -o "' + pathSaida + '"')
            else: #neste caso a 60
                os.system(
                    pathConversor + ' -i "' + pathVideo + '" -c hevc --vbrhq 4000 --audio-codec aac --audio-bitrate 192 -o "' + pathSaida + '"')
            print("O arquivo " + pathVideo + " foi convertido com sucesso!")
        elif resolucao == 1080:
            if fps <= 30:
                os.system(
                    pathConversor + ' -i "' + pathVideo + '" -c hevc --vbrhq 4000 --audio-codec aac --audio-bitrate 192 -o "' + pathSaida + '"')
            else: #neste caso a 60
                os.system(
                    pathConversor + ' -i "' + pathVideo + '" -c hevc --vbrhq 8000 --audio-codec aac --audio-bitrate 192 -o "' + pathSaida + '"')
            print("O arquivo " + pathVideo + " foi convertido com sucesso!")
        elif resolucao == 1440:
            if fps <= 30:
                os.system(
                    pathConversor + ' -i "' + pathVideo + '" -c hevc --vbrhq 8000 --audio-codec aac --audio-bitrate 192 -o "' + pathSaida + '"')
            else: #neste caso a 60
                os.system(
                    pathConversor + ' -i "' + pathVideo + '" -c hevc --vbrhq 17000 --audio-codec aac --audio-bitrate 192 -o "' + pathSaida + '"')
            print("O arquivo " + pathVideo + " foi convertido com sucesso!")
        elif resolucao == 2160:
            if fps <= 30:
                os.system(pathConversor + ' -i "' + pathVideo + '" -c hevc --vbrhq 17000 --audio-codec aac --audio-bitrate 192 -o "' + pathSaida + '"')
            else: #neste caso a 60
                os.system(pathConversor + ' -i "' + pathVideo + '" -c hevc --vbrhq 34000 --audio-codec aac --audio-bitrate 192 -o "' + pathSaida + '"')
            print("O arquivo " + pathVideo + " foi convertido com sucesso!")
        else:
            print("Esta resolução ainda não é suportada!")



        




    input("Todos os arquivos foram convertidos com sucesso! Aperte qualquer botão para encerrar o programa")





    #os.system executa os arquivos do sistema