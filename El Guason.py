
#------------------------------------------------------------------------------------------------------------------------------------------------
############################################################## Final Compu Grafica ############################################################## 
#------------------------------------------------------------------------------------------------------------------------------------------------
#Librerias
import os
import pygame
import sys
from pygame.locals import *
import time
import threading
import random
#------------------------------------------------------------------------------------------------------------------------------------------------
ANCHO = 1366
ALTO = 768
BASE_PERSONAJE = 705
VELOCIDAD = +5
nivelador=0
centSeg=0
unidSeg=0
deceSeg=0
unidMin=0
deceMin=0
#------------------------------------------------------------------------------------------------------------------------------------------------
class TextoTiempo:
    def __init__(self, TipoFuente = 'Fuentes/Zombified.ttf', Tamano = 40):
        pygame.font.init()
        self.font = pygame.font.Font(TipoFuente, Tamano)
        self.size = Tamano
 
    def render(self, surface, text, color, pos):
        text = unicode(text, "UTF-8")
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size 
             
def TiempoJuego():
    global centSeg, unidSeg, deceSeg, unidMin, deceMin, nivelador, ReiniciarTiempo 
    nivelador+=1
    if nivelador == 7:
       nivelador=0
       centSeg+=1
    if centSeg==9:
       centSeg=0
       unidSeg+=1
    if unidSeg==10:
       unidSeg=0
       deceSeg+=1
    if deceSeg==6:
       deceSeg=0
       unidMin+=1
    if unidMin==10:
       unidMin=0
       deceMin+=1
    if deceMin==10:
       deceMin=0
                                     
def ConcatenacionTiempo(decMin ,uniMin ,decSeg ,uniSeg ,cenSeg):  
    timeText=''
    timeText+=str(decMin)+str(uniMin)+":"+str(decSeg)+str(uniSeg)+":"+str(cenSeg)
    return timeText
#------------------------------------------------------------------------------------------------------------------------------------------------
class Personaje(pygame.sprite.Sprite):
    cambio_x = 0
    cambio_y = 0
    nivel = None
    nivel2 = None 
    posicion = None
    def __init__( self ):
        pygame.sprite.Sprite.__init__( self )
        self.Avanzar = pygame.image.load('Imagenes/PersonajeAvanzar.png').convert_alpha() 
        self.Retroceder = pygame.image.load('Imagenes/PersonajeRetroceder.png').convert_alpha() 
        self.InvencibleAvanzar = pygame.image.load('Imagenes/PersonajeInvencibleAvanzar.png').convert_alpha()
        self.InvencibleRetroceder = pygame.image.load('Imagenes/PersonajeInvencibleRetroceder.png').convert_alpha() 

        self.PersonajeAvanzar = {}
        self.PersonajeAvanzar[0] = (631, 0, 76, 116) #Agacharse
        self.PersonajeAvanzar[1] = (525, 0, 92, 116) #Saltar
        self.PersonajeAvanzar[2] = (432, 0, 72, 116) #Quieto
        self.PersonajeAvanzar[3] = (30, 0, 72, 116)
        self.PersonajeAvanzar[4] = (132, 0, 57, 116)
        self.PersonajeAvanzar[5] = (223, 0, 78, 116)
        self.PersonajeAvanzar[6] = (330, 0, 74, 116)

        self.PersonajeRetroceder = {}
        self.PersonajeRetroceder[0] = (0, 0, 75, 116) #Agacharse
        self.PersonajeRetroceder[1] = (88, 0, 92, 116) #Saltar
        self.PersonajeRetroceder[2] = (203, 0, 74, 116) #Quieto
        self.PersonajeRetroceder[3] = (602, 0, 77, 116)
        self.PersonajeRetroceder[4] = (518, 0, 57, 116) 
        self.PersonajeRetroceder[5] = (404, 0, 80, 116) 
        self.PersonajeRetroceder[6] = (303, 0, 73, 116)

        self.PersonajeInvencibleAvanzar = {}
        self.PersonajeInvencibleAvanzar[0] = (631, 0, 76, 116) #Agacharse
        self.PersonajeInvencibleAvanzar[1] = (525, 0, 92, 116) #Saltar
        self.PersonajeInvencibleAvanzar[2] = (432, 0, 72, 116) #Quieto
        self.PersonajeInvencibleAvanzar[3] = (30, 0, 72, 116)
        self.PersonajeInvencibleAvanzar[4] = (132, 0, 57, 116)
        self.PersonajeInvencibleAvanzar[5] = (223, 0, 78, 116)
        self.PersonajeInvencibleAvanzar[6] = (330, 0, 74, 116)

        self.PersonajeInvencibleRetroceder = {}
        self.PersonajeInvencibleRetroceder[0] = (0, 0, 75, 116) #Agacharse
        self.PersonajeInvencibleRetroceder[1] = (88, 0, 92, 116) #Saltar
        self.PersonajeInvencibleRetroceder[2] = (203, 0, 74, 116) #Quieto
        self.PersonajeInvencibleRetroceder[3] = (602, 0, 77, 116)
        self.PersonajeInvencibleRetroceder[4] = (518, 0, 57, 116) 
        self.PersonajeInvencibleRetroceder[5] = (404, 0, 80, 116) 
        self.PersonajeInvencibleRetroceder[6] = (303, 0, 73, 116)

        self.cual = 2
        self.cuanto = 100
        self.tiempo = 0
        self.izquierda = False
        self.DibujoInvencible = False
        self.ObtenerDibujoPersonaje()
        self.rect = self.image.get_rect()

    def ObtenerDibujoPersonaje(self):
        if self.izquierda == True:
           if self.DibujoInvencible == True:
              self.image=self.InvencibleRetroceder.subsurface(self.PersonajeInvencibleRetroceder[self.cual])
           else:
              self.image=self.Retroceder.subsurface(self.PersonajeRetroceder[self.cual])
        if self.izquierda == False:
           if self.DibujoInvencible == True:
              self.image=self.InvencibleAvanzar.subsurface(self.PersonajeInvencibleAvanzar[self.cual])
           else:
              self.image=self.Avanzar.subsurface(self.PersonajeAvanzar[self.cual])
      
    def update(self): 
        if self.cual > 6:
           self.cual = 3
        self.ObtenerDibujoPersonaje()
        self.Gravedad()

        self.rect.x += self.cambio_x
        ImpactosBloques = pygame.sprite.spritecollide(self, self.nivel.ListaPlataformas, False)
        for bloque in ImpactosBloques:
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            elif self.cambio_x < 0:
                self.rect.left = bloque.rect.right

        self.rect.y += self.cambio_y
        ImpactosBloques = pygame.sprite.spritecollide(self, self.nivel.ListaPlataformas, False) 
        for bloque in ImpactosBloques:
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top + 7
            elif self.cambio_y < 0:
                self.rect.top = bloque.rect.bottom
            self.cambio_y = 0

   
    def Gravedad(self):
        if self.cambio_y == 0:
           self.cambio_y = 1
        else:
           self.cambio_y += .35
        if self.rect.y >= BASE_PERSONAJE - self.rect.height and self.cambio_y >= 0:
           self.cambio_y = 0
           self.rect.y = BASE_PERSONAJE - self.rect.height

    def Saltar(self):
        self.rect.y += 2
        ImpactosPlataformasY = pygame.sprite.spritecollide(self, self.nivel.ListaPlataformas, False)
        self.rect.y -= 2
        if len(ImpactosPlataformasY) > 0 or self.rect.bottom >= BASE_PERSONAJE:
            self.cambio_y = -12

    def SaltarMismoPunto(self):
        self.cambio_x = 0

    def AvanzarIzquierda(self):
        self.cambio_x = -5

    def AvanzarDerecha(self):
        self.cambio_x = +5

    def Detenerse(self):
        self.cambio_x = 0

    def Agacharse(self):
        self.cambio_x = 0     
