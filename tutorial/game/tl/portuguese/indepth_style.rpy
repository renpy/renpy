
# game/indepth_style.rpy:40
translate portuguese new_gui_17a0326e:

    # e "When you create a new project, Ren'Py will automatically create a GUI - a Graphical User Interface - for it."
    e "Quando você cria um novo projeto, o Ren'Py cria automaticamente uma GUI, uma interface gráfica do usuário, para ele."

# game/indepth_style.rpy:42
translate portuguese new_gui_12c814ed:

    # e "It defines the look of both in-game interface, like this text box, and out-of-game interface like the main and game menus."
    e "Ela define a aparência tanto da interface dentro do jogo, como esta caixa de texto, quanto da interface fora do jogo, como o menu principal e os menus do jogo."

# game/indepth_style.rpy:44
translate portuguese new_gui_0a2a73bb:

    # e "The default GUI is meant to be nice enough for a simple project. With a few small changes, it's what you're seeing in this game."
    e "A GUI padrão foi feita para ser boa o suficiente para um projeto simples. Com algumas pequenas mudanças, é o que você está vendo neste jogo."

# game/indepth_style.rpy:46
translate portuguese new_gui_22adf68e:

    # e "The GUI is also meant to be easy for an intermediate creator to customize. Customizing the GUI consists of changing the image files in the gui directory, and changing variables in gui.rpy."
    e "A GUI também foi feita para ser fácil de personalizar por um criador intermediário. Personalizá-la consiste em mudar os arquivos de imagem no diretório gui e alterar variáveis em gui.rpy."

# game/indepth_style.rpy:48
translate portuguese new_gui_da21de30:

    # e "At the same time, even when customized, the default GUI might be too recognizable for an extremely polished game. That's why we've made it easy to totally replace."
    e "Ao mesmo tempo, mesmo quando personalizada, a GUI padrão pode ser reconhecível demais para um jogo extremamente refinado. É por isso que facilitamos substituí-la por completo."

# game/indepth_style.rpy:50
translate portuguese new_gui_45765574:

    # e "We've put an extensive guide to customizing the GUI on the Ren'Py website. So if you want to learn more, visit the {a=https://www.renpy.org/doc/html/gui.html}GUI customization guide{/a}."
    e "Colocamos um guia extenso para personalizar a GUI no site do Ren'Py. Então, se quiser aprender mais, visite o {a=https://www.renpy.org/doc/html/gui.html}guia de personalização da GUI{/a}."

# game/indepth_style.rpy:58
translate portuguese styles_fa345a38:

    # e "Ren'Py has a powerful style system that controls what displayable look like."
    e "O Ren'Py tem um poderoso sistema de estilos que controla a aparência dos exibíveis."

# game/indepth_style.rpy:60
translate portuguese styles_6189ee12:

    # e "While the default GUI uses variables to provide styles with sensible defaults, if you're replacing the GUI or creating your own screens, you'll need to learn about styles yourself."
    e "Embora a GUI padrão use variáveis para fornecer estilos com valores padrão razoáveis, se você estiver substituindo a GUI ou criando suas próprias telas, precisará aprender sobre estilos por conta própria."

# game/indepth_style.rpy:66
translate portuguese styles_menu_a4a6913e:

    # e "What would you like to know about styles?" nointeract
    e "O que você gostaria de saber sobre estilos?" nointeract

# game/indepth_style.rpy:98
translate portuguese style_basics_9a79ef89:

    # e "Styles let a displayable look different from game to game, or even inside the same game."
    e "Os estilos permitem que um exibível tenha aparência diferente de jogo para jogo, ou até dentro do mesmo jogo."

# game/indepth_style.rpy:103
translate portuguese style_basics_48777f2c:

    # e "Both of these buttons use the same displayables. But since different styles have been applied, the buttons look different from each other."
    e "Ambos estes botões usam os mesmos exibíveis. Mas, como estilos diferentes foram aplicados, eles parecem diferentes um do outro."

# game/indepth_style.rpy:108
translate portuguese style_basics_57704d8c:

    # e "Styles are a combination of information from four different places."
    e "Os estilos são uma combinação de informações vindas de quatro lugares diferentes."

# game/indepth_style.rpy:121
translate portuguese style_basics_144731f6:

    # e "The first place Ren'Py can get style information from is part of a screen. Each displayable created by a screen can take a style name and style properties."
    e "O primeiro lugar de onde o Ren'Py pode obter informações de estilo é uma tela. Cada exibível criado por uma tela pode receber um nome de estilo e propriedades de estilo."

# game/indepth_style.rpy:138
translate portuguese style_basics_67e48162:

    # e "When a screen displayable contains text, style properties prefixed with text_ apply to that text."
    e "Quando um exibível de tela contém texto, as propriedades de estilo com o prefixo 'text_' se aplicam a esse texto."

# game/indepth_style.rpy:151
translate portuguese style_basics_03516b4a:

    # e "The next is as part of a displayable created in an image statement. Style properties are just arguments to the displayable."
    e "O próximo é como parte de um exibível criado em uma instrução image. As propriedades de estilo são apenas argumentos do exibível."

# game/indepth_style.rpy:160
translate portuguese style_basics_ccc0d1ca:

    # egreen "Style properties can also be given as arguments when defining a character."
    egreen "As propriedades de estilo também podem ser fornecidas como argumentos ao definir um personagem."

