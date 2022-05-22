
# game/tutorial_atl.rpy:205
translate french tutorial_positions_a09a3fd1:

    # e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."
    e "Dans ce tutoriel, je vais vous apprendre comment Ren’Py positionne les éléments à l’écran. Mais avant cela, apprenons-en un peu plus sur la façon dont Python gère les nombres."

# game/tutorial_atl.rpy:207
translate french tutorial_positions_ba39aabc:

    # e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."
    e "Il y a deux types principaux de nombres en Python : les entiers et les nombres décimaux. Un entier est uniquement composé de chiffres, tandis qu’un nombre décimal contient une virgule (NDLT : un point en notation anglaise)."

# game/tutorial_atl.rpy:209
translate french tutorial_positions_a60b775d:

    # e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."
    e "Par exemple, 100 est un entier tandis que 0.5 est un nombre décimal. Dans ce système, il y a deux zéros : 0 est un entier et 0.0 est un nombre décimal."

# game/tutorial_atl.rpy:211
translate french tutorial_positions_7f1a560c:

    # e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."
    e "Ren’Py utilise des entiers pour représenter des coordonnées absolues et des nombres décimaux pour représenter des fractions d’une surface dont la taille est connue."

# game/tutorial_atl.rpy:213
translate french tutorial_positions_8e7d3e52:

    # e "When we're positioning something, the area is usually the entire screen."
    e "Quand nous positionnons quelque chose, la surface est généralement l’écran en entier."

# game/tutorial_atl.rpy:215
translate french tutorial_positions_fdcf9d8b:

    # e "Let me get out of the way, and I'll show you where some positions are."
    e "Laissez-moi sortir du champ et je vais vous montrer où sont certaines positions."

# game/tutorial_atl.rpy:229
translate french tutorial_positions_76d7a5bf:

    # e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."
    e "Le point d’origine est l’angle supérieur gauche de l’écran. C’est là où la position x (xpos) et la position y (ypos) valent toutes les deux zéro."

# game/tutorial_atl.rpy:235
translate french tutorial_positions_be14c7c3:

    # e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."
    e "Quand nous augmentons 'xpos', nous nous déplaçons vers la droite. Voici la position 0.5, ce qui signifie la moitié de l’écran."

# game/tutorial_atl.rpy:240
translate french tutorial_positions_9b91be6c:

    # e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."
    e "Augmenter 'xpos' à 1.0 nous déplace jusqu’à la bordure droite de l’écran."

# game/tutorial_atl.rpy:246
translate french tutorial_positions_2b293304:

    # e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 1280 pixels across, using an xpos of 640 will return the target to the center of the top row."
    e "Nous pouvons aussi fournir une position absolue pour 'xpos', ce qui correspond au nombre de pixels depuis la gauche de l’écran. Par exemple, comme cette fenêtre fait 1280 pixels de large, un 'xpos' de 640 correspondra au centre de la première ligne de l’écran."

# game/tutorial_atl.rpy:248
translate french tutorial_positions_c4d18c0a:

    # e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."
    e "L’axe y ou 'ypos' fonctionne de la même façon. Jusqu’ici nous avions 'ypos' à 0.0."

# game/tutorial_atl.rpy:254
translate french tutorial_positions_16933a61:

    # e "Here's a ypos of 0.5."
    e "Voici un 'ypos' à 0.5."

# game/tutorial_atl.rpy:259
translate french tutorial_positions_6eb36777:

    # e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."
    e "Un 'ypos' de 1.0 indique une position au bas de l’écran. Si vous regardez attentivement, vous pouvez voir un indicateur de position clignotant juste sous le texte de la fenêtre."

# game/tutorial_atl.rpy:261
translate french tutorial_positions_a423050f:

    # e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."
    e "De même que 'xpos', 'ypos' peut également être un entier. Dans ce cas, ypos donnera le nombre de pixels total depuis le haut de l’écran."

# game/tutorial_atl.rpy:267
translate french tutorial_positions_bc7a809a:

    # e "Can you guess where this position is, relative to the screen?" nointeract
    e "Pouvez-vous deviner quelle est cette position, relativement à l’écran ?" nointeract

