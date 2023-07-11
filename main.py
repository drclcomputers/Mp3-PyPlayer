from tkinter import *
from tkinter import filedialog
from pygame import mixer
import json
import time
from PIL import Image, ImageTk
import os

a=1
stime=None
mixer.init()
mixer.music.set_volume(1)

pausetest=False
musicloadtest=False
repeatvar=False

timp=0

def play():
    global pausetest, musicloadtest, timp, stime, other, helpi, playback
    for i in fileslist.curselection():
        mixer.music.load(fileslist.get(i))
        musicloadtest=True
    if musicloadtest==True:
        other.entryconfig('Repeat', state="active")
        helpi.entryconfig('Skin', state="disabled")
        playback.entryconfig("Pause", state="active")
        playback.entryconfig("Next", state="active")
        playback.entryconfig("Previous", state="active")
        playback.entryconfig('Stop', state="active")
        pausebutton.config(state="normal")
        stopbutton.config(state="normal")
        nextbutton.config(state="normal")
        backbutton.config(state="normal")
        window.update()
        try:
            if pausetest==False:
                mixer.music.play()
                stime=time.time()
            if pausetest==True:
                mixer.music.play()
                mixer.music.set_pos(timp)
                pausetest=False
        except:
            print("Load music!")
    else:
        print("Load music!")

def pause():
    global pausetest, timp, stime, ftime, other
    mixer.music.stop()
    pausetest=True
    ftime=time.time()
    timp=ftime-stime
    other.entryconfig('Repeat', state="disabled")
    playback.entryconfig("Pause", state="disabled")

def stop():
    global musicloadtest, pausetest, timp, helpi, other
    mixer.music.stop()
    mixer.music.unload()
    fileslist.select_clear(0, END)
    musicloadtest=False
    pausetest=False
    timp=0
    other.entryconfig('Repeat', state="disabled")
    helpi.entryconfig('Skin', state="active")
    playback.entryconfig("Pause", state="disabled")
    playback.entryconfig("Next", state="disabled")
    playback.entryconfig("Previous", state="disabled")
    playback.entryconfig('Stop', state="disabled")
    pausebutton.config(state="disabled")
    stopbutton.config(state="disabled")
    nextbutton.config(state="disabled")
    backbutton.config(state="disabled")

def openfile():
    global a, musicloadtest
    types = [('MP3 Files', '*.mp3'), ('WAV Files', '*.wav'), ('OGG Files', '*.ogg')]
    files=filedialog.askopenfilename(filetypes=types)
    fileslist.insert(a, files)
    musicloadtest=True
    a+=1

def deletefile():
    for i in fileslist.curselection():
        fileslist.delete(i, None)

def volumeset():
    global volum
    mixer.music.set_volume(volum.get())

def skinchoose():
    global data, f, skinvar, j
    skinwindow=Toplevel(window)
    skinwindow.geometry("200x100")
    skinwindow.title("Choose Skin")
    skinwindow.resizable(0, 0)
    j=open('skin.json')
    aux=json.load(j)
    skinvar=IntVar()
    basic=Radiobutton(skinwindow, variable=skinvar, value=0)
    basic.place(x=5, y=5)
    classic=Radiobutton(skinwindow, variable=skinvar, value=1)
    classic.place(x=5, y=20)
    dxd=Radiobutton(skinwindow, variable=skinvar, value=2)
    dxd.place(x=5, y=35)
    initiald=Radiobutton(skinwindow, variable=skinvar, value=3)
    initiald.place(x=5, y=50)
    basictext=Label(skinwindow, text="Basic")
    basictext.place(x=20, y=5)
    classictext=Label(skinwindow, text="Classic")
    classictext.place(x=20, y=20)
    dxdtext=Label(skinwindow, text="Highschool DXD")
    dxdtext.place(x=20, y=35)
    initialdtext=Label(skinwindow, text="Initial D")
    initialdtext.place(x=20, y=50)
    h=aux['skinaux']
    match h:
        case 0:
            basic.select()
        case 1:
            classic.select()
        case 2:
            dxd.select()
        case 3:
            initiald.select()
   
    def aprob():
        global skinvar
        x=skinvar.get()
        aux['skinaux']=x
        with open("skin.json", "w") as sk:
            json.dump(aux, sk, indent=4)
        initiere()
    
    aprobbutton=Button(skinwindow, text="Ok", command=aprob)
    aprobbutton.place(x=150, y=20)
    renuntbutton=Button(skinwindow, text="Cancel", command=skinwindow.destroy)
    renuntbutton.place(x=150, y=60)

