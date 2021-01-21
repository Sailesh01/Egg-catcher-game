# -*- coding: utf-8 -*-
"""
Created on Sat May 16 14:31:24 2020

@author: ranas
"""
from itertools import cycle
from random import randrange
from tkinter import Tk, Canvas, messagebox, font

canvas_width=800
canvas_height=400

win=Tk()

c=Canvas(win,width=canvas_width, height=canvas_height, background="deep sky blue")
c.create_rectangle(-5,canvas_height-100,canvas_width+5,canvas_height+5,fill="green",width=0)
c.create_oval(-80,-80,120,120,fill="orange",width=0)

c.pack()

colors=cycle(["light blue","light pink","light yellow","light green","red","blue","green","yellow","purple","pink"])
egg_width=45
egg_height=55
egg_score=10
egg_speed=500
egg_interval=4000
difficulty_factor=0.95

catcher_color="blue"
catcher_width=100
catcher_height=100
cat_startx=canvas_width/2  - catcher_width/2
cat_starty=canvas_height - catcher_height - 20
cat_startx2=cat_startx + catcher_width
cat_starty2=cat_starty + catcher_height

catcher=c.create_arc(cat_startx, cat_starty, cat_startx2, cat_starty2, start=200, extent=140, style='arc', outline=catcher_color, width=3)

score=0
score_text=c.create_text(5,10,anchor="nw", font=('Arial',18,'bold'), fill="dark blue", text="Score : "+str(score))

lives_remaining=3
lives_text=c.create_text(canvas_width-240,10,anchor="nw", font=('Arial',18,'bold'), fill="dark blue", text="Lives Remaining : "+str(lives_remaining))

eggs=[]

def create_eggs():
    x=randrange(10,740)
    y=40
    new_egg=c.create_oval(x,y,x + egg_width,y + egg_height,fill= next(colors), width=0)
    eggs.append(new_egg)
    win.after(egg_interval,create_eggs)
    
def mov_eggs():
    for egg in eggs:
        (x1,y1,x2,y2)=c.coords(egg)
        c.move(egg,0,10)
        if (y2>canvas_height):
            egg_dropped(egg)
    win.after(egg_speed, mov_eggs)
    
def egg_dropped(egg):
    eggs.remove(egg)
    lose_a_life()
    if lives_remaining==0:
        messagebox.showinfo("GAME OVER!","Final Score : "+str(score))
        win.destroy()
        
def lose_a_life():
    global lives_remaining
    lives_remaining-=1
    c.itemconfigure(lives_text, text="Lives Remaining : "+str(lives_remaining))
    
def catch():
    (catchX,catchY,catchX2,catchY2)=c.coords(catcher)
    for egg in eggs:
        (eggX,eggY,eggX2,eggY2)=c.coords(egg)
        if catchX < eggX and eggX2 < catchX2 and catchY2-eggY2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    win.after(100,catch)
    
def increase_score(points):
    global score, egg_speed, egg_interval
    score+=points
    egg_speed=int(egg_speed*difficulty_factor)
    egg_interval=int(egg_interval*difficulty_factor)
    c.itemconfigure(score_text, text="Score : "+str(score))
    
def move_left(event):
    (x1,y1,x2,y2)=c.coords(catcher)
    if x1>0:
        c.move(catcher,-20,0)
    
def move_right(event):
    (x1,y1,x2,y2)=c.coords(catcher)
    if x2<canvas_width:
        c.move(catcher,20,0)
        
c.bind("<Left>",move_left)
c.bind("<Right>",move_right)
c.focus_set()

win.after(1000,create_eggs)
win.after(1000,mov_eggs)
win.after(1000,catch)



win.mainloop()