# game/tutorial_atl.rpy:273
translate french tutorial_positions_6f926e18:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "Désole, c’est faux. 'xpos' vaut .75 et 'yos' vaut .25."

# game/tutorial_atl.rpy:275
translate french tutorial_positions_5d5feb98:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "En d’autres mots, c’est 75%% de la largeur depuis la gauche et 25%% de la hauteur depuis le haut."

# game/tutorial_atl.rpy:279
translate french tutorial_positions_77b45218:

    # e "Good job! You got that position right."
    e "Bon travail ! Vous avez trouvé la bonne position."

# game/tutorial_atl.rpy:283
translate french tutorial_positions_6f926e18_1:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "Désole, c’est faux. 'xpos' vaut .75 et 'yos' vaut .25."

# game/tutorial_atl.rpy:285
translate french tutorial_positions_5d5feb98_1:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "En d’autres mots, c’est 75%% de la largeur depuis la gauche et 25%% de la hauteur depuis le haut."

# game/tutorial_atl.rpy:299
translate french tutorial_positions_e4380a83:

    # e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."
    e "La seconde position qui nous intéresse concerne l’ancre (NDLT : anchor en anglais). L’ancre est le point de repère pour le positionnement."

# game/tutorial_atl.rpy:301
translate french tutorial_positions_d1db1246:

    # e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."
    e "Pour cet exemple, nous avons un 'xanchor' de 0.0 et un 'yanchor'. C’est donc le coin supérieur gauche du logo."

# game/tutorial_atl.rpy:306
translate french tutorial_positions_6056873f:

    # e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."
    e "Quand nous augmentons 'xanchor' à 1.0, l’ancre se déplace jusqu’à la droite de l’image."

# game/tutorial_atl.rpy:311
translate french tutorial_positions_7cdb8dcc:

    # e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."
    e "De façon similaire, quand 'xanchor' et 'yanchor' valent 1.0, l’ancre est positionnée sur le coin inférieur droit."

# game/tutorial_atl.rpy:318
translate french tutorial_positions_03a07da8:

    # e "To place an image on the screen, we need both the position and the anchor."
    e "Pour placer une image à l’écran, nous avons besoin de sa position et de celle de l’ancre."

# game/tutorial_atl.rpy:326
translate french tutorial_positions_8945054f:

    # e "We then line them up, so that both the position and anchor are at the same point on the screen."
    e "Quand nous positionnons l’image, l’ancre et le repère sont placés au même point à l’écran."

# game/tutorial_atl.rpy:336
translate french tutorial_positions_2b184a93:

    # e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."
    e "Quand nous plaçons la position et l’ancre au coin supérieur gauche, l’image se déplace au coin supérieur gauche."

# game/tutorial_atl.rpy:345
translate french tutorial_positions_5aac4f3f:

    # e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."
    e "Avec la bonne combinaison de position et d’ancre, n’importe quelle position à l'écran peut être choisi, sans se soucier de la taille de l’image."

# game/tutorial_atl.rpy:357
translate french tutorial_positions_3b59b797:

    # e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."
    e "Il est souvent utile de définir 'xpos' et 'xanchor' avec la même valeur. Nous appelons cela 'xalign' et cela donne une position fractionnelle de l’écran."

# game/tutorial_atl.rpy:362
translate french tutorial_positions_b8ebf9fe:

    # e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."
    e "Par exemple, quand nous définissons xalign à 0.0, les éléments sont alignés à gauche de l’écran."

# game/tutorial_atl.rpy:367
translate french tutorial_positions_8ce35d52:

    # e "When we set it to 1.0, then we're aligned to the right side of the screen."
    e "Quand nous l’initialisons à 1.0, alors ils sont alignés à la droite de l’écran."

# game/tutorial_atl.rpy:372
translate french tutorial_positions_6745825f:

    # e "And when we set it to 0.5, we're back to the center of the screen."
    e "Et quand nous le déclarons à 0.5, nous revenons au centre de l’écran."

