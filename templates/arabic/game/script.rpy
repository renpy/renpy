# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define e = Character('إيلين', color="#c8ffc8")

init python:
    if not persistent.default_language_set:
        persistent.default_language_set = True
        _preferences.language = "arabic"

# The game starts here.
label start:

    e "لقد بدأت حكاية رينباي جديدة."

    e "كل ما عليك فعله هو إضافة نصوص و صور و إرسالها للعالم!"

    return
