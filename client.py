import socket
import ast

class ForcaClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.estado_jogo = None
        self.id=0

    def conectar_servidor(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        id = self.client_socket.recv(1024).decode()
        self.id=id
        print('Conectado ao servidor. ')
        print('Seu Id é '+ self.id)

    def receber_estado_jogo(self):
        try:
            data = self.client_socket.recv(1024).decode()
            if not data:
                pass
            else:
                dataSplit=data.split()
                if(dataSplit[0]=="win"):
                 print("Parabéns você ganhou. A palavra era "+dataSplit[1])
                 self.estado_jogo=None
                elif (dataSplit[0] == "winAnother"):
                    print("Jogador "  +dataSplit[1] + " ganhou. A palavra era "+dataSplit[2])
                elif (dataSplit[0] == "lose"):
                    print("Acabaram as tentativas, a palavra era "+dataSplit[1])
                    print(" GAME OVER. Resetando o jogo...")
                    self.estado_jogo = None
                else:
                    self.estado_jogo = ast.literal_eval(data)
                    print("\n")
                    print('RODADA ', self.estado_jogo['rodada'])
                    print('Dica:', self.estado_jogo['dica'])
                    print('Quantidade de caracteres:', self.estado_jogo['quantidade_caracteres'])
                    print('Letras reveladas:', ' '.join(self.estado_jogo['letras_reveladas']))
                    print('Letras erradas tentadas:', ' '.join(self.estado_jogo['letras_erradas']))
                    print('Tentativas restantes:', self.estado_jogo['tentativas_restantes'])
                    print('Jogador atual:', self.estado_jogo['jogador_atual'])
                    print("\n")
        except ConnectionAbortedError:
            print(f"A conexão foi abruptamente encerrada.")


    def enviar_tentativa(self, tipo, tentativa):
        data = f'{tipo} {tentativa}'
        self.client_socket.send(data.encode())

    def jogar(self):
        self.conectar_servidor()

        while True:
            self.receber_estado_jogo()

            if self.estado_jogo!=None and str(self.estado_jogo['jogador_atual']) == self.id :
                print('Sua vez de jogar!')

                while True:
                    tipo = input('Digite "palavra" para adivinhar a palavra ou "letra" para adivinhar uma letra: ')

                    if tipo == 'palavra':
                        palavra = input('Digite a palavra completa: ')
                        self.enviar_tentativa(tipo, palavra)
                        break
                    elif tipo == 'letra':
                        letra = input('Digite uma letra: ')
                        while(letra in self.estado_jogo['letras_erradas'] or letra in self.estado_jogo['letras_reveladas']):
                            print("Letra ja jogada")
                            letra = input('Digite uma letra: ')

                        self.enviar_tentativa(tipo, letra)
                        break
                    else:
                        print('Tipo de tentativa inválido. Tente novamente.')

            if self.estado_jogo != None:
                print('Aguardando jogada dos outros jogadores...')

            if self.estado_jogo!=None and str(self.estado_jogo['jogador_atual']) != self.id:
                print('Aguardando sua vez de jogar...')

def main():
    host = '' 
    port = 5555

    forca_client = ForcaClient(host, port)
    forca_client.jogar()

if __name__ == '__main__':
    main()