# game/tutorial_atl.rpy:374
translate french tutorial_positions_64428a07:

    # e "Setting yalign is similar, except along the y-axis."
    e "Définir 'yalign' est similaire, sauf que nous utilisons l’ordonnée, l’axe des y."

# game/tutorial_atl.rpy:376
translate french tutorial_positions_cfb77d42:

    # e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."
    e "Souvenez-vous que 'xalign' est simplement un raccourci pour donner à 'xpos' et 'xanchor' la même valeur. 'yalign' en fait de même avec 'ypos' et 'yanchor'."

# game/tutorial_atl.rpy:381
translate french tutorial_positions_cfc1723e:

    # e "The xcenter and ycenter properties position the center of the image. Here, with xcenter set to .75, the center of the image is three-quarters of the way to the right side of the screen."
    e "Les propriétés 'xcenter' et 'ycenter' positionne le centre de l’image. Ici, avec un 'xcenter' à .75, le centre de l’image est au trois-quarts du chemin vers la droite de l’écran."

# game/tutorial_atl.rpy:386
translate french tutorial_positions_7728dbf9:

    # e "The difference between xalign and xcenter is more obvious when xcenter is 1.0, and the image is halfway off the right side of the screen."
    e "La différence entre 'xalign' et 'xcenter' se remarque surtout quand 'xcenter' vaut 1.0. On remarque que la moitié droite de l’image se trouve hors de l’écran."

# game/tutorial_atl.rpy:394
translate french tutorial_positions_1b1cedc6:

    # e "There are the xoffset and yoffset properties, which are applied after everything else, and offset things to the right or bottom, respectively."
    e "Il y a également les propriétés 'xoffset' et 'yoffset' qui s’appliquent toujours en dernier. Il s'agit respectivement des décalages vers la droite et vers le bas."

# game/tutorial_atl.rpy:399
translate french tutorial_positions_e6da2798:

    # e "Of course, you can use negative numbers to offset things to the left and top."
    e "Bien sûr, vous pouvez utiliser des nombres négatifs pour créer des décalages vers la gauche et vers le haut."

# game/tutorial_atl.rpy:404
translate french tutorial_positions_e0fe2d81:

    # e "Lastly, I'll mention that there are combined properties like align, pos, anchor, and center. Align takes a pair of numbers, and sets xalign to the first and yalign to the second. The others are similar."
    e "En dernier, je mentionnerai ici que les valeurs comme 'align', 'pos', 'anchor' et 'center' sont combinées. La variable reçoit une paire de nombres, le premier étant la valeur en x et la seconde la valeur en y."

# game/tutorial_atl.rpy:411
translate french tutorial_positions_0f4ca2b6:

    # e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."
    e "Une fois que vous avez compris les positions, vous pouvez utiliser les transformations de mouvements à appliquer aux différents éléments à l’écran."

# game/tutorial_atl.rpy:418
translate french tutorial_atl_d5d6b62a:

    # e "Ren'Py uses transforms to animate, manipulate, and place images. We've already seen the very simplest of transforms in use:"
    e "Ren’Py utilise les transformations pour animer, manipuler et placer des images. Nous avons déjà vu les transformations les plus simples :"

# game/tutorial_atl.rpy:425
translate french tutorial_atl_7e853c9d:

    # e "Transforms can be very simple affairs that place the image somewhere on the screen, like the right transform."
    e "Les transformations peuvent être de très simples outils qui placent une image quelque part sur l’écran, comme la transformation à droite."

# game/tutorial_atl.rpy:429
translate french tutorial_atl_87a6ecbd:

    # e "But transforms can also be far more complicated affairs, that introduce animation and effects into the mix. To demonstrate, let's have a Gratuitous Rock Concert!"
    e "Mais les transformations peuvent aussi être des cas plus compliqués qui introduisent des animations et effets, le tout mixé. Pour démonstration, participons à un concert de rock gratuit !"

# game/tutorial_atl.rpy:437
translate french tutorial_atl_65badef3:

    # e "But first, let's have... a Gratuitous Rock Concert!"
    e "Mais d’abord, assistons à ce concert de rock gratuit !"

