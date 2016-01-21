# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define e = Character('ایلین', color="#c8ffc8")

init python:
    if not persistent.default_language_set:
        persistent.default_language_set = True
        _preferences.language = "persian"

# The game starts here.
label start:

    e "شما اولین بازی خود رو ساختید."

    e "بعد از اینکه متن ، تصویر و موسیقی اضافه کردید میتوانید به جهان منتشرش کنید!"

    return