# game/indepth_style.rpy:162
translate portuguese style_basics_013ab314:

    # egreen "Arguments beginning with who_ are style properties applied to the character's name, while those beginning with what_ are applied to the character's dialogue."
    egreen "Argumentos que começam com 'who_' são propriedades de estilo aplicadas ao nome do personagem, enquanto os que começam com 'what_' são aplicados ao diálogo do personagem."

# game/indepth_style.rpy:164
translate portuguese style_basics_dbe80939:

    # egreen "Style properties that don't have a prefix are also applied to the character's name."
    egreen "Propriedades de estilo sem prefixo também são aplicadas ao nome do personagem."

# game/indepth_style.rpy:174
translate portuguese style_basics_ac6a8414:

    # e "Finally, there is the the style statement, which creates or changes a named style. By giving Text the style argument, we tell it to use the blue_text style."
    e "Por fim, há a instrução 'style', que cria ou altera um estilo nomeado. Ao dar a 'Text' o argumento style, dizemos a ela para usar o estilo 'blue_text'."

# game/indepth_style.rpy:180
translate portuguese style_basics_3d9bdff7:

    # e "A style property can inherit from a parent. If a style property is not given in a style, it comes from the parent of that style."
    e "Um estilo pode herdar de um pai. Se uma propriedade de estilo não for dada em um estilo, ela virá do pai desse estilo."

# game/indepth_style.rpy:182
translate portuguese style_basics_49c5fbfe:

    # e "By default the parent of the style has the same name, with the prefix up to the the first underscore removed. If the style does not have an underscore in its name, 'default' is used."
    e "Por padrão, o pai do estilo tem o mesmo nome, com o prefixo até o primeiro sublinhado removido. Se o estilo não tiver sublinhado no nome, usa-se 'default'."

# game/indepth_style.rpy:184
translate portuguese style_basics_6ab170a3:

    # e "For example, blue_text inherits from text, which in turn inherits from default. The default style defines all properties, so it doesn't inherit from anything."
    e "Por exemplo, 'blue_text' herda de 'text', que por sua vez herda de 'default'. O estilo 'default' define todas as propriedades, então não herda de nada."

# game/indepth_style.rpy:190
translate portuguese style_basics_f78117a7:

    # e "The parent can be explicitly changed by giving the style statement an 'is' clause. In this case, we're explictly setting the style to the parent of text."
    e "O pai pode ser alterado explicitamente dando à instrução 'style' uma cláusula 'is'. Neste caso, estamos definindo explicitamente o estilo para herdar de 'text'."

# game/indepth_style.rpy:194
translate portuguese style_basics_6007040b:

    # e "Each displayable has a default style name. By default, it's usually the lower-case displayable name, like 'text' for Text, or 'button' for buttons."
    e "Cada exibível tem um nome de estilo padrão. Normalmente, ele é o nome do exibível em minúsculas, como 'text' para Text ou 'button' para botões."

# game/indepth_style.rpy:196
translate portuguese style_basics_35db9a05:

    # e "In a screen, a displayable can be given the style_prefix property to give a prefix for that displayable and it's children."
    e "Em uma tela, um exibível pode receber a propriedade 'style_prefix' para dar um prefixo a esse exibível e a seus filhos."

# game/indepth_style.rpy:198
translate portuguese style_basics_422a87f7:

    # e "For example, a text displayable with a style_prefix of 'help' will be given the style 'help_text'."
    e "Por exemplo, um exibível de texto com um style_prefix de 'help' receberá o estilo 'help_text'."

# game/indepth_style.rpy:200
translate portuguese style_basics_bad2e207:

    # e "Lastly, when a displayable is a button, or inside a button, it can take style prefixes."
    e "Por fim, quando um exibível é um botão, ou está dentro de um botão, ele pode usar prefixos de estilo."

# game/indepth_style.rpy:202
translate portuguese style_basics_22ed20a1:

    # e "The prefixes idle_, hover_, and insensitive_ are used when the button is unfocused, focused, and unfocusable."
    e "Os prefixos 'idle_', 'hover_' e 'insensitive_' são usados quando o botão está desfocado, focado e incapaz de receber foco."

# game/indepth_style.rpy:204
translate portuguese style_basics_7a58037e:

    # e "These can be preceded by selected_ to change how the button looks when it represents a selected value or screen."
    e "Eles podem ser precedidos por 'selected_' para mudar a aparência do botão quando ele representa um valor ou tela selecionada."

# game/indepth_style.rpy:233
translate portuguese style_basics_0cdcb8c3:

    # e "This screen shows the style prefixes in action. You can click on a button to select it, or click outside to advance."
    e "Esta tela mostra os prefixos de estilo em ação. Você pode clicar em um botão para selecioná-lo, ou clicar fora para avançar."

# game/indepth_style.rpy:240
translate portuguese style_basics_aed05094:

    # e "Those are the basics of styles. If GUI customization isn't enough for you, styles let you customize just about everything in Ren'Py."
    e "Esses são os fundamentos dos estilos. Se a personalização da GUI não for suficiente para você, os estilos permitem personalizar quase tudo no Ren'Py."

# game/indepth_style.rpy:253
translate portuguese style_general_81f3c8ff:

    # e "The first group of style properties that we'll go over are the general style properties. These work with every displayable, or at least many different ones."
    e "O primeiro grupo de propriedades de estilo que veremos são as propriedades gerais. Elas funcionam com todos os exibíveis, ou pelo menos com muitos deles."

