import pygame as py
from math import *
import random
from pygame import Vector2 as vec2
py.init()
win = py.display.set_mode((800, 800))
running, playing = True, True
OWHITE = 0xDDDDDD
HEIGHT, WIDTH = 10, 10
PIXH, PIXW = 800 / HEIGHT, 800 / WIDTH
AREA = HEIGHT * WIDTH
epoch = 0
clock = py.time.Clock()
def scrtup(ip: vec2):
    return (ip.x + 250, 250 - ip.y)
def arrow(ip: vec2, ep: vec2, color):
    py.draw.line(win, color, ip, ep)
    if((ep - ip) != vec2(0, 0)):
        arrvec = (ep - ip).normalize() * min(20, (ep - ip).length()/4)
        py.draw.polygon(win, color, [ep, ep + arrvec.rotate(150), ep + arrvec.rotate(-150)]) 
def drawGrid():
    for y in range(HEIGHT + 1):
        for x in range(WIDTH + 1):
            py.draw.circle(win, 0x222222, (x * PIXW, y * PIXH), 5)
    for y in range(HEIGHT + 1):
        py.draw.line(win, 0x222222, (0, y * PIXH), (800, y * PIXH))
    for x in range(WIDTH + 1):
        py.draw.line(win, 0x222222, (x * PIXW, 0), (x * PIXW, 800))  
vertvecs = [20 for i in range(AREA - WIDTH)]
horizvecs = [20 for i in range(AREA - HEIGHT)]
def getDiv(x, y):
    ind = x + y * WIDTH
    d = 0
    if(y != 0):
        d -= vertvecs[ind - WIDTH]
    if(x != 0):
        d -= horizvecs[ind - y - 1]
    if(y != HEIGHT - 1):
        d += vertvecs[ind]
    if(x != WIDTH - 1):
        d += horizvecs[ind - y]
    return d
def balanceInflow(iters):
    for λ in range(iters):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                ind = x + y * WIDTH
                p = sum(map(int, (y != 0, x != 0, y != HEIGHT - 1, x != WIDTH - 1)))
                d = getDiv(x, y)
                if(y != 0):
                    vertvecs[ind - WIDTH] += d / p
                if(x != 0):
                    horizvecs[ind - y - 1] += d / p
                if(y != HEIGHT - 1):
                    vertvecs[ind] -= d / p
                if(x != WIDTH - 1):
                    horizvecs[ind - y] -= d / p
def horizVecPos(x, y):
    return (x + 1) * PIXW, (y + 0.5) * PIXH
def vertiVecPos(x, y):
    return (x + 0.5) * PIXW, (y + 1) * PIXH
def genVelocity(x, y):
    #ci - closest interstion, cc - closest centre
    cix = (x + PIXW / 2) // PIXW
    ciy = (y + PIXH / 2) // PIXH
    ccx = x // PIXW
    ccy = y // PIXH
    #lvv - legal vert vecs, lhv - legal horiz vecs
    lvv = [cix != 0 and ccy != 0, cix != WIDTH and ccy != 0, cix != 0 and ccy != HEIGHT - 1, cix != WIDTH and ccy != HEIGHT - 1]
    lhv = [ccx != 0 and ciy != 0, ccx != WIDTH - 1 and ciy != 0, ccx != 0 and ciy != HEIGHT, ccx != WIDTH - 1 and ciy != HEIGHT]
    #cvv - core vertical vec, chv - core horizontal vec
    cvv = (ccx, ciy - 1)
    chv = (cix - 1, ccy)
    #wshv - weighted sum of horizontal vecs, wsvv - weighted sum of vertical vecs
    wshv = vec2(0, 0)
    wsvv = vec2(0, 0)
    if(lvv[0]):
        scal = (abs(x - ccx) * abs(y - ccy) / (PIXW * PIXH))
        wsvv += scal * (vertvecs[chv[0] + WIDTH * (chv[1])])
    
while running:
    clock.tick(60)
    epoch += 0.01
    events = py.event.get()
    keys = py.key.get_pressed()
    mpos = py.mouse.get_pos()
    for event in events:
        if event.type == py.QUIT:
            running = False
    if keys[py.K_q]:
        running = False
    if keys[py.K_i]:
        for i in range(len(horizvecs)):
            horizvecs[i] = random.random() * 200 - 100
            vertvecs[i] = random.random() * 200 - 100
        horsum = sum(horizvecs)
        versum = sum(vertvecs)
        avgsum = horsum + versum
        for i in range(len(horizvecs)):
            horizvecs[i] -= avgsum / len(horizvecs)
            vertvecs[i] -= avgsum / len(horizvecs)
    balanceInflow(1)
    win.fill(OWHITE)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            ind = x + y * WIDTH
            div = getDiv(x, y)
            div = int(min(20, max(-20, div))) + 20
            py.draw.rect(win, 0x060000 * div + 0x0000ff, (y * PIXH - 1, x * PIXW - 1, PIXH - 2, PIXW - 2))
    for y in range(HEIGHT - 1):
        for x in range(WIDTH):
            pos = vec2((x + 0.5) * PIXW, (y + 1) * PIXH)
            spos = vec2((x + 0.5) * PIXW, (y + 1) * PIXH + vertvecs[x + y * WIDTH])
            arrow(pos, spos, 0xff0000)
    for y in range(HEIGHT):
        for x in range(WIDTH - 1):
            pos = vec2((x + 1) * PIXW, (y + 0.5) * PIXH)
            spos = vec2((x + 1) * PIXW + horizvecs[x + y * (WIDTH - 1)], (y + 0.5) * PIXH)
            arrow(pos, spos, 0x00ff00)
    genVelocity(mpos[0], mpos[1])
    py.display.update()