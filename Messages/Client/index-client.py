#Bibliotecas necessárias para conexão e multiplas execuções em paralelo.
import socket
import threading

def main():

    #Objeto socket para a conexão AF_INET = IPV4, SOCK_STREAM = Arquitetura TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Tentar fazer a conexão com servidor, passando os parametros e porta em uma tupla.
    try:
        client.connect(('localhost', 5050))
    except:
        return print('\nNão foi possivel se conectar ao servidor!\n')
    
    #Se não caiu no execept, vai pedir o nome do usuário.
    username = input('usuário> ')
    print('\nConectado')

    #É necessário criar as threads para as funções que vão rodar em paralelo no servidor e inicia-las.
    #Passo quem vou rodar e em uma lista seus argumentos.
    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()


def receiveMessages(client):
    #Sempre tentar receber o que vem do servidor
    while True:
        try:
            #Recebemos até 2048 bytes para leitura e decodificamos como string.
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possivel permanecer conectado no servidor!\n')
            print('Pressione <Enter> para continuar...')
            client.close()
            break


def sendMessages(client, username):
    #Sempre, vai tentar ficar capturando as mensagens dos usuários e aberto a enviar.
    while True:
        try:
            #Onde o usuário envia as mensagens em bytes porque o servidor devolve em bytes.
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return 


main()
