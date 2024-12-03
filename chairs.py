import pygame
import sys
import math

# Inicializa o Pygame
pygame.init()

# Definir dimensões da tela
largura = 1400
altura = 800
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Chairs!')

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AZUL_ESCURO = (23, 20, 31)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
ROXO = (166, 38, 166)

# Fontes
fonte1 = pygame.font.SysFont(None, 60)  
fonte2 = pygame.font.SysFont("Cantarell", 72, bold=True)
fonte3 = pygame.font.SysFont("Cantarell", 36, bold=True)
fonte4 = pygame.font.SysFont(None, 62)
fonte5 = pygame.font.SysFont(None, 20)

#seleções
dificuldade = 1
fases = 1

#---------------------------------------------------------------------------
"""
    Atualiza a posição e a velocidade de um objeto considerando a resistência do ar.

    1. Converte o ângulo de lançamento para radianos.
    2. Calcula os componentes da velocidade inicial nos eixos X e Y.
    3. Aplica as equações diferenciais com resistência proporcional à velocidade para calcular:
       - Velocidades nos eixos X e Y após o tempo `t`.
       - Novas posições nos eixos X e Y após o tempo `t`.
    4. Retorna a posição e a velocidade atualizadas.

    Parâmetros:
        t (float): O tempo transcorrido desde o início do movimento.
        angulo (float): O ângulo de lançamento em graus, medido em relação ao eixo X.
        velocidade_inicial (float): A velocidade inicial do objeto no instante do lançamento.
        posicao_inicial_x (float): A posição inicial do objeto no eixo X.
        posicao_inicial_y (float): A posição inicial do objeto no eixo Y.
        g (float): A aceleração gravitacional (em metros por segundo ao quadrado).
        k (float): A constante de resistência do ar, proporcional à velocidade.

    Retorna:
        tuple: Um par de tuplas contendo:
            - A posição atual do objeto (x, y) no espaço.
            - A velocidade atual do objeto (velocidade_x, velocidade_y).
"""
def atualizar_posicao_e_velocidade_com_resistencia(
    t, angulo, velocidade_inicial, posicao_inicial_x, posicao_inicial_y, g, k
):
    angulo_rad = math.radians(angulo)
    
    # Componentes da velocidade inicial
    velocidade_inicial_x = velocidade_inicial * math.cos(angulo_rad)
    velocidade_inicial_y = velocidade_inicial * math.sin(angulo_rad)
    
    # Calcula a nova velocidade com resistência
    velocidade_x = velocidade_inicial_x * math.exp(-k * t)
    velocidade_y = (velocidade_inicial_y - g / k) * math.exp(-k * t) + g / k

    # Calcula nova posição
    x = posicao_inicial_x + (velocidade_inicial_x / k) * (1 - math.exp(-k * t))
    y = posicao_inicial_y - ((1 / k) * (velocidade_inicial_y + g / k) * (1 - math.exp(-k * t)) - (g * t / k))
    
    return (x, y), (velocidade_x, velocidade_y)


"""
    Desenha um vetor representando a direção e magnitude da velocidade inicial de um objeto.

    1. Calcula o comprimento do vetor proporcional à velocidade inicial.
    2. Determina as coordenadas finais do vetor com base no ângulo e comprimento.
    3. Desenha o vetor como uma linha usando a função `pygame.draw.line`.
    4. Calcula as coordenadas para a ponta da seta que indica a direção do vetor.
    5. Desenha a ponta da seta usando a função `pygame.draw.polygon`.

    Parâmetros:
        x (float): A posição inicial do vetor no eixo X.
        y (float): A posição inicial do vetor no eixo Y.
        angulo (float): O ângulo do vetor em graus, medido em relação ao eixo X.
        velocidade_inicial (float): A velocidade inicial do objeto, usada para determinar o comprimento do vetor (em unidades arbitrárias).
"""
def desenhar_vetor_direcao(x, y, angulo, velocidade_inicial):
    comprimento_vetor = velocidade_inicial * 0.5
    angulo_rad = math.radians(angulo)
    fim_vetor_x = x + comprimento_vetor * math.cos(angulo_rad)
    fim_vetor_y = y - comprimento_vetor * math.sin(angulo_rad)
    pygame.draw.line(tela, ROXO, (int(x), int(y)), (int(fim_vetor_x), int(fim_vetor_y)), 3)

    comprimento_seta = 12
    angulo_seta = math.radians(25)
    ponta1_x = fim_vetor_x - comprimento_seta * math.cos(angulo_rad - angulo_seta)
    ponta1_y = fim_vetor_y + comprimento_seta * math.sin(angulo_rad - angulo_seta)
    ponta2_x = fim_vetor_x - comprimento_seta * math.cos(angulo_rad + angulo_seta)
    ponta2_y = fim_vetor_y + comprimento_seta * math.sin(angulo_rad + angulo_seta)
    pygame.draw.polygon(tela, ROXO, [(fim_vetor_x, fim_vetor_y), (ponta1_x, ponta1_y), (ponta2_x, ponta2_y)])

