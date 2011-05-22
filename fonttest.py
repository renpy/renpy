import ftfont

ftfont.init()

f = file("common/DejaVuSans.ttf", "rb")
font = ftfont.FTFont(f, 0)