# game/tutorial_atl.rpy:445
translate french tutorial_atl_e0d3c5ec:

    # e "That was a lot of work, but it was built out of small parts."
    e "C’était beaucoup de travail, mais cela a été fait petits bouts par petits bouts."

# game/tutorial_atl.rpy:447
translate french tutorial_atl_f2407514:

    # e "Most transforms in Ren'Py are built using the Animation and Transform Language, or ATL for short."
    e "La plupart des transformations en Ren’Py sont construites en utilisation le Langage d’Animation et de Transformation (Animation and Transform Language) ou ATL pour faire court."

# game/tutorial_atl.rpy:449
translate french tutorial_atl_1f22f875:

    # e "There are currently three places where ATL can be used in Ren'Py."
    e "Il y a actuellement trois endroits où les ATL peuvent être utilisés dans Ren’Py."

# game/tutorial_atl.rpy:454
translate french tutorial_atl_fd036bdf:

    # e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."
    e "Le premier endroit où les ATL peuvent être utilisés, c’est dans une déclaration 'image'. Au lieu d’un affichage habituel, une image peut être définie comme un bloc de code ATL."

# game/tutorial_atl.rpy:456
translate french tutorial_atl_7cad2ab9:

    # e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."
    e "Quand c’est utilisé de cette façon, nous devons nous assurer que les ATL incluent un ou plusieurs éléments affichables déjà affichés à l’écran."

# game/tutorial_atl.rpy:461
translate french tutorial_atl_c78b2a1e:

    # e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."
    e "La seconde approche consiste à utiliser la déclaration 'transform'. Ceci assigne le bloc ATL à une variable python, l’autorisant à être utilisé dans une clause ou dans une autre transformation."

# game/tutorial_atl.rpy:473
translate french tutorial_atl_da7a7759:

    # e "Finally, an ATL block can be used as part of a show statement, instead of the at clause."
    e "Enfin, un bloc ATL peut être utilisé dans une déclaration 'show', à la place de la clause 'at'."

# game/tutorial_atl.rpy:480
translate french tutorial_atl_1dd345c6:

    # e "When ATL is used as part of a show statement, values of properties exist even when the transform is changed. So even though your click stopped the motion, the image remains in the same place."
    e "Quand les ATL sont utilisés dans une déclaration 'show', les valeurs des propriétés existent même si la transformation a changé. Ainsi, même durant un clic, le clic stoppe l’animation, l’image reste à la même place."

# game/tutorial_atl.rpy:488
translate french tutorial_atl_98047789:

    # e "The key to ATL is what we call composability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."
    e "La clé de l’ATL est ce que nous appelons la composabilité. ATL est fait de commandes relativement simples qui peuvent être combinées ensemble pour créer des transformations complexes."

# game/tutorial_atl.rpy:490
translate french tutorial_atl_ed82983f:

    # e "Before I explain how ATL works, let me explain what animation and transformation are."
    e "Avant que je n’explique comment les ATL fonctionnent, laissez-moi expliquer ce que sont les animations et les transformations."

# game/tutorial_atl.rpy:495
translate french tutorial_atl_2807adff:

    # e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."
    e "Une animation, c’est quand l’élément en train d’être affiché change. Par exemple, actuellement je change mon expression."

# game/tutorial_atl.rpy:522
translate french tutorial_atl_3eec202b:

    # e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."
    e "Les transformations incluent les mouvements et les distorsions d’images. Cela inclut leur positionnement à l’écran, les zooms avant et arrière, leur rotation et les changements d’opacité."

# game/tutorial_atl.rpy:530
translate french tutorial_atl_fbc9bf83:

    # e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."
    e "Pour introduire les ATL, commençons par regarder une simple animation. Celle-ci se résume à cinq lignes de code ATL, contenue dans une déclaration 'image'."

# game/tutorial_atl.rpy:532
translate french tutorial_atl_bf92d973:

    # e "To change a displayable, simply mention it on a line of ATL. Here, we're switching back and forth between two images."
    e "Pour changer un élément affichable, mentionnez-le simplement dans une ligne ATL. Ici, nous alternons deux images."