# game/indepth_style.rpy:264
translate portuguese style_general_a8d99699:

    # e "Every displayable takes the position properties, which control where it can be placed on screen. Since I've already mentioned them, I won't repeat them here."
    e "Cada exibível recebe propriedades de posição, que controlam onde ele pode ser colocado na tela. Como eu já as mencionei, não vou repeti-las aqui."

# game/indepth_style.rpy:275
translate portuguese style_general_58d4a18f:

    # e "The xmaximum and ymaximum properties set the maximum width and height of the displayable, respectively. This will cause Ren'Py to shrink things, if possible."
    e "As propriedades 'xmaximum' e 'ymaximum' definem, respectivamente, a largura e a altura máximas do exibível. Isso fará o Ren'Py encolher as coisas, se possível."

# game/indepth_style.rpy:277
translate portuguese style_general_cae9a39f:

    # e "Sometimes, the shrunken size will be smaller than the size given by xmaximum and ymaximum."
    e "Às vezes, o tamanho reduzido será menor do que o tamanho dado por 'xmaximum' e 'ymaximum'."

# game/indepth_style.rpy:279
translate portuguese style_general_5928c24e:

    # e "Similarly, the xminimum and yminimum properties set the minimum width and height. If the displayable is smaller, Ren'Py will try to make it bigger."
    e "Da mesma forma, as propriedades 'xminimum' e 'yminimum' definem a largura e a altura mínimas. Se o exibível for menor, o Ren'Py tentará aumentá-lo."

# game/indepth_style.rpy:289
translate portuguese style_general_35a8ee5e:

    # e "The xsize and ysize properties set the minimum and maximum size to the same value, fixing the size."
    e "As propriedades 'xsize' e 'ysize' definem o tamanho mínimo e máximo para o mesmo valor, fixando o tamanho."

# game/indepth_style.rpy:291
translate portuguese style_general_fcfb0640:

    # e "These only works for displayables than can be resized. Some displayables, like images, can't be made bigger or smaller."
    e "Elas só funcionam para exibíveis que podem ser redimensionados. Alguns exibíveis, como imagens, não podem ser aumentados ou diminuídos."

# game/indepth_style.rpy:299
translate portuguese style_general_cd5cc97c:

    # e "The area property takes a tuple - a parenthesis bounded list of four items. The first two give the position, and the second two the size."
    e "A propriedade 'area' recebe uma tupla, uma lista entre parênteses com quatro itens. Os dois primeiros dão a posição, e os dois últimos, o tamanho."

# game/indepth_style.rpy:308
translate portuguese style_general_e5a58f0b:

    # e "Finally, the alt property changes the text used by self-voicing for the hearing impaired."
    e "Por fim, a propriedade 'alt' altera o texto usado pela voz automática para pessoas com deficiência visual."

# game/indepth_style.rpy:335
translate portuguese style_text_fe457b8f:

    # e "The text style properties apply to text and input displayables."
    e "As propriedades de estilo de texto se aplicam aos exibíveis 'text' e 'input'."

# game/indepth_style.rpy:337
translate portuguese style_text_7ab53f03:

    # e "Text displayables can be created implicitly or explicitly. For example, a textbutton creates a text displayable with a style ending in button_text."
    e "Exibíveis de texto podem ser criados implícita ou explicitamente. Por exemplo, um 'textbutton' cria um exibível de texto com um estilo que termina em button_text."

# game/indepth_style.rpy:339
translate portuguese style_text_6dd42a57:

    # e "These can also be set in gui.rpy by changing or defining variables with names like gui.button_text_size."
    e "Elas também podem ser definidas em gui.rpy, alterando ou definindo variáveis com nomes como gui.button_text_size."

# game/indepth_style.rpy:347
translate portuguese style_text_c689130e:

    # e "The bold style property makes the text bold. This can be done using an algorithm, rather than a different version of the font."
    e "A propriedade de estilo bold deixa o texto em negrito. Isso pode ser feito usando um algoritmo, em vez de uma versão diferente da fonte."

# game/indepth_style.rpy:355
translate portuguese style_text_3420bfe4:

    # e "The color property changes the color of the text. It takes hex color codes, just like everything else in Ren'Py."
    e "A propriedade 'color' altera a cor do texto. Ela usa códigos de cor hexadecimais, como quase todo o resto no Ren'Py."

# game/indepth_style.rpy:363
translate portuguese style_text_14bd6327:

    # e "The first_indent style property determines how far the first line is indented."
    e "A propriedade de estilo 'first_indent' determina o recuo da primeira linha."

# game/indepth_style.rpy:371
translate portuguese style_text_779ac517:

    # e "The font style property changes the font the text uses. Ren'Py takes TrueType and OpenType fonts, and you'll have to include the font file as part of your visual novel."
    e "A propriedade de estilo 'font' muda a fonte usada pelo texto. O Ren'Py aceita fontes TrueType e OpenType, e você terá que incluir o arquivo da fonte como parte da sua visual novel."

# game/indepth_style.rpy:379
translate portuguese style_text_917e2bca:

    # e "The size property changes the size of the text."
    e "A propriedade 'size' altera o tamanho do texto."

# game/indepth_style.rpy:388
translate portuguese style_text_1a46cd43:

    # e "The italic property makes the text italic. Again, this is better done with a font, but for short amounts of text Ren'Py can do it for you."
    e "A propriedade 'italic' deixa o texto em itálico. Novamente, isso é melhor feito com uma fonte, mas para pequenas quantidades de texto o Ren'Py pode fazer isso por você."

