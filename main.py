import pygame
import numpy as np
import pygame.gfxdraw
from pygame.locals import (
    Rect,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    K_RETURN,
    K_SPACE,
    QUIT,
    K_s,
    K_r,
    K_a,
)
from vortex import Vortex
from colors import standard, black, white


def createVortex(pos, circulation):
    vortexArray.append(Vortex(pos, circulation))


# Drawing functions


def drawPoint(position, color=standard, r=8):
    x, y = np.round(position).astype(int)
    s = np.round(r / 2).astype(int)
    pygame.gfxdraw.filled_circle(screen, x - s, y - s, r, color)
    pygame.gfxdraw.aacircle(screen, x - s, y - s, r, color)


def drawVortex(vortex, color=standard, r=8):
    drawPoint(vortex.pos, color, r)


def drawVortices(vortexArray):
    for vortex in vortexArray:
        drawVortex(vortex, vortex.color)


def eraseBottomLeft():
    # Where the play/ pause symbol is
    screen.fill(black, Rect(bottomLeft[0], bottomLeft[1], 50, 50))


def eraseFrame():
    # screen.fill(black)
    pygame.draw.rect(screen, black, screen.get_rect())


def clearFrame(vortexArray):
    # Put the background colour back over all modified vortices.
    if vortexArray:
        for vortex in vortexArray:
            drawVortex(vortex, black)


def updateTitleToNumberOfVortices():
    pygame.display.set_caption(str(len(vortexArray)))


pygame.init()

currentCirculation = 1
accurate = False
# More accurate means the trajectories will actually be correct
# in particular in the 2-vortex different vorticities problem, but it is
# significantly slower. Less accurate means sometimes the trajectories are
# wrong, but the general gist is there.
vortexArray = []
scrapArray = []  # All the vortices set to be destroyed.
open = True
play = False
textMode = False
n = 1

window = pygame.display.set_mode((1800, 1000))
screen = pygame.display.get_surface()
center = screen.get_rect().center

text = ""
font = pygame.font.SysFont("segoeui", 50)
playSymbol = pygame.image.load("play.png")
pauseSymbol = pygame.image.load("pause.png")
bottomLeft = screen.get_rect().bottomleft + np.array((20, -60))


eraseFrame()


while open:
    eraseBottomLeft()
    if not play:
        screen.blit(pauseSymbol, bottomLeft)
    else:
        screen.blit(playSymbol, bottomLeft)
        clearFrame(vortexArray)
        scrapArray = []
        for i in range(n):
            for vortex in vortexArray:
                vortex.computeVelocity(vortexArray)
            for vortex in vortexArray:
                vortex.move(100 / n)  # maintains framerate

                if vortex.outOfBounds():
                    scrapArray.append(vortex)

            for vortex in scrapArray:
                vortexArray.remove(vortex)
                updateTitleToNumberOfVortices()
        drawVortices(vortexArray)

    # Handling user input

    if textMode:
        renderedText = font.render("Circulation: " + text, False, white)
        screen.blit(renderedText, (20, 20))

    for event in pygame.event.get():
        if event.type == QUIT:
            open = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                play = not play
                for vortex in vortexArray:
                    drawVortex(vortex, vortex.color)
            if textMode:
                if event.key == K_RETURN:
                    textMode = False
                    renderedText = font.render(
                        "Circulation: " + text, False, black
                    )

                    screen.blit(renderedText, (20, 20))
                    try:
                        currentCirculation = float(text)
                    except ValueError:
                        currentCirculation = 1
                    text = ""
                else:
                    text += event.unicode
            else:
                if event.key == K_s:
                    textMode = True
                if event.key == K_r:
                    eraseFrame()
                    vortexArray = []
                    updateTitleToNumberOfVortices()
                if event.key == K_a:
                    accurate = not accurate
                    if accurate:
                        n = 20
                    else:
                        n = 1
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:
                if event.button == 1:
                    createVortex(pygame.mouse.get_pos(), currentCirculation)

                if event.button == 3:
                    createVortex(pygame.mouse.get_pos(), -currentCirculation)

                drawVortex(vortexArray[-1], vortexArray[-1].color)
                updateTitleToNumberOfVortices()
    pygame.display.update()