# game/tutorial_atl.rpy:534
translate french tutorial_atl_51a41db4:

    # e "Since we're defining an image, the first line of ATL must give a displayable. Otherwise, there would be nothing to show."
    e "Comme nous sommes en train de définir une image, la première ligne des ATL doit être un élément affichable. Sinon, il n’y aurait rien à montrer."

# game/tutorial_atl.rpy:536
translate french tutorial_atl_3d065074:

    # e "The second and fourth lines are pause statements, which cause ATL to wait half a second each before continuing. That's how we give the delay between images."
    e "La seconde et la quatrième ligne sont des déclarations 'pause', qui interrompent l’ATL durant une demie seconde avant de poursuivre. C’est comme cela que nous créons un délai entre les images."

# game/tutorial_atl.rpy:538
translate french tutorial_atl_60f2a5e8:

    # e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."
    e "La ligne finale est une déclaration de répétition 'repeat'. Cela fait recommencer l’ATL au début. Vous ne pouvez avoir qu’une seule déclaration 'repeat' par bloc."

# game/tutorial_atl.rpy:543
translate french tutorial_atl_146cf4c4:

    # e "If we were to write repeat 2 instead, the animation would loop twice, then stop."
    e "Si nous avions écrit 'repeat 2' à la place, l’animation n’aurait bouclé que deux fois avant de s’arrêter."

# game/tutorial_atl.rpy:548
translate french tutorial_atl_d90b1838:

    # e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."
    e "Omettre la déclaration 'repeat' signifie que l’animation s’arrête une fois que nous avons atteint le fin du bloc de code ATL."

# game/tutorial_atl.rpy:554
translate french tutorial_atl_e5872360:

    # e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."
    e "Par défaut, les affichables sont remplacés instantanément. Nous pouvons alors utiliser une clause 'with' pour fournir une transition entre les affichables."

# game/tutorial_atl.rpy:561
translate french tutorial_atl_2e9d63ea:

    # e "With animation done, we'll see how we can use ATL to transform images, starting with positioning an image on the screen."
    e "L’animation est vue, nous allons voir comment nous pouvons utiliser les transformations d’images en commençant par le positionnement de l’image à l’écran."

# game/tutorial_atl.rpy:570
translate french tutorial_atl_ddc55039:

    # e "The simplest thing we can to is to statically position an image. This is done by giving the names of the position properties, followed by the property values."
    e "La transformation la plus simple consiste à positionner une image. Ceci peut être fait en donnant le nom des propriétés de positionnement suivi par leurs valeurs."

# game/tutorial_atl.rpy:575
translate french tutorial_atl_43516492:

    # e "With a few more statements, we can move things around on the screen."
    e "Avec un peu plus de déclarations, nous pouvons déplacer les éléments de part et d’autre de l’écran."

# game/tutorial_atl.rpy:577
translate french tutorial_atl_fb979287:

    # e "This example starts the image off at the top-right of the screen, and waits a second. It then moves it to the left side, waits another second, and repeats."
    e "Cet exemple commence par positionner l’image dans le coin supérieur droit de l’écran et attend une seconde. Ensuite, il la déplace vers la gauche pour y attendre encore une seconde. Enfin, la transformation se répète en boucle."

# game/tutorial_atl.rpy:579
translate french tutorial_atl_7650ec09:

    # e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."
    e "Les déclarations 'pause' et 'repeat' sont les mêmes déclarations que celles que nous utilisons pour les animations. Elles fonctionnent quelque soit le code ATL."

# game/tutorial_atl.rpy:584
translate french tutorial_atl_d3416d4f:

    # e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."
    e "Avoir une image qui saute d’un côté à l’autre de l’écran n’est pas très utile. C’est pourquoi l’ATL supporte les déclarations 'interpolation'."

# game/tutorial_atl.rpy:586
translate french tutorial_atl_4e7512ec:

    # e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."
    e "La déclaration 'interpolation' vous permet de faire varier progressivement la valeur d’une propriété de transformation, de son ancienne valeur à la nouvelle."

