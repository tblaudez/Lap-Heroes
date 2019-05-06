#Importation
from tkinter import *
from random import *
from random import randint
import os, sys

#Lancement de Tkinter
fen1 = Tk()
custom_path = os.getcwd()
TAILLE_P = 60
carte,cdbloc,pacman,cdpac,listsens = [], [], [], [], []
sortie = ['1','2','3','4','5','6' ]
cdsortie, sorti, cdbouf, bouf, cdfant, fant, sensf   = [],[],[],[],[],[],[]
taille = TAILLE_P/3
jeux = True

#Fullscreen
#w, h = fen1.winfo_screenwidth(), fen1.winfo_screenheight() #On prend les donnee de l'ecran et on le met ne plein ecran
#fen1.overrideredirect(1)
#fen1.geometry("%dx%d+0+0" % (w, h))
fen1.bind("<Escape>", lambda e: fen1.destroy())

############CARTE#############
largeur = 0
fichier = open(custom_path + '/BOSS/PACMAN/MAP.txt', 'r')
for i in fichier:
    carte.append(list(i.replace("\n","")))
    largeur += 1
#creation map
L = len(carte[1])*TAILLE_P
l = largeur*TAILLE_P
can1 = Canvas(fen1, bg="black", height= l, width = L)
for i in range(len(carte[1])):
        for j in range(largeur):
            if carte[j][i] == " ":
                bouffe = can1.create_rectangle(i*TAILLE_P+taille,j*TAILLE_P+taille, i*TAILLE_P+taille+10, j*TAILLE_P+taille+10, fill='yellow')
                cdbouf.append([i*TAILLE_P,j*TAILLE_P])
                bouf.append(bouffe)
            if carte[j][i]=='X':
                can1.create_rectangle(i*TAILLE_P, j*TAILLE_P, i*TAILLE_P+TAILLE_P, j*TAILLE_P+TAILLE_P,width=2, fill='grey')
                cdbloc.append([i*TAILLE_P,j*TAILLE_P])
            if carte[j][i]=='P':
                pac = can1.create_rectangle(i*TAILLE_P, j*TAILLE_P, i*TAILLE_P+TAILLE_P, j*TAILLE_P+TAILLE_P, fill='red')
                x1 = i*TAILLE_P
                y1 = j*TAILLE_P
                pacman.append(pac)
                cdpac.append([x1,y1])
            if carte[j][i] in sortie:
                cdsortie.append([i*TAILLE_P,j*TAILLE_P])
                sorti.append(carte[j][i])
                if carte[j][i] == '1' or carte[j][i] == '3':
                    cdbloc.append([i*TAILLE_P,j*TAILLE_P-TAILLE_P])

                if carte[j][i] == '2' or carte[j][i] == '4':
                    cdbloc.append([i*TAILLE_P,j*TAILLE_P+TAILLE_P])
                    
                if carte[j][i] == '5':
                    cdbloc.append([i*TAILLE_P-TAILLE_P,j*TAILLE_P])
                  
                if carte[j][i] == '6':
                    cdbloc.append([i*TAILLE_P+TAILLE_P,j*TAILLE_P])
                   
                        
                    

for i in cdsortie:
    F = can1.create_rectangle(i[0],i[1],i[0]+TAILLE_P,i[1]+TAILLE_P,fill='green')
    cdfant.append([i[0],i[1]])
    fant.append(F)
    sensf.append(0)

    
can1.pack(side=LEFT)
#DEPLACEMENTs
sens = 'debut'
dx = 0#deplacements au debut de la partie
dy = 0

def depl_gauche(ev=None):
    global sens, dx, dy, depl
    sens = 'gauche'
    dx = -TAILLE_P
    dy = 0
def depl_droite(ev=None):
    global sens, dx, dy, depl
    sens = 'droite'
    dx = TAILLE_P
    dy = 0
def depl_haut(ev=None):
    global sens, dx, dy, depl
    sens = 'haut'
    dx = 0
    dy = -TAILLE_P
def depl_bas(ev=None):
    global sens, dx, dy, depl
    sens = 'bas'
    dx = 0
    dy = TAILLE_P
