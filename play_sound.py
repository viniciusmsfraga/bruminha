import pygame
pygame.mixer.init()
pygame.mixer.music.load("/home/pi/0564.ogg")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
        continue