# game/indepth_style.rpy:397
translate portuguese style_text_472f382d:

    # e "The justify property makes the text justified, lining all but the last line up on the left and the right side."
    e "A propriedade 'justify' deixa o texto justificado, alinhando todas as linhas, exceto a última, à esquerda e à direita."

# game/indepth_style.rpy:405
translate portuguese style_text_87b075f8:

    # e "The kerning property kerns the text. When it's negative, characters are closer together. When positive, characters are farther apart."
    e "A propriedade 'kerning' ajusta o espaçamento do texto. Quando é negativa, os caracteres ficam mais próximos. Quando é positiva, ficam mais afastados."

# game/indepth_style.rpy:415
translate portuguese style_text_fe7dec14:

    # e "The line_leading and line_spacing properties put spacing before each line, and between lines, respectively."
    e "As propriedades 'line_leading' e 'line_spacing' colocam espaçamento antes de cada linha e entre as linhas, respectivamente."

# game/indepth_style.rpy:424
translate portuguese style_text_aee9277a:

    # e "The outlines property puts outlines around text. This takes a list of tuples, which is a bit complicated."
    e "A propriedade 'outlines' coloca contornos ao redor do texto. Ela recebe uma lista de tuplas, o que é um pouco complicado."

# game/indepth_style.rpy:426
translate portuguese style_text_b4c5190f:

    # e "But if you ignore the brackets and parenthesis, you have the width of the outline, the color, and then horizontal and vertical offsets."
    e "Mas se você ignorar os colchetes e parênteses, terá a largura do contorno, a cor e, em seguida, os deslocamentos horizontal e vertical."

# game/indepth_style.rpy:434
translate portuguese style_text_5a0c2c02:

    # e "The rest_indent property controls the indentation of lines after the first one."
    e "A propriedade 'rest_indent' controla o recuo das linhas depois da primeira."

# game/indepth_style.rpy:443
translate portuguese style_text_430c1959:

    # e "The text_align property controls the positioning of multiple lines of text inside the text displayable. For example, 0.5 means centered."
    e "A propriedade 'text_align' controla o posicionamento de várias linhas de texto dentro do exibível de texto. Por exemplo, 0.5 significa centralizado."

# game/indepth_style.rpy:445
translate portuguese style_text_19aa0833:

    # e "It doesn't change the position of the text displayable itself. For that, you'll often want to set the text_align and xalign to the same value."
    e "Ela não muda a posição do próprio exibível de texto. Para isso, muitas vezes você vai querer definir 'text_align' e 'xalign' com o mesmo valor."

# game/indepth_style.rpy:455
translate portuguese style_text_efc3c392:

    # e "When both text_align and xalign are set to 1.0, the text is properly right-justified."
    e "Quando tanto 'text_align' quanto 'xalign' são definidos como 1.0, o texto fica corretamente alinhado à direita."

# game/indepth_style.rpy:464
translate portuguese style_text_43be63b9:

    # e "The underline property underlines the text."
    e "A propriedade 'underline' sublinha o texto."

# game/indepth_style.rpy:471
translate portuguese style_text_343f6d34:

    # e "Those are the most common text style properties, but not the only ones. Here are a few more that you might need in special circumstances."
    e "Essas são as propriedades de estilo de texto mais comuns, mas não as únicas. Aqui estão algumas outras que você pode precisar em circunstâncias especiais."

# game/indepth_style.rpy:479
translate portuguese style_text_e7204a95:

    # e "By default, text in Ren'Py is antialiased, to smooth the edges. The antialias property can turn that off, and make the text a little more jagged."
    e "Por padrão, o texto no Ren'Py usa antialiasing para suavizar as bordas. A propriedade antialias pode desativar isso e deixar o texto um pouco mais serrilhado."

# game/indepth_style.rpy:487
translate portuguese style_text_a5316e4c:

    # e "The adjust_spacing property is a very subtle one, that only matters when a player resizes the window. When True, characters will be shifted a bit so the Text has the same relative spacing."
    e "A propriedade 'adjust_spacing' é bem sutil, e só importa quando o jogador redimensiona a janela. Quando ela é 'True', os caracteres são deslocados um pouco para que o texto mantenha o mesmo espaçamento relativo."

# game/indepth_style.rpy:496
translate portuguese style_text_605d4e4a:

    # e "When False, the text won't jump around as much. But it can be a little wider or narrower based on screen size."
    e "Quando ela é 'False', o texto não ficará pulando tanto. Mas pode acabar um pouco mais largo ou mais estreito dependendo do tamanho da tela."

# game/indepth_style.rpy:505
translate portuguese style_text_acf8a0e1:

    # e "The layout property has a few special values that control where lines are broken. The 'nobreak' value disables line breaks entirely, making the text wider."
    e "A propriedade 'layout' tem alguns valores especiais que controlam onde as linhas são quebradas. O valor 'nobreak' desativa completamente as quebras de linha, deixando o texto mais largo."

# game/indepth_style.rpy:516
translate portuguese style_text_785729cf:

    # e "When the layout property is set to 'subtitle', the line breaking algorithm is changed to try to make all lines even in length, as subtitles usually are."
    e "Quando a propriedade 'layout' é definida como 'subtitle', o algoritmo de quebra de linha é alterado para tentar deixar todas as linhas com comprimentos parecidos, como acontece em legendas."

