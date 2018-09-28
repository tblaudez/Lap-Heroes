#!/usr/bin/python3.4

#Importation
from tkinter import *
import random, os, sys

#Lancement de Tkinter
fen1 = Tk()
custom_path = '/Users/tblaudez/Downloads/test'


#TAILLES
TAILLE_P = 60

#Fullscreen
#w, h = fen1.winfo_screenwidth(), fen1.winfo_screenheight() #On prend les donnée de l'écran et on le met ne plein écran
#fen1.overrideredirect(1)
#fen1.geometry("%dx%d+0+0" % (w, h))
fen1.bind("<Escape>", lambda e: fen1.destroy())

mapact = '1'
mapsave = '3' #On choisit la map où le personnage commence

d = 0
life = 20


#######################################################################
#PERSONNAGE
imagelink = ['linkdroite','linkgauche','linkface','linkdos','linkdosE','linkfaceE','linkgaucheE','linkdroiteE']
for i in imagelink:
    image = PhotoImage(file = '%s/Images/Personnages/link/%s.gif' %(custom_path,i)) # Il s'agit d'une boucle où va chercher les images dans le dossier et on les transforme en image TK du même nom (pareil pour le decor et les PNJ)
    exec("%s = image" %i)


#DECOR
imagedecor = ['arbre','goudron','deck','mur','bibliotheque','ordinateurG','ordinateurD','ordinateurB','ordinateurH','porte',
               'bancB','bancH','bancG','bancD','casier','noir','carreaux','porte','toilettes','robinetsG','robinetsD','deck',
               'goudron','table','algeco','ordinateurG','ordinateurD','ordinateurB','ordinateurH'] #images

for i in imagedecor:
    exec("%s = PhotoImage(file = '%s/Images/Decor/%s.gif')" %(i,custom_path,i))

#PNJ
for i in range(1,24):
    exec("pnj%s = PhotoImage(file = '%s/Images/PNJ/pnj%s.gif')" %(i,custom_path,i))
    
    

grosarbre = PhotoImage(file = custom_path + '/Images/Decor/arbre.gif').zoom(8,8)
fare = PhotoImage(file = custom_path + '/Images/Decor/fare.gif').zoom(3,3)
portefermee = porte

###########################################################################

def start(nm): #nm : numero map
    global carte, cdbloc, largeur, fichier, listmonstre, ennemie, sortie, listpnj, cdpnj, eleve, cdmonstre, custom_path #La fonction primaire : elle crée/reinitialise les listes puis lance la création de map
    carte, cdbloc, listmonstre, cdmonstre, listpnj, cdpnj = [],[],[],[],[],[]
    sortie, eleve = {}, {}
    largeur = 0

    fichier = open('%s/MAPS/MAP%s.txt' %(custom_path,nm), 'r')
    for i in fichier:
        carte.append(list(i.replace("\n",""))) #Lecture du fichier adéquat et création de la carte sous forme de liste
        largeur += 1
    creamap()
    vie(0)

    fichier.close() #On ferme le fichier
        
        

