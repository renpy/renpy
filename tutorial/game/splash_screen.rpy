# JEDIT code to make a splash screen

# splash screen: 
# "An initial screen displayed by interactive software, usually containing a logo,
# version information, and a copyright notice."


label splashscreen:
     scene black  # colour of splash screen
     pause 1.0

     show text "welcome to this game" with dissolve # input text and chosen animation 
     pause 2.0

     hide text with dissolve  # end of splash screen 
     pause 1.0
     
     # NOTE: Can add multiple splash screens by copying the same format above onwards 

     return # splash screen disappears and displays original main menu 
     