# game/indepth_style.rpy:524
translate portuguese style_text_9c26f218:

    # e "The strikethrough property draws a line through the text. It seems pretty unlikely you'd want to use this one."
    e "A propriedade 'strikethrough' traça uma linha sobre o texto. Parece bem improvável que você queira usar esta."

# game/indepth_style.rpy:534
translate portuguese style_text_c7229243:

    # e "The vertical style property places text in a vertical layout. It's meant for Asian languages with special fonts."
    e "A propriedade de estilo 'vertical' coloca o texto em um layout vertical. Ela é voltada para idiomas asiáticos com fontes especiais."

# game/indepth_style.rpy:540
translate portuguese style_text_724bd5e0:

    # e "And those are the text style properties. There might be a lot of them, but we want to give you a lot of control over how you present text to your players."
    e "E essas são as propriedades de estilo de texto. Pode parecer muita coisa, mas queremos dar a você bastante controle sobre como apresentar texto aos seus jogadores."

# game/indepth_style.rpy:580
translate portuguese style_button_300b6af5:

    # e "Next up, we have the window and button style properties. These apply to windows like the text window at the bottom of this screen and frames like the ones we show examples in."
    e "A seguir, temos as propriedades de estilo de 'window' e 'button'. Elas se aplicam a janelas como a janela de texto no rodapé desta tela e a frames como os que mostramos nos exemplos."

# game/indepth_style.rpy:582
translate portuguese style_button_255a18e4:

    # e "These properties also apply to buttons, in-game and out-of-game. To Ren'Py, a button is a window you can click."
    e "Essas propriedades também se aplicam a botões, dentro e fora do jogo. Para o Ren'Py, um botão é uma janela em que você pode clicar."

# game/indepth_style.rpy:593
translate portuguese style_button_9b53ce93:

    # e "I'll start off with this style, which everything will inherit from. To make our lives easier, it inherits from the default style, rather than the customizes buttons in this game's GUI."
    e "Vou começar com este estilo, do qual todo o resto vai herdar. Para facilitar nossa vida, ele herda do estilo 'default', em vez dos botões personalizados da GUI deste jogo."

# game/indepth_style.rpy:595
translate portuguese style_button_aece4a8c:

    # e "The first style property is the background property. It adds a background to the a button or window. Since this is a button, idle and hover variants choose different backgrounds when focused."
    e "A primeira propriedade de estilo é 'background'. Ela adiciona um fundo ao botão ou à janela. Como este é um botão, as variantes 'idle' e 'hover' escolhem fundos diferentes quando ele recebe foco."

# game/indepth_style.rpy:597
translate portuguese style_button_b969f04a:

    # e "We also center the two buttons, using the xalign position property."
    e "Também centralizamos os dois botões usando a propriedade de posição 'xalign'."

# game/indepth_style.rpy:601
translate portuguese style_button_269ae069:

    # e "We've also customized the style of the button's text, using this style. It centers the text and makes it change color when hovered."
    e "Também personalizamos o estilo do texto do botão usando este estilo. Ele centraliza o texto e faz sua cor mudar quando o botão recebe foco."

# game/indepth_style.rpy:612
translate portuguese style_button_1009f3e1:

    # e "Without any padding around the text, the button looks odd. Ren'Py has padding properties that add space inside the button's background."
    e "Sem nenhum preenchimento ao redor do texto, o botão parece estranho. O Ren'Py tem propriedades de padding que adicionam espaço dentro do fundo do botão."

# game/indepth_style.rpy:621
translate portuguese style_button_5bdfa45a:

    # e "More commonly used are the xpadding and ypadding style properties, which add the same padding to the left and right, or the top and bottom, respectively."
    e "Mais comumente usadas são as propriedades de estilo 'xpadding' e 'ypadding', que adicionam o mesmo preenchimento à esquerda e à direita, ou em cima e embaixo, respectivamente."

# game/indepth_style.rpy:629
translate portuguese style_button_81283d42:

    # e "The margin style properties work the same way, except they add space outside the background. The full set exists: left_margin, right_margin, top_margin, bottom_margin, xmargin, and ymargin."
    e "As propriedades de estilo 'margin' funcionam do mesmo jeito, exceto pelo fato de adicionarem espaço fora do fundo. O conjunto completo existe: 'left_margin', 'right_margin', 'top_margin', 'bottom_margin', 'xmargin' e 'ymargin'."

# game/indepth_style.rpy:638
translate portuguese style_button_0b7aca6b:

    # e "The size_group style property takes a string. Ren'Py will make sure that all the windows or buttons with the same size_group string are the same size."
    e "A propriedade de estilo 'size_group' recebe uma string. O Ren'Py garantirá que todas as janelas ou botões com o mesmo valor de 'size_group' tenham o mesmo tamanho."

# game/indepth_style.rpy:647
translate portuguese style_button_4c6da7d9:

    # e "Alternatively, the xfill and yfill style properties make a button take up all available space in the horizontal or vertical directions."
    e "Como alternativa, as propriedades de estilo 'xfill' e 'yfill' fazem um botão ocupar todo o espaço disponível na direção horizontal ou vertical."

# game/indepth_style.rpy:657
translate portuguese style_button_fd5338b2:

    # e "The foreground property gives a displayable that is placed on top of the contents and background of the window or button."
    e "A propriedade 'foreground' fornece um exibível que é colocado sobre o conteúdo e o fundo da janela ou do botão."

