
# game/indepth_displayables.rpy:15
translate french simple_displayables_db46fd25:

    # e "Ren'Py has the concept of a displayable, which is something like an image that can be shown and hidden."
    e "Ren’Py a un concept de « displayable » que nous allons traduire par un « élément affichable », comme une image qui peut être cachée ou affichée."

# game/indepth_displayables.rpy:22
translate french simple_displayables_bfe78cb7:

    # e "The image statement is used to give an image name to a displayable. The easy way is to simply give an image filename."
    e "La déclaration 'image' est utilisée pour donner un nom d’image à un élément affichable. La façon la plus simple est de fournir le nom du fichier image."

# game/indepth_displayables.rpy:29
translate french simple_displayables_cef4598b:

    # e "But that's not the only thing that an image can refer to. When the string doesn't have a dot in it, Ren'Py interprets that as a reference to a second image."
    e "Mais ce n’est pas la seule chose à laquelle une image peut faire référence. Lorsque la chaine de caractère ne contient pas de point, Ren’Py interprète cela comme une référence à une autre image."

# game/indepth_displayables.rpy:41
translate french simple_displayables_a661fb63:

    # e "The string can also contain a color code, consisting of hexadecimal digits, just like the colors used by web browsers."
    e "La chaîne peut également contenir un code couleur, une chaîne de caractères hexadécimaux, comme les couleurs déclarées pour les navigateurs web."

# game/indepth_displayables.rpy:43
translate french simple_displayables_7f2efb23:

    # e "Three or six digit colors are opaque, containing red, green, and blue values. The four and eight digit versions append alpha, allowing translucent colors."
    e "Trois ou six chiffres sont concaténés pour donner les valeurs de rouge, de vert et de bleu. Le quatrième ou les septième et huitième chiffres donnent la valeur 'alpha', la transparence de la couleur."

# game/indepth_displayables.rpy:53
translate french simple_displayables_9cd108c6:

    # e "The Transform displayable takes a displayable and can apply transform properties to it."
    e "L’élément affichable 'Transform' prend en argument un élément affichable et lui applique une transformation."

# game/indepth_displayables.rpy:55
translate french simple_displayables_f8e1ba3f:

    # e "Notice how, since it takes a displayable, it can take another image. In fact, it can take any displayable defined here."
    e "Regardez, comme il peut prendre un élément affichable en paramètre, il peut utiliser une image. En fait, il peut prendre n’importe quel élément affichable déjà défini."

# game/indepth_displayables.rpy:63
translate french simple_displayables_c6e39078:

    # e "There's a more complete form of Solid, that can take style properties. This lets us change the size of the Solid, where normally it fills the screen."
    e "Il y a un autre élément affichable, le 'Solid', qui peut être initialisé avec des propriétés de style. Cela nous permet de changer la taille du 'Solid' qui normalement remplit tout l’écran."

# game/indepth_displayables.rpy:72
translate french simple_displayables_b102a029:

    # e "The Text displayable lets Ren'Py treat text as if it was an image."
    e "Le 'Text' est un autre élément affichable, Ren’Py le traite comme une image."

# game/indepth_displayables.rpy:80
translate french simple_displayables_0befbee0:

    # e "This means that we can apply other displayables, like Transform, to Text in the same way we do to images."
    e "Cela signifie que nous pouvons appliquer dessus d’autres éléments affichables, comme une transformation."

# game/indepth_displayables.rpy:91
translate french simple_displayables_fcf2325f:

    # e "The Composite displayable lets us group multiple displayables together into a single one, from bottom to top."
    e "L’élément affichable 'Composite' nous permet de regrouper plusieurs éléments ensemble et de les traiter comme un seul."

# game/indepth_displayables.rpy:101
translate french simple_displayables_3dc0050e:

    # e "Some displayables are often used to customize the Ren'Py interface, with the Frame displayable being one of them. The frame displayable takes another displayable, and the size of the left, top, right, and bottom borders."
    e "Certains éléments affichables sont souvent utilisés pour personnaliser l’interface de Ren’Py, comme l’élément 'Frame' (cadre en français). L’élément 'frame' prend en argument un autre élément affichable et la taille des bordures de gauche, du haut, de droite et du bas."

# game/indepth_displayables.rpy:111
translate french simple_displayables_801b7910:

    # e "The Frame displayable expands or shrinks to fit the area available to it. It does this by scaling the center in two dimensions and the sides in one, while keeping the corners the same size."
    e "L’élément 'frame' étend ou rétrécit son contenu pour remplir l’aire disponible. Il le fait en étendant le centre dans les deux dimensions et en étendant les bords dans une seule. Les coins gardent ainsi la même dimension."

# game/indepth_displayables.rpy:118
translate french simple_displayables_00603985:

    # e "A Frame can also tile sections of the displayable supplied to it, rather than scaling."
    e "La section centrale de l’élément peut être tuilée plutôt qu’étirée. Le centre se duplique en mosaïque."

# game/indepth_displayables.rpy:126
translate french simple_displayables_d8b23480:

    # e "Frames might look a little weird in the abstract, but when used with a texture, you can see how we create scalable interface components."
    e "Les cadres peuvent paraître un peu étranges dans la théorie, mais quand ils sont utilisés avec une texture, vous pouvez voir comment nous pouvons les utiliser comme composants d’interface."

# game/indepth_displayables.rpy:132
translate french simple_displayables_ae3f35f5:

    # e "These are just the simplest displayables, the ones you'll use directly the most often."
    e "Il ne s’agissait que des éléments affichables les plus simples, ceux que vous utiliserez le plus fréquemment."

# game/indepth_displayables.rpy:134
translate french simple_displayables_de555a92:

    # e "You can even write custom displayables for minigames, if you're proficient at Python. But for many visual novels, these will be all you'll need."
    e "Vous pouvez également créer vos propres éléments affichables pour réaliser de mini-jeux, surtout si vous êtes à l’aise avec Python. Mais pour la plupart des romans visuels, c’est tout ce dont vous aurez besoin."

translate french strings:

    # indepth_displayables.rpy:67
    old "This is a text displayable."
    new "Ceci est un texte affichable."