# game/tutorial_atl.rpy:588
translate french tutorial_atl_685eeeaa:

    # e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."
    e "Ici, nous avons une déclaration 'interpolation' sur la seconde ligne ATL. Elle démarre avec le nom de la fonction temporelle, dans ce cas-ci 'linear'."

# game/tutorial_atl.rpy:590
translate french tutorial_atl_c5cb49de:

    # e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."
    e "C’est suivi par le temps exprimé en seconde. Ici, trois secondes. La déclaration se termine avec la liste des propriétés, chacune suivie par sa nouvelle valeur."

# game/tutorial_atl.rpy:592
translate french tutorial_atl_04b8bc1d:

    # e "The value of each property is interpolated from its value when the statement starts to the value at the end of the statement. This is done once per frame, allowing smooth animation."
    e "La valeur de chaque propriété est ensuite interpolée depuis sa valeur de départ vers la valeur finale de la déclaration. C’est un déplacement progressif qui évolue pour chaque frame (un déplacement par fps)."

# game/tutorial_atl.rpy:603
translate french tutorial_atl_2958f397:

    # e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."
    e "ATL supporte des types de déplacement plus complexes, comme 'circle' et 'spline motion', mais nous ne les verrons pas ici."

# game/tutorial_atl.rpy:607
translate french tutorial_atl_d08fe8d9:

    # e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."
    e "En dehors des éléments affichables, la pause, l’interpolation et la répétition, il existe quelques déclarations supplémentaires que nous pouvons utiliser pour les ATL."

# game/tutorial_atl.rpy:619
translate french tutorial_atl_84b22ac0:

    # e "ATL transforms created using the statement become ATL statements themselves. Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."
    e "Les transformations ATL créés en utilisant des déclarations deviennent elle-même des déclarations. Ainsi les positions par défaut sont elles-mêmes transformées, ce qui signifie que nous pouvons utiliser 'left', 'right' et 'center' au sein d’un bloc ATL."

# game/tutorial_atl.rpy:635
translate french tutorial_atl_331126c1:

    # e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."
    e "Ici, nous avons deux nouvelles déclarations. Ce bloc de déclaration vous permet d’inclure un bloc de code ATL. Étant donné que la déclaration 'repeat' ne s’applique qu’aux blocs indentés, cela vous permet de ne répéter qu’une partie de la transformation ATL."

# game/tutorial_atl.rpy:637
translate french tutorial_atl_24f67b67:

    # e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."
    e "Nous avons également la déclaration 'time', qui s’exécute après le nombre de secondes indiqué. Elle s’exécutera même si une autre déclaration est en train de tourner. Cette autre déclaration sera interrompue."

# game/tutorial_atl.rpy:639
translate french tutorial_atl_b7709507:

    # e "So this example bounces the image back and forth for eleven and a half seconds, and then moves it to the right side of the screen."
    e "Cet exemple montre une image naviguant de droite à gauche, mais à 11,5 secondes elle ira se positionner définitivement à droite de l’écran."

# game/tutorial_atl.rpy:653
translate french tutorial_atl_f903bc3b:

    # e "The parallel statement lets us run two blocks of ATL code at the same time."
    e "La déclaration 'parallel' permet d’exécuter deux blocs de code ATL en même temps."

# game/tutorial_atl.rpy:655
translate french tutorial_atl_5d0f8f9d:

    # e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."
    e "Ici, le premier bloc déplace l’image horizontalement et le second bloc la déplace verticalement. Comme elles ont des vitesses différentes, on a l’impression que l’image rebondit sur les bords de l’écran."

# game/tutorial_atl.rpy:669
translate french tutorial_atl_28a7d27e:

    # e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."
    e "Enfin, la déclaration 'choice' fait que Ren’Py choisit aléatoirement un bloc de code ATL. Ceci vous permet de faire quelques variations dans ce que Ren’Py montre."

# game/tutorial_atl.rpy:675
translate french tutorial_atl_2265254b:

    # e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out {a=https://renpy.org/doc/html/atl.html}the ATL chapter in the reference manual{/a}."
    e "Ce tutoriel n’a fait qu’effleurer la surface de ce que les codes ATL peuvent faire. Par exemple, nous n’avons pas couvert les déclarations 'on' et 'event'. Pour plus d’informations, vous pouvez consulter {a=https://renpy.org/doc/html/atl.html}le chapitre ATL du manuel de référence{/a}."

