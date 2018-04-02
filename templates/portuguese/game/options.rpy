## Este arquivo contém algumas das opções que podem ser mudadas para
## personalizar o jogo Ren'Py. Ele apenas contém as opções mais comuns.
## Você ainda pode adicionar mais personalizações.
##
## As linhas começadas com dois hashtags '#' são comentários, você não deve
## apagá-las. As linhas começadas apenas com um hashtag '#' 
## contém código não ativo e você pode desejar apagar a hashtag '#' acaso
## julgar apropriado.

init -1 python hide:

    ## Esta variável habilita as ferramentas de desenvolvedor. Deve ser
    ## ajustada para falsa ('False') antes do lançamento do jogo, assim o usuário 
    ## não poderá utilizar 'cheats' utilizando as ferramentas do desenvolvedor.

    config.developer = True

    ## Estes são os controles da largura e da altura da tela. 

    config.screen_width = 800
    config.screen_height = 600

    ## Estes são os controles para modificar o título da janela, quando Ren'Py é executado em modo janela.

    config.window_title = u"PROJECT_NAME"

    ## Estes são os controles do nome e da versão do jogo; eles são utilizados nos 
    ## rastreamentos e outros logs de depuração.
    
    config.name = "PROJECT_NAME"
    config.version = "0.0"

    #########################################
    ## Temas

    ## Para utilizar uma função de tema, utilizamos themes.roundrect.
    ## Este tema configura o uso de retângulos arredondados.
    ##
    ## A função de tema aceita uma série de parâmetros que podem 
    ## personalizar o esquema de cores.

    theme.roundrect(

        ## Cor base de um elemento (widget).
        widget = "#003c78",

        ## Cor de um elemento com foco.
        widget_hover = "#0050a0",

        ## Cor do texto em um elemento.
        widget_text = "#c8ffff",

        ## Cor do texto em um elemento selecionado (por exemplo,
        ## o valor atual de uma preferência).
        widget_selected = "#ffffc8",

        ## Cor de um elemento desabilitado.
        disabled = "#404040",

        ## Cor do texto de um elemento desabilitado.
        disabled_text = "#c8c8c8",

        ## Cor das etiquetas de informação.
        label = "#ffffff",

        ## Cor do quadro ('Frame') que contém os elementos.
        frame = "#6496c8",

        ## Se esta variável estiver designada como 'True', a janela interna do jogo terá os
        ## cantos arredondados. Se for 'False', será retângular.
        rounded_window = False,

        ## Fundo do menu principal. Pode ser uma cor que
        ## começa com '#' ou também pode ser o nome de um arquivo de imagem.
        ## No segundo caso, deve ocupar completamente o comprimento e altura da tela. 
        mm_root = "#dcebff",

        ## Fundo do menu do jogo. Pode ser uma cor que
        ## começa com '#' ou também pode ser o nome de um arquivo de imagem.
        ## No segundo caso, deve ocupar completamente o comprimento e altura da tela.
        gm_root = "#dcebff",

        ## Acabamos com esse tema. O tema personalizará vários
        ## estilos, que podem ser modificados mais abaixo. 
        )

    #########################################
    ## Estas configurações permitem personalizar a tela que contém 
    ## o diálogo e a narração, substituindo-a com uma imagem.

    ## Fundo da tela. Em um quadro ('Frame'), os dois números são
    ## as dimensões das bordas esquerda/direita e 
    ## superior/inferior, respectivamente.

    # style.window.background = Frame("frame.png", 12, 12)

    ## A margem é o espaço ao redor da tela, cujo qual o
    ## fundo não aparece.

    # style.window.left_margin = 6
    # style.window.right_margin = 6
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    ## O 'preenchimento' ('padding') é o espaço dentro da janela, 
    ## em que o o fundo é desenhado, mas não o texto.

    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    ## Altura mínima da tela, incluíndo margem e preenchimento.

    # style.window.yminimum = 250


    #########################################
    ## Esta seção permite você alterar a disposição do menu principal.

    ## O ajuste funciona da seguinte maneira: primeiro é
    ## estabelecido um ponto de ancoragem (anchor) dentro de um elemento
    ## gráfico (disponível) e a posição (pos) de um ponto na tela. 
    ## Por fim, é colocado o elemento gráfico de forma 
    ## que ambos os pontos coincidam.

    ## Os pontos de ancoragem e de posição (anchor/pos) podem ser indicados 
    ## com um número inteiro ou decimal (int/float). Se ele for inteiro, 
    ## os pixels desde o canto superior esquerdo. Se ele for decimal, 
    ## é interpretado como a fração das dimensões do elemento gráfico ou da
    ## tela.

    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5


    #########################################
    ## Personalização do tipo de letra utilizado por padrão.

    ## O arquivo que contém a fonte padrão.

    # style.default.font = "DejaVuSans.ttf"

    ## O tamanho padrão da fonte.

    # style.default.size = 22

    ## Nota: Isso apenas muda o tamanho da fonte do texto. Outros botões 
    ## têm seus próprios estilos.


    #########################################
    ## Ajuste de alguns sons utilizados por Ren'Py.

    ## Ajuste para falso ('False') acaso o jogo não tiver efeitos de som. 

    config.has_sound = True

    ## Ajuste para falso ('False') acaso o jogo não tiver música. 

    config.has_music = True

    ## Ajuste para verdadeiro ('True') acaso o jogo conter vozes. 

    config.has_voice = False

    ## Sons utilizados quando se clica em um botão.

    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    ## Sons utilizados quando se entra ou sai do menu do jogo.

    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    ## Som de exemplo utilizado para checar o volume do som.

    # config.sample_sound = "click.wav"

    ## Música do menu principal.

    # config.main_menu_music = "main_menu_theme.ogg"


    #########################################
    ## Ajuda

    ## Configuração das opções de ajuda dos menus de Ren'Py.
    ## Pode ser:
    ## - Uma etiqueta (label) no 'script', em cujo qual se chama essa
    ##   etiqueta para mostrar a ajuda ao usuário.
    ## - O nome de um arquivo relativo ao diretório base, que é aberto 
    ##   em um navegador web.
    ## - 'None', para desabilitar a ajuda (deve-se eliminar o botão
    ##   de ajuda nas telas).
    config.help = "README.html"


    #########################################
    ## Transições.

    ## Usada da abertura para o menu do jogo. 
    config.enter_transition = None

    ## Usada quando saímos do menu do jogo para o jogo. 
    config.exit_transition = None

    ## Usada entre as telas do menu do jogo.
    config.intra_transition = None

    ## Usada do menu principal para o menu do jogo.
    config.main_game_transition = None

    ## Usada para retornar para o menu principal do jogo. 
    config.game_main_transition = None

    ## Usada quando entramos no menu principal pela tela de abertura
    config.end_splash_transition = None

    ## Usada quando entramos no menu principal após o jogo ser terminado. 
    config.end_game_transition = None

    ## Usada quando o jogo é carregado.
    config.after_load_transition = None

    ## Usada quando se mostra uma janela.
    config.window_show_transition = None

    ## Usada quando se oculta uma janela.
    config.window_hide_transition = None

    ## Usada quando se usa texto no modo NVL imediatamente depois do 
    ## texto em modo ADV.
    config.adv_nvl_transition = dissolve

    ## Usada quando se usa texto no modo ADV imediatamente depois do 
    ## texto em modo NVL.
    config.nvl_adv_transition = dissolve

    ## Usada quando se mostra a tela Sim/Não ('Yes/No')
    config.enter_yesno_transition = None

    ## Usada quando se oculta a tela Sim/Não ('Yes/No')
    config.exit_yesno_transition = None

    ## Usada quando se entra em uma repetição ('Replay')
    config.enter_replay_transition = None

    ## Usada ao sair de uma repetição ('Replay')
    config.exit_replay_transition = None

    ## Usada quando a imagem é substituída por uma sentença 'say' com
    ## atributos de imagem.
    config.say_attribute_transition = None

    #########################################
    ## Nome do diretório no qual estão armazenados os dados do jogo.
    ## (Deve ser ajustado no início, antes dos outros blocos 'init', para
    ## que a informação salva possa ser encontrada pelo código 'init'.)
python early:
    config.save_directory = "PROJECT_NAME-UNIQUE"

init -1 python hide:
    #########################################
    ## Valores padrão das opções. 

    ## Nota: Estas opções são somente consideradas na primeira vez que
    ## um jogo é executado. Para que sejam carregadas uma segunda vez, 
    ## por favor deletar 'game/saves/persistent'.

    ## Ajuste para verdadeiro ('True') para iniciar com a tela cheia (fullscreen).

    config.default_fullscreen = False

    ## Velocidade do texto padrão em caracteres por segundo. 0 é infinito. 

    config.default_text_cps = 0

    ## O ajuste de auto-avanço por padrão. 

    config.default_afm_time = 10

    #########################################
    ## Mais customizações podem vir aqui.