################################jeu###############
def start():
    global x1, y1, jeux
    x1 += dx
    y1 += dy
    
    if [x1,y1] in cdbloc:
        x1 -= dx
        y1 -= dy
    for i in range(len(bouf)):
        if [x1,y1] == cdbouf[i]:
            can1.delete(bouf[i])            
        
    porte()
    cdpac[0]=[x1,y1]
    can1.coords(pac, x1, y1, x1+TAILLE_P, y1+TAILLE_P)
        
    if jeux:
        fen1.after(150,start)
    
def porte():
    global x1,y1
    for i in range(len(cdsortie)):
        if cdsortie[i] == [x1,y1]:
            if sorti[i] == '1':
                for i in range(len(sorti)):
                    if sorti[i] == '2':
                        x1 = cdsortie[i][0]
                        y1 = cdsortie[i][1]
                        return
            if sorti[i] == '2':
                for i in range(len(sorti)):
                    if sorti[i] == '1':
                        [x1,y1] = cdsortie[i]
                        return
            if sorti[i] == '3':
                for i in range(len(sorti)):
                    if sorti[i] == '4':
                        [x1,y1] = cdsortie[i]
                        return
            if sorti[i] == '4':
                for i in range(len(sorti)):
                    if sorti[i] == '3':
                        [x1,y1] = cdsortie[i]
                        return
            if sorti[i] == '5':
                for i in range(len(sorti)):
                    if sorti[i] == '6':
                        [x1,y1] = cdsortie[i]
                        return
            if sorti[i] == '6':
                for i in range(len(sorti)):
                    if sorti[i] == '5':
                        [x1,y1] = cdsortie[i]
                        return

####################IA FANTOMES#####################
def IA():
    for i in range(len(fant)):
        xf = cdfant[i][0]
        yf = cdfant[i][1]
        fantavance(xf, yf, i)
        
        
    if jeux:
        fen1.after(800, IA)
            
def fantavance(xf, yf, i):
    mfx1=0
    mfy1=0
    if sensf[i] == 1:
        mfx1 = TAILLE_P
        mfy1 = 0
    if sensf[i] == 2:
        mfx1 = -TAILLE_P
        mfy1 = 0 
    if sensf[i] == 3:
        mfx1 = 0
        mfy1 = TAILLE_P
    if sensf[i] == 4:
        mfx1 = 0
        mfy1 = -TAILLE_P
    xfi = xf + mfx1
    yfi = yf + mfy1
    if [xfi , yfi] not in cdbloc and [xfi , yfi] not in cdfant : 
        can1.coords(fant[i], xfi, yfi, xfi+TAILLE_P, yfi+TAILLE_P)
        cdfant[i][0] = xfi
        cdfant[i][1] = yfi
        
    else:
        num = randint(1,4)
        if num == 1:
            mfx = TAILLE_P
            mfy = 0
        if num == 2:
            mfx = -TAILLE_P
            mfy = 0 
        if num == 3:
            mfx = 0
            mfy = TAILLE_P
        if num == 4:
            mfx = 0
            mfy = -TAILLE_P
        
        xfi = xf + mfx
        yfi = yf + mfy
        if [xfi , yfi] not in cdbloc : 
            can1.coords(fant[i], xfi, yfi, xfi+TAILLE_P, yfi+TAILLE_P)
            cdfant[i][0] = xfi
            cdfant[i][1] = yfi
            sensf[i] = num
        else:
            fantavance(xf , yf, i)
            
        
def victoire(ev=None):
    global jeux
    jeux = False
    Message(can1, anchor= CENTER, bg='grey' ,bd= 3,relief= RIDGE, justify= CENTER, aspect= 1000, text="CELA NE SE PEUT !").place(x= 800, y=500)
    Button(can1, text='Continuer', command= finjeux).place(x= 950, y=500)

def finjeux():
    fen1.destroy()
    sys.path.append(os.path.abspath(custom_path))
    import lapheroes
    
        
####################################################
#Liaisons des touches
fen1.bind("<a>",depl_gauche)
fen1.bind("<d>",depl_droite)
fen1.bind("<w>",depl_haut)
fen1.bind("<s>",depl_bas)
fen1.bind("<e>",victoire)
#lancement de la partie#######
start()
IA()
fichier.close()
fen1.mainloop()