# game/tutorial_atl.rpy:684
translate french transform_properties_391169cf:

    # e "Ren'Py has quite a few transform properties that can be used with ATL, the Transform displayable, and the add Screen Language statement."
    e "Ren’Py dispose également de quelques petites propriétés de transformation qui peuvent être utilisés avec les ATL. L'élément 'Transform' qui ajoute des déclarations 'Screen Language'."

# game/tutorial_atl.rpy:685
translate french transform_properties_fc895a1f:

    # e "Here, we'll show them off so you can see them in action and get used to what each does."
    e "Ici, nous allons les mettre en valeur pour que vous puissiez les voir en action et vous habituer à ce que chacune fait."

# game/tutorial_atl.rpy:701
translate french transform_properties_88daf990:

    # e "First off, all of the position properties are also transform properties. These include the pos, anchor, align, center, and offset properties."
    e "D’abord, toutes les propriétés de position sont aussi des propriétés de transformation. Cela inclut les propriétés 'pos', 'anchor', 'align', 'center' et 'offset'."

# game/tutorial_atl.rpy:719
translate french transform_properties_d7a487f1:

    # e "The position properties can also be used to pan over a displayable larger than the screen, by giving xpos and ypos negative values."
    e "Les propriétés de position peuvent aussi être utilisées pour déplacer une image plus large que l’écran en donnant des valeurs négatives à 'xpos' et 'ypos'."

# game/tutorial_atl.rpy:729
translate french transform_properties_89e0d7c2:

    # "The subpixel property controls how things are lined up with the screen. When False, images can be pixel-perfect, but there can be pixel jumping."
    "La propriété 'subpixel' contrôle comment les éléments sont alignés avec l’écran. Quand la valeur est False, chaque pixel est parfait, mais il peut y avoir des sauts de pixel."

# game/tutorial_atl.rpy:736
translate french transform_properties_4194527e:

    # "When it's set to True, movement is smoother at the cost of blurring images a little."
    "En revanche, quand c’est initialisé à True, le mouvement est lissé, mais les images peuvent être légèrement floue pendant le déplacement."

# game/tutorial_atl.rpy:755
translate french transform_properties_35934e77:

    # e "Transforms also support polar coordinates. The around property sets the center of the coordinate system to coordinates given in pixels."
    e "Les transformations supportent aussi les coordonnées polaires. La propriété 'around' définit le centre du système de coordonnées exprimé en pixels."

# game/tutorial_atl.rpy:763
translate french transform_properties_605ebd0c:

    # e "The angle property gives the angle in degrees. Angles run clockwise, with the zero angle at the top of the screen."
    e "La propriété 'angle' donne un angle en degrés. Les angles se mesurent dans le sens des aiguilles d’une montre et un angle de zéro désigne le haut de l’écran."

# game/tutorial_atl.rpy:772
translate french transform_properties_6d4555ed:

    # e "The radius property gives the distance in pixels from the anchor of the displayable to the center of the coordinate system."
    e "La propriété 'radius' exprime la distance en pixels entre l’ancre de l’élément affichable et le centre du système de coordonnées."

# game/tutorial_atl.rpy:786
translate french transform_properties_7af037a5:

    # e "There are several ways to resize a displayable. The zoom property lets us scale a displayable by a factor, making it bigger and smaller."
    e "Il y a plusieurs moyens de redimensionner un élément affichable. La propriété 'zoom' permet de mettre à l’échelle l’élément affichable selon un facteur, le rendant donc plus grand ou plus petit."

# game/tutorial_atl.rpy:799
translate french transform_properties_b6527546:

    # e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."
    e "Les propriétés 'xzoom' et 'yzoom' permettre d’appliquer des échelles différentes selon les directions X et Y."