def creamap():
    global carte, P, x1, y1, nm, largeur, cdbloc, can1,can2, position, base, ennemie, listmonstre
    position = 'bas'
    L = len(carte[1])*TAILLE_P
    l = largeur*TAILLE_P
    can1 = Canvas(fen1, bg="darkgrey", height= l, width = L) #Création du canvas
    can2 = Canvas(can1, bg="darkgrey", height= 50, width = 100)
    can2.place(x=60, y= 60)

    for i in range(len(carte[1])): #On balaye la carte (.txt) et on crée le sol à chaque bloc
        for j in range(largeur):
                can1.create_image(i*TAILLE_P, j*TAILLE_P, anchor=NW, image=goudron)
                if mapact in ['5','3','&','-','8','(','_']:
                    can1.create_image(i*TAILLE_P, j*TAILLE_P, anchor=NW, image=deck)  #On choisit le sol de base pour les maps (ex : toilettes = carreaux, CDI = deck)
                elif mapact in ['7']:
                    can1.create_image(i*TAILLE_P, j*TAILLE_P, anchor=NW, image=carreaux)


    sprite = {'X':mur, 'C':casier, 'N':noir, 'F':fare, 'Z':grosarbre,'T':table,'D':deck,'A':arbre,'L':bibliotheque,
             '>':bancD,'<':bancG,'H':bancB,'^':bancH,'%':porte,'@':portefermee,'W':toilettes,'G':goudron,'B':algeco}

    
    if mapact == '3':
        sprite['>'] = ordinateurD
        sprite['<'] = ordinateurG
        sprite['^'] = ordinateurH #< > ^ µ représentent le sens de certain objets, ils changent de 'skins' selon la map où l'on se trouve (ex : toilettes = robinets, CDI = bureaux avec ordi)
        sprite[';'] = ordinateurB
    if mapact == '7':
        sprite['>'] = robinetsD
        sprite['<'] = robinetsG
        
    for t in sprite:
        for i in range(len(carte[1])):
            for j in range(largeur):
                if carte[j][i]== t: #Pour tout les éléments dans le dict 'sprite', si un caractère dans le bloc note correspond à un élément du dict alors on crée la photo correspondant à ce caractère
                    can1.create_image(i*TAILLE_P, j*TAILLE_P, anchor=NW, image=sprite[t])

    for i in range(23):
        t = str(chr(65+i).lower())
        exec("eleve[t] = pnj%s" %(i+1))
        
    for t in eleve:
        for i in range(len(carte[1])):
            for j in range(largeur):
                if carte[j][i]== t: #Pour tout les éléments dans le dict 'sprite', si un caractère dans le bloc note correspond à un élément du dict alors on crée la photo correspondant à ce caractère
                    can1.create_image(i*TAILLE_P, j*TAILLE_P, anchor=NW, image=eleve[t])

    for i in range(len(carte[1])):
            for j in range(largeur):
                if carte[j][i].isdigit() == True:                                                               #Dans ce gros paquet se trouvent les éléments 'spéciaux', ceux qui doivent avoir leurs
                    can1.create_image(i*TAILLE_P, j*TAILLE_P, anchor = NW, image = porte)                       #coordonnées enregistrées dans des listes/dict pour la suite du jeux
                    sortie[carte[j][i]] = [i*TAILLE_P, j*TAILLE_P]
                elif carte[j][i] in ['&','-','(','_']:
                    sortie[carte[j][i]] = [i*TAILLE_P, j*TAILLE_P]
                    
                if carte[j][i] in ['<','>','^',';','%','@'] or carte[j][i].isalpha() == True: #Ici sont réunis tout les blocs qui engendrent des collisions
                    cdbloc.append([i*TAILLE_P, j*TAILLE_P])
                    if (carte[j][i] in ['<','>'] and mapact == '7') or (carte[j][i] == 'Z' and mapact == '1'):
                        cdbloc.remove([i*TAILLE_P, j*TAILLE_P])

                if carte[j][i].islower() == True or carte[j][i] in ['@','C']:
                    cdpnj.append([i*TAILLE_P,j*TAILLE_P]) #Coordonnées d'objets pour les dialogues
                    listpnj.append(carte[j][i])

                if carte[j][i] == '}':
                    x = i*TAILLE_P
                    y = j*TAILLE_P
                    MONSTRE = can1.create_rectangle(x, y, x+TAILLE_P,y+TAILLE_P, fill='red')
                    cdmonstre.append([x,y])
                    listmonstre.append(MONSTRE)

    for i in sortie:
         if i == mapsave:
            x1 = sortie[i][0]
            y1 = sortie[i][1]
            P = can1.create_image( x1, y1,anchor = NW, image= linkface) #Ici on définie les coordonnées du joueur en fonction de la sortie d'où il vient
                
    can1.pack(side=LEFT)





"""Fonctions de deplacement qui invoquent la fonction "avance" avec differents paramètres pour chaque type de deplacement"""
"""De plus, chaque fonction change le sprite du personnage afin de le tourner dans le bon sens"""
def depl_gauche(ev=None):
    global P, position, can1
    avance(-TAILLE_P,0)
    can1.delete(P)
    P = can1.create_image(x1,y1,anchor = NW, image= linkgauche)
    position = 'gauche'
   
