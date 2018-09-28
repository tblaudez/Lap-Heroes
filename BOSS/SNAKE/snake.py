#Importation
from tkinter import *
from random import *
import os, sys

#Lancement de Tkinter
fen1 = Tk()
custom_path = '/Users/tblaudez/Downloads/test'
TAILLE_P = 60
carte,cdbloc =  [], [] # commun
snak,cdsnake,listsens = [], [], [] #spécifique au snake 1

#Fullscreen
#w, h = fen1.winfo_screenwidth(), fen1.winfo_screenheight() #On prend les donnée de l'écran et on le met ne plein écran
#fen1.overrideredirect(1)
#fen1.geometry("%dx%d+0+0" % (w, h))
fen1.bind("<Escape>", lambda e: fen1.destroy())

############CARTE#############################################################################################
def boot():
    global can2, can1, x1, y1, snake, largeur, scor, L
    largeur = 0
    fichier = open(custom_path + '/BOSS/SNAKE/MAP.txt', 'r')
    for i in fichier:
        carte.append(list(i.replace("\n","")))
        largeur += 1
    #création map
    L = len(carte[1])*TAILLE_P
    l = largeur*TAILLE_P
    can2 = Canvas(fen1, bg="black", height= TAILLE_P, width = L)
    scor = can2.create_text(L/2,10,fill='white',text = '0')
    can2.pack(side=TOP)
    can1 = Canvas(fen1, bg="black", height= l, width = L)
    for i in range(len(carte[1])):
            for j in range(largeur):
                if carte[j][i]=='X':
                    can1.create_rectangle(i*TAILLE_P, j*TAILLE_P, i*TAILLE_P+TAILLE_P, j*TAILLE_P+TAILLE_P,width=2, fill='grey')
                    cdbloc.append([i*TAILLE_P,j*TAILLE_P])
                if carte[j][i]=='S':
                    snake = can1.create_rectangle(i*TAILLE_P, j*TAILLE_P, i*TAILLE_P+TAILLE_P, j*TAILLE_P+TAILLE_P, fill='red')
                    x1 = i*TAILLE_P
                    y1 = j*TAILLE_P
                    snak.append(snake)
                    cdsnake.append([x1,y1])
                
    fichier.close()
    can1.pack(side=LEFT)
    bouffe()
    start()
########################################################################################################################################
#DEPLACEMENTs snake 1
sens = 'début'
dx = 0#déplacements au début de la partie
dy = 0
depl = 0#deplacemetn libre(variable pour régler bug des sens qui peuvent s'inverser)
def depl_gauche(ev=None):
    global sens, dx, dy, depl
    if sens != 'droite' and depl == 0:#si deplacement n'est pas pris
        sens = 'gauche'
        dx = -TAILLE_P
        dy = 0
        depl = 1 #déplacement choisit donc on "lock" le deplacemnt
def depl_droite(ev=None):
    global sens, dx, dy, depl
    if sens != 'gauche' and depl == 0:
        sens = 'droite'
        dx = TAILLE_P
        dy = 0
        depl = 1
def depl_haut(ev=None):
    global sens, dx, dy, depl
    if sens != 'bas' and depl == 0:
        sens = 'haut'
        dx = 0
        dy = -TAILLE_P
        depl = 1
def depl_bas(ev=None):
    global sens, dx, dy, depl
    if sens != 'haut' and depl == 0:
        sens = 'bas'
        dx = 0
        dy = TAILLE_P
        depl = 1
#################################################################################################################

############ACTIONS DU SNAKE1###########################

