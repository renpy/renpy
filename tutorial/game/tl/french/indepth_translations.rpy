
# game/indepth_translations.rpy:12
translate french translations_c4ef181f:

    # e "Ren'Py includes support for translating your game into languages other than the one it was originally written in."
    e "Ren’Py inclut un support pour traduire votre jeu dans plusieurs autres langues que celle dans laquelle vous l’avez originellement créé."

# game/indepth_translations.rpy:14
translate french translations_20b9a600:

    # e "This includes the translation of every string in the game, including dialogue, menu choice, and interface strings, and of images and other assets."
    e "Celui inclut la traduction de chaque chaîne dans le jeu, incluant donc les dialogues, les menus de choix, les textes de l’interface, mais aussi les images et les autres points."

# game/indepth_translations.rpy:16
translate french translations_07c7643c:

    # e "While Ren'Py can find dialogue and menu choice strings for you, you'll have to indicate which other strings need translation."
    e "Ren’Py peut également trouver les dialogues et les différents éléments de menus pour vous, vous aurez à indiquer quelles autres chaines vous souhaitez traduire."

# game/indepth_translations.rpy:20
translate french translations_317d73e5:

    # e "For example, here is how we define a character and her name."
    e "Par exemple, voici comment nous définissons un personnage et son nom."

# game/indepth_translations.rpy:24
translate french translations_ab0f3c94:

    # e "To mark Lucy's name as translatable, we surround it by parentheses preceded by a single underscore."
    e "Pour déclarer le nom de Lucy comme traductible, nous l’encadrons de parenthèses et ajoutons un simple underscore."

# game/indepth_translations.rpy:26
translate french translations_c81acfc7:

    # e "Notice how we don't translate the reddish color that we use for her name. That stays the same for all languages."
    e "Remarquez que nous ne traduisons pas la couleur rougeâtre que nous utilisons pour son nom. C’est la même chose pour tous les langages."

# game/indepth_translations.rpy:33
translate french translations_8272a0ef:

    # e "Once that's done, you can generate the translation files. That's done by going to the launcher, and clicking translate."
    e "Une fois ceci fait, vous pouvez générer les fichiers de traduction. Cela se lance depuis le lanceur en cliquant sur « Générer les fichiers de traduction »."

# game/indepth_translations.rpy:35
translate french translations_fde34832:

    # e "After you type in the name of the language you'll be translating to, choosing Generate Translations will scan your game and create translation files."
    e "Après que vous ayez saisi le nom du langage dans lequel vous allez traduire votre jeu, en choisissant « Extraire les traductions » vous allez lancer le scan de votre jeu et Ren’Py va créer les fichiers de traductions."

# game/indepth_translations.rpy:37
translate french translations_e2ebb4af:

    # e "The files will be generated in game/tl/language, where language is the name of the language you typed in."
    e "Le fichiers seront générés dans le répertoire game/tl/langage. Le mot 'langage' sera remplacé par le nom du langage que vous avez donné."

# game/indepth_translations.rpy:39
translate french translations_28ec40b9:

    # e "You'll need to edit those files to include translations for everything in your game."
    e "Vous devrez alors éditer chacun de ces fichier pour inclure les traduction pour chaque élément de votre jeu."

# game/indepth_translations.rpy:41
translate french translations_f6d3fd2d:

    # e "If you want to localize image files, you can also place them in game/tl/language."
    e "Si vous souhaitez avoir des images traduites en fonction de la langue du jeu, placez la copie modifiée dans le répertoire game/tl/langage."

# game/indepth_translations.rpy:48
translate french translations_71bf6e72:

    # e "If the default fonts used by the game do not support the language you are translating to, you will have to change them."
    e "Si les polices par défaut de votre jeu ne supporte pas la langue dans laquelle vous le traduisez, alors vous aurez à les remplacer."

# game/indepth_translations.rpy:50
translate french translations_82c9748e:

    # e "The translate python statement can be used to set the values of gui variables to change the font."
    e "La déclaration python 'translate' peut être utilisée pour définir les valeurs des variables 'gui' pour changer la police."

# game/indepth_translations.rpy:52
translate french translations_a0042025:

    # e "The translate style statement sets style properties more directly."
    e "La déclaration de style 'translate' initialise les propriétés de style directement."

# game/indepth_translations.rpy:54
translate french translations_b10990ce:

    # e "If you need to add new files, such as font files, you can place them into the game/tl/language directory where Ren'Py will find them."
    e "Si vous devez ajouter de nouveaux fichiers, comme des fichiers de police, vous pouvez les placer dans le répertoire game/tl/langage, c’est là où Ren’Py pourra les trouver."

# game/indepth_translations.rpy:58
translate french translations_01fcacc2:

    # e "Finally, you'll have to add support for picking the language of the game. That usually goes into the preferences screen, found in screens.rpy."
    e "Finalement, vous allez ajouter un outil pour permettre au joueur de choisir la nouvelle langue du jeu. Cela se fait généralement dans l’écran des préférences qui se trouve dans le fichier screens.rpy."

# game/indepth_translations.rpy:60
translate french translations_a91befcc:

    # e "Here's an excerpt of the preferences screen of this tutorial. The Language action tells Ren'Py to change the language. It takes a string giving a language name, or None."
    e "Voici une extraction de l’écran 'preferences' de ce tutoriel. L’action 'Language' indique à Ren’Py de changer de langue. Elle prend en argument 'None' ou bien une chaîne de caractère correspondant au nom de la langue."

# game/indepth_translations.rpy:62
translate french translations_9b7d6401:

    # e "The None language is special, as it's the default language that the visual novel was written in. Since this tutorial was written in English, Language(None) selects English."
    e "Le langage 'None' est spécial, c’est le langage par défaut du jeu, celui dans lequel vous l’avez écrit. Comme ce tutoriel a été écrit en anglais, Language(None) sélectionne la langue anglaise."
