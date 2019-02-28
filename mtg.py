###### IMPORTS AND FUNCTIONS ########

from tkinter import *
from io import BytesIO
from PIL import Image, ImageTk
from random import randint
import scrython
import tkinter.ttk as ttk
import requests
import sys
import time
from threading import *
from tkinter import simpledialog
from tkinter import messagebox
import webbrowser
import itertools

cardMarketLink = ""
EDHRECLink = ""
scryfallLink = ""

def sIV(v, setC, cName):
    for i in range(len(v)):
        if((v[i]['set'].upper() == setC) and (v[i]['name'] == cName)):
            return i

def link2Img(link, r):
    response = requests.get(link)
    img = Image.open(BytesIO(response.content)).resize(r)
    return ImageTk.PhotoImage(img)

def Cc(s):
    return list(''.join(t) for t in itertools.product(*zip(s.lower(), s.upper())))

def takeToLink(event):
    webbrowser.open(link)

def takeToMKM(event):
    webbrowser.open(cardMarketLink)

def takeToEDHREC(event):
    webbrowser.open(EDHRECLink)

def takeToScryfall(event):
    webbrowser.open(scryfallLink)

def imageSidebar(event):
    global link, scryfallLink, EDHRECLink, cardMarketLink
    curItem = tv.item(tv.focus())
    ind = sIV(cardV, curItem['values'][1], curItem['text'])
    print(ind)
    card = cardV[ind]
    print(card)
    f11label.bind("<Double-Button-1>", takeToMKM)
    f12label.bind("<Double-Button-1>", takeToEDHREC)
    f13label.bind("<Double-Button-1>", takeToScryfall)
    link = card['image_uris']['large']
    scryfallLink = card['scryfall_uri']
    EDHRECLink = card['related_uris']['edhrec']
    cardMarketLink = card['purchase_uris']['cardmarket']
    if(link != None):
        imgTK = link2Img(link, (380,540))
        imgLabel.image = imgTK
        imgLabel.configure(image = imgTK)
    else:
        link = linkDefault
        imgLabel.image = imgTKDefault
        imgLabel.configure(image = imgTKDefault)
        f11label.unbind("<Double-Button-1>")
        f11label.unbind("<Double-Button-1>")
        f11label.unbind("<Double-Button-1>")

def makeentry(parent, caption, r, width=None, **options):
    Label(parent, text=caption).grid(row = r, column = 0, padx = (20, 35), pady=(10,5))
    entry = Entry(parent, **options)
    entry.delete(0, END)
    entry.grid(row = r, column = 2, columnspan = 5, pady=(10,5))
    entry.bind("<Return>", cardFindByName)
    if width:
        entry.config(width=width)
    return entry

def cardFindByName(*args):
    strser = obj.getSS()
    obj.cb.config(state = DISABLED)
    obj.e.unbind("<Return>")
    obj.searchB['state'] = 'disabled'
    a = obj.getName()
    r = randint(1,100)
    tv.delete(*tv.get_children())
    progressbar['maximum'] = 100
    for i in range(r):
        time.sleep(0.03)
        progressbar['value'] = i
        progressbar.update()
    global cardV
    query = "++name:" + a
    cardV = list(scrython.cards.Search(q=query).data())
    capitalizations = Cc(a)
    for i in range(len(cardV)):
        if(strser == 0):    
            try:
                tv.insert('', i, text=cardV[i]['name'], values=(cardV[i]['set_name'], cardV[i]['set'].upper(), cardV[i]['mana_cost'], cardV[i]['rarity'].capitalize(), cardV[i]['artist']))
            except:
                tv.insert('', i, text=cardV[i]['name'], values=(cardV[i]['set_name'], cardV[i]['set'].upper(), '', cardV[i]['rarity'].capitalize(), cardV[i]['artist']))
        else:
            if(cardV[i]['name'] in capitalizations):
                try:
                    tv.insert('', i, text=cardV[i]['name'], values=(cardV[i]['set_name'], cardV[i]['set'].upper(), cardV[i]['mana_cost'], cardV[i]['rarity'].capitalize(), cardV[i]['artist']))
                except:
                    tv.insert('', i, text=cardV[i]['name'], values=(cardV[i]['set_name'], cardV[i]['set'].upper(), '', cardV[i]['rarity'].capitalize(), cardV[i]['artist']))
    if(len(tv.get_children()) == 0):
        messagebox.showinfo("Feelsbadman", "Unfortunately no card was found! :( Try Again!")
    for i in range(r+1, 101):
        time.sleep(0.02)
        progressbar['value'] = i
        progressbar.update()
    obj.e.delete(0, END)
    obj.cb.config(state = NORMAL)
    obj.searchB['state'] = 'normal'
    progressbar['value'] = 0
    obj.e.bind("<Return>", cardFindByName)

    
#####################################