def depl_droite(ev=None):
    global P, position, can1
    avance(TAILLE_P,0)
    can1.delete(P)
    P = can1.create_image(x1,y1,anchor = NW, image= linkdroite)
    position = 'droite'

def depl_haut(ev=None):
    global P, position, can1
    avance(0, -TAILLE_P)
    can1.delete(P)
    P = can1.create_image(x1,y1,anchor = NW, image= linkdos)
    position = 'haut'

def depl_bas(ev=None):
    global P, position, can1
    can1.delete(P)
    P = can1.create_image(x1,y1,anchor = NW, image= linkface)
    avance(0, TAILLE_P)
    position = 'bas'
        

           
def avance(gd, hb):
    """Fonction qui actualise la position du perso à chaque touche préssée et annule celle-ci si la-dite position se trouve dans un mur"""
    global x1, y1, cdbloc, can1, listmonstre, mapsave, mapact, d
    
    x2, y2 = x1, y1 #On crée des coordonnées 'de sauvegarde'
    x1 += gd
    y1 += hb #On change les coordonnées du joueur sans les appliquer
    collision = False #De base il n'y a pas de collision

    if [x1, y1] in cdbloc or [x1,y1] in cdpnj or [x1,y1] in cdmonstre:
        collision = True

    if collision == False: #s'il n'y a pas eu de collision, on applique le déplacement
        can1.coords(P,x1,y1) 

    elif collision == True: #S'il y a eu une collision, on revient au coordonnées 'de sauvegarde'
        x1 = x2
        y1 = y2


    for i in sortie:
        if [x1,y1] == sortie[i]: #Si le joueur se retrouve sur une sortie on actualse la map 'actuelle' et la map 'de sauvegarde' (d'où le joeur vient)
            can1.destroy()
            mapsave = mapact
            mapact = i
            collision = 3
            start(mapact) #On lance la fonction primaire sur une nouvelle map -> on supprime tout et rebelotte, retour au début du programme
            return
    if d == 1:
        try:
            can1.after(100, dis.destroy)
            can1.after(100, butboss.destroy)
        except NameError:
            d = 0
        d = 0
    
"""Cette fonction remplace pendant quelques dizièmes de secondes le sprite du joueur afin donner
l'illusion d'un coup d'épée, le sens du joeur est respecté"""
def coup(ev=None):
    global position, P,  x1, y1, PE
    can1.coords(P,2000,2000) #On 'téléporte' le personnage loins hors de l'écran
    fen1.unbind("<space>")
    fen1.unbind("<a>")
    fen1.unbind("<d>")
    fen1.unbind("<w>")
    fen1.unbind("<s>")

    if position == "haut":
        xE = x1
        yE = y1-TAILLE_P 
        PE = can1.create_image(x1, y1, anchor = NW, image = linkdosE)
        
    elif position == "gauche":
        xE = x1-TAILLE_P
        yE = y1
        PE = can1.create_image(x1, y1, anchor = NW, image = linkgaucheE) #Ici on chnage le sprite du joeur et on définit les coordonnées de la 'case' touchée par l'épée
        
    elif position == "droite":
        xE = x1+TAILLE_P
        yE = y1
        PE = can1.create_image(x1, y1, anchor = NW, image = linkdroiteE)
        
    elif position == "bas":
        xE = x1
        yE = y1+TAILLE_P
        PE = can1.create_image(x1, y1, anchor = NW, image = linkfaceE)
            
    tuer(xE, yE)
    fen1.after(250, delete) #Après 250ms on remet out en ordre avec la fonction delete()
    

def tuer(xE, yE):
    for i in range(len(listmonstre)):
        if [xE, yE] == cdmonstre[i]: #Si un monstre se trouve sur la case visée, on le détruit
            can1.delete(listmonstre[i])
            listmonstre.remove(listmonstre[i])
            cdmonstre.remove(cdmonstre[i])
            break
            
