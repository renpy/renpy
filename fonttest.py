import ftfont

ftfont.init()

f = file("common/DejaVuSans.ttf", "rb")
font = ftfont.Font(f, 0)