"""
    Verifica se ocorreu colisão entre dois objetos.

    1. Calcula a distância entre os centros dos dois objetos.
    2. Compara a distância com a soma dos raios dos dois objetos para determinar se há colisão.

    Parâmetros:
        x1 (float): Coordenada X do centro do primeiro objeto.
        y1 (float): Coordenada Y do centro do primeiro objeto.
        x2 (float): Coordenada X do centro do segundo objeto.
        y2 (float): Coordenada Y do centro do segundo objeto.
        raio_objeto1 (float): Raio do primeiro objeto.
        raio_objeto2 (float): Raio do segundo objeto.

    Retorna:
        bool: `True` se os objetos estiverem colidindo (ou seja, a distância entre seus centros for menor ou igual à soma dos seus raios), caso contrário, `False`.

"""
def verificar_colisao(x1, y1, x2, y2, raio_objeto1, raio_objeto2):
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distancia <= (raio_objeto1 + raio_objeto2)

"""
    Reposiciona o alvo em uma nova posição aleatória dentro de uma área predefinida.

    1. Gera uma nova coordenada X aleatória dentro do intervalo [600, largura - 200].
    2. Gera uma nova coordenada Y aleatória dentro do intervalo [300, altura - 150].
    3. Retorna as novas coordenadas.

    Retorna:
        tuple: Uma tupla contendo as novas coordenadas (x, y) do alvo.
"""
def reposicionar_marcal():
    # Gera uma nova posição aleatória para o marcal
    import random
    novo_x = random.randint(600, largura - 200)
    novo_y = random.randint(300, altura - 150)
    return novo_x, novo_y

"""
    Processa a entrada contínua do teclado para ajustar os parâmetros do lançamento e reiniciar o jogo.

    1. Verifica o estado atual de todas as teclas pressionadas.
    2. Ajusta o ângulo do lançamento com base nas teclas de direção para cima (`K_UP`) e para baixo (`K_DOWN`).
    3. Ajusta a velocidade inicial com base nas teclas de direção para a direita (`K_RIGHT`) e para a esquerda (`K_LEFT`).
    4. Marca o lançamento como ativado se a tecla `K_RETURN` for pressionada.
    5. Define a intenção de reiniciar o jogo se a tecla `K_SPACE` for pressionada.
    6. Limita o ângulo do lançamento ao intervalo [0, 90] graus.
    7. Limita a velocidade inicial ao intervalo [0, 150].

    Parâmetros:
        sens_ang (float): A sensibilidade para ajustes no ângulo (incremento ou decremento por iteração).
        sens_vel (float): A sensibilidade para ajustes na velocidade inicial (incremento ou decremento por iteração).
        lancado (bool): Estado atual indicando se o lançamento já foi iniciado.
        angulo (float): O ângulo atual do lançamento.
        velocidade_inicial (float): A velocidade inicial atual do objeto.

    Retorna:
        tuple: Uma tupla contendo:
            - angulo (float): O ângulo ajustado após o processamento.
            - velocidade_inicial (float): A velocidade inicial ajustada após o processamento.
            - lancado (bool): Estado atualizado indicando se o lançamento foi ativado.
            - restart (bool): Indicação se o jogo deve ser reiniciado.
"""
def processar_entrada_continua(sens_ang, sens_vel, lancado, angulo, velocidade_inicial):
    
    # Obtém o estado atual de todas as teclas
    teclas = pygame.key.get_pressed()

    #restart do jogo
    restart = True

    # Ajusta o ângulo
    if teclas[pygame.K_UP]:
        angulo += sens_ang
    if teclas[pygame.K_DOWN]:
        angulo -= sens_ang
        
    # Ajusta a velocidade
    if teclas[pygame.K_RIGHT]:
        velocidade_inicial += sens_vel
    if teclas[pygame.K_LEFT]:
        velocidade_inicial -= sens_vel

    if teclas[pygame.K_RETURN]:
        lancado = True;
    if teclas[pygame.K_SPACE]:
        restart = False
    
    # Limita o ângulo entre 0 e 90 graus
    angulo = max(0, min(90, angulo))
    # Limita a velocidade inicial entre 0 e 150
    velocidade_inicial = max(0, min(600, velocidade_inicial))

    return angulo, velocidade_inicial, lancado, restart