def delete():
    global P,x1, y1
    can1.delete(PE)
    can1.coords(P,x1,y1) #On supprime le sprite 'épée' et on rammène le perso à sa place de départ
    fen1.bind("<a>",depl_gauche)
    fen1.bind("<d>",depl_droite)
    fen1.bind("<w>",depl_haut)
    fen1.bind("<s>",depl_bas)
    fen1.bind("<space>",coup)


def IA():
    for i in range(len(listmonstre)):
        xf = cdmonstre[i][0]
        yf = cdmonstre[i][1]
        ennemi_avance(xf, yf, i)
    fen1.after(600, IA)

def ennemi_avance(xf,yf,i):
    num = random.randint(1,4)
    if xf == x1 and yf > y1:
        num = 4
    elif xf == x1 and yf < y1:
        num = 3
    elif yf == y1 and xf > x1:
        num = 2
    elif yf == y1 and xf < x1:
        num = 1
        
    if num == 1:
        mvtfantx = TAILLE_P
        mvtfanty = 0
    elif num == 2:
        mvtfantx = -TAILLE_P
        mvtfanty = 0
    elif num == 3:
        mvtfantx = 0
        mvtfanty = TAILLE_P
        
    elif num == 4:
        mvtfantx = 0
        mvtfanty =  -TAILLE_P

    xfi = xf + mvtfantx
    yfi = yf + mvtfanty

    if [xfi, yfi] == [x1,y1]:
        vie(-2)
    elif [xfi , yfi] not in cdbloc and [xfi , yfi] not in cdmonstre and [xfi, yfi] != [x1,y1]:
        can1.coords(listmonstre[i], xfi, yfi, xfi+TAILLE_P, yfi+TAILLE_P)
        cdmonstre[i][0] = xfi
        cdmonstre[i][1] = yfi
    else:
        xfi = xf - mvtfantx
        yfi = yf - mvtfanty


def dialogue(ev=None):
    global dis, d, butboss, custom_path
    choix = []
    if d != 1:
        if [x1, y1-TAILLE_P] in cdpnj:  #Si le joueur se trouve sous un pnj présent dans la liste, on ouvre la boite di dialogue correspondant au-dit pnj

            pnj = listpnj[cdpnj.index([x1, y1-TAILLE_P])]
            if pnj.islower() == False:
                pnj =  '#' + pnj

            d = 1
            dialogue = open('%s/Dialogues/%s.txt' %(custom_path,pnj), 'r')
            paroles = dialogue.read()

            if '@' in paroles:
                paroles = random.choice(paroles.splitlines()).replace("@","")

            dis = Message(can1, anchor= CENTER, bg='grey', bd= 3, relief= RIDGE, justify= CENTER, aspect= 1000, text=paroles)
            dis.place(anchor= NW, x= 12*TAILLE_P, y= 15*TAILLE_P, width= 700, height= 120)

            if pnj in ['j','o','w']:
                butboss = Button(can1,text='Commencer', command= lambda: start_boss(pnj))
                butboss.place(anchor = NW, x = 17*TAILLE_P, y = 16.5*TAILLE_P)
            dialogue.close()

def start_boss(boss):
    global custom_path
    if boss == 'j':
        sys.path.append(os.path.abspath("%s/BOSS/SNAKE" %custom_path))
        fen1.destroy()
        import snake
    elif boss == 'w':
        sys.path.append(os.path.abspath("%s/BOSS/PACMAN" %custom_path))
        fen1.destroy()
        import pacman

def vie(dmg):
    global life, hp
    life += dmg
    if dmg != 0:
        hp.destroy()
    hp = Message(can2, anchor= CENTER, bg='grey', bd= 3, relief= RIDGE, justify= CENTER, aspect= 1000, text='%s/20' %life)
    hp.pack()

    if life == 0:
        fen1.destroy()
    
    
        


#Liaison des touches
fen1.bind("<a>",depl_gauche)
fen1.bind("<d>",depl_droite)    
fen1.bind("<w>",depl_haut)
fen1.bind("<s>",depl_bas) #on assigne toute les touche à des fonctions
fen1.bind("<e>", dialogue)
fen1.bind("<space>", coup)


start(1) #On démarre le jeux avec la fonction primaire
IA()
fen1.mainloop()

    
    
















