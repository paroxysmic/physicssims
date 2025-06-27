import pygame as py
import random
from pygame import Vector2 as vec2
win = py.display.set_mode((500, 500))
running, playing = True, True
BLACK, WHITE, RED, BLUE = 0x000000, 0xFFFFFF, 0xff0000, 0x0000FF
OBLACK, OWHITE = 0x222222, 0xDDDDDD
bnum = 20
def collerp(a, b, t):
    red = int(((a >> 16) & 0xff) * (1 - t) + ((b >> 16) & 0xff) * t)
    gre = int(((a >> 8) & 0xff) * (1 - t) + ((b >> 8) & 0xff) * t)
    blu = int((a & 0xff) * (1 - t) + (b & 0xff) * t)
    return (red << 16) + (gre << 8) + blu
class Ball:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.acc = vec2(0, -9.81)
    def updatePos(self):
        self.vel += self.acc * 0.1
        self.pos += (self.vel * 1e-1) + (self.acc * 5e-3)
    def render(self):
        py.draw.circle(win, BLUE, (self.pos.x + 250, 250 - self.pos.y), 5)
    def collHandler(self):
        if self.pos.x > 245 or self.pos.x < -245:
            self.vel.x *= -0.8
            self.vel.y *= 0.8
        if self.pos.y > 245 or self.pos.y < -245:
            self.vel.y *= -0.8
            self.vel.x *= 0.8
        self.pos.x = min(245, max(-245, self.pos.x))
        self.pos.y = min(245, max(-245, self.pos.y))
class Spring:
    def __init__(self, b1: Ball, b2: Ball, deflen):
        self.b1 = b1
        self.b2 = b2
        self.deflen = deflen
        self.currlen = (b1.pos - b2.pos).length()
        self.stress = abs(self.deflen - self.currlen)
    def render(self):
        self.currlen = (self.b1.pos - self.b2.pos).length()
        self.stress = abs(self.deflen - self.currlen)
        if self.currlen != 0:
            sprcol = collerp(BLUE, RED, abs(min(1, max(-1, self.stress / 100))))
            plist = []
            parvec = (self.b1.pos - self.b2.pos)
            travec = parvec.rotate(90).normalize() * 3
            for i in range(1, 12):
                res = self.b2.pos + (parvec * (1/4 + i/24) + travec * (2 * (i % 2) - 1))
                plist.append((250 + res.x, 250 - res.y))
            plist.insert(0, (250 + (parvec * 0.25).x + self.b2.pos.x, 250 - (parvec * 0.25).y - self.b2.pos.y))
            plist.insert(0, (250 + self.b2.pos.x, 250 - self.b2.pos.y))
            plist.append((250 + (parvec * 0.75).x + self.b2.pos.x, 250 - (parvec * 0.75).y - self.b2.pos.y))
            plist.append((250 + self.b1.pos.x, 250 - self.b1.pos.y))
            py.draw.lines(win, sprcol, False, plist, 2)
        self.b1.render()
        self.b2.render()
    def updatePos(self):
        #using hooke's law :)
        parvec = (self.b1.pos - self.b2.pos).normalize()
        self.b1.acc = -parvec * self.stress / 200
        self.b2.acc = parvec * self.stress / 200
        self.b1.updatePos()
        self.b2.updatePos()
        self.b1.collHandler()
        self.b2.collHandler()
blist = [Ball(vec2(i / bnum * 500 - 250, 0), vec2(random.random() * 40 - 20, random.random() * 20 - 10)) for i in range(bnum)]
slist = [Spring(blist[i], blist[i + 1], random.randint(30, 50)) for i in range(bnum - 1)]
clock = py.time.Clock()
s1 = Spring(Ball(vec2(-100, 0), vec2(0, 0)), Ball(vec2(100, 0), vec2(0, 0)), 150)
while running:
    clock.tick(60)
    events = py.event.get()
    keys = py.key.get_pressed()
    for event in events:
        if event.type == py.QUIT:
            running = False
    if keys[py.K_q]:
        running = False
    # for spring in slist:
    #     spring.updatePos()
    s1.updatePos()
    win.fill(OWHITE)
    # for spring in slist:
    #     spring.render()
    s1.render()
    py.display.update()