n = 150 #vitesse du fen1.after
q = 0 #compte le nombre de queue(pour augmenter la vitesse)
h = 0 #variable pour débuter l'enregistrement des sens
s = 0 #score
jeux = True

        
def start():
    global x1, y1, sauvsens, n, cdsnake, listsens, h, q, depl, s
    if h == 0: #pour le sens du début
        listsens.append(sens)
        h = 1
    listsens[0] = sens #le sens en tête de liste sera toujours celui de la tête
    x1 = x1+dx #on définit les nouvelles coords de la tête
    y1 = y1+dy
    if [x1,y1] in cdbloc or [x1,y1] in cdsnake and [x1,y1] != cdsnake[0] :#collisions avec les bords ou avec sa queue
        can1.delete(snake)#mort
        print('dead')
        print(s)
        dead()
        return
    if [x1,y1] == [xb,yb] : #si la tête bouffe 
        can1.delete(bouf)#on efface la bouffe actuelle
        queue()#on crée un bout de queue
        bouffe()#on recrée de la bouffe  
    if q == 5:#augmentation de la vitesse tout les 5 points
        n -= 10
        q = 0
    avance()#on avance tout le reste en fonction de la tête
    cdsnake[0] = [x1,y1]#les coord en tête doivent etre ceux de la tête
    can1.coords(snake,x1,y1,x1+TAILLE_P,y1+TAILLE_P)#on crée la tête
    depl = 0
    score()
    if jeux:
        fen1.after(n, start) #on recommence
def queue():
    global cdsnake, snak, q, s
    m = cdsnake[len(cdsnake)-1]
    for i in range(len(listsens)):
        if i == len(listsens)-1:#on prend le dernier sens de la liste donc de la queue
            sensder = listsens[i]
            if sensder == 'droite':
                xq = m[0]-TAILLE_P
                yq = m[1]
            if sensder == 'gauche':
                xq = m[0]+TAILLE_P
                yq = m[1]
            if sensder == 'haut':
                xq = m[0]
                yq = m[1]+TAILLE_P
            if sensder == 'bas':
                xq = m[0]
                yq = m[1]-TAILLE_P
    Q = can1.create_rectangle(xq,yq,xq+TAILLE_P,yq+TAILLE_P, fill='white')
    snak.append(Q)
    cdsnake.append([xq,yq])
    listsens.append(sensder)
    q += 1
    s += 1
    if s == 30:
        victoire()
def avance():
    precdsnake= []
    global cdsnake, snak, listsens
    for i in range(len(snak)):
        if i == 0:
            precdsnake.append(cdsnake[i])
        if i > 0:
            l = i - 1
            precdsnake.append(cdsnake[l])
    cdsnake = precdsnake
    for i in range(len(snak)):
        l = i - 1
        can1.coords(snak[i],cdsnake[i][0],cdsnake[i][1],cdsnake[i][0]+TAILLE_P,cdsnake[i][1]+TAILLE_P)
        listsens[i] = listsens[l]
def bouffe():
    global xb, yb, bouf, carte
    xb = randrange(len(carte[1]))*TAILLE_P
    yb = randrange(largeur)*TAILLE_P
    if [xb,yb] in cdbloc or [xb,yb] in cdsnake:
        bouffe()
    else:
        bouf = can1.create_rectangle(xb, yb, xb+TAILLE_P, yb+TAILLE_P,width=2, fill='pink')
def dead():
    global n, snak
    if len(snak) == 0:
        can1.destroy()
        can2.destroy()
        boot()
    else:
        can1.delete(snak[0])
        snak.remove(snak[0])
        fen1.after(50,dead)
def score():
    global scor
    sc = str(s)
    can2.delete(scor)
    scor = can2.create_text(L/2,10, fill='white',text = sc)
def victoire():
    global jeux
    jeux = False
    Message(can1, anchor= CENTER, bg='grey' ,bd= 3,relief= RIDGE, justify= CENTER, aspect= 1000, text="CELA NE SE PEUT !").place(x= 800, y=500)
    Button(can1, text='Continuer', command= finjeux).place(x= 950, y=500)

def finjeux():
    fen1.destroy()
    sys.path.append(os.path.abspath(custom_path))
    import lapheroes
    
    
    
#Liaisons des touches snake 1
fen1.bind("<a>",depl_gauche)
fen1.bind("<d>",depl_droite)
fen1.bind("<w>",depl_haut)
fen1.bind("<s>",depl_bas)
#lancement de la partie#######
boot()
fen1.mainloop()
