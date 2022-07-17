print("hi")
#!/usr/bin/python
from distutils.command.install_egg_info import to_filename
from os import path
from asyncio.windows_events import NULL
from cgitb import text
from functools import partial
from math import floor
from random import randint
from tkinter import *
from turtle import width
import pathlib
from webbrowser import get
#folder path
folder_path=pathlib.Path(__file__).parent.resolve()

top = Tk()
frame1=Frame(top)
frame2=Frame(top)
top.title("mine sweaper")

size=15
hardness=0
discoverd=[]
minesCount=0
mineField=[]
btns=[]


foundMines=[]
#get flag image 
flag_img_name="flag2"
flag_img_format="png"
mine_img_name="mine"
mine_img_format="png"
flag_img=PhotoImage(file=path.join(folder_path,flag_img_name+'.'+flag_img_format))
mine_img=PhotoImage(file=path.join(folder_path,mine_img_name+'.'+mine_img_format))

def checkPosition(i):
    x=floor(i/size)
    y=i%size 
    if x<size and x>=0 and y<size and y>=0:
        return True   
def gameOver():
    for i in range(size):
        for j in range(size):
            if mineField[j+i*size]==True:
                btns[j+i*size].config(borderwidth=1,fg="#990000",bg="white",text="B",image=mine_img,width=30)
            else:
                None
    label=Label(top,text="Game Over",fg="red")
    label.tkraise()
    label.pack()            
def checkButtonCount(x,y):
    num=0
    mask=roundMask(x,y)
    if mineField[x+ y*size]==True:
        return 'b'
    for i in mask:
        if mineField[i]==True:
            num+=1
    if num==0: 
        return " "
    return num       
def roundMask(x,y):
    mask=[]
    if  x+1<size and y+1<size:
        mask.append(x+1+(y+1)*size)
    if  x+1<size :
        mask.append(x+1+y*size)
    if  x+1<size and y-1>=0 :
        mask.append(x+1+(y-1)*size)
    if  x-1 >=0  and y-1>=0 :
        mask.append(x-1+(y-1)*size)
    if x-1 >=0 :
        mask.append(x-1+y*size)
    if x-1 >=0 and y+1<size:
        mask.append(x-1+(y+1)*size)
    if  y-1>=0 :
        mask.append(x+(y-1)*size)
    if  y+1<size:
        mask.append(x+(y+1)*size)
    mask.append(x+y*size)
    return mask
def notMine(x,y):
    global discoverd
    mask=spaceSpread(x,y)  
    for i in mask:
        tmpx,tmpy=get2dPos(i)
        tmplist=roundMask(tmpx,tmpy)
        for j in tmplist:
            if mineField[j]==False:
                if i not in discoverd:
                    discoverd.append(i)
                btns[j]['fg']="#000000"
                btns[j]['bg']="#999999"
    mask=roundMask(x,y)
    for i in mask:
        if mineField[i]==False:
            if i not in discoverd:
                discoverd.append(i)
            btns[i]['fg']="#000000"
            btns[i]['bg']="#999999"        
def buttonPressed(x,y):
    if mineField[x+y*size]==True:
        print("lost")
        gameOver()
    else:
        notMine(x,y)
        checkState() 
def right_button_clicked(e):
    if (e.x,e.y) in foundMines:
        e.widget.configure(image='',width=4,bg="#8BAFC8")
        return
    e.widget.configure(image=flag_img,width=32,bg="#888888",fg="#8BAFC8")
    foundMines.append((e.x,e.y)) 
def get2dPos(_1dPos):
    y=floor(_1dPos/size)
    x=_1dPos%size 
    return x,y
def spaceSpread(x,y):
    spaces=[]
    result=[]
    visted=[(False)]*(size*size)
    visted[x+y*size]=True
    result.append(x+y*size)
    for i in roundMask(x,y):
        if i in spaces:
            continue
        if mineField[i]==False and btns[i]["text"]==" ":
            spaces.append(i)
    if len(spaces)>0:
        spaces.pop()            
    while len(spaces) >0:
        x,y=get2dPos(spaces.pop(0))
        result.append(x+ y*size)
        visted[x+y*size]=True
        for i in roundMask(x,y):
            if i in spaces:
                continue
            if mineField[i]==False and visted[i]==False and btns[i]["text"]==" ":
                spaces.append(i)         
    return result                      
def Easy():
    global hardness
    global size
    size=7
    frame2.pack_forget()
    frame1.pack()
    hardness=4
    setGameGrid()
def Normal():
    global hardness
    global size
    size=10
    frame2.pack_forget()
    frame1.pack()
    hardness=6
    setGameGrid()
def Hard():
    global hardness
    global size
    size=15
    frame2.pack_forget()
    frame1.pack()
    hardness=8
    setGameGrid()
def startMenu():
    easy=Button(frame2,width=30,  height=5, bg="blue",fg="white",command=Easy ,text="easy")
    normal=Button(frame2,width=30,height=5, bg="blue",fg="white",command=Normal,text="Normal")
    hard=Button(frame2,width=30  ,height=5, bg="blue",fg="white",command=Hard ,text="Hard")
    easy.pack()
    normal.pack()
    hard.pack()
    easy.tkraise()
    normal.tkraise()
    hard.tkraise()
    frame2.pack()
def setGameGrid():
    global minesCount
    for i in range(size):
        for j in range(size):
            if randint(1,20)<=hardness:
                mineField.append(True)
                minesCount+=1
            else:
                mineField.append(False)    
            
    # make the buttons
    for i in range(size):
        for j in range(size):
            parButtonPressed=partial(buttonPressed,j,i)
            tmpbtn=Button(frame1,text="h",width=4,fg="#8BAFC8",bg="#8BAFC8",command=parButtonPressed)
            tmpbtn.bind("<Button-3>",right_button_clicked)
            btns.append(tmpbtn)
    # set every position count of mines around
    for i in range(0,size):
        for j in range(0,size):
            btns[j+i*size].grid(row=i,column=j) 
            btns[j+i*size]['text']=checkButtonCount(j,i)  
    print(hardness,"hi")        
def checkState():
    print(minesCount,len(discoverd))
    if minesCount==(size*size)-len(discoverd):
        label=Label(top,text="you won ",fg="blue")
        label.tkraise()
        label.pack()   
startMenu()


top.mainloop()