def next():
    for i in fileslist.curselection():
        if i+1<len(fileslist.get(0, END)):
            mixer.music.stop()
            mixer.music.unload()
            mixer.music.load(fileslist.get(i+1))
            mixer.music.play()
            fileslist.select_clear(0, END)
            fileslist.select_set(i+1)
        else:
            mixer.music.rewind()

def back():
    for i in fileslist.curselection():
        if i>0:
            mixer.music.stop()
            mixer.music.unload()
            mixer.music.load(fileslist.get(i-1))
            mixer.music.play()
            fileslist.select_clear(0, END)
            fileslist.select_set(i-1)
        else:
            mixer.music.rewind()

def repeat():
    global stime, timp, pausetest, repeatvar, other
    if mixer.music.get_busy():
        ftime=time.time()
        timp=ftime-stime
        if repeatvar.get()==True:
            mixer.music.play(-1)
            mixer.music.set_pos(timp)
        else:
            mixer.music.play()
            mixer.music.set_pos(timp)
    else:
        other.entryconfig("Repeat", state='disabled')

def about():
    aboutwindow=Toplevel(window)
    aboutwindow.geometry("200x100")
    aboutwindow.title("About")
    aboutwindow.resizable(0, 0)
    image1=Image.open("logo2.png")
    img=image1.resize((30, 30))
    img=image1.resize((30, 30))
    imagelabel=ImageTk.PhotoImage(img)
    testimg=Label(aboutwindow, image=imagelabel)
    testimg.image=imagelabel
    testimg.pack(anchor="center")
    text=Label(aboutwindow, text="Mp3 PyPlayer").pack(anchor='center')
    vertext=Label(aboutwindow, text="ver 0.9").pack(anchor="center")
    opentext=Label(aboutwindow, text="An open-source project").pack(anchor="s")

def helpfile():
    os.startfile("help.txt")

