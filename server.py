import random
import socket
import threading


class ForcaServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_sockets = []
        self.jogadores=[]
        self.lock = threading.Lock()
        self.palavras_dicas = [
            ('cachorro', 'Melhor amigo do homem, conhecido por sua lealdade e companheirismo'),
            ('gato', 'Animal de estimação independente e ágil, conhecido por sua habilidade de caça'),
            ('coala', 'Mamífero arborícola e herbívoro, encontrado principalmente na Austrália'),
            ('zebra', 'Animal listrado encontrado nas savanas africanas'),
            ('macaco', 'Primate conhecido por sua inteligência e habilidades de escalada'),
            ('tartaruga', 'Réptil de casco duro que se move lentamente e se protege dentro de sua concha'),
            ('lebre', 'Animal de orelhas longas e ágil, conhecido por sua velocidade'),
            ('papagaio', 'Ave colorida e falante, capaz de imitar sons e palavras'),
            ('gavião', 'Ave de rapina com asas largas e excelente visão para caçar'),
            ('polvo', 'Cefalópode marinho com tentáculos e habilidades de camuflagem impressionantes'),
            ('elefante', 'Maior mamífero terrestre com tromba e presas impressionantes'),
            ('golfinho', 'Mamífero marinho conhecido por sua inteligência e habilidades acrobáticas'),
            ('panda', 'Ursinho fofo e amante de bambu, encontrado principalmente na China'),
            ('tigre', 'Grande felino com listras distintas e excelente habilidade de caça'),
            ('borboleta', 'Inseto colorido e delicado, passa por um estágio de metamorfose'),
            ('pinguim', 'Ave não voadora que habita principalmente regiões polares'),
            ('girafa', 'Mamífero de pescoço longo, conhecido por ser o animal mais alto da terra'),
            ('leopardo', 'Felino ágil e camuflado, conhecido por suas habilidades de escalada'),
            ('cobra', 'Réptil alongado e sem patas, muitas vezes venenoso'),
            ('águia', 'Ave de rapina com visão aguçada e habilidades de voo impressionantes'),
        ]
        self.palavra_secreta = ''
        self.dica = ''
        self.letras_acertadas = []
        self.tentativas = 0
        self.letras_erradas = []
        self.jogador_atual = 0 #index do jogador atual na lista de jogadores
        self.jogo_iniciado = False
        self.idClient = 0
        self.rodada = 1

    def iniciar_servidor(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print('Servidor iniciado. Aguardando conexões...')

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f'Conexão estabelecida com {client_address[0]}:{client_address[1]}')
            self.client_sockets.append(client_socket)
            data = str(self.idClient).encode()
            client_socket.send(data)
            self.jogadores.append(self.idClient)
            self.idClient = self.idClient + 1
            self.lock.acquire()
            self.enviar_estado_jogo(client_socket)
            self.lock.release()

            thread = threading.Thread(target=self.lidar_com_cliente, args=(client_socket,))
            thread.start()

    def lidar_com_cliente(self, client_socket):
        while True:
            reset = False
            data = client_socket.recv(1024).decode()
            if not data:
                if(self.jogador_atual==len(self.jogadores)-1):
                    del self.jogadores[self.jogador_atual]
                    self.jogador_atual=0
                else:
                    del self.jogadores[self.jogador_atual]
                self.client_sockets.remove(client_socket)
                client_socket.close()
                self.lock.acquire()
                for client in self.client_sockets:
                    print("client", client)
                    self.enviar_estado_jogo(client)
                self.lock.release()
                break

            tipo_tentativa, chute = data.split()

            if self.jogador_atual == self.client_sockets.index(client_socket):
                if tipo_tentativa == 'palavra':
                    if chute == self.palavra_secreta:
                        self.enviar_mensagem(client_socket, 'win ' + self.palavra_secreta)
                        count = 0
                        for c in self.client_sockets:
                            if (count != self.jogador_atual):
                                self.enviar_mensagem(c, 'winAnother' + " " + str(
                                    self.jogador_atual) + " " + self.palavra_secreta)
                            count += 1
                        reset = True

                    else:
                        self.tentativas -= 1
                        if self.tentativas == 0:
                            for c in self.client_sockets:
                                self.enviar_mensagem(c, 'lose' + " " + self.palavra_secreta)
                            reset = True


                elif tipo_tentativa == 'letra':

                    if chute.isalpha() and len(chute) == 1:
                        if chute in self.palavra_secreta:
                            for i, letra in enumerate(self.palavra_secreta):
                                if letra == chute:
                                    self.letras_acertadas[i] = chute
                            if '_' not in self.letras_acertadas:
                                self.enviar_mensagem(client_socket, 'win ' + self.palavra_secreta)
                                count = 0
                                for c in self.client_sockets:
                                    if (count != self.jogador_atual):
                                        self.enviar_mensagem(c, 'winAnother' + " " + str(
                                            self.jogador_atual) + " " + self.palavra_secreta)
                                    count += 1

                                reset = True
                        else:
                            self.letras_erradas.append(chute)
                            self.tentativas -= 1
                            if self.tentativas == 0:
                                for c in self.client_sockets:
                                    self.enviar_mensagem(c, 'lose' + " " + self.palavra_secreta)
                                reset = True

                if ((self.jogador_atual + 1) % len(self.client_sockets) == 0):
                    self.rodada += 1

                if (reset):
                    self.resetar_jogo()

                self.jogador_atual = (self.jogador_atual + 1) % len(self.client_sockets)

                self.lock.acquire()
                for client in self.client_sockets:
                    self.enviar_estado_jogo(client)
                self.lock.release()

        client_socket.close()

    def enviar_estado_jogo(self, client_socket):

        estado_jogo = {
            'palavra_secreta': self.palavra_secreta,
            'dica': self.dica,
            'quantidade_caracteres': len(self.palavra_secreta),
            'letras_reveladas': self.letras_acertadas,
            'tentativas_restantes': self.tentativas,
            'letras_erradas': self.letras_erradas,
            'rodada': self.rodada,
            'jogador_atual': self.jogadores[self.jogador_atual]
        }
        data = str(estado_jogo).encode()
        client_socket.send(data)

    def enviar_mensagem(self, client_socket, mensagem):
        data = mensagem.encode()
        client_socket.send(data)

    def iniciar_jogo(self):
        self.palavra_secreta, self.dica = random.choice(self.palavras_dicas)
        self.letras_acertadas = ['_' for _ in self.palavra_secreta]
        self.tentativas = 7
        self.letras_erradas = []
        self.jogador_atual = 0
        self.jogo_iniciado = True

        print('Jogo iniciado!')
        print('Aguardando jogadores...')

        self.lock.acquire()
        for client in self.client_sockets:
            self.enviar_estado_jogo(client)
        self.lock.release()

    def resetar_jogo(self):
        self.palavra_secreta, self.dica = random.choice(self.palavras_dicas)
        self.letras_acertadas = ['_' for _ in self.palavra_secreta]
        self.tentativas = 7
        self.letras_erradas = []
        self.rodada = 1


def main():
    host = '192.168.100.21'
    port = 5555

    forca_server = ForcaServer(host, port)
    threading.Thread(target=forca_server.iniciar_jogo).start()
    forca_server.iniciar_servidor()


if __name__ == '__main__':
    main()