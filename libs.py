def text_objects(texto, fonte):
    cor = (0, 0, 0)
    textSurface = fonte.render(texto, True, cor)
    return textSurface, textSurface.get_rect()

def login(file, arg):
    file = open (file, arg)
    file.write("\n")
    file.write(str(input("Insira Nome: ")))
    file.write("\n")
    file.write(str(input("Insira Email: ")))
    file.write("\n")
    file.close()