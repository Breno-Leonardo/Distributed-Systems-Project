# Distributed-Systems-Project

## Jogo da forca multiplayer

* **Importante lembrar de definir o host no server.py e client.py**

## Server

O servidor  é responsável por gerenciar o estado do jogo e facilitar a comunicação entre vários clientes conectados ao servidor. Ele utiliza os módulos socket e threading para lidar com conexões de clientes de forma concorrente.

### Inicialização do Servidor

O servidor é inicializado criando uma instância da classe ForcaServer e chamando o método iniciar_servidor(). O servidor aguardará conexões de clientes nesse momento.

### Manipulação de Conexões de Clientes

Quando um cliente se conecta ao servidor, uma nova thread é criada para lidar com as requisições desse cliente. A classe ForcaServer possui o método lidar_com_cliente() que é executado nessa thread.

Dentro do método lidar_com_cliente(), o servidor aguarda mensagens do cliente. O cliente pode enviar dois tipos de tentativas: adivinhar uma palavra ou adivinhar uma letra. O servidor verifica se é a vez do jogador atual e se a tentativa é válida. Em seguida, atualiza o estado do jogo de acordo com a tentativa recebida. Se o palpite da palavra estiver correto, o jogador vence e os outros jogadores são notificados. Se o palpite de letra estiver correto, o servidor revela a letra na palavra secreta. Se as tentativas acabarem, o jogador perde e todos os jogadores são notificados.

Após lidar com a requisição do cliente, o servidor atualiza o estado do jogo e envia para todos os clientes conectados usando o método enviar_estado_jogo().

### Lógica do Jogo

A classe ForcaServer contém métodos para iniciar o jogo (iniciar_jogo()) e reiniciar o jogo (resetar_jogo()). Quando o jogo é iniciado, uma palavra secreta é selecionada aleatoriamente e o estado do jogo é definido inicialmente. A palavra secreta é representada por traços (_) que são revelados à medida que o jogador acerta letras. O jogador tem um número limitado de tentativas para adivinhar a palavra antes de perder o jogo.

### Método

A classe ForcaServer possui os seguintes métodos principais:

* __init__(self, host, port): O construtor da classe ForcaServer que inicializa as variáveis do servidor.
* iniciar_servidor(self): Inicia o servidor, aguardando conexões de clientes.
* lidar_com_cliente(self, client_socket): Lida com as requisições de um cliente específico.
* enviar_estado_jogo(self, client_socket): Envia o estado atual do jogo para um cliente específico.
* enviar_mensagem(self, client_socket, mensagem): Envia uma mensagem como vitória ou derrota para um cliente específico.
* iniciar_jogo(self): Inicia o jogo, selecionando uma palavra secreta e definindo o estado inicial.
* resetar_jogo(self): Reinicia o jogo, selecionando uma nova palavra secreta e reiniciando o estado.

### Utilização
Para utilizar o servidor, você precisa criar uma instância da classe ForcaServer, passando o endereço IP do servidor e a porta a ser usada. Em seguida, inicie o jogo chamando o método iniciar_jogo() e, finalmente, inicie o servidor chamando o método iniciar_servidor(). O servidor aguardará conexões de clientes e gerenciará o jogo em tempo real.


## Client

O cliente é responsável por se conectar ao servidor e interagir com o jogo em tempo real. Ele utiliza o módulo socket para estabelecer a conexão com o servidor.

### Conexão com o Servidor

O cliente é inicializado criando uma instância da classe ForcaClient, passando o endereço IP do servidor e a porta a ser usada. Em seguida, a função conectar_servidor() é chamada para estabelecer a conexão com o servidor. Após a conexão bem-sucedida, o cliente recebe um ID único do servidor.

### Recebendo o Estado do Jogo

O cliente utiliza o método receber_estado_jogo() para receber e exibir o estado atual do jogo enviado pelo servidor. O estado do jogo pode conter informações como a rodada atual, a dica, as letras reveladas, as letras erradas tentadas, as tentativas restantes e o jogador atual. O estado do jogo é exibido na saída padrão.

### Enviando Tentativas

O cliente utiliza o método enviar_tentativa(tipo, tentativa) para enviar tentativas para o servidor. O parâmetro tipo especifica o tipo de tentativa: "palavra" para adivinhar a palavra completa ou "letra" para adivinhar uma letra. O parâmetro tentativa contém a palavra completa ou a letra a ser enviada.

### Jogando o Jogo

A função jogar() controla o fluxo de jogo do cliente. Após estabelecer a conexão com o servidor, o cliente entra em um loop infinito. Ele recebe o estado do jogo atual e verifica se é a vez do jogador atual. Se for a vez do jogador atual, o cliente solicita uma tentativa do usuário (palavra ou letra) e a envia para o servidor. Caso contrário, o cliente aguarda sua vez de jogar.

### Utilização
Para utilizar o cliente, você precisa executar o código Python fornecido. Certifique-se de ter o endereço IP e a porta corretos do servidor. O cliente se conectará ao servidor e aguardará as instruções para jogar o jogo. Quando for a sua vez, digite "palavra" para adivinhar a palavra completa ou "letra" para adivinhar uma letra. 