"""
    Exibe a tela de resultados ao final do jogo, com a pontuação final e a opção de reiniciar.

    1. Monitora eventos do Pygame para permitir o fechamento da janela ou reinício do jogo:
        - Fecha o jogo se o evento de saída (`QUIT`) for detectado.
        - Reinicia o jogo se a tecla `K_SPACE` for pressionada.
    2. Exibe mensagens informando o estado do jogo, incluindo:
        - Uma mensagem de "Fim de Jogo".
        - A pontuação final do jogador.
        - Uma mensagem de desfecho indicando vitória ou derrota, dependendo se a pontuação alcançou ou superou a meta.
        - Uma instrução para pressionar a tecla `ESPAÇO` para reiniciar.
    3. Centraliza e renderiza os textos na tela usando a fonte definida (`fonte1`) e cores específicas para cada mensagem.

    Parâmetros:
        pontuacao (int): A pontuação final obtida pelo jogador.
        meta (int): A pontuação mínima necessária para vencer o jogo.

    Retorna:
        None
"""
def mostrar_resultados(pontuacao, meta):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # Reinicia o jogo
                    return
        
        # Mostrar textos
        texto_fim = fonte1.render("FIM DE JOGO!", True, BRANCO)
        texto_pontuacao_final = fonte1.render(f"Pontuação Final: {pontuacao}", True, BRANCO)
        texto_reiniciar = fonte1.render("Pressione ESPAÇO para jogar novamente", True, BRANCO)
        
        if pontuacao >= meta:
            texto_desfecho = fonte1.render("PARABENS! você venceu esta fase", True, VERDE)
        else:
            texto_desfecho = fonte1.render("Não foi dessa vez, tente novamente...", True, VERMELHO)

        tela.blit(texto_fim, (largura // 2 - texto_fim.get_width() // 2, altura // 2 + 150))
        tela.blit(texto_desfecho, (largura // 2 - texto_desfecho.get_width() // 2, altura // 2 + 50))
        tela.blit(texto_pontuacao_final, (largura // 2 - texto_pontuacao_final.get_width() // 2, altura // 2 - 50))
        tela.blit(texto_reiniciar, (largura // 2 - texto_reiniciar.get_width() // 2, altura // 2 - 150))

        pygame.display.flip()

#---------------------------------------------------------------------------

"""
    Desenha o menu principal na tela do jogo.

    1. Carrega e redimensiona a imagem de fundo para se ajustar ao tamanho da tela.
    2. Desenha o título do jogo no topo do menu.
    3. Cria botões interativos para diferentes opções, incluindo:
        - "Iniciar Jogo"
        - "Dificuldade"
        - "Selecionar Fase"
        - "Como Jogar"
        - "Sair"
    4. Centraliza os textos nos botões e os renderiza com bordas arredondadas.
    5. Atualiza a tela para exibir o menu completo.

    Parâmetros:
        None

    Retorna:
        None
"""
def draw_menu():
    planofundo = pygame.image.load("images/startmenu.webp")
    planofundo = pygame.transform.scale(planofundo, (1600, 1200))
    
    tela.blit(planofundo, (0, 0))

    # Desenhando o título
    titulo = fonte2.render('Chairs: throw at Marçal', True, BRANCO)
    tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 100))

    # Botão "Iniciar Jogo"
    start_button = pygame.Rect(150, 250, 300, 50)
    pygame.draw.rect(tela, BRANCO, start_button, border_radius=20)
    start_text = fonte3.render('Iniciar Jogo', True, PRETO)
    
    tela.blit(start_text, (start_button.left + start_button.width//2 - start_text.get_width()//2,
    start_button.top+start_button.height//2 - start_text.get_height()//2))

    #Botão "Dificuldade"
    dificult_button = pygame.Rect(150, 350, 300, 50)
    pygame.draw.rect(tela, BRANCO, dificult_button, border_radius=20)
    dificult_text = fonte3.render('Dificuldade', True, PRETO)

    tela.blit(dificult_text,(dificult_button.left + dificult_button.width//2 - dificult_text.get_width()//2,
    dificult_button.top+dificult_button.height//2 - dificult_text.get_height()/2))

    #Botão "Fases"
    fases_button = pygame.Rect(150, 450, 300, 50)
    pygame.draw.rect(tela, BRANCO, fases_button, border_radius=20)
    fases_text = fonte3.render('Selecionar fase', True, PRETO)

    tela.blit(fases_text,(fases_button.left + fases_button.width//2 - fases_text.get_width()//2,
    fases_button.top+fases_button.height//2 - fases_text.get_height()/2))

    #Botão "Como Jogar"
    htp_button = pygame.Rect(150, 550, 300, 50)
    pygame.draw.rect(tela, BRANCO, htp_button, border_radius=20)
    htp_text = fonte3.render('Como jogar', True, PRETO)

    tela.blit(htp_text,(htp_button.left + htp_button.width//2 - htp_text.get_width()//2,
    htp_button.top+htp_button.height//2 - htp_text.get_height()/2))

    # Botão "Sair"
    exit_button = pygame.Rect(150, 650, 300, 50)
    pygame.draw.rect(tela, BRANCO, exit_button, border_radius=20)
    exit_text = fonte3.render('Sair', True, PRETO)

    tela.blit(exit_text, (exit_button.left + exit_button.width//2 - exit_text.get_width()//2,
    exit_button.top+exit_button.height//2 - exit_text.get_height()//2))


    pygame.display.update()

"""
    Gera e desenha um botão com o texto fornecido na tela.

    1. Cria um botão retangular com bordas arredondadas.
    2. Renderiza o texto fornecido centralizado no botão.
    3. Exibe o botão na tela.

    Parâmetros:
        None

    Retorna:
        None
"""
def gerar_btn():
    dificult_button = pygame.Rect(150, 350, 300, 50)
    pygame.draw.rect(tela, BRANCO, dificult_button, border_radius=20)
    dificult_text = fonte3.render('texto', True, PRETO)

    tela.blit(dificult_text,(dificult_button.left + dificult_button.width//2 - dificult_text.get_width()//2,
    dificult_button.top+dificult_button.height//2 - dificult_text.get_height()/2))

"""
    Exibe uma janela para alterar parâmetros de dificuldade ou fase do jogo.

    1. Cria uma nova janela temporária de 600x800 pixels.
    2. Define o título da janela com base no parâmetro fornecido:
        - "Selecione a dificuldade" se o parâmetro for "dificuldade".
        - "Selecione a fase" caso contrário.
    3. Exibe botões interativos com as opções correspondentes ao parâmetro:
        - Para "dificuldade": "Fácil", "Médio", "Difícil".
        - Para "fase": "Terra", "Lua", "Marte".
    4. Detecta cliques nos botões e altera o valor global das variáveis `dificuldade` ou `fases`.
    5. Após selecionar uma opção, retorna à janela principal do jogo.

    Parâmetros:
        parametro (str): Define o tipo de ajuste a ser feito. Pode ser:
            - "dificuldade": Exibe opções para alterar a dificuldade do jogo.
            - Outro valor: Exibe opções para alterar a fase do jogo.

    Retorna:
        None
"""
def mudar_parametro(parametro):
    nova_janela = pygame.display.set_mode((600, 800))

    if parametro == "dificuldade":
        pygame.display.set_caption("Selecione a dificuldade")
    else:
        pygame.display.set_caption("Selecione a fase")
    
    cadeado = True
    while cadeado:
        
        global fases, dificuldade
        clicado = False
        nova_janela.fill(AZUL_ESCURO)

        b1 = pygame.Rect(150, 200, 300, 100)
        pygame.draw.rect(nova_janela, BRANCO, b1, border_radius=20)
        b2 = pygame.Rect(150, 400, 300, 100)
        pygame.draw.rect(nova_janela, BRANCO, b2, border_radius=20)
        b3 = pygame.Rect(150, 600, 300, 100)
        pygame.draw.rect(nova_janela, BRANCO, b3, border_radius=20)
        if parametro == "dificuldade":
            b1_text = fonte3.render('Fácil', True, PRETO)
            b2_text = fonte3.render('Médio', True, PRETO)
            b3_text = fonte3.render('Difícil', True, PRETO)

        else:
            b1_text = fonte3.render('Terra', True, PRETO)
            b2_text = fonte3.render('Lua', True, PRETO)
            b3_text = fonte3.render('Marte', True, PRETO)
        
        nova_janela.blit(b1_text, (b1.left + b1.width//2 - b1_text.get_width()//2, b1.top+b1.height//2 - b1_text.get_height()/2))
        nova_janela.blit(b2_text, (b2.left + b2.width//2 - b2_text.get_width()//2, b2.top+b2.height//2 - b2_text.get_height()/2))
        nova_janela.blit(b3_text, (b3.left + b3.width//2 - b3_text.get_width()//2, b3.top+b3.height//2 - b3_text.get_height()/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cadeado = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not clicado:
                if b1.collidepoint(event.pos):
                    clicado = True
                    if parametro == "dificuldade":
                        dificuldade = 1
                    else:
                        fases = 1
                    cadeado = False
                elif b2.collidepoint(event.pos) and not clicado:
                    clicado = True
                    if parametro == "dificuldade":
                        dificuldade = 2
                    else:
                        fases = 2
                    cadeado = False
                elif b3.collidepoint(event.pos) and not clicado:
                    clicado = True
                    if parametro == "dificuldade":
                        dificuldade = 3
                    else:
                        fases = 3
                    cadeado = False
            elif event.type == pygame.MOUSEBUTTONUP and clicado:
                clicado = False

        pygame.display.flip()

    # Retorna para a janela principal
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Chairs!')
    draw_menu()


"""
    Função que exibe uma janela pop-up com as instruções de como jogar o jogo "Chairs: Throw at Marçal". 

    Descrição:
        O pop-up fornece detalhes sobre os controles e o objetivo do jogo, permitindo que o jogador entenda como interagir com o jogo. A função fica em execução até que o jogador feche a janela de instruções, momento em que retorna ao menu principal.
        1. A função cria uma nova janela (600x800 pixels) para exibir as instruções.
        2. A janela contém um texto detalhado sobre como jogar, incluindo os controles e o objetivo.
        3. O texto é quebrado em várias linhas para garantir que se ajuste à largura da janela.
        5. Ao fechar a janela, o jogo retorna ao menu principal, restaurando a janela original.

    Parâmetros:
        None

    Retorno:
        None

"""
def abrir_pop_up():
    # Criar a nova janela
    nova_janela = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Como Jogar - Chairs: Throw at Marçal")
    
    # Definir cores
    COR_FUNDO = AZUL_ESCURO
    COR_TITULO = (255, 215, 0)  # Amarelo dourado para destaque
    COR_TEXTO = BRANCO
    COR_SECAO = (255, 165, 0)  # Laranja para seções
    
    # Definir fontes com tamanhos diferentes
    fonte_titulo = pygame.font.Font(None, 48)
    fonte_secao = pygame.font.Font(None, 36)
    fonte_texto = pygame.font.Font(None, 28)
    
    def render_texto_centralizado(superficie, texto, fonte, cor, y_pos, largura_max):
        texto_surface = fonte.render(texto, True, cor)
        texto_rect = texto_surface.get_rect(centerx=superficie.get_rect().centerx, top=y_pos)
        superficie.blit(texto_surface, texto_rect)
        return texto_rect.bottom
    
    def render_texto_justificado(superficie, texto, fonte, cor, pos_inicial, largura_max):
        palavras = texto.split()
        linhas = []
        linha_atual = []
        for palavra in palavras:
            teste_linha = ' '.join(linha_atual + [palavra])
            teste_surface = fonte.render(teste_linha, True, cor)
            if teste_surface.get_width() <= largura_max:
                linha_atual.append(palavra)
            else:
                linhas.append(' '.join(linha_atual))
                linha_atual = [palavra]
        
        if linha_atual:
            linhas.append(' '.join(linha_atual))
        
        y_offset = pos_inicial[1]
        for linha in linhas:
            texto_surface = fonte.render(linha, True, cor)
            texto_rect = texto_surface.get_rect(centerx=superficie.get_rect().centerx, top=y_offset)
            superficie.blit(texto_surface, texto_rect)
            y_offset += fonte.get_height() + 5
        
        return y_offset
    
    cadeado = True
    while cadeado:
        # Preencher o fundo
        nova_janela.fill(COR_FUNDO)
        
        # Renderizar título
        y_pos = 50
        y_pos = render_texto_centralizado(nova_janela, "Chairs: Throw at Marçal", fonte_titulo, COR_TITULO, y_pos, 500)
        y_pos += 30  # Espaço após o título
        
        # Renderizar seções
        y_pos = render_texto_centralizado(nova_janela, "Objetivo", fonte_secao, COR_SECAO, y_pos, 500)
        y_pos += 20
        y_pos = render_texto_justificado(nova_janela, 
            "Seu objetivo é acertar o Marçal o máximo de vezes possível antes que o tempo acabe. Alcance a pontuação meta para vencer o jogo!", 
            fonte_texto, COR_TEXTO, (50, y_pos), 500)
        
        y_pos += 30
        y_pos = render_texto_centralizado(nova_janela, "Controles", fonte_secao, COR_SECAO, y_pos, 500)
        y_pos += 20
        
        # Lista de controles com ícones ou marcadores
        controles = [
            "Seta para Cima: Aumentar ângulo",
            "Seta para Baixo: Diminuir ângulo",
            "Seta para a Direita: Aumentar velocidade",
            "Seta para a Esquerda: Diminuir velocidade",
            "Espaço: Lançar cadeira"
        ]
        
        for controle in controles:
            y_pos = render_texto_justificado(nova_janela, controle, fonte_texto, COR_TEXTO, (50, y_pos), 500)
            y_pos += 10
        
        # Mensagem de rodapé
        y_pos += 30
        render_texto_centralizado(nova_janela, "Boa sorte! O Marçal está esperando...", fonte_texto, COR_SECAO, y_pos, 500)
        
        # Manipulação de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cadeado = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cadeado = False
        
        # Atualizar a tela
        pygame.display.flip()
    
    # Retornar para a janela principal
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Chairs!')
    draw_menu()

"""
    Inicia o jogo, gerenciando a física do lançamento, a interação do jogador, e os elementos visuais.

    1. Configuração inicial:
        - Define variáveis de física como gravidade (g), resistência do ar (k), e tempo total do jogo.
        - Ajusta os parâmetros de acordo com a dificuldade e a fase selecionadas.

    2. Elementos gráficos:
        - Configura imagens de fundo, projétil (cadeira), alvo (Marçal), e ícones informativos.
        - Renderiza informações na tela, incluindo ângulo, velocidade, pontuação, tempo restante, e meta de pontos.

    3. Interatividade:
        - Detecta e processa entradas do jogador para alterar ângulo e velocidade antes do lançamento.
        - Atualiza a posição do projétil após o lançamento, considerando resistência do ar e gravidade.
        - Detecta colisões com o alvo (marçal), atualizando a pontuação e reposicionando o alvo.

    4. Condições de término:
        - Reinicia o projétil se ele sair da tela.
        - Finaliza o jogo e exibe resultados se o tempo acabar.

    5. Sistema de desenho:
        - Adiciona a trajetória do projétil ao traçado e redesenha a cada quadro.
        - Atualiza a tela a 60 quadros por segundo usando `pygame.time.Clock`.

    Parâmetros:
        - relogio (pygame.time.Clock): Controla a taxa de atualização dos quadros.

    Retorna:
        None
"""
def start_game(relogio):
    # Variáveis de Física
    g = 9.81  # Aceleração default
    air_rest = 0;
    angulo = 45  # Ângulo de lançamento em graus
    velocidade_inicial = 50  # Velocidade inicial
    t = 0  # Tempo
    k = 0.05  # Coeficiente de resistência do ar

    #meta de pontuação default para a dificuldade
    meta_pontuacao = 15
    #tempo total default
    tempo_total = 60


    # Variáveis de controle de sensibilidade
    sens_ang = 0.5  # Velocidade de mudança do ângulo
    sens_vel = 0.5  # Velocidade de mudança da velocidade inicial

    # Posição inicial do projétil
    posicao_inicial_x, posicao_inicial_y = 100, altura - 250
    posicao_x, posicao_y = posicao_inicial_x, posicao_inicial_y



    lancado = False
    jogo_ativo = False
    pontuacao = 0
    tracado_pontos = []

    # Prepara a imagem da cadeira
    cadeira = pygame.image.load("images/cadeira.png")
    cadeira = pygame.transform.scale(cadeira, (150, 150))
    boneco_largura, boneco_altura = cadeira.get_size()

    # Prepara a imagem e caracteristicas do marcal
    marcal = pygame.image.load("images/marcal.png")

    tracado = pygame.image.load("images/quadrado.png")
    tracado = pygame.transform.scale(tracado, (7, 7))

    if dificuldade == 1:
        tempo_total = 60
        meta_pontuacao = 15
        marcal = pygame.transform.scale(marcal, (125, 125))
    elif dificuldade == 2:
        tempo_atual = 60
        meta_pontuacao = 20
        marcal = pygame.transform.scale(marcal, (100, 100))
    else:
        tempo_total = 30
        meta_pontuacao = 15
        marcal = pygame.transform.scale(marcal, (75, 75))

    marcal_largura, marcal_altura = marcal.get_size()
    marcal_x, marcal_y = 990, 550

    # Sistema de tempo
    tempo_inicial = pygame.time.get_ticks()
    
    # Prepara o plano de fundo
    if fases == 1:
        g = 9.81
        k = 0.03
        fundo_img = pygame.image.load("images/debate.png").convert()
    elif fases == 2:
        k = 0.00001
        g = 1.62
        fundo_img = pygame.image.load("images/lua2.png").convert()
    else:
        k = 0.3
        g = 8.87
        fundo_img = pygame.image.load("images/marte.jpeg").convert()
    
    fundo_img = pygame.transform.scale(fundo_img, (1400, 800))

    #prepara o icone da resistencia do ar
    air_rest_icon = pygame.image.load("images/air_resistence.png")
    air_rest_icon = pygame.transform.scale(air_rest_icon, (50, 50))

    #prepara o icone da gravidade
    grav_icon = pygame.image.load("images/grav.png")
    grav_icon = pygame.transform.scale(grav_icon, (50, 50))

    jogo_ativo = True
    while jogo_ativo:
        
        tela.blit(fundo_img, (0, 0)) #desenha o fundo
        

        for evento in pygame.event.get(): #fechar jogo
            if evento.type == pygame.QUIT:
                jogo_ativo = False
   
        # Calcula o tempo restante
        tempo_atual = pygame.time.get_ticks()
        tempo_passado = (tempo_atual - tempo_inicial) // 1000  # Converte para segundos
        tempo_restante = tempo_total - tempo_passado
        if tempo_restante <= 0 and jogo_ativo:        # Verifica se o tempo acabou
            jogo_ativo = False

        if jogo_ativo:
            if not lancado:

                tracado_pontos.clear()

                # Processa entrada contínua das teclas
                angulo, velocidade_inicial, lancado, _ = processar_entrada_continua(sens_ang, sens_vel, lancado, angulo, velocidade_inicial)
                
                #cadeira = pygame.transform.rotate(boneco_aux, angulo);
                desenhar_vetor_direcao(posicao_x, posicao_y, angulo, velocidade_inicial)
                posicao_x, posicao_y = posicao_inicial_x, posicao_inicial_y

            # Atualiza a posição somente se foi lançado
            else:
                # Dentro do loop principal, ao calcular a nova posição
                (posicao_x, posicao_y), _ = atualizar_posicao_e_velocidade_com_resistencia(
                    t, angulo, velocidade_inicial, posicao_inicial_x, posicao_inicial_y, g, k
                )
                t += 0.1

                # Verifica colisão com o marcal
                if verificar_colisao(
                    posicao_x + boneco_largura//2, posicao_y + boneco_altura // 2,
                    marcal_x + marcal_largura//2, marcal_y + marcal_altura//2,
                    0.6 * boneco_largura, 0.25 * marcal_largura
                ):
                    pontuacao += 1
                    lancado = False
                    # Reposiciona o marcal após acertar
                    marcal_x, marcal_y = reposicionar_marcal()
                    t = 0

            # Se o projétil sair da tela, reinicia
            if posicao_y > altura or posicao_x > largura:
                lancado = False
                posicao_x, posicao_y = posicao_inicial_x, posicao_inicial_y
                t = 0

            # Desenha o marcal
            tela.blit(marcal, (int(marcal_x), int(marcal_y)))

            # Desenha todos os pontos armazenados no traçado
            for i, ponto in enumerate(tracado_pontos):
                if i % 3 == 0:  # Se o índice for par, desenha o ponto
                    tela.blit(tracado, ponto)

            # Adiciona a posição atual ao traçado
            tracado_pontos.append((int(posicao_x + boneco_largura * 0.1), int(posicao_y + boneco_altura // 2)))

            # Desenha a imagem da cadeira
            tela.blit(cadeira, (int(posicao_x), int(posicao_y)))    

        # Interface do usuário
        fonte1 = pygame.font.Font(None, 36)
        
        # Mostra informações durante o jogo
        if jogo_ativo:
            texto_angulo = fonte1.render(f"Ângulo: {angulo:.1f}°", True, BRANCO)
            texto_velocidade = fonte1.render(f"Velocidade: {velocidade_inicial:.1f} m/s", True, BRANCO)
            texto_pontuacao = fonte1.render(f"Pontuação: {pontuacao}", True, VERDE)
            texto_tempo = fonte1.render(f"Tempo: {tempo_restante}s", True, VERMELHO)
            texto_meta = fonte1.render(f"Meta de pontos: {meta_pontuacao} pontos", True, AZUL) 
            texto_grav = fonte4.render(f"{g} m/s", True, BRANCO)
            if k == 0.00001:
                texto_air_rest = fonte4.render("0", True, BRANCO)
            else:
                texto_air_rest = fonte4.render(f"{k}", True, BRANCO)


            tela.blit(texto_angulo, (10, 10))
            tela.blit(texto_velocidade, (10, 50))
            tela.blit(texto_pontuacao, (10, 90))
            tela.blit(texto_tempo, (10, 130))
            tela.blit(texto_meta, (10, 170))
            tela.blit(air_rest_icon, (830, 20))
            tela.blit(grav_icon, (1100, 20))
            tela.blit(texto_air_rest, (910 , 25) )
            tela.blit(texto_grav, (1170 , 25) )
        else:
            mostrar_resultados(pontuacao, meta_pontuacao)
            draw_menu()

        pygame.display.flip()
        relogio.tick(60) 
#--------------------------------------------------------------------------------
"""
    Função principal que gerencia o menu inicial do jogo e as interações do jogador.

    1. Configuração inicial:
        - Inicializa o estado do menu (`in_menu`) e o controle de clique (`clicado`).
        - Desenha o menu inicial na tela e define os botões (iniciar, sair, ajuda, dificuldade, e fases).

    2. Sistema de eventos:
        - Detecta eventos do pygame, como fechar o jogo (`QUIT`) ou interagir com os botões via cliques do mouse.
        - Realiza a ação correspondente ao botão clicado:
            - Inicia o jogo chamando `start_game`.
            - Encerra o programa.
            - Exibe a janela de ajuda com `abrir_pop_up`.
            - Modifica parâmetros de dificuldade ou fase com `mudar_parametro`.

    3. Controle de cliques:
        - Garante que cada clique seja processado uma única vez ao controlar o estado do botão pressionado.

    Parâmetros:
        None

    Retorna:
        None
"""
def main():
    in_menu = True
    clicado = False
    draw_menu()

    start_button = pygame.Rect(150, 250, 300, 50)
    exit_button = pygame.Rect(150, 650, 300, 50)
    htp_button = pygame.Rect(150, 550, 300, 50)
    dificult_button = pygame.Rect(150, 350, 300, 50)
    fases_button = pygame.Rect(150, 450, 300, 50)

    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not clicado:
                if start_button.collidepoint(event.pos):
                    jogo_ativo = True;
                    clicado = True;
                    relogio = pygame.time.Clock()
                    start_game(relogio)
                elif exit_button.collidepoint(event.pos):
                    clicado = True
                    pygame.quit()
                    sys.exit()
                elif htp_button.collidepoint(event.pos):
                    clicado = True
                    abrir_pop_up();
                elif dificult_button.collidepoint(event.pos):
                    clicado = True
                    mudar_parametro("dificuldade")
                elif fases_button.collidepoint(event.pos):
                    clicado = True
                    mudar_parametro("fases")
            elif event.type == pygame.MOUSEBUTTONUP and clicado:
                clicado = False

if __name__ == '__main__':
    main()