# game/tutorial_atl.rpy:809
translate french transform_properties_b98b780b:

    # e "By making xzoom or yzoom a negative number, we can flip the image horizontally or vertically."
    e "En donnant à 'xzoom' ou 'yzoom' une valeur négative, nous pouvons inverser l’image horizontalement ou verticalement."

# game/tutorial_atl.rpy:819
translate french transform_properties_74d542ff:

    # e "Instead of zooming by a scale factor, the size transform property can be used to scale a displayable to a size in pixels."
    e "Au lieu de zoomer avec un facteur d’échelle, la propriété de transformation 'size' peut être utilisée pour redimensionner l’élément affichable à une valeur précise de pixels."

# game/tutorial_atl.rpy:834
translate french transform_properties_438ed776:

    # e "The alpha property is used to change the opacity of a displayable. This can make it appear and disappear."
    e "La propriété 'alpha' est utilisée pour changer l’opacité d’un élément affichable. Ceci peut être utilisé pour le faire apparaitre ou disparaitre."

# game/tutorial_atl.rpy:847
translate french transform_properties_aee19f86:

    # e "The rotate property rotates a displayable."
    e "La propriété 'rotate' permet de pivoter un élément affichable."

# game/tutorial_atl.rpy:858
translate french transform_properties_57b3235a:

    # e "By default, when a displayable is rotated, Ren'Py will include extra space on all four sides, so the size doesn't change as it rotates. Here, you can see the extra space on the left and top, and it's also there on the right and bottom."
    e "Par défaut, quand un élément affichable est pivoté, Ren’Py inclut des espaces supplémentaires à chacun des quatre côtés. Ainsi la taille ne change pas durant la rotation. Ici, nous pouvons voir les espaces supplémentaires à gauche et en haut. Il en est de même en bas et à droite."

# game/tutorial_atl.rpy:870
translate french transform_properties_66d29ee8:

    # e "By setting rotate_pad to False, we can get rid of the space, at the cost of the size of the displayable changing as it rotates."
    e "En initialisant 'rotade_pad' à False, nous pouvons supprimer ces espaces, ainsi la quantité d’espace prise par l’élément affichable change durant la rotation."

# game/tutorial_atl.rpy:881
translate french transform_properties_7f32e8ad:

    # e "The tile transform properties, xtile and ytile, repeat the displayable multiple times."
    e "Les propriétés de transformation 'tile', 'xtile' et 'ytile, répètent l’élément affichable plusieurs fois."

# game/tutorial_atl.rpy:891
translate french transform_properties_207b7fc8:

    # e "The crop property crops a rectangle out of a displayable, showing only part of it."
    e "La propriété 'crop' découpe un rectangle autour de l’élément affichable pour n’en afficher que le contenu."

# game/tutorial_atl.rpy:905
translate french transform_properties_e7e22d28:

    # e "When used together, crop and size can be used to focus in on specific parts of an image."
    e "Utiliser ensemble, 'crop' et 'size' peuvent être utilisés pour attirer l’attention sur certaines parties de l’image."

# game/tutorial_atl.rpy:917
translate french transform_properties_f34abd82:

    # e "The xpan and ypan properties can be used to pan over a displayable, given an angle in degrees, with 0 being the center."
    e "Les propriétés 'xpan' et 'ypan' peuvent être utilisées sur un élément affichable pour effectuer un mouvement panoramique en donnant un angle en degrés avec 0 pour le centre."

# game/tutorial_atl.rpy:924
translate french transform_properties_bfa3b139:

    # e "Those are all the transform properties we have to work with. By putting them together in the right order, you can create complex things."
    e "Voilà toutes les propriétés de transformation avec lesquelles nous pouvons travailler. En les plaçant ensemble dans un ordre précis, vous pourrez créer toute sorte de transformations complexes."

translate french strings:

    # tutorial_atl.rpy:267
    old "xpos 1.0 ypos .5"
    new "xpos 1.0 ypos .5"

    # tutorial_atl.rpy:267
    old "xpos .75 ypos .25"
    new "xpos .75 ypos .25"

    # tutorial_atl.rpy:267
    old "xpos .25 ypos .33"
    new "xpos .25 ypos .33"