# game/indepth_style.rpy:659
translate portuguese style_button_b8af697c:

    # e "One way to use it is to provide extra decorations to a button that's serving as a checkbox. Another would be to use it with a Frame to provide a glossy shine that overlays the button's contents."
    e "Uma forma de usá-la é fornecer decorações extras a um botão que esteja servindo como caixa de seleção. Outra seria usá-la com um 'Frame' para fornecer um brilho sobreposto ao conteúdo do botão."

# game/indepth_style.rpy:668
translate portuguese style_button_c0b1b62e:

    # e "There are also a few style properties that only apply to buttons. The hover_sound and activate_sound properties play sound files when a button is focused and activated, respectively."
    e "Há também algumas propriedades de estilo que só se aplicam a botões. As propriedades 'hover_sound' e 'activate_sound' reproduzem sons quando um botão recebe foco e é ativado, respectivamente."

# game/indepth_style.rpy:677
translate portuguese style_button_02fa647e:

    # e "Finally, the focus_mask property applies to partially transparent buttons. When it's set to True, only areas of the button that aren't transparent cause a button to focus."
    e "Por fim, a propriedade 'focus_mask' se aplica a botões parcialmente transparentes. Quando definida como 'True', apenas as áreas não transparentes do botão fazem com que ele receba foco."

# game/indepth_style.rpy:759
translate portuguese style_bar_414d454a:

    # e "To demonstrate styles, let me first show two of the images we'll be using. This is the image we're using for parts of the bar that are empty."
    e "Para demonstrar estilos, deixe-me primeiro mostrar duas das imagens que usaremos. Esta é a imagem que estamos usando para as partes vazias da barra."

# game/indepth_style.rpy:763
translate portuguese style_bar_9422b7b0:

    # e "And here's what we use for parts of the bar that are full."
    e "E isto é o que usamos para as partes cheias da barra."

# game/indepth_style.rpy:775
translate portuguese style_bar_8ae6a14b:

    # e "The left_bar and right_bar style properties, and their hover variants, give displayables for the left and right side of the bar. By default, the value is shown on the left."
    e "As propriedades de estilo 'left_bar' e 'right_bar', e suas variantes de hover, fornecem exibíveis para os lados esquerdo e direito da barra. Por padrão, o valor é mostrado à esquerda."

# game/indepth_style.rpy:777
translate portuguese style_bar_7f0f50e5:

    # e "Also by default, both the left and right displayables are rendered at the full width of the bar, and then cropped to the appropriate size."
    e "Além disso, por padrão, tanto o exibível da esquerda quanto o da direita são renderizados com a largura total da barra e depois recortados para o tamanho apropriado."

# game/indepth_style.rpy:779
translate portuguese style_bar_9ef4f62f:

    # e "We give the bar the ysize property to set how tall it is. We could also give it xsize to choose how wide, but here it's limited by the width of the frame it's in."
    e "Damos à barra a propriedade 'ysize' para definir sua altura. Também poderíamos dar 'xsize' para escolher sua largura, mas aqui ela é limitada pela largura do frame em que está."

# game/indepth_style.rpy:792
translate portuguese style_bar_d4c29710:

    # e "When the bar_invert style property is True, the bar value is displayed on the right side of the bar. The left_bar and right_bar displayables might also need to be swapped."
    e "Quando a propriedade de estilo 'bar_invert' é 'True', o valor da barra é exibido no lado direito dela. Também pode ser necessário trocar os exibíveis 'left_bar' e 'right_bar'."

# game/indepth_style.rpy:806
translate portuguese style_bar_cca67222:

    # e "The bar_resizing style property causes the bar images to be resized to represent the value, rather than being rendered at full size and cropped."
    e "A propriedade de estilo 'bar_resizing' faz com que as imagens da barra sejam redimensionadas para representar o valor, em vez de serem renderizadas em tamanho total e recortadas."

# game/indepth_style.rpy:819
translate portuguese style_bar_7d361bac:

    # e "The thumb style property gives a thumb image, that's placed based on the bars value. In the case of a scrollbar, it's resized if possible."
    e "A propriedade de estilo 'thumb' fornece uma imagem de thumb, que é posicionada com base no valor da barra. No caso de uma scrollbar, ela é redimensionada, se possível."

# game/indepth_style.rpy:821
translate portuguese style_bar_b6dfb61b:

    # e "Here, we use it with the base_bar style property, which sets both bar images to the same displayable."
    e "Aqui, nós a usamos com a propriedade de estilo 'base_bar', que define as duas imagens da barra como o mesmo exibível."

# game/indepth_style.rpy:836
translate portuguese style_bar_996466ad:

    # e "The left_gutter and right_gutter properties set a gutter on the left or right size of the bar. The gutter is space the bar can't be dragged into, that can be used for borders."
    e "As propriedades 'left_gutter' e 'right_gutter' definem uma margem interna no lado esquerdo ou direito da barra. Essa área é um espaço para onde a barra não pode ser arrastada, e pode ser usado para bordas."

# game/indepth_style.rpy:851
translate portuguese style_bar_fa41a83c:

    # e "The bar_vertical style property displays a vertically oriented bar. All of the other properties change names - left_bar becomes top_bar, while right_bar becomes bottom_bar."
    e "A propriedade de estilo 'bar_vertical' exibe uma barra orientada verticalmente. Todas as outras propriedades mudam de nome: 'left_bar' vira 'top_bar', enquanto 'right_bar' vira 'bottom_bar'."