#------------------------------------------------------------------------------------------------------------------------------------------------
class DisparoDerecha( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__( self )
        self.image = pygame.image.load('Imagenes/BalaDerecha.png').convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def update( self ):
        self.rect.move_ip((15,0))
        if self.rect.left >= ANCHO or EliminarDisparo == True:
           self.kill()

class DisparoIzquierda( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__( self )
        self.image = pygame.image.load('Imagenes/BalaIzquierda.png').convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def update( self ):
        self.rect.move_ip((-15,0))
        if self.rect.right <= 0 or EliminarDisparo == True:
           self.kill() 
#------------------------------------------------------------------------------------------------------------------------------------------------
class FondoAnimado( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_base = pygame.image.load('Imagenes/FondoNivel1.png').convert_alpha() 
        self.image = self.imagen_base
        self.rect = self.image.get_rect()
        self.rect.topleft = (posx,posy)

    def update( self ):
        if scroll:
           if FondoDerecha == True:
              if self.rect.right <= ANCHO:
                 self.rect.right = ANCHO
                 personaje.AvanzarDerecha()
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if self.rect.left >= 0:
                 self.rect.left = 0
                 personaje.AvanzarIzquierda()
              else:
                 self.rect.move_ip(VELOCIDAD,0)
#------------------------------------------------------------------------------------------------------------------------------------------------
class FondoAnimado2( pygame.sprite.Sprite ):
    def __init__( self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_base = pygame.image.load('Imagenes/FondoNivel2.png').convert_alpha() 
        self.image = self.imagen_base
        self.rect = self.image.get_rect()
        self.rect.topleft = (posx,posy)
        self.scroll2 = False

    def update( self ):
        if self.scroll2 == True:
           if FondoDerecha == True:
              if self.rect.right <= ANCHO:
                 self.rect.right = ANCHO
                 personaje.AvanzarDerecha()
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if self.rect.left >= 0:
                 self.rect.left = 0
                 personaje.AvanzarIzquierda()
              else:
                 self.rect.move_ip(VELOCIDAD,0)
        if scroll:
           if FondoDerecha == True:
              if self.rect.right <= ANCHO:
                 self.rect.right = ANCHO
                 personaje.AvanzarDerecha()
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if self.rect.left >= 0:
                 self.rect.left = 0
                 personaje.AvanzarIzquierda()
              else:
                 self.rect.move_ip(VELOCIDAD,0)

#------------------------------------------------------------------------------------------------------------------------------------------------
class Plataforma(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Imagenes/PlataformaNivel1.png').convert_alpha()   
        self.rect = self.image.get_rect()

    def update(self):
        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class Plataforma2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Imagenes/PlataformaNivel222.png').convert_alpha()   
        self.rect = self.image.get_rect()

    def update(self):
        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)                 
                 
class PlataformasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        self.ListaPlataformas = pygame.sprite.Group()
        nivel = [[800, 260],
                 [810, 510],
                 [1180, 340],
                 [1780, 500],
                 [2780, 500],
                 [2980, 350],
                 [3180, 200],
                 [3480, 500],
                 [3580, 200],
                 [4000, 300],
                 [4200, 500],
                 [4680, 300],
                 [4780, 500],
                 [5480, 200],
                 [5080, 350]
                   ]
        for plataforma in nivel:
            bloque = Plataforma()
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            self.ListaPlataformas.add(bloque) 

    def update(self):
        self.ListaPlataformas.update()
     
    def draw(self, pantalla):
        self.ListaPlataformas.draw(pantalla)      
#------------------------------------------------------------------------------------------------------------------------------------------------
                 
class PlataformasNivel2(pygame.sprite.Sprite):
    def __init__(self):
        self.ListaPlataformas = pygame.sprite.Group()
        nivel = [[800, 280],[3200,295],[4400,300],[3400,120],
                 [1000, 510],[1200, 280],[3600,295],[4000, 300],
                 [1400, 510],[2000, 280],
                 [1600, 510],[2200, 280],
                 [1800,510],[2400, 280],
                 [3000,510],[2600,280],
                 [3800,510],[2800,280],
                 [4500,510],
                 ]

        for plataforma in nivel:
            bloque = Plataforma2()
            bloque.rect.x = plataforma[0]
            bloque.rect.y = plataforma[1]
            self.ListaPlataformas.add(bloque) 

    def update(self):
        self.ListaPlataformas.update()
     
    def draw(self, pantalla):
        self.ListaPlataformas.draw(pantalla)      
         
#------------------------------------------------------------------------------------------------------------------------------------------------
class Monedas(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenCompleta = imagen
        cual=0
        self.AnimacionMoneda=[]
        while cual < 7:
            self.AnimacionMoneda.append(self.ImagenCompleta.subsurface((cual*40,0,40,38)))
            cual += 1
        self.animacion= 0
        self.actualizacion = pygame.time.get_ticks()
        self.image = self.AnimacionMoneda[self.animacion]
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
            self.animacion= self.animacion + 1
            if self.animacion > 6:
                self.animacion = 0
            self.image = self.AnimacionMoneda[self.animacion]
            self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class MonedasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaMonedas = pygame.sprite.Group()
        self.Moneda = pygame.image.load("Imagenes/MonedaAnimada.png")
        self.transparente = self.Moneda.get_at((0,0))
        self.Moneda.set_colorkey(self.transparente)
        posicionmoneda = [[825, 230],
                          [865, 230],
                          [905, 230],
                          [945, 230],
                          [845, 190],
                          [885, 190],
                          [925, 190],
                          [865, 150],
                          [905, 150],
                          [885, 110],

                          [1810, 650],
                          [1850, 650],
                          [1890, 650],
                          [1930, 650],
                          [1970, 650],

                          [2400, 400],
                          [2440, 400],
                          [2480, 400],
                          [2520, 400],
                          [2560, 400],

                          [4225, 465],
                          [4265, 465],
                          [4305, 465],
                          [4345, 465],
                          [4245, 425],
                          [4285, 425],
                          [4325, 425],
                          [4265, 385],
                          [4304, 385],
                          [4285, 345]]
        for recorrido in posicionmoneda:
            moneda = Monedas((recorrido[0],recorrido[1]), self.Moneda)
            self.ListaMonedas.add(moneda) 

    def update(self):
        self.ListaMonedas.update()
     
    def draw(self, pantalla):
        self.ListaMonedas.draw(pantalla)  
#------------------------------------------------------------------------------------------------------------------------------------------------
class Zombies(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Zombie1 = pygame.image.load("Imagenes/EnemigoZombie.png").convert_alpha()
        self.Zombie2 = pygame.transform.flip(self.Zombie1, True, False)
      

        self.zombie1 = {}
        self.zombie1[0] = (0, 0, 55, 86)
        self.zombie1[1] = (55, 0, 69, 86)
        self.zombie1[2] = (126, 0, 75, 86)
        self.zombie1[3] = (207, 0, 58, 86)
        self.zombie1[4] = (270, 0, 83, 86)
        self.zombie1[5] = (358, 0, 61, 86)
        self.zombie1[6] = (428, 0, 53, 86)
        self.zombie1[7] = (481, 0, 69, 86)

        self.zombie2 = {}
        self.zombie2[0] = (0, 0, 78, 86)
        self.zombie2[1] = (79, 0, 52, 86)
        self.zombie2[2] = (142, 0, 58, 86)
        self.zombie2[3] = (203, 0, 87, 86)
        self.zombie2[4] = (294, 0, 59, 86)
        self.zombie2[5] = (357, 0, 76, 86)
        self.zombie2[6] = (437, 0, 70, 86)
        self.zombie2[7] = (505, 0, 56, 86)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.Zombie2.subsurface(self.zombie2[self.cual])
        else:
            self.image=self.Zombie1.subsurface(self.zombie1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 7:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)
        
class ZombiesNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaZombies = pygame.sprite.Group()

        posicionzombie = [[1270, 260],
                          [915, 430],
                          [1500, 620],
                          [1600, 620],
                          [1700, 620],
                          [2200, 620],
                          [3900, 620],
                          [5200, 610],
                          [5050, 610],
                          [4850, 610]]
        for recorrido in posicionzombie:
            zombie = Zombies(recorrido[0],recorrido[1])
            self.ListaZombies.add(zombie)

    def update(self):
        self.ListaZombies.update()
     
    def draw(self, pantalla):
        self.ListaZombies.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Fantasmas(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Fantasma1 = pygame.image.load("Imagenes/EnemigoFantasma.png").convert_alpha()
        self.Fantasma2 = pygame.transform.flip(self.Fantasma1, True, False)
        
        self.fantasma1 = {}
        self.fantasma1[0] = (0, 0, 70, 87)
        self.fantasma1[1] = (70, 0, 70, 87)
        self.fantasma1[2] = (140, 0, 70, 87)

        self.fantasma2 = {}
        self.fantasma2[0] = (140, 0, 70, 87)
        self.fantasma2[1] = (70, 0, 70, 87)
        self.fantasma2[2] = (0, 0, 70, 87)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
           self.image=self.Fantasma2.subsurface(self.fantasma2[self.cual])
        else:
           self.image=self.Fantasma1.subsurface(self.fantasma1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 2:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class FantasmasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaFantasmas = pygame.sprite.Group()

        posicionfantasma = [[1530, 610],
                            [1750, 620],
                            [1870, 415],
                            [2700, 610],
                            [3280, 120],
                            [5150, 610],
                            [5000, 610],
                            [4800, 610]
                            ]
        for recorrido in posicionfantasma:
            fantasma = Fantasmas(recorrido[0],recorrido[1])
            self.ListaFantasmas.add(fantasma) 

    def update(self):
        self.ListaFantasmas.update()
     
    def draw(self, pantalla):
        self.ListaFantasmas.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
#JEFE NIVEL 1
class Dragones(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.Dragon1 = pygame.image.load("Imagenes/EnemigoDragon.png").convert_alpha()
        self.Dragon2 = pygame.transform.flip(self.Dragon1, True, False)
        
        self.dragon1 = {}
        self.dragon1[0] = (0, 0, 100, 96)
        self.dragon1[1] = (100, 0, 100, 96)
        self.dragon1[2] = (200, 0, 100, 96)
        self.dragon1[3] = (300, 0, 100, 96)

        self.dragon2 = {}
        self.dragon2[0] = (300, 0, 100, 96)
        self.dragon2[1] = (200, 0, 100, 96)
        self.dragon2[2] = (100, 0, 100, 96)
        self.dragon2[3] = (0, 0, 100, 96)
        
        self.actualizacion = pygame.time.get_ticks()
        self.cual = 0     
        self.izquierda = False   
        self.obtenerDibujo()
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.dx = 1
        self.PosicionX = posX

    def obtenerDibujo(self):
        if self.izquierda:
            self.image=self.Dragon2.subsurface(self.dragon2[self.cual])
        else:
            self.image=self.Dragon1.subsurface(self.dragon1[self.cual])

    def update(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
           self.cual += 1
           if self.cual > 3:
              self.cual = 0
           self.obtenerDibujo()
           self.actualizacion= pygame.time.get_ticks()
        
        TiempoMovimiento =pygame.time.get_ticks()/1000         
        t = TiempoMovimiento
        if t==2 or t==6 or t==10 or t==14 or t==18 or t==22 or t==26 or t==30 or t==34 or t==38 or t==42 or t==46 or t==50 or t==54 or t==58 or t==62 or t==66 or t==70 or t==74 or t==78 or t==82 or t==86 or t==90 or t==94 or t==98 or t==102 or t==106 or t==110 or t==114 or t==118 or t==122 or t==126 or t==130 or t==134 or t==138 or t==142 or t==146 or t==150 or t==154 or t==158 or t==162  or t==166 or t==170 or t==174 or t==178 or t==182 or t==186 or t==190 or t==194 or t==198 or t==202:
           self.izquierda = True

                
        if t==4 or t==8 or t==12 or t==16 or t==20 or t==24 or t==28 or t==32 or t==36 or t==40 or t==44 or t==48 or t==52 or t==56 or t==60 or t==64 or t==68 or t==72 or t==76 or t==80 or t==84 or t==88 or t==92 or t==96 or t==100 or t==104 or t==108 or t==112 or t==116 or t==120 or t==124 or t==128 or t==132 or t==136 or t==140 or t==144 or t==148 or t==152 or t==156 or t==160 or t==164 or t==168 or t==172 or t==176 or t==180 or t==184 or t==188 or t==192 or t==196 or t==200 or t==204:
           self.izquierda = False

        if self.izquierda == True:
           self.rect.move_ip(-self.dx,0)
        else:
           self.rect.move_ip(self.dx,0)

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class DragonesNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaDragones = pygame.sprite.Group()

        posiciondragon = [[5150, 260]]
        for recorrido in posiciondragon:
            dragon = Dragones(recorrido[0],recorrido[1])
            self.ListaDragones.add(dragon) 

    def update(self):
        self.ListaDragones.update()
     
    def draw(self, pantalla):
        self.ListaDragones.draw(pantalla) 


#nivel 2


#------------------------------------------------------------------------------------------------------------------------------------------------
class Vidas(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Imagenes/Vidas.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class VidasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaVidas = pygame.sprite.Group()
        self.Vida = pygame.image.load("Imagenes/Vidas.png")
        self.transparente = self.Vida.get_at((0,0))
        self.Vida.set_colorkey(self.transparente)
        posicionvida = [[1270, 100],
                        [3690, 100],
                        [2999, 300],
                        [4000, 100],
                        [5000, 100]
                        ]
        for recorrido in posicionvida:
            vida = Vidas((recorrido[0],recorrido[1]), self.Vida)
            self.ListaVidas.add(vida) 

    def update(self):
        self.ListaVidas.update()
     
    def draw(self, pantalla):
        self.ListaVidas.draw(pantalla) 

#------------------------------------------------------------------------------------------------------------------------------------------------
class Balas(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Imagenes/Balas.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class BalasNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaBalas = pygame.sprite.Group()
        self.Bala = pygame.image.load("Imagenes/Balas.png")
        self.transparente = self.Bala.get_at((0,0))
        self.Bala.set_colorkey(self.transparente)
        posicionbala = [[1870, 250],
                        [3490, 400],
                        ]
        for recorrido in posicionbala:
            bala = Balas((recorrido[0],recorrido[1]), self.Bala)
            self.ListaBalas.add(bala) 

    def update(self):
        self.ListaBalas.update()
     
    def draw(self, pantalla):
        self.ListaBalas.draw(pantalla)  
#------------------------------------------------------------------------------------------------------------------------------------------------
class Invencibles(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Imagenes/Invencible1.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class InvenciblesNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaInvencibles = pygame.sprite.Group()
        self.Invencible = pygame.image.load("Imagenes/Invencible.png")
        self.transparente = self.Invencible.get_at((0,0))
        self.Invencible.set_colorkey(self.transparente)
        posicioninvencible = [[3290, 100]]
        for recorrido in posicioninvencible:
            invencible = Invencibles((recorrido[0],recorrido[1]), self.Invencible)
            self.ListaInvencibles.add(invencible) 

    def update(self):
        self.ListaInvencibles.update()
     
    def draw(self, pantalla):
        self.ListaInvencibles.draw(pantalla)

#------------------------------------------------------------------------------------------------------------------------------------------------
class Meta(pygame.sprite.Sprite):
    def __init__(self, coordenadas, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Imagenes/Meta.png")
        self.rect = self.image.get_rect()
        self.rect.center = coordenadas
        self.actualizacion = pygame.time.get_ticks()
        self.maximo = self.rect.bottom+5
        self.minimo = self.rect.top-5
        self.dy = 1

    def update(self):
        if self.actualizacion + 40 < pygame.time.get_ticks():
           self.rect.move_ip(0,self.dy)
           if self.rect.bottom > self.maximo or self.rect.top < self.minimo:
              self.dy = -self.dy
           self.actualizacion= pygame.time.get_ticks()

        if scroll:
           if FondoDerecha == True:
              if personaje.rect.x > 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(-VELOCIDAD,0)
           if FondoDerecha == False:
              if personaje.rect.x < 680:
                 self.rect.move_ip(0,0)
              else:
                 self.rect.move_ip(VELOCIDAD,0)

class MetaNivel1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ListaMeta = pygame.sprite.Group()
        self.Meta = pygame.image.load("Imagenes/Meta.png")
        self.transparente = self.Meta.get_at((0,0))
        self.Meta.set_colorkey(self.transparente)
        posicionmeta = [[5600, 150]]
        for recorrido in posicionmeta:
            meta = Meta((recorrido[0],recorrido[1]), self.Meta)
            self.ListaMeta.add(meta) 

    def update(self):
        self.ListaMeta.update()
     
    def draw(self, pantalla):
        self.ListaMeta.draw(pantalla) 
#------------------------------------------------------------------------------------------------------------------------------------------------
class Sounds():
    def __init__(self):
       self.OpcionMenu = pygame.mixer.Sound(os.path.join("Sonidos/OpcionMenu.wav"))
       self.OpcionMenu.set_volume(1)
       self.EnterMenu = pygame.mixer.Sound(os.path.join("Sonidos/EnterMenu.mp3"))
       self.EnterMenu.set_volume(1)
       self.Pausa = pygame.mixer.Sound(os.path.join("Sonidos/Pausa.wav"))
       self.Pausa.set_volume(1)
       self.Salto = pygame.mixer.Sound(os.path.join("Sonidos/Saltar.wav"))
       self.Salto.set_volume(0.2)
       self.Disparo = pygame.mixer.Sound(os.path.join("Sonidos/Disparar.wav"))
       self.Disparo.set_volume(0.8)
       self.Destruido = pygame.mixer.Sound(os.path.join("Sonidos/Destruido.wav"))
       self.Destruido.set_volume(1)
       self.VidaMenos = pygame.mixer.Sound(os.path.join("Sonidos/VidaMenos.wav"))
       self.VidaMenos.set_volume(1)
       self.GameOver = pygame.mixer.Sound(os.path.join("Sonidos/GameOver.wav"))
       self.GameOver.set_volume(1)
       self.MasVida = pygame.mixer.Sound(os.path.join("Sonidos/VidaMas.wav"))
       self.MasVida.set_volume(1)
       self.MasMoneda = pygame.mixer.Sound(os.path.join("Sonidos/Moneda.wav"))
       self.MasMoneda.set_volume(1)
       self.MasBala = pygame.mixer.Sound(os.path.join("Sonidos/Balas.wav"))
       self.MasBala.set_volume(1)
       self.MasVelocidad = pygame.mixer.Sound(os.path.join("Sonidos/Velocidad.wav"))
       self.MasVelocidad.set_volume(1)
       self.Invencible = pygame.mixer.Sound(os.path.join("Sonidos/Invencible.wav"))
       self.Invencible.set_volume(1)
       self.MusicaInvencible = pygame.mixer.Sound(os.path.join("Sonidos/MusicaInvencible.wav"))
       self.MusicaInvencible.set_volume(1)
       self.Meta = pygame.mixer.Sound(os.path.join("Sonidos/Meta.wav"))
       self.Meta.set_volume(1)
#------------------------------------------------------------------------------------------------------------------------------------------------
#INICIALIZACION DE VARIABLES
pygame.init()
pygame.mixer.init()
#------------------------------------------------------------------------------------------------------------------------------------------------
#COLORES
blanco = (255,255,255)
negro = (0,0,0)
amarillo = (255,255,0)
dorado = (231,174,24)
azulclaro = (0,255,255)
violeta = (204,0,102)
rojo = (255,0,0)
rojooscuro = (190,17,17)
verde = (0,255,0)
azul = (0,0,255)
morado = (153,51,255)
naranja = (255,128,0)
gris = (128,128,128)
#------------------------------------------------------------------------------------------------------------------------------------------------
#DIMENSIONES DE LA VENTANA
pantalla = pygame.display.set_mode((ANCHO,ALTO),pygame.FULLSCREEN)
pygame.display.set_caption("EL GUASON")
#------------------------------------------------------------------------------------------------------------------------------------------------
#DIMENSIONES DEL MENU
MenuX = 410
MenuY = 478
DimensionMenu = [MenuX,MenuY]
#------------------------------------------------------------------------------------------------------------------------------------------------
#DIMENSIONES DEL MENU DE PAUSA
MenuPausaX = 410
MenuPausaY = 478
DimensionMenuPausa = [MenuPausaX,MenuPausaY]
#------------------------------------------------------------------------------------------------------------------------------------------------
#IMAGENES Y MUSICA DEL MENU
Seleccion = pygame.image.load('Imagenes/Seleccion.png').convert_alpha()
pygame.mixer.music.load('Sonidos/MisionImposible.wav')
pygame.mixer.music.play(-1)
#------------------------------------------------------------------------------------------------------------------------------------------------
#MUSICA Y SONIDOS
sounds = Sounds()
#------------------------------------------------------------------------------------------------------------------------------------------------
#PERSONAJE
personaje = Personaje()
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#TIPOS DE FUENTES TEXTOS
FuenteEstadisticas = pygame.font.Font('Fuentes/Zombified.ttf', 30)
FuenteGameOver = pygame.font.Font('Fuentes/Zombified.ttf', 110)
FuenteMisionCompleta = pygame.font.Font('Fuentes/Zombified.ttf', 80)
FuentePresioneEspacio = pygame.font.Font('Fuentes/Zombified.ttf', 50)
FuentePuntaje = pygame.font.Font('Fuentes/Zombified.ttf', 30)
#------------------------------------------------------------------------------------------------------------------------------------------------
#VARIABLES DE JUEGO
salir = False
scroll = False
FondoDerecha = False
reloj = pygame.time.Clock() 
textoTiempo = TextoTiempo()
EliminarDisparo = False
ReiniciarTiempo = False 
CambioNivel2 = False
#------------------------------------------------------------------------------------------------------------------------------------------------
# ESTRUCTURA DEL TEXTO DEL MENU 
def TextoMenu(texto, posx, posy, negro):
    fuente = pygame.font.Font("Fuentes/bloodcrow.ttf", 35)
    salida = pygame.font.Font.render(fuente, texto, 0, negro)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
#------------------------------------------------------------------------------------------------------------------------------------------------
# ESTRUCTURA DEL TEXTO DEL MENU DE PAUSA
def TextoMenuPausa(texto, posx, posy, negro):
    fuente = pygame.font.Font("Fuentes/Zombified.ttf", 60)
    salida = pygame.font.Font.render(fuente, texto, 0, negro)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
#------------------------------------------------------------------------------------------------------------------------------------------------
ImagenMoneda = {}
ImagenMoneda[0] = (0, 0, 40, 40)
ImagenMoneda[1] = (40, 0, 40, 40)
ImagenMoneda[2] = (80, 0, 30, 40)
ImagenMoneda[3] = (110, 0, 16 , 40)
ImagenMoneda[4] = (126, 0, 30 , 40)
ImagenMoneda[5] = (156, 0, 38, 40)
ImagenMoneda[6] = (194, 0, 38, 40)
cual1 = 0
cuanto1 = 100
tiempo1 = 0
def IconoAnimadoMonedas():
   global cual1, tiempo1
   if pygame.time.get_ticks()-tiempo1 > cuanto1:
      tiempo1 = pygame.time.get_ticks()
      cual1 = cual1 + 1
      if cual1 > 6:
         cual1 = 0
#------------------------------------------------------------------------------------------------------------------------------------------------
pos4 = -150
tiempo4 = 0
def MovimientoCalavera():
   global pos4, tiempo4
   pos4 = pos4 + 1
   if pos4 > 10:
      pos4 = 10
#------------------------------------------------------------------------------------------------------------------------------------------------
pos5 = -350
tiempo5 = 0
def MovimientoTitulo():
   global pos5, tiempo5
   pos5 = pos5 + 5
   if pos5 > 500:
      pos5 = 500
#------------------------------------------------------------------------------------------------------------------------------------------------
pos6 = -500
tiempo6 = 0
def MovimientoGameOver():
   global pos6, tiempo6
   pos6 = pos6 + 3
   if pos6 > 400:
      pos6 = 400
#------------------------------------------------------------------------------------------------------------------------------------------------
pos7 = -350
tiempo7 = 0
def MovimientoNivel1Completo():
   global pos7, tiempo7
   pos7 = pos7 + 2
   if pos7 > 250:
      pos7 = 250
#------------------------------------------------------------------------------------------------------------------------------------------------
pos8 = 1000
def MovimientoLogoUniversidad():
   global pos8
   pos8 = pos8 - 4
   if pos8 < 250:
      pos8 = 250
#------------------------------------------------------------------------------------------------------------------------------------------------
pos9 = 2200
def MovimientoComputador():
   global pos9
   pos9 = pos9 - 4
   if pos9 < 600:
      pos9 = 600
#------------------------------------------------------------------------------------------------------------------------------------------------
pos10 = 1250
def MovimientoComputacionGrafica():
   global pos10
   pos10 = pos10 - 2
   if pos10 < 670:
      pos10 = 670
#------------------------------------------------------------------------------------------------------------------------------------------------
pos11 = 1100
def MovimientoNombre1():
   global pos11
   pos11 = pos11 - 2
   if pos11 < 610:
      pos11 = 610
#------------------------------------------------------------------------------------------------------------------------------------------------
pos12 = 1200
def MovimientoNombre2():
   global pos12
   pos12 = pos12 - 2
   if pos12 < 660:
      pos12 = 660

pos22 = 1300
def MovimientoNombre3():
   global pos22
   pos22 = pos22 - 2
   if pos22 < 710:
      pos22 = 710
#------------------------------------------------------------------------------------------------------------------------------------------------
pos13 = -200
def MovimientoMision1Completa():
   global pos13
   pos13 = pos13 + 2
   if pos13 > 255:
      pos13 = 255
#------------------------------------------------------------------------------------------------------------------------------------------------
pos14 = 1400
def MovimientoPresioneEspacioMeta():
   global pos14
   pos14 = pos14 - 2
   if pos14 < 430:
      pos14 = 430
#------------------------------------------------------------------------------------------------------------------------------------------------
pos15 = 1400
def MovimientoPresioneEspacioGameOver():
   global pos15
   pos15 = pos15 - 2
   if pos15 < 400:
      pos15 = 400
#------------------------------------------------------------------------------------------------------------------------------------------------
#################################################### FUNCION PRINCIPAL DE INICIO DEL JUEGO #################################################### 
#------------------------------------------------------------------------------------------------------------------------------------------------
def IniciarJuego():
    Puntaje = 0
    CantidadVidas = 5
    CantidadBalas = 20
    CantidadMonedas = 0
    #IMAGEN DE FONDO NIVEL 1
    FondoAnimado1 = FondoAnimado(0,0)
    FondoAnimadoGrupo = pygame.sprite.RenderUpdates(FondoAnimado1)
    #CREACION DE PLATAFORMAS NIVEL 1
    GrupoPlataformas = []
    GrupoPlataformas.append(PlataformasNivel1())
    DibujoPlataformas = GrupoPlataformas[0]
    personaje.nivel = DibujoPlataformas
    #CREACION DE MONEDAS
    GrupoMonedas = []
    GrupoMonedas.append(MonedasNivel1())
    DibujoMonedas = GrupoMonedas[0]
    personaje.posicionmoneda = DibujoMonedas
    #CREACION DE ZOMBIES
    GrupoZombies = []
    GrupoZombies.append(ZombiesNivel1())
    DibujoZombies = GrupoZombies[0]
    personaje.posicionzombie = DibujoZombies
    #CREACION DE FANTASMAS
    GrupoFantasmas = []
    GrupoFantasmas.append(FantasmasNivel1())
    DibujoFantasmas = GrupoFantasmas[0]
    personaje.posicionfantasma = DibujoFantasmas

    #CREACION DE DRAGONES
    GrupoDragones = []
    GrupoDragones.append(DragonesNivel1())
    DibujoDragones = GrupoDragones[0]
    personaje.posiciondragon = DibujoDragones
    #CREACION DE MODIFICADOR VIDAS
    GrupoVidas = []
    GrupoVidas.append(VidasNivel1())
    DibujoVidas = GrupoVidas[0]
    personaje.posicionvida = DibujoVidas 
    #CREACION DE MODIFICADOR BALAS
    GrupoBalas = []
    GrupoBalas.append(BalasNivel1())
    DibujoBalas = GrupoBalas[0]
    personaje.posicionbala = DibujoBalas
    #CREACION DE MODIFICADOR INVENCIBLE
    GrupoInvencibles = []
    GrupoInvencibles.append(InvenciblesNivel1())
    DibujoInvencibles = GrupoInvencibles[0]
    personaje.posicioninvencible = DibujoInvencibles

    #CREACION DE META
    j=1
    GrupoMeta = []
    GrupoMeta.append(MetaNivel1())
    DibujoMeta = GrupoMeta[0]
    personaje.posicionmeta = DibujoMeta  
    #ICONOS DE OBJETOS
    IconoVidas = pygame.image.load('Imagenes/Vidas.png').convert_alpha()
    IconoBalas = pygame.image.load('Imagenes/Balas.png').convert_alpha()
    IconoMoneda = pygame.image.load('Imagenes/IconoMonedaAnimada.png').convert_alpha()
    IconoReloj = pygame.image.load('Imagenes/Reloj.png').convert_alpha()
    MonedaInstrucciones = pygame.image.load('Imagenes/Moneda.png').convert_alpha()
    #PERSONAJE
    PersonajeGrupo = pygame.sprite.RenderUpdates(personaje)
    personaje.rect.x = 50
    personaje.rect.y = BASE_PERSONAJE
    ListaSpritesActivos = pygame.sprite.Group()
    ListaSpritesActivos.add(personaje)
    #DISPAROS
    DisparosGrupo = pygame.sprite.RenderUpdates()
#------------------------------------------------------------------------------------------------------------------------------------------------
    pygame.event.clear
    os.system('clear')
    salir = False
    FinGameOver = False
    FinMeta = False
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Sonidos/PiratasDelCaribe.wav')
    pygame.mixer.music.play(-1)

    FondoGameOver = pygame.image.load('Imagenes/FondoGameOver.png').convert_alpha() 
    EsqueletoGameOver = pygame.image.load('Imagenes/EsqueletoGameOver.png').convert_alpha()
    FondoMensajeMeta = pygame.image.load('Imagenes/FondoMensajeMeta.png').convert_alpha() 
    PersonajeMeta = pygame.image.load('Imagenes/PersonajeMeta.png').convert_alpha() 
    CalaveraMeta = pygame.image.load('Imagenes/CalaveraMeta.png').convert_alpha() 

    TextoGameOver = FuenteGameOver.render("GAME OVER", 1, (negro))
    TextoMision1Completa = FuenteMisionCompleta.render("MUY BIEN, AQUI TERMINA EL MODO PUEBA", 1, (verde))
    TextoMision1Completaf = FuenteMisionCompleta.render("GANASTE", 1, (verde))
    TextoPresioneEspacioMeta = FuentePresioneEspacio.render("GANASTE!!", 1, (verde))
    TextoPresioneEspacioMeta1 = FuentePresioneEspacio.render("HAS LOGRADO RESCATAR TU HARLEY QUINN", 1, (verde))
    TextoPresioneEspacioGameOver = FuentePresioneEspacio.render("PRESIONE ESPACIO PARA CONTINUAR", 1, (verde))

    Mas100Puntos = FuentePuntaje.render("+100", 1, (blanco))

    global event, scroll, FondoDerecha, EliminarDisparo, MenuPausaY, DimensionMenuPausa
    global centSeg, unidSeg, deceSeg, unidMin, deceMin, PausaTiempo, CambioNivel2 
    while salir != True: 
       reloj.tick(60) 
       tecla = pygame.key.get_pressed()
       for event in pygame.event.get():   
           if event.type == pygame.QUIT:
              salir = True
           if tecla[pygame.K_s]:
              sys.exit()
           if tecla[pygame.K_SPACE]:
                print "Disparar"
                scroll = False
                if CantidadBalas == 0 or CantidadVidas == 0 or FinMeta == True:
                   CantidadBalas = CantidadBalas
                else:
                   sounds.Disparo.play()
                   CantidadBalas -= 1
                   if personaje.izquierda == True:
                      DisparosGrupo.add(DisparoIzquierda(personaje.rect.left-30, personaje.rect.y+40))
                   if personaje.izquierda == False:
                      DisparosGrupo.add(DisparoDerecha(personaje.rect.right-30, personaje.rect.y+40))
#------------------------------------------------------------------------------------------------------------------------------------------------   
       if event.type == pygame.KEYDOWN:

          if tecla[pygame.K_RIGHT]:
             personaje.izquierda = False
             if CambioNivel2 == True:

                FondoDerecha = True
                if CantidadVidas == 0 or FinMeta == True:
                   FondoAnimado2.scroll2 = False
                   scroll=False
                else:
                   if pygame.time.get_ticks()-personaje.tiempo > personaje.cuanto:
                      personaje.tiempo = pygame.time.get_ticks()
                      personaje.cual +=1
                   if personaje.rect.x >= 680:
                      FondoAnimado2.scroll2 = True
                      scroll = True
                      personaje.cambio_x = 0
                   if personaje.rect.x < 680:    
                      FondoAnimado2.scroll2 = False
                      scroll = False
                      personaje.AvanzarDerecha()

                
             else:
                FondoDerecha = True
                if CantidadVidas == 0 or FinMeta == True:
                   scroll = False
                else:
                   if pygame.time.get_ticks()-personaje.tiempo > personaje.cuanto:
                      personaje.tiempo = pygame.time.get_ticks()
                      personaje.cual +=1
                   if personaje.rect.x >= 680:
                      scroll = True
                      personaje.cambio_x = 0
                   if personaje.rect.x < 680:    
                      scroll = False
                      personaje.AvanzarDerecha()

          if tecla[pygame.K_LEFT]:
             personaje.izquierda = True
             if CambioNivel2 == True:
                FondoDerecha = False
                if CantidadVidas == 0 or FinMeta == True:
                   FondoAnimado2.scroll2 = False
                   scroll = False
                else:
                   if pygame.time.get_ticks()-personaje.tiempo > personaje.cuanto:
                      personaje.tiempo = pygame.time.get_ticks()
                      personaje.cual +=1
                   if personaje.rect.x <= 680:
                      FondoAnimado2.scroll2 = True
                      scroll = True
                      personaje.cambio_x = 0
                   if personaje.rect.x > 680:    
                      FondoAnimado2.scroll2 = False
                      scroll = False
                      personaje.AvanzarIzquierda()

             else:
                FondoDerecha = False
                if CantidadVidas == 0 or FinMeta == True:
                   scroll = False
                else:
                   if pygame.time.get_ticks()-personaje.tiempo > personaje.cuanto:
                      personaje.tiempo = pygame.time.get_ticks()
                      personaje.cual +=1
                   if personaje.rect.x <= 680:
                      scroll = True
                      personaje.cambio_x = 0
                   if personaje.rect.x > 680:    
                      scroll = False
                      personaje.AvanzarIzquierda()

          if tecla[pygame.K_UP]:
             FondoAnimado2.scroll2 = True
             sounds.Salto.play(1)
             personaje.Saltar()
             personaje.cual = 1


          if tecla[pygame.K_DOWN]:
             scroll = False
             personaje.Agacharse()
             personaje.cual = 0
#------------------------------------------------------------------------------------------------------------------------------------------------
          if tecla[pygame.K_ESCAPE]:
             if FinMeta == True or FinGameOver == True:
                Pausa = False
             else:
                Pausa = True
                OpcionMenuPausa = 1
                pygame.mixer.music.pause()
                sounds.Pausa.play(-1)
                sounds.Pausa.stop()
                while Pausa:
                   reloj.tick(60) 
                   tecla = pygame.key.get_pressed()
                   for event in pygame.event.get():
                      if event.type == pygame.QUIT:
                         pygame.quit()
                      if tecla[pygame.K_UP] and OpcionMenuPausa > 1 and MenuPausaY > DimensionMenuPausa[1]:
                         sounds.OpcionMenu.play()
                         OpcionMenuPausa -= 1
                         MenuPausaY = MenuPausaY-40
                      if tecla[pygame.K_DOWN] and OpcionMenuPausa < 3 and MenuPausaY > DimensionMenuPausa[0]:
                         sounds.OpcionMenu.play()
                         OpcionMenuPausa += 1
                         MenuPausaY = MenuPausaY+40
                      if tecla[K_RETURN]:
	                 if OpcionMenuPausa == 1:
	                    print "REANUDAR JUEGO"
                            sounds.Pausa.stop()
                            sounds.EnterMenu.play()
                            Pausa = False
                            pygame.mixer.music.unpause()
	                 if OpcionMenuPausa == 2:
                            print "VOLVER AL MENU PRINCIPAL"
                            sounds.Pausa.stop()
                            sounds.EnterMenu.play()
	                    salir = True
                            Pausa = False
                            pygame.mixer.music.load('Sonidos/PiratasDelCaribe.wav')
                            pygame.mixer.music.play(-1)
                            Menu(opcion)
	                 if OpcionMenuPausa == 3:
                            sounds.EnterMenu.play()
                            sys.exit()
                   MenuPausa(OpcionMenuPausa)
                   pygame.display.update()
#------------------------------------------------------------------------------------------------------------------------------------------------                   
       if event.type == pygame.KEYUP:
          personaje.cual = 2

          if tecla[pygame.K_RIGHT]:
             personaje.Detenerse()
             scroll = False

          if tecla[pygame.K_LEFT]:
             personaje.Detenerse()
             scroll = False
#------------------------------------------------------------------------------------------------------------------------------------------------
       Puntos = FuenteEstadisticas.render("PUNTAJE = " + str(Puntaje), True, verde)

       ColisionBalasZombies = pygame.sprite.groupcollide(DisparosGrupo, personaje.posicionzombie.ListaZombies, True, True)
       for zombie in ColisionBalasZombies:
          print "+100 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          zombie.kill()
          Puntaje += 100
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasFantasmas = pygame.sprite.groupcollide(DisparosGrupo, personaje.posicionfantasma.ListaFantasmas, True, True)
       for fantasma in ColisionBalasFantasmas:
          print "+200 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          fantasma.kill()
          Puntaje += 200
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionBalasDragones = pygame.sprite.groupcollide(DisparosGrupo, personaje.posiciondragon.ListaDragones, True, True)
       for dragon in ColisionBalasDragones:
          print "+300 Puntos"
          sounds.Salto.stop()
          sounds.Destruido.play()
          dragon.kill()
          Puntaje += 300
#------------------------------------------------------------------------------------------------------------------------------------------------
       Vidas = FuenteEstadisticas.render("VIDAS = " + str(CantidadVidas), True, rojooscuro)

       ColisionModificableVidas = pygame.sprite.spritecollide(personaje, personaje.posicionvida.ListaVidas, False)
       for vida in ColisionModificableVidas:
          print "+1 Vida"
          sounds.Salto.stop()
          sounds.MasVida.play()
          vida.kill()
          CantidadVidas += 1
#------------------------------------------------------------------------------------------------------------------------------------------------
       if personaje.DibujoInvencible==True:
          ColisionPersonajeZombie = pygame.sprite.spritecollide(personaje, personaje.posicionzombie.ListaZombies, False)
          for zombie in ColisionPersonajeZombie:
             print "+100 Puntos"
             sounds.Salto.stop()
             sounds.Destruido.play()
             zombie.kill()
             Puntaje += 100

       else:
          ColisionPersonajeZombie = pygame.sprite.spritecollide(personaje, personaje.posicionzombie.ListaZombies, False)
          for zombie in ColisionPersonajeZombie:
             print "-1 Vida"
             sounds.Salto.stop()
             sounds.VidaMenos.play()
             if CantidadVidas == 0:
                CantidadVidas = 0
                print "GAME OVER"
                FinGameOver = True
                zombie.kill()
                personaje.kill()
                EliminarDisparo = True
                PausaTiempo = True
                sounds.GameOver.play(-1)
             else:
                CantidadVidas -= 1
                zombie.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       if personaje.DibujoInvencible==True:
          ColisionPersonajeFantasma = pygame.sprite.spritecollide(personaje, personaje.posicionfantasma.ListaFantasmas, False)
          for fantasma in ColisionPersonajeFantasma:
             print "+200 Puntos"
             sounds.Salto.stop()
             sounds.Destruido.play()
             fantasma.kill()
             Puntaje += 200

       else:
          ColisionPersonajeFantasma = pygame.sprite.spritecollide(personaje, personaje.posicionfantasma.ListaFantasmas, False)
          for fantasma in ColisionPersonajeFantasma:
             print "-1 Vida"
             sounds.Salto.stop()
             sounds.VidaMenos.play()
             if CantidadVidas == 0:
                CantidadVidas = 0
                print "GAME OVER"
                FinGameOver = True
                fantasma.kill()
                personaje.kill()
                EliminarDisparo = True
                PausaTiempo = True
                sounds.GameOver.play(-1)
             else:
                CantidadVidas -= 1
                fantasma.kill()     
#------------------------------------------------------------------------------------------------------------------------------------------------
       if personaje.DibujoInvencible==True:
          ColisionPersonajeDragon = pygame.sprite.spritecollide(personaje, personaje.posiciondragon.ListaDragones, False)
          for dragon in ColisionPersonajeDragon:
             print "+300 Puntos"
             sounds.Salto.stop()
             sounds.Destruido.play()
             dragon.kill()
             Puntaje += 300

       else:
          ColisionPersonajeDragon = pygame.sprite.spritecollide(personaje, personaje.posiciondragon.ListaDragones, False)
          for dragon in ColisionPersonajeDragon:
             print "-1 Vida"
             sounds.Salto.stop()
             sounds.VidaMenos.play()
             if CantidadVidas == 0:
                CantidadVidas = 0
                print "GAME OVER"
                FinGameOver = True
                dragon.kill()
                personaje.kill()
                EliminarDisparo = True
                PausaTiempo = True
                sounds.GameOver.play(-1)
             else:
                CantidadVidas -= 1
                dragon.kill()
#------------------------------------------------------------------------------------------------------------------------------------------------
       Balas = FuenteEstadisticas.render("CARTAS = " + str(CantidadBalas), True, gris)
       ColisionModificableBalas = pygame.sprite.spritecollide(personaje, personaje.posicionbala.ListaBalas, False)
       for bala in ColisionModificableBalas:
          print "+5 Balas"
          sounds.Salto.stop()
          sounds.MasBala.play()
          bala.kill()
          CantidadBalas += 5
#------------------------------------------------------------------------------------------------------------------------------------------------
       Monedas = FuenteEstadisticas.render("MONEDAS = " + str(CantidadMonedas), True, morado)
       ColisionMonedas = pygame.sprite.spritecollide(personaje, personaje.posicionmoneda.ListaMonedas, False)
       for moneda in ColisionMonedas:
          print "+1 Moneda"
          sounds.Salto.stop()
          sounds.MasMoneda.play()
          moneda.kill()
          CantidadMonedas += 1
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionModificableInvencibles = pygame.sprite.spritecollide(personaje, personaje.posicioninvencible.ListaInvencibles, False)
       for invencible in ColisionModificableInvencibles:
          print "Invencible"
          invencible.kill()
          personaje.DibujoInvencible = True

       if personaje.DibujoInvencible==True:
          tiempo=pygame.time.get_ticks()/4000
          if tiempo == 12:
            personaje.DibujoInvencible=False
#------------------------------------------------------------------------------------------------------------------------------------------------
       ColisionMeta = pygame.sprite.spritecollide(personaje, personaje.posicionmeta.ListaMeta, False)
       for meta in ColisionMeta:
          print "META, FIN DE NIVEL"
          FinMeta = True
          personaje.kill()
          meta.kill()
          EliminarDisparo = True
          PausaTiempo = True
          sounds.Meta.play()
#------------------------------------------------------------------------------------------------------------------------------------------------
       Tiempo = FuenteEstadisticas.render("TIEMPO = ", True, blanco)

       if CambioNivel2 == True:
          j=2
          personaje.nivel = DibujoPlataformas2
          personaje.posicionmeta = DibujoMeta2
          personaje.posicionvida = DibujoVidas2
          personaje.posicionbala = DibujoBalas2
          ListaSpritesActivos.add(personaje)
          FondoAnimadoGrupo2.update()
          FondoAnimadoGrupo2.draw(pantalla)
          DibujoPlataformas2.update()
          DibujoPlataformas2.draw(pantalla)
          DibujoZombies2.update()
          DibujoZombies2.draw(pantalla)
          DibujoFantasmas2.update()
          DibujoFantasmas2.draw(pantalla)
          DibujoDragones2.update()
          DibujoDragones2.draw(pantalla)
          DibujoMeta2.update()
          DibujoMeta2.draw(pantalla)
          DibujoVidas2.update()
          DibujoVidas2.draw(pantalla)
          DibujoBalas2.update()
          DibujoBalas2.draw(pantalla)
          DibujoInvencibles.update()
          DibujoInvencibles.draw(pantalla)
          
       else:
          FondoAnimadoGrupo.update()
          FondoAnimadoGrupo.draw(pantalla)
          DibujoPlataformas.update()
          DibujoPlataformas.draw(pantalla)
          DibujoMonedas.update()
          DibujoMonedas.draw(pantalla)
          DibujoZombies.update()
          DibujoZombies.draw(pantalla)
          DibujoFantasmas.update()
          DibujoFantasmas.draw(pantalla)
          DibujoDragones.update()
          DibujoDragones.draw(pantalla)
          DibujoVidas.update()
          DibujoVidas.draw(pantalla)
          DibujoBalas.update()
          DibujoBalas.draw(pantalla)
          DibujoInvencibles.update()
          DibujoInvencibles.draw(pantalla)
          DibujoMeta.update()
          DibujoMeta.draw(pantalla)

       if personaje.rect.right > ANCHO:
          personaje.rect.right = ANCHO
       if personaje.rect.left < 0:
          personaje.rect.left = 0

       ListaSpritesActivos.update()
       ListaSpritesActivos.draw(pantalla)
       DisparosGrupo.update()
       DisparosGrupo.draw(pantalla)

       pantalla.blit(Seleccion,(4,4))
       pantalla.blit(IconoVidas,(4,54))
       pantalla.blit(IconoBalas,(4,104))
       IconoAnimadoMonedas()
       pantalla.blit(IconoMoneda,(4,154),ImagenMoneda[cual1])
       pantalla.blit(IconoReloj,(1045,4))
       pantalla.blit(Puntos,(59,8))
       pantalla.blit(Vidas,(59,54))
       pantalla.blit(Balas,(59,104))
       pantalla.blit(Monedas,(59,154))
       pantalla.blit(Tiempo,(1100,13))

       if FinGameOver == True or CantidadVidas == 0:
          personaje.kill()
          pygame.mixer.music.stop()
          sounds.GameOver.play(-1)
          pantalla.blit(FondoGameOver,(200,100))
          pantalla.blit(EsqueletoGameOver,(800,50))
          MovimientoGameOver()
          pantalla.blit(TextoGameOver,(pos6,280))
          MovimientoPresioneEspacioGameOver()
          pantalla.blit(TextoPresioneEspacioGameOver,(400,pos15))
          if tecla[pygame.K_SPACE]:
             sounds.GameOver.stop()
             pygame.mixer.music.load('Sonidos/PiratasDelCaribe.wav')
             pygame.mixer.music.play(-1)
             salir = True

       if FinMeta == True:
          #pygame.mixer.music.stop()
          pantalla.blit(FondoMensajeMeta,(200,100))
          pantalla.blit(PersonajeMeta,(350,450))
          pantalla.blit(CalaveraMeta,(600,50))
          MovimientoMision1Completa()
          if j == 1:
            #pantalla.blit(TextoMision1Completa,(pos13,340))
            #MovimientoPresioneEspacioMeta()
            pantalla.blit(TextoPresioneEspacioMeta,(640,310))
            pantalla.blit(TextoPresioneEspacioMeta1,(280,370))
          
          if j == 2:
            personaje.kill()
            #pygame.mixer.music.stop()
            FondoInstrucciones = pygame.image.load('Imagenes/FondoInstrucciones1.png').convert()
            pantalla.blit(FondoInstrucciones,(0,0))
            fuente3 = pygame.font.Font('Fuentes/Zombified.ttf', 60)
            intro1 = fuente3.render("         FELICIDADES...         ", 1, (verde))
            intro2 = fuente3.render("        EXTERMINASTE A          ", 1, (morado))
            intro21 = fuente3.render("         LOS ZOMBIES           ", 1, (morado))
            intro3 = fuente3.render("         GRACIAS A TI           ", 1, (morado))
            intro4 = fuente3.render("       TODA LA HUMANIDAD        ", 1, (morado))
            intro5 = fuente3.render("      EVOLUCIONARA DE NUEVO     ", 1, (morado))
            pantalla.blit(FondoInstrucciones,(0,0))
            pantalla.blit(intro1,(280,200))
            pantalla.blit(intro2,(280,250))
            pantalla.blit(intro21,(280,300))
            pantalla.blit(intro3,(280,350))
            pantalla.blit(intro4,(280,400))
            pantalla.blit(intro5,(280,450))
            if tecla[pygame.K_ESCAPE] or tecla[pygame.K_SPACE]:
              sounds.GameOver.stop()
              pygame.mixer.music.load('Sonidos/PiratasDelCaribe.wav')
              pygame.mixer.music.play(-1)
              salir = True
          
          if tecla[pygame.K_SPACE]:
             salir = True

       TiempoJuego()
       cadena=ConcatenacionTiempo(deceMin,unidMin,deceSeg,unidSeg,centSeg)
       textoTiempo.render(pantalla, cadena, blanco, (1230, 8))

       pygame.display.update()    
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
def Instrucciones():
    salir = False
    FondoInstrucciones = pygame.image.load('Imagenes/FondoInstrucciones.png').convert()
    fuente = pygame.font.Font('Fuentes/Zombified.ttf', 80)
    fuente2 = pygame.font.Font('Fuentes/Zombified.ttf', 30)
    Titulo = fuente.render("EL GUASON", 1, (dorado))
    Avanzar = fuente2.render("Avanzar", 1, (morado))
    Retroceder = fuente2.render("Retroceder", 1, (morado))
    Saltar = fuente2.render("Saltar", 1, (morado))
    Agacharse = fuente2.render("Mover", 1, (morado))
    Disparar = fuente2.render("Disparar", 1, (morado))
    Pausar = fuente2.render("Pausar", 1, (morado))
    VolverAlMenu = fuente2.render("Volver al Menu", 1, (verde))
    Vida = fuente2.render("+1 Vida", 1, (verde))
    Velocidad = fuente2.render("+ Velocidad", 1, (verde))
    Escudo = fuente2.render("Invencible", 1, (verde))
    Moneda = fuente2.render("+1 Moneda", 1, (verde))
    Balas = fuente2.render("+10 Balas", 1, (verde))
    pantalla.blit(FondoInstrucciones,(0,0))
    pantalla.blit(Titulo,(500,120))
    #pantalla.blit(Avanzar,(403,570))
    #pantalla.blit(Retroceder,(160,570))
    #pantalla.blit(Saltar,(310,500))
    pantalla.blit(Agacharse,(666,512))
    pantalla.blit(Disparar,(372,510))
    pantalla.blit(Pausar,(227,382))
    pantalla.blit(Vida,(117,637))
    #pantalla.blit(Velocidad,(440,650))
    pantalla.blit(Escudo,(255,637))
    pantalla.blit(Moneda,(417,637))
    pantalla.blit(Balas,(597,637))

    while salir != True:
       tecla = pygame.key.get_pressed()   
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             salir = True
          if tecla[pygame.K_ESCAPE]:
             print "REGRESAR AL MENU"
             salir = True
       pygame.display.flip()

#------------------------------------------------------------------------------------------------------------------------------------------------
def Creditos():
    salir = False
    FondoCreditos = pygame.image.load('Imagenes/FondoCreditos.png').convert()
    LogoUniversidad = pygame.image.load('Imagenes/LogoUniversidad.png').convert_alpha()
    #Computador = pygame.image.load('Computador1.png').convert_alpha()
    fuente = pygame.font.Font('Fuentes/Zombified.ttf', 80)
    fuente2 = pygame.font.Font('Fuentes/Zombified.ttf', 50)
    fuente3 = pygame.font.Font('Fuentes/Zombified.ttf', 50)
    Titulo = fuente.render("EL GUASON", 1, (dorado))
    ComputacionGrafica = fuente2.render("COMPUTACION GRAFICA", 1, (verde))
    Nombre1 = fuente3.render("Alejandro Escobar", 1, (morado))
    Nombre2 = fuente3.render("Richard Murillo", 1, (morado))
    Nombre3 = fuente3.render("Mateo Castro", 1, (morado))
    while salir != True:
       reloj.tick(60) 
       tecla = pygame.key.get_pressed()   
       for event in pygame.event.get():
          if event.type == pygame.QUIT:
             salir = True
          if tecla[pygame.K_ESCAPE]:
             print "REGRESAR AL MENU"
             salir = True
       pantalla.blit(FondoCreditos,(0,0))
       pantalla.blit(Titulo,(500,120))
       MovimientoLogoUniversidad()
       pantalla.blit(LogoUniversidad,(pos8,500))
       MovimientoComputador()
       #pantalla.blit(Computador,(pos9,500))
       MovimientoComputacionGrafica()
       pantalla.blit(ComputacionGrafica,(300,pos10))
       MovimientoNombre1()
       pantalla.blit(Nombre1,(800,pos11))
       MovimientoNombre2()
       pantalla.blit(Nombre2,(800,pos12))
       MovimientoNombre3()
       pantalla.blit(Nombre3,(800,pos22))
       pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------------
# Menu Inicial
def Menu(opcion):
    Fondo = pygame.image.load('Imagenes/FondoMenu.jpg').convert()
    Personaje = pygame.image.load('Imagenes/PersonajeMenu.png').convert_alpha()
    Seleccion = pygame.image.load('Imagenes/Seleccion.png').convert_alpha() 
    fuente = pygame.font.Font('Fuentes/Zombified.ttf', 80)
    Titulo = fuente.render("EL GUASON", 1, (dorado))
    pantalla.blit(Fondo,(0,0))
    pantalla.blit(Personaje,(400,500))
    #MovimientoTitulo()
    pantalla.blit(Titulo,(500,120))
    MovimientoCalavera()
    if opcion == 1:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",900,540,(verde))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",900,590,(morado))
       Historia,opcion3=TextoMenu("HISTORIA",900,640,(morado))
       Creditos,opcion4 = TextoMenu("CREDITOS",900,690,(morado))
       Salir,opcion5 = TextoMenu("SALIR",900,740,(morado))
       pantalla.blit(Seleccion,(MenuX+260,MenuY+35))
    if opcion == 2:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",900,540,(morado))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",900,590,(verde))
       Historia,opcion3=TextoMenu("HISTORIA",900,640,(morado))
       Creditos,opcion4 = TextoMenu("CREDITOS",900,690,(morado))
       Salir,opcion5 = TextoMenu("SALIR", 900, 740,(morado))
       pantalla.blit(Seleccion,(MenuX+245,MenuY+45))
    if opcion == 3:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",900,540,(morado))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",900,590,(morado))
       Historia,opcion3=TextoMenu("HISTORIA",900,640,(verde))
       Creditos,opcion4 = TextoMenu("CREDITOS",900,690,(morado))
       Salir,opcion5 = TextoMenu("SALIR", 900, 740,(morado))
       pantalla.blit(Seleccion,(MenuX+320,MenuY+55))
    if opcion == 4:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",900,540,(morado))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",900,590,(morado))
       Historia,opcion3=TextoMenu("HISTORIA",900,640,(morado))
       Creditos,opcion4 = TextoMenu("CREDITOS",900,690,(verde))
       Salir,opcion5 = TextoMenu("SALIR", 900, 740,(morado))
       pantalla.blit(Seleccion,(MenuX+320,MenuY+65))  
    if opcion == 5:
       IniciarJuego,opcion1 = TextoMenu("INICIAR  JUEGO",900,540,(morado))
       Instrucciones,opcion2 = TextoMenu("INSTRUCCIONES",900,590,(morado))
       Historia,opcion3=TextoMenu("HISTORIA",900,640,(morado))
       Creditos,opcion4 = TextoMenu("CREDITOS",900,690,(morado))
       Salir,opcion5 = TextoMenu("SALIR", 900, 740,(verde))
       pantalla.blit(Seleccion,(MenuX+360,MenuY+75))
    pantalla.blit(IniciarJuego,opcion1)
    pantalla.blit(Instrucciones,opcion2)
    pantalla.blit(Historia,opcion3)
    pantalla.blit(Creditos,opcion4)
    pantalla.blit(Salir,opcion5)
#------------------------------------------------------------------------------------------------------------------------------------------------
def Historia():
    salir = False
    FondoInstrucciones = pygame.image.load('Imagenes/FondoMenu1.png').convert()
    pantalla.blit(FondoInstrucciones,(0,0))
    Personaje = pygame.image.load('Imagenes/PersonajeMenu.png').convert_alpha()
    Invencible = pygame.image.load("Imagenes/Invencible.png")
    EsqueletoGameOver = pygame.image.load('Imagenes/EsqueletoGameOver.png').convert_alpha()
    IconoVidas = pygame.image.load('Imagenes/Vidas.png').convert_alpha()
    IconoBalas = pygame.image.load('Imagenes/Balas.png').convert_alpha()
    fuente = pygame.font.Font('Fuentes/Zombified.ttf', 80)
    fuente3 = pygame.font.Font('Fuentes/Zombified.ttf', 40)
    Titulo = fuente.render("EL GUASON", 1, (dorado))
    w1 = fuente3.render("Bienvenido al modo historia de EL GUASON, ", 1, (verde))
    w2 = fuente3.render("aqui conoceras mas de este apasionante juego", 1, (verde))
    pantalla.blit(Titulo,(500,120))
    pantalla.blit(w1,(190,200))
    pantalla.blit(w2,(190,250))
    
    while salir != True:
       tecla = pygame.key.get_pressed()   
       for event in pygame.event.get():
          if tecla[pygame.K_RIGHT]:
                  pantalla.blit(FondoInstrucciones,(0,0))
                  fuente3 = pygame.font.Font('Fuentes/Zombified.ttf', 50)
                  intro1 = fuente3.render("El Guason ha cambiado,", 1, (morado))
                  intro2 = fuente3.render("ha mutado y ahora es mas grande",1,(morado))
                  intro3 = fuente3.render("y fuerte que todos los superheroes," , 1, (morado))
                  intro4 = fuente3.render("no le cuesta trabajo derrotarlos y asi" , 1, (morado))
                  intro5 = fuente3.render("se puede observar que el mal ha triunfado " , 1, (morado))
                  intro6 = fuente3.render("Pero aun queda algo de esperanza, aunque " , 1, (morado))
                  intro7 = fuente3.render("derrote todos los superheroes, el solo " , 1, (morado))
                  intro8 = fuente3.render("quiere estar con su Harley Quinn" , 1, (morado))
                  intro9 = fuente3.render("y que sean muy felices" , 1, (morado))
                  
                  pantalla.blit(Titulo,(500,120))
                  pantalla.blit(intro1,(70,200))
                  pantalla.blit(intro2,(70,250))
                  pantalla.blit(intro3,(70,300))
                  pantalla.blit(intro4,(70,350))
                  pantalla.blit(intro5,(70,400))
                  pantalla.blit(intro6,(70,500))
                  pantalla.blit(intro7,(70,550))
                  pantalla.blit(intro8,(70,600))
                  pantalla.blit(intro9,(70,650))

          if tecla[pygame.K_ESCAPE]:
             print "REGRESAR AL MENU"
             salir = True
       pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------------
def MenuPausa(OpcionMenuPausa):
    SeleccionPausa = pygame.image.load('Imagenes/Seleccion.png').convert_alpha() 
    FondoMenuPausa = pygame.image.load('Imagenes/FondoMenuPausa.png').convert_alpha()
    pantalla.blit(FondoMenuPausa,(200,100))
    if OpcionMenuPausa == 1:
       ReanudarJuego,OpcionMenuPausa1 = TextoMenuPausa("REANUDAR JUEGO",710,300,(verde))
       VolverMenuPrincipal,OpcionMenuPausa2 = TextoMenuPausa("VOLVER AL MENU PRINCIPAL",710,370,(morado))
       SalirEscritorio,OpcionMenuPausa3 = TextoMenuPausa("SALIR AL ESCRITORIO",710,440,(morado))
       #pantalla.blit(SeleccionPausa,(MenuX+90,MenuY-205))
    if OpcionMenuPausa == 2:
       ReanudarJuego,OpcionMenuPausa1 = TextoMenuPausa("REANUDAR JUEGO",710,300,(morado))
       VolverMenuPrincipal,OpcionMenuPausa2 = TextoMenuPausa("VOLVER AL MENU PRINCIPAL",710,370,(verde))
       SalirEscritorio,OpcionMenuPausa3 = TextoMenuPausa("SALIR AL ESCRITORIO", 710, 440,(morado))
       #pantalla.blit(SeleccionPausa,(MenuX-2,MenuY-133))
    if OpcionMenuPausa == 3:
       ReanudarJuego,OpcionMenuPausa1 = TextoMenuPausa("REANUDAR JUEGO",710,300,(morado))
       VolverMenuPrincipal,OpcionMenuPausa2 = TextoMenuPausa("VOLVER AL MENU PRINCIPAL",710,370,(morado))
       SalirEscritorio,OpcionMenuPausa3 = TextoMenuPausa("SALIR AL ESCRITORIO", 710, 440,(verde))
       #pantalla.blit(SeleccionPausa,(MenuX+55,MenuY-62))
    pantalla.blit(ReanudarJuego,OpcionMenuPausa1)
    pantalla.blit(VolverMenuPrincipal,OpcionMenuPausa2)
    pantalla.blit(SalirEscritorio,OpcionMenuPausa3)
#------------------------------------------------------------------------------------------------------------------------------------------------
opcion = 1
while salir != True:
    reloj.tick(60) 
    tecla = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salir = True
        if tecla[pygame.K_s]:
	    sys.exit()
        if tecla[pygame.K_UP] and opcion > 1 and MenuY > DimensionMenu[1]:
            sounds.OpcionMenu.play()
            opcion -= 1
            MenuY = MenuY-40
            Seleccion
        if tecla[pygame.K_DOWN] and opcion < 5 and MenuY > DimensionMenu[0]:
            sounds.OpcionMenu.play()
            opcion += 1
            MenuY = MenuY+40
            Seleccion
	if tecla[K_RETURN]:
	    if opcion == 1:
	       print "ACCEDER AL JUEGO"
               sounds.EnterMenu.play()
               IniciarJuego()
               ReiniciarTiempo = True
	    if opcion == 2:
               print "ACCEDER A LAS INSTRUCCIONES"
               sounds.EnterMenu.play()
               Instrucciones()
	    if opcion==3:
	       print "ACCEDER A HISTORIA"
	       sounds.EnterMenu.play()
	       Historia()
	    if opcion == 4:
               print "ACCEDER A LOS CREDITOS"
               sounds.EnterMenu.play()
               Creditos()
	    if opcion == 5:
	       sys.exit()
    Menu(opcion)
    pygame.display.flip()
pygame.quit()