class Magic:
    
    def __init__(self, master):

        self.strser = 0
        #self.rarity = StringVar(master)
        #self.rarity.set("None")

        self.frame = Frame(master)

        self.e = makeentry(master, "Enter Card Name:", 0, 80)
        #self.rar = OptionMenu(master,  self.rarity, "None", "Common", "Uncommon", "Rare", "Mythic Rare", "Special")
        #self.rar.grid(row = 4, column = 0, pady = (20,5), columnspan = 3)

        self.cb = Checkbutton(master, text="Strict Search", variable = self.strser, command = self.change)
        self.cb.grid(row = 0, column = 7, pady=(10,5))

        self.searchB = Button(master, text="Search!", command = cardFindByName, height=2)
        self.searchB.grid(row=10, column = 2, padx = (15,10), pady=10)

    def getName(self):
        return self.e.get()
    def getSS(self):
        return self.strser
    def change(self):
        if(self.strser == 0):
            self.strser = 1
        else:
            self.strser = 0

#####################################

root = Tk()
root.title('SUPER ADVANCED MTG FINDER!')
root.state('zoomed')

sidebar = Frame(root, width= 700, bg='#3e3e3e', height = 820, relief='sunken', borderwidth=3)
sidebar.grid(row = 0, column = 21, rowspan=200, sticky=E, padx = (60,5), pady = 10)
sidebar.grid_propagate(False)

link = "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/thumb/f/f8/Magic_card_back.jpg/200px-Magic_card_back.jpg?version=502b3920ffde0bf30d2a6227e79639ff"
linkDefault = "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/thumb/f/f8/Magic_card_back.jpg/200px-Magic_card_back.jpg?version=502b3920ffde0bf30d2a6227e79639ff"

imgTKDefault = link2Img(link, (388,540))

imgLabel = Label(sidebar, image = imgTKDefault, bg = '#3e3e3e')
imgLabel.image = imgTKDefault
imgLabel.grid(row = 0, column = 0, columnspan = 20, padx=(156,0), pady=(30,0))
imgLabel.bind("<Double-Button-1>", takeToLink)

f1 = Frame(sidebar, width = 600, height = 200, borderwidth = 5, relief='sunken')
f1.grid(row = 1, column = 0, columnspan = 50, pady=(10, 10), padx=(40,0))

f11 = Frame(f1, width = 200, height = 200, borderwidth = 5, relief='sunken')
f12 = Frame(f1, width = 200, height = 200, borderwidth = 5, relief='sunken')
f13 = Frame(f1, width = 200, height = 200, borderwidth = 5, relief='sunken')
f11.grid(row = 0, column = 0, sticky = NW)
f12.grid(row = 0, column = 1, sticky = NW)
f13.grid(row = 0, column = 2, sticky = NW)


f11link = "http://www.60cards.net/media/avatars/5db30d43f3791ae82e8f09070647e4cb.jpg"
f12link = "http://www.commanderinmtg.com/wp-content/uploads/2016/07/EDHREC-Square-logo.png"
f13link = "https://pbs.twimg.com/profile_images/1023001888835264512/zoaDNx19_400x400.jpg"

imgf11 = link2Img(f11link, (190,190))
imgf12 = link2Img(f12link, (190,190))
imgf13 = link2Img(f13link, (190,190))

f11label = Label(f11, image = imgf11)
f12label = Label(f12, image = imgf12)
f13label = Label(f13, image = imgf13)

f11label.grid(row = 0, column = 0)
f12label.grid(row = 0, column = 0)
f13label.grid(row = 0, column = 0)

progressbar = ttk.Progressbar(root, orient = 'horizontal', length = 420, mode='determinate')
progressbar.grid(row = 10, column = 3, padx = (10,15), pady=5)

bottombar = Frame(root, width = 720, bg='#ffffff', height = 420, relief='sunken', borderwidth=3)
bottombar.grid(row=20, column=0, columnspan=500, sticky=W, padx = (15,5), pady=(405,10))

tv = ttk.Treeview(bottombar, height=15, columns=('Card Set', 'Set Code', 'Mana Cost', 'Rarity', 'Artist'))
tv.grid(column = 0, row =0)
tv.column('#0', width = 200)
tv.column('Card Set', width = 150)
tv.column('Set Code', width = 80)
tv.column('Mana Cost', width = 100)
tv.column('Rarity', width = 100)
tv.column('Artist', width = 100)
tv.heading('#0', text='Card Name')
tv.heading('Card Set', text='Card Set')
tv.heading('Set Code', text='Set Code')
tv.heading('Mana Cost', text='Mana Cost')
tv.heading('Rarity', text='Rarity')
tv.heading('Artist', text='Artist')
tv.bind('<ButtonRelease-1>', imageSidebar)

global obj
obj = Magic(root)

root.mainloop()

#PESQUISAS MAIS PROFUNDAS!