# game/indepth_style.rpy:856
translate portuguese style_bar_5d33c5dc:

    # e "Finally, there's one style we can't show here, and it's unscrollable. It controls what happens when a scrollbar can't be moved at all."
    e "Por fim, há um estilo que não podemos mostrar aqui, chamado 'unscrollable'. Ele controla o que acontece quando uma barra de rolagem não pode ser movida de jeito nenhum."

# game/indepth_style.rpy:858
translate portuguese style_bar_e8e32280:

    # e "By default, it's shown. But if unscrollable is 'insensitive', the bar becomes insensitive. If it's 'hide', the bar is hidden, but still takes up space."
    e "Por padrão, ela é mostrada. Mas se unscrollable for 'insensitive', a barra se torna insensível. Se for 'hide', a barra é ocultada, mas ainda ocupa espaço."

# game/indepth_style.rpy:862
translate portuguese style_bar_f1292000:

    # e "That's it for the bar properties. By using them, a creator can customize bars, scrollbars, and sliders."
    e "Isso é tudo sobre as propriedades de barra. Usando-as, um criador pode personalizar barras, barras de rolagem e sliders."

# game/indepth_style.rpy:961
translate portuguese style_box_5fd535f4:

    # e "The hbox displayable is used to lay its children out horizontally. By default, there's no spacing between children, so they run together."
    e "O exibível 'hbox' é usado para organizar seus filhos horizontalmente. Por padrão, não há espaçamento entre eles, então ficam grudados."

# game/indepth_style.rpy:967
translate portuguese style_box_0111e5dc:

    # e "Similarly, the vbox displayable is used to lay its children out vertically. Both support style properties that control placement."
    e "Da mesma forma, o exibível 'vbox' é usado para organizar seus filhos verticalmente. Ambos oferecem suporte a propriedades de estilo que controlam o posicionamento."

# game/indepth_style.rpy:972
translate portuguese style_box_5a44717b:

    # e "To make the size of the box displayable obvious, I'll add a highlight to the box itself, and not the frame containing it."
    e "Para deixar o tamanho da caixa mais evidente, vou adicionar um destaque à própria caixa, e não ao frame que a contém."

# game/indepth_style.rpy:980
translate portuguese style_box_239e7a8f:

    # e "Boxes support the xfill and yfill style properties. These properties make a box expand to fill the available space, rather than the space of the largest child."
    e "Caixas suportam as propriedades de estilo 'xfill' e 'yfill'. Essas propriedades fazem a caixa expandir para preencher o espaço disponível, em vez de ficar no tamanho do maior filho."

# game/indepth_style.rpy:990
translate portuguese style_box_e513c946:

    # e "The spacing style property takes a value in pixels, and adds that much spacing between each child of the box."
    e "A propriedade de estilo 'spacing' recebe um valor em pixels e adiciona esse espaçamento entre cada filho da caixa."

# game/indepth_style.rpy:1000
translate portuguese style_box_6ae4f94d:

    # e "The first_spacing style property is similar, but it only adds space between the first and second children. This is useful when the first child is a title that needs different spacing."
    e "A propriedade de estilo 'first_spacing' é parecida, mas só adiciona espaço entre o primeiro e o segundo filhos. Isso é útil quando o primeiro filho é um título que precisa de um espaçamento diferente."

# game/indepth_style.rpy:1010
translate portuguese style_box_0c518d9f:

    # e "The box_reverse style property reverses the order of entries in the box."
    e "A propriedade de estilo 'box_reverse' inverte a ordem dos itens da caixa."

# game/indepth_style.rpy:1023
translate portuguese style_box_f73c1422:

    # e "We'll switch back to a horizontal box for our next example."
    e "Voltaremos para uma caixa horizontal no próximo exemplo."

# game/indepth_style.rpy:1033
translate portuguese style_box_285592bb:

    # e "The box_wrap style property fills the box with children until it's full, then starts again on the next line."
    e "A propriedade de estilo 'box_wrap' preenche a caixa com filhos até ela ficar cheia, e então recomeça na linha seguinte."

# game/indepth_style.rpy:1046
translate portuguese style_box_a7637552:

    # e "Grids bring with them two more style properties. The xspacing and yspacing properties control spacing in the horizontal and vertical directions, respectively."
    e "Grids trazem consigo mais duas propriedades de estilo. As propriedades 'xspacing' e 'yspacing' controlam o espaçamento nas direções horizontal e vertical, respectivamente."

# game/indepth_style.rpy:1053
translate portuguese style_box_4006f74b:

    # e "Lastly, we have the fixed layout. The fixed layout usually expands to fill all space, and shows its children from back to front."
    e "Por fim, temos o layout 'fixed'. Layouts fixed normalmente se expandem para preencher todo o espaço e mostram seus filhos de trás para frente."

# game/indepth_style.rpy:1055
translate portuguese style_box_4a2866f0:

    # e "But of course, we have some style properties that can change that."
    e "Mas, claro, temos algumas propriedades de estilo que podem mudar isso."

# game/indepth_style.rpy:1064
translate portuguese style_box_66e042c4:

    # e "When the xfit style property is True, the fixed lays out all its children as if it was full size, and then shrinks in width to fit them. The yfit style works the same way, but in height."
    e "Quando a propriedade de estilo 'xfit' é 'True', o fixed organiza todos os seus filhos como se estivesse em tamanho total, e depois encolhe na largura para se ajustar a eles. O estilo yfit funciona da mesma forma, mas na altura."

