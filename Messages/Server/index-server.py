import socket
import threading

#Lista onde vou armazenar meus clientes.
clients = []

def main():
    
    #Vamos criar o objeto server, com o mesmo IPV4 e TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Tentando ligar o servidor.
    try:
        #Necessario estar dentro da tupla!
        server.bind(('localhost', 5050))
        #Definindo numero de conexões no modo de escuta, sem numero vai até onde o servidor aguentar.
        server.listen()
    except:
        return print('\nNão foi possivel iniciar o servidor!\n')

    #Laço que sempre verifica para aceitar novas conexões.
    while True:
        #Armazenando o cliente e o endereço nas variaveis e salvando o cliente na lista.
        client, addr = server.accept()
        clients.append(client)

        #Para rodar em paralelo cada um dos clients.
        #threading.Thread(target=messagesTratament, args=[client]).start()
        threadClients = threading.Thread(target=messagesTratament , args=[client])
        threadClients.start()


#Funçao se verifica se há menssagens enviada pelos clientes e mandar para os outros.
def messagesTratament(client):
    while True:
        try:
            #Tem que ser igual o numero de bytes porque estamos recebendo aqui para tratar.
            msg = client.recv(2048)
            broadcast(msg, client)
        except:
            deleteClient(client)
            break


#Função recebe a mensagem e quem a enviou.
def broadcast(msg, client):
    #Aqui vou percorrer e verificar se o client é o mesmo que enviou a mensagem, para enviar só para
    #os outros clientes.
    for clientsUser in clients:
        if clientsUser != client:
            try:
                clientsUser.send(msg)
            except:
                #Se o não conseguir é porque o client da vez desconectou, então deleta ele.
                deleteClient(clientsUser)


def deleteClient(client):
    clients.remove(client)


main()






