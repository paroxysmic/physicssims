import pygame as py
from math import *
import random
from pygame import Vector2 as vec2
py.init()
win = py.display.set_mode((800, 800))
running, playing = True, True
OWHITE = 0xDDDDDD
HEIGHT, WIDTH = 20, 20
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
vertvecs = [0 for i in range(AREA - WIDTH)]
horizvecs = [0 for i in range(AREA - HEIGHT)]
ihat, jhat = vec2(1, 0), vec2(0, 1)
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
    cix = int((x + PIXW / 2) // PIXW) 
    ciy = int((y + PIXH / 2) // PIXH)
    ccx = int(x // PIXW)
    ccy = int(y // PIXH)
    #lvv - legal vert vecs, lhv - legal horiz vecs
    lvv = [cix != 0 and ccy != 0, cix != WIDTH and ccy != 0, cix != 0 and ccy != HEIGHT - 1, cix != WIDTH and ccy != HEIGHT - 1]
    lhv = [ccx != 0 and ciy != 0, ccx != WIDTH - 1 and ciy != 0, ccx != 0 and ciy != HEIGHT, ccx != WIDTH - 1 and ciy != HEIGHT]
    #cvv - core verti vec, chv - core horiz vec
    cvv = (ccx, ciy - 1)
    chv = (cix - 1, ccy)
    #wshv - weighted sum of horiz vecs, wsvv - weighted sum of verti vecs
    #NOTE: both of these are scalars!!!
    wshv = 0
    wsvv = 0
    #ulvv - upper left verti vec, ulhv - upper left horiz vec
    ulhv = (ccx * PIXW, (ciy - 0.5) * PIXH)
    ulvv = ((cix - 0.5) * PIXW, ccy * PIXH)
    #hsfs - horiz scalar factors, vsfs - verti scalar factors (for the weighting)
    hsfs = [(x - ulhv[0]) * (y - ulhv[1]), (PIXW + ulhv[0] - x) * (y - ulhv[1]),
            (x - ulhv[0]) * (PIXH + ulhv[1] - y), (PIXW + ulhv[0] - x) * (PIXH + ulhv[1] - y)]
    vsfs = [(x - ulvv[0]) * (y - ulvv[1]), (PIXW + ulvv[0] - x) * (y - ulvv[1]),
            (x - ulvv[0]) * (PIXH + ulvv[1] - y), (PIXW + ulvv[0] - x) * (PIXH + ulvv[1] - y)]
    hsfs = [num / (PIXW * PIXH) for num in hsfs]
    vsfs = [num / (PIXW * PIXH) for num in vsfs]
    if(lvv[0]):
        wsvv += (vsfs[0] * vertvecs[chv[0] + (chv[1] - 1) * WIDTH])
    if(lvv[1]):
        wsvv += (vsfs[1] * vertvecs[(chv[0] + 1) + ((chv[1] - 1) * WIDTH)])
    if(lvv[2]):
        wsvv += (vsfs[2] * vertvecs[chv[0] + chv[1] * WIDTH])
    if(lvv[3]):
        wsvv += (vsfs[3] * vertvecs[(chv[0] + 1) + chv[1] * WIDTH])
    if(lhv[0]):
        wshv += (hsfs[0] * horizvecs[(cvv[0] - 1) + (cvv[1] * (WIDTH - 1))])
    if(lhv[1]):
        wshv += (hsfs[1] * horizvecs[cvv[0] + (cvv[1] * (WIDTH - 1))])
    if(lhv[2]):
        wshv += (hsfs[2] * horizvecs[(cvv[0] - 1) + ((cvv[1] + 1) * (WIDTH - 1))])
    if(lhv[3]):
        wshv += (hsfs[3] * horizvecs[cvv[0] + ((cvv[1] + 1) * (WIDTH - 1))])        
    return (wshv, wsvv)
bposs = [[(i / 3) * PIXW, (j / 3) * PIXH] for i in range(WIDTH * 3) for j in range(HEIGHT * 3)]
while running:
    clock.tick(60)
    epoch += 0.01
    events = py.event.get()
    keys = py.key.get_pressed()
    mpos = py.mouse.get_pos()
    for event in events:
        if event.type == py.QUIT:
            running = False
        if event.type == py.MOUSEBUTTONDOWN:
            bposs.append([mpos[0], mpos[1]])
    if keys[py.K_q]:
        running = False
    if keys[py.K_i]:
        for i in range(len(horizvecs)):
            horizvecs[i] = random.random() * 60 - 30
        for i in range(len(vertvecs)):
            vertvecs[i] = random.random() * 60 - 30
        horsum = sum(horizvecs)
        versum = sum(vertvecs)
        avgsum = horsum + versum
        for i in range(len(horizvecs)):
            horizvecs[i] -= avgsum / len(horizvecs)
        for i in range(len(vertvecs)):
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
    bposs = [pos for pos in bposs if (pos[0] > 0 and pos[0] < 800 and pos[1] > 0 and pos[1] < 800)]
    for pos in bposs:
        vel = genVelocity(pos[0], pos[1])
        pos[0] += vel[0] * 0.4
        pos[1] += vel[1] * 0.4
        py.draw.circle(win, 0x000000, (pos[0], pos[1]), 5)
    py.display.update()