# game/indepth_style.rpy:1072
translate portuguese style_box_6a593b10:

    # e "The order_reverse style property changes the order in which the children are shown. Instead of back-to-front, they're displayed front-to-back."
    e "A propriedade de estilo 'order_reverse' muda a ordem em que os filhos são mostrados. Em vez de trás para frente, eles são exibidos da frente para trás."

# game/indepth_style.rpy:1084
translate portuguese style_inspector_21bc0709:

    # e "Sometimes it's hard to figure out what style is being used for a particular displayable. The displayable inspector can help with that."
    e "Às vezes é difícil descobrir qual estilo está sendo usado para um determinado exibível. O inspetor de exibíveis pode ajudar nisso."

# game/indepth_style.rpy:1086
translate portuguese style_inspector_243c50f0:

    # e "To use it, place the mouse over a portion of the Ren'Py user interface, and hit shift+I. That's I for inspector."
    e "Para usá-lo, coloque o mouse sobre uma parte da interface do Ren'Py e pressione shift+I. O I é de inspector."

# game/indepth_style.rpy:1088
translate portuguese style_inspector_bcbdc396:

    # e "Ren'Py will pop up a list of displayables the mouse is over. Next to each is the name of the style that displayable uses."
    e "O Ren'Py exibirá uma lista dos exibíveis sobre os quais o mouse está posicionado. Ao lado de cada um estará o nome do estilo que ele usa."

# game/indepth_style.rpy:1090
translate portuguese style_inspector_d981e5c8:

    # e "You can click on the name of the style to see where it gets its properties from."
    e "Você pode clicar no nome do estilo para ver de onde ele obtém suas propriedades."

# game/indepth_style.rpy:1092
translate portuguese style_inspector_ef46b86d:

    # e "By default, the inspector only shows interface elements like screens, and not images. Type shift+alt+I if you'd like to see images as well."
    e "Por padrão, o inspetor mostra apenas elementos de interface, como telas, e não imagens. Pressione shift+alt+I se quiser ver imagens também."

# game/indepth_style.rpy:1094
translate portuguese style_inspector_b59c6b69:

    # e "You can try the inspector right now, by hovering this text and hitting shift+I."
    e "Você pode experimentar o inspetor agora mesmo, passando o mouse sobre este texto e pressionando shift+I."

translate portuguese strings:

    # indepth_style.rpy:20
    old "Button 1"
    new "Botão 1"

    # indepth_style.rpy:22
    old "Button 2"
    new "Botão 2"

    # indepth_style.rpy:66
    old "Style basics."
    new "Noções básicas de estilos."

    # indepth_style.rpy:66
    old "General style properties."
    new "Propriedades gerais de estilo."

    # indepth_style.rpy:66
    old "Text style properties."
    new "Propriedades de estilo de texto."

    # indepth_style.rpy:66
    old "Window and Button style properties."
    new "Propriedades de estilo de Window e Button."

    # indepth_style.rpy:66
    old "Bar style properties."
    new "Propriedades de estilo de Bar."

    # indepth_style.rpy:66
    old "Box, Grid, and Fixed style properties."
    new "Propriedades de estilo de Box, Grid e Fixed."

    # indepth_style.rpy:66
    old "The Displayable Inspector."
    new "O Inspetor de Exibíveis."

    # indepth_style.rpy:66
    old "That's all I want to know."
    new "Isso é tudo o que eu quero saber."

    # indepth_style.rpy:112
    old "This text is colored green."
    new "Este texto é verde."

    # indepth_style.rpy:126
    old "Danger"
    new "Perigo"

    # indepth_style.rpy:142
    old "This text is colored red."
    new "Este texto é vermelho."

    # indepth_style.rpy:170
    old "This text is colored blue."
    new "Este texto é azul."

    # indepth_style.rpy:248
    old "Orbiting Earth in the spaceship, I saw how beautiful our planet is.\n–Yuri Gagarin"
    new "Orbitando a Terra na nave espacial, vi como nosso planeta é bonito.\n–Yuri Gagarin"

    # indepth_style.rpy:303
    old "\"Orbiting Earth in the spaceship, I saw how beautiful our planet is.\" Said by Yuri Gagarin."
    new "\"Orbitando a Terra na nave espacial, vi como nosso planeta é bonito.\" Dito por Yuri Gagarin."

    # indepth_style.rpy:326
    old "Vertical"
    new "Vertical"

    # indepth_style.rpy:329
    old "Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that knows not victory nor defeat.\n\n–Theodore Roosevelt"
    new "É muito melhor ousar grandes feitos, conquistar triunfos gloriosos, mesmo que marcados pelo fracasso, do que se juntar àqueles espíritos pobres que nem desfrutam nem sofrem muito, porque vivem no crepúsculo cinzento que não conhece vitória nem derrota.\n\n–Theodore Roosevelt"

    # indepth_style.rpy:561
    old "Top Choice"
    new "Escolha Superior"

    # indepth_style.rpy:566
    old "Bottom Choice"
    new "Escolha Inferior"

    # indepth_style.rpy:879
    old "First Child"
    new "Primeiro Filho"

    # indepth_style.rpy:880
    old "Second Child"
    new "Segundo Filho"

    # indepth_style.rpy:881
    old "Third Child"
    new "Terceiro Filho"

    # indepth_style.rpy:884
    old "Fourth Child"
    new "Quarto Filho"

    # indepth_style.rpy:885
    old "Fifth Child"
    new "Quinto Filho"

    # indepth_style.rpy:886
    old "Sixth Child"
    new "Sexto Filho"
