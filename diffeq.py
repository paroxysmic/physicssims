import pygame as py
import random
from pygame import Vector2 as vec2
win = py.display.set_mode((500, 500))
running, playing = True, True
OWHITE = 0xDDDDDD
clock = py.time.Clock()
def scrtup(ip: vec2):
    return (ip.x + 250, 250 - ip.y)
def arrow(ip: vec2, ep : vec2, color):
    py.draw.line(win, color, scrtup(ip), scrtup(ep))
    arrvec = (ep - ip).normalize() * min(20, (ep - ip).length()/4)
    py.draw.polygon(win, color, [scrtup(ep), scrtup(ep + arrvec.rotate(150)), scrtup(ep + arrvec.rotate(-150))])
def ode(ip: vec2):
    return vec2(10, ip.y * -0.3)
while running:
    clock.tick(60)
    events = py.event.get()
    keys = py.key.get_pressed()
    mpos = py.mouse.get_pos()
    for event in events:
        if event.type == py.QUIT:
            running = False
    if keys[py.K_q]:
        running = False
    win.fill(OWHITE)
    for i in range(21):
        for j in range(21):
            tvec = vec2(25 * (i - 11), 25 * (j - 11))
            col = ode(tvec).length()
            arrow(tvec, tvec + ode(tvec), (col * 3.06, col * 2.01, col))
    py.display.update()