def initiere():
    global window, fileslist, pausetest, musicloadtest, volum, timp, data, f, j, skin, a, repeatvar, aux, image1, other, helpi, playback, pausebutton, nextbutton, backbutton, stopbutton
    with open('skin.json', 'r') as j:
        aux=json.load(j)
    a=aux['skinaux']
    match a:
        case 0:
            f=open("basic.json")
            data=json.load(f)
        case 1:
            f=open("clasic.json")
            data=json.load(f)
        case 2:
            f=open("animedxd.json")
            data=json.load(f)
        case 3:
            f=open("animed.json")
            data=json.load(f)
    window=Tk()
    window.title("Mp3 PyPlayer ver 0.9")
    p1=PhotoImage(file='logo2.png')
    window.iconphoto(True, p1)
    window.geometry("320x200")
    window.resizable(0, 0)
    if a==1:
        window.config(bg=data['bg'])
        image1=Image.open("logo3.png")
        image1=image1.resize((75, 75))
        imagelabel=ImageTk.PhotoImage(image1)
        testimg=Label(image=imagelabel, borderwidth=0)
        testimg.image=imagelabel
        testimg.place(x=20, y=100)
    if a==2:
        window.config(bg=data['bg'])
        image1=Image.open("logodxd2.png")
        image1=image1.resize((120, 110))
        imagelabel=ImageTk.PhotoImage(image1)
        testimg=Label(image=imagelabel, borderwidth=0)
        testimg.image=imagelabel
        testimg.place(x=0, y=90)
    if a==3:
        window.config(bg=data['bg'])
        image1=Image.open("logod2.png")
        image1=image1.resize((120, 80))
        imagelabel=ImageTk.PhotoImage(image1)
        testimg=Label(image=imagelabel, borderwidth=0)
        testimg.image=imagelabel
        testimg.place(x=0, y=115)
    menubar=Menu(window)
    window.config(menu=menubar)
    filemenu=Menu(menubar, tearoff=False, background=data['menu'], fg=data['menutext'])
    playback=Menu(menubar, tearoff=False, background=data['menu'], fg=data['menutext'])
    other=Menu(menubar, tearoff=False, background=data['menu'], fg=data['menutext'])
    helpi=Menu(menubar, tearoff=False, background=data['menu'], fg=data['menutext'])

    volume=Menu(other, tearoff=False)
    skin=Menu(helpi, tearoff=False)

    filemenu.add_command(label="Open...", command=openfile)
    filemenu.add_command(label="Delete", command=deletefile)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    playback.add_command(label="Play", command=play)
    playback.add_command(label="Pause", command=pause)
    playback.add_command(label="Stop", command=stop)
    playback.add_command(label="Next", command=next)
    playback.add_command(label="Previous", command=back)
    menubar.add_cascade(label="Playback", menu=playback)

    other.add_cascade(label="Volume", menu=volume)
    volum=DoubleVar()
    volume.add_radiobutton(label="Mute", command=volumeset, variable=volum, value=0)
    volume.add_radiobutton(label="10%", command=volumeset, variable=volum, value=0.1)
    volume.add_radiobutton(label="25%", command=volumeset, variable=volum, value=0.25)
    volume.add_radiobutton(label="50%", command=volumeset, variable=volum, value=0.5)
    volume.add_radiobutton(label="75%", command=volumeset, variable=volum, value=0.75)
    volume.add_radiobutton(label="100%", command=volumeset, variable=volum, value=1)

    repeatvar=BooleanVar(value=False)
    other.add_checkbutton(label="Repeat", command=repeat, variable=repeatvar, offvalue=False, onvalue=True)
    menubar.add_cascade(label="Other", menu=other)

    helpi.add_command(label="Skin", command=skinchoose)
    helpi.add_separator()
    helpi.add_command(label="View help", command=helpfile)
    helpi.add_command(label="About", command=about)
    menubar.add_cascade(label="Help", menu=helpi)

    playbutton=Button(text="|>", command=play, bg=data['play'], fg=data['text'])
    playbutton.place(x=20, y=20)

    pausebutton=Button(text="| |", command=pause, bg=data['pause'], fg=data['textpause'])
    pausebutton.place(x=50, y=20)

    stopbutton=Button(text="X", command=stop, bg=data['stop'], fg=data['text'])
    stopbutton.place(x=80, y=20)

    nextbutton=Button(text=">>", command=next, bg=data['skip'], fg=data['text'])
    nextbutton.place(x=72, y=60)

    backbutton=Button(text="<<", command=back, bg=data['back'], fg=data['text'])
    backbutton.place(x=20, y=60)

    add=Button(text="Add", command=openfile, bg=data['add'], fg=data['text'])
    add.place(x=160, y=20)

    delete=Button(text="Delete", command=deletefile, bg=data['delete'], fg=data['text'])
    delete.place(x=220, y=20)

    fileslist=Listbox(width=30, height=7)
    fileslist.place(x=120, y=60)

    if not mixer.music.get_busy():
        other.entryconfig('Repeat', state="disabled")
        playback.entryconfig("Pause", state="disabled")
        playback.entryconfig("Next", state="disabled")
        playback.entryconfig("Previous", state="disabled")
        playback.entryconfig('Stop', state="disabled")
        pausebutton.config(state="disabled")
        nextbutton.config(state="disabled")
        backbutton.config(state="disabled")
        stopbutton.config(state="disabled")

initiere()

window.mainloop()
mixer.quit()