from libs import login, text_objects
import pygame
import random
import time

login('log.txt', 'a')

pygame.init()  # função para iniciar o pygame
largura = 800
altura = 600
icone = pygame.image.load("assets/images/yoshi_ico.png")
pygame.display.set_caption("Yoshi dos cria")
pygame.display.set_icon(icone)
display = pygame.display.set_mode((largura, altura))
fps = pygame.time.Clock()
branco = (255, 255, 255)


def message_display(text):
    fonte = pygame.font.Font("freesansbold.ttf",50)
    TextSurf, TextRect = text_objects(text, fonte)
    TextRect.center = ((largura/2), (altura/2))
    display.blit(TextSurf, TextRect)
    pygame.display.update()

def restart():
    time.sleep(3)
    jogo()

def dead(score):
    pygame.mixer.music.stop()
    message_display("Você Morreu com "+str(score-1)+" pontos!")

def placar(score, vidas):
    font = pygame.font.SysFont(None, 25)
    texto = font.render("score:"+str(score), True, branco)
    texto2 = font.render("vidas:"+str(vidas), True, branco)
    display.blit(texto2, (0, 20))
    display.blit(texto, (0, 0))
    
def jogo():
    comidaType = comidaID = 0

    # [ini] sound assets
    pygame.mixer.music.load('assets/sounds/music.mp3')
    pygame.mixer.music.play(-1) # looping
    sounds_act = ['yoshi-ha.mp3', 'yoshi-pam.mp3', 'yoshi-wa.mp3', 'yoshi-yap.mp3']
    sounds_stats = ['yoshi-spit.mp3', 'yoshi-ow.mp3']
    # [end] sound assets

    # [ini] image assets
    fundo = pygame.image.load("assets/images/background.jpg")
    fundo = pygame.transform.scale(fundo, (800, 600))
    comida_lista = [['trash0.png', 'trash1.png', 'trash2.png', 'trash3.png', 'trash4.png', 'trash5.png'], ['fruit0.png', 'fruit1.png', 'fruit2.png', 'fruit3.png', 'fruit4.png', 'fruit5.png']]
    comidaType = random.randint(0, 1) # pega tipo da comida trash/candy
    comidaID = random.randint(0, 5) # pega index do tipo, 0 a 5
    comida = pygame.image.load('assets/images/'+comida_lista[comidaType][comidaID])
    comida = pygame.transform.scale(comida, (120, 120))
    yoshi = (pygame.image.load("assets/images/yoshi-still.png"))
    yoshi = pygame.transform.scale(yoshi, (120, 120))
    # [end] image assets

    playerPosicaoX = largura * 0.45
    playerPosicaoY = altura * 0.8
    yoshiLargura = 120
    movimentoX = 0
    comidaX = largura * 0.45
    comidaY = -220
    comidaLargura = 120
    comidaAltura = 120
    comidaVelocidade = 5
    vidas = 3
    score = 1
    anti_loop = False

    display.fill(branco)
    message_display('Pegue apenas o que é saudável!')
    pygame.display.update()
    time.sleep(3)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()  # break para executar o fim do código
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    yoshi = (pygame.image.load("assets/images/yoshi-running-left.gif"))
                    yoshi = pygame.transform.scale(yoshi, (120, 120))
                    if comidaVelocidade < 10:
                        movimentoX = -10*comidaVelocidade/5*0.1-10
                    else:
                        movimentoX = -12
                elif evento.key == pygame.K_RIGHT:
                    yoshi = (pygame.image.load("assets/images/yoshi-running-right.gif"))
                    yoshi = pygame.transform.scale(yoshi, (120, 120))
                    if comidaVelocidade < 10:
                        movimentoX = 10*score*0.1+10
                    else:
                        movimentoX = 12
            if evento.type == pygame.KEYUP:
                movimentoX = 0
                yoshi = (pygame.image.load("assets/images/yoshi-still.png"))
                yoshi = pygame.transform.scale(yoshi, (120, 120))

        display.fill(branco)  
        display.blit(fundo, (0, 0))  
        playerPosicaoX = playerPosicaoX + movimentoX
        if playerPosicaoX < 0:
            playerPosicaoX = 0
        elif playerPosicaoX > 680:
            playerPosicaoX = 680

        display.blit(yoshi, (playerPosicaoX, playerPosicaoY))
        display.blit(comida, (comidaX, comidaY))
        comidaY += comidaVelocidade

        # [ini] colisão com player, reinicia posição
        if (comidaY + comidaAltura >= playerPosicaoY) and (((comidaX > playerPosicaoX) and (playerPosicaoX+yoshiLargura > comidaX)) or ((comidaX+comidaLargura > playerPosicaoX) and (comidaX+comidaLargura < playerPosicaoX+yoshiLargura))):
            comidaY = -220
            comidaX = random.randrange(0, largura-50) # reseta comida
            if comidaVelocidade < 10:
                comidaVelocidade += 0.9

            if comida_lista[comidaType][comidaID] in comida_lista[1]:
                score += 1
                pygame.mixer.Sound.play(pygame.mixer.Sound('assets/sounds/'+sounds_act[random.randint(0, 3)]))
            elif comida_lista[comidaType][comidaID] in comida_lista[0]:
                vidas -= 1
                if vidas == 0:
                    placar(score, vidas)
                    pygame.display.update()
                    pygame.mixer.Sound.play(pygame.mixer.Sound('assets/sounds/'+sounds_stats[1]))
                    dead(score)
                    restart()
                else:
                    pygame.mixer.Sound.play(pygame.mixer.Sound('assets/sounds/'+sounds_stats[0]))


            comidaType = random.randint(0, 1) # pega tipo da comida trash/candy
            comidaID = random.randint(0, 5) # pega index do tipo, 0 a 5
            comida = pygame.image.load('assets/images/'+comida_lista[comidaType][comidaID])
            comida = pygame.transform.scale(comida, (120, 120))
        # [fim] colisão com player, reinicia posição


        placar(score, vidas)


        # [ini] colisão:
        if altura > comidaY + comidaAltura/2 and anti_loop == True:  # reseta anti-loop de vidas
            anti_loop = False

        if comidaY > altura+comidaAltura/2 and anti_loop == False:
            if comidaVelocidade < 10:
                comidaVelocidade += 0.9 # aumenta velocidade do obj

            if comida_lista[comidaType][comidaID] in comida_lista[1]:
                vidas -= 1
                pygame.mixer.Sound.play(pygame.mixer.Sound('assets/sounds/'+sounds_stats[0]))
                
            if vidas == 0:
                placar(score, vidas)
                pygame.display.update()
                pygame.mixer.Sound.play(pygame.mixer.Sound('assets/sounds/'+sounds_stats[1]))
                dead(score)
                restart()


            comidaY = -220 # reseta pos comidaY
            comidaX = random.randrange(0, largura-50) # reseta pos comidaX
            anti_loop = True # anti loop

            comidaType = random.randint(0, 1) # pega tipo da comida trash/candy
            comidaID = random.randint(0, 5) # pega index do tipo, 0 a 5
            comida = pygame.image.load('assets/images/'+comida_lista[comidaType][comidaID]) # reseta comida e seu tipo
            comida = pygame.transform.scale(comida, (120, 120)) # reseta comida e seu tipo
        # [fim] colisão:

        pygame.display.update()
        fps.tick(60)
jogo()