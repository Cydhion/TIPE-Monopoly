##EXPLICATION DES COMPORTEMENTS
'''Comportements polarisés'''
#INVESTISSEUR : "Achète toutes les propriétés possibles" (ROUGE)
#CONSERVATEUR : "N'achète jamais de propriétés" (BLEU)

'''Comportements modérés'''
#RENTABILITE : "Achète une propriété si elle représente un gain important" (JAUNE)
#SECURITE : "Achète une propriété si elle ne représente pas un danger financier" (MARRON)
#MOYENNE : "Achète une propriété selon le rapport rentabilité/sécurité" (VERT)

##IMPORTATION DE MODULES
import matplotlib.pyplot as plt
import numpy as np
import random

##VARIABLES DE LA SITUATION ETUDIEE
VALEURS_PLATEAU={"CASES":{"Nombre":12},"START":{"Valeur":20},"HOUSE":{"Nombre":4,"Valeurs":[{"Gain":2,"Prix":15},{"Gain":5,"Prix":40},{"Gain":10,"Prix":100},{"Gain":10,"Prix":90}]},"DOLLAR":{"Nombre":0,"Valeur":5},"PRISON":{"Position":6,"Tours":3},"GO_PRISON":{"Nombre":1}}
MATRICE_PLATEAU=["S","E","H","E","E","H","P","E","H","GP","E","H"]
JOUEURS={"J1":{"Argent":150,"Comportement":"INVESTISSEUR","Couleur":"red"},"J2":{"Argent":150,"Comportement":"CONSERVATEUR","Couleur":"blue"}}
CONDITION_DE_VICTOIRE=500
SEUIL_DE_RENTABILITE=np.mean(np.array([VALEURS_PLATEAU["HOUSE"]["Valeurs"][k]["Gain"] for k in range(VALEURS_PLATEAU["HOUSE"]["Nombre"])]))
SEUIL_DE_SECURITE=np.mean(np.array([VALEURS_PLATEAU["HOUSE"]["Valeurs"][k]["Prix"] for k in range(VALEURS_PLATEAU["HOUSE"]["Nombre"])]))

##MODELISATION DES CASES
class Cell:
    def __init__(self,nature,worth):
        self.__nature=nature
        self.__worth=worth
        self.__owner="None"
    ### Définition des méthodes ###
    def getNature(self):
        '''Renvoie la nature de la case'''
        return self.__nature
    def getWorth(self):
        '''Renvoie la valeur de la case'''
        return self.__worth
    def getOwner(self):
        '''Renvoie le propriétaire de la case'''
        return self.__owner
    def modifyOwner(self,owner):
        '''Modifie le propriétaire d'une case'''
        self.__owner=owner

##MODELISATION DU PLATEAU
class Board:
    def __init__(self,nb_cell,nb_house,nb_dollar,nb_go_prison,pos_prison,prison_turns):
        self.__nb_cell=nb_cell
        self.__nb_house=nb_house
        self.__nb_dollar=nb_dollar
        self.__nb_go_prison=nb_go_prison
        self.__pos_prison=pos_prison
        self.__prison_turns=prison_turns
        self.__plate=[]
    ### Définition des méthodes ###
    def getNbCell(self):
        '''Renvoie le nombre de cases du plateau'''
        return self.__nb_cell
    def getNbHouse(self):
        '''Renvoie le nombre de cases "maison" du plateau'''
        return self.__nb_house
    def getNbDollar(self):
        '''Renvoie le nombre de cases "dollar" du plateau'''
        return self.__nb_dollar
    def getNbGo_prison(self):
        '''Renvoie le nombre de cases "go_prison" du plateau'''
        return self.__nb_go_prison
    def getPosPrison(self):
        '''Renvoie la position de la case "prison" du plateau'''
        return self.__pos_prison
    def getPrisonTurns(self):
        '''Renvoie le nombre de tours en prison'''
        return self.__prison_turns
    def getPlate(self):
        '''Renvoie la liste modélisant le plateau'''
        return self.__plate
    def getCell(self,index):
        '''Renvoie la case d'indice : index'''
        return self.getPlate()[index]
    def initializeBoard(self):
        '''Initialise le plateau selon la matrice d'implémentation'''
        nb_house=self.getNbHouse()-1
        for k in range(len(MATRICE_PLATEAU)):
            if MATRICE_PLATEAU[k]=="S":
                self.__plate.append(Cell("|START|",VALEURS_PLATEAU["START"]["Valeur"]))
            elif MATRICE_PLATEAU[k]=="H":
                self.__plate.append(Cell("~HOUSE~",VALEURS_PLATEAU["HOUSE"]["Valeurs"][nb_house]))
                nb_house=nb_house-1
            elif MATRICE_PLATEAU[k]=="D":
                self.__plate.append(Cell("~DOLLAR~",VALEURS_PLATEAU["DOLLAR"]["Valeur"]))
            elif MATRICE_PLATEAU[k]=="P":
                self.__plate.append(Cell("~PRISON~","None"))
            elif MATRICE_PLATEAU[k]=="GP":
                self.__plate.append(Cell("~GO_PRISON~","None"))
            else:
                self.__plate.append(Cell("EMPTY","None"))
    def randomizeBoard(self):
        '''Initialise le plateau aléatoirement'''
        random.shuffle(self.getPlate())
        k=0
        while self.getCell(k).getNature()!="|START|":
            k=k+1;
        temp=self.getCell(k)
        self.getPlate()[k]=self.getCell(0)
        self.getPlate()[0]=temp

##MODELISATION DES JOUEURS
class Player:
    def __init__(self,money,behaviour,colour):
        self.__money=money
        self.__behaviour=behaviour
        self.__colour=colour
        self.__position=0
        self.__prison_turns_left=0
        self.__prison_pass=0
        self.__house_pass=0
        self.__properties=[]
    ### Définition des méthodes ###
    def getMoney(self):
        '''Renvoie l'argent du joueur'''
        return self.__money
    def modifyMoney(self,quantity):
        '''Ajoute une quantité d'argent au joueur'''
        self.__money=self.getMoney()+quantity
    def getBehaviour(self):
        '''Renvoie le comportement du joueur'''
        return self.__behaviour
    def getColour(self):
        '''Renvoie la couleur associée au joueur'''
        return self.__colour
    def getPosition(self):
        '''Renvoie la position (indice du plateau) du joueur'''
        return self.__position
    def modifyPosition(self,quantity,plate_size):
        '''Modifie la position du joueur selon le lancer de dé'''
        self.__position=(self.getPosition()+quantity)%plate_size
    def setPosition(self,index):
        '''Modifie la position du joueur selon une valeur fixe'''
        self.__position=index
    def getPrisonTurnsLeft(self):
        '''Renvoie le nombre de tours restants en prison'''
        return self.__prison_turns_left
    def modifyPrisonTurnsLeft(self,turns):
        '''Modifie le nombre de tours restants en prison'''
        self.__prison_turns_left=turns
    def getPrisonPass(self):
        '''Renvoie le nombre de fois que le joueur est allé en prison'''
        return self.__prison_pass
    def modifyPrisonPass(self):
        '''Incrémente le nombre de fois que le joueur est allé en prison'''
        self.__prison_pass=self.getPrisonPass()+1
    def getHousePass(self):
        '''Renvoie le nombre de fois que le joueur est passé sur une maison'''
        return self.__house_pass
    def modifyHousePass(self):
        '''Incrémente le nombre de fois que le joueur est passé sur une maison'''
        self.__house_pass=self.getHousePass()+1
    def getProperties(self):
        '''Renvoie la liste des propriétés du joueur (indices des cases)'''
        return self.__properties
    def modifyProperties(self,property):
        '''Ajoute une propriété à la liste du joueur'''
        self.getProperties().append(property)
    def diceRoll(self):
        '''Renvoie la valeur du lancer de dé'''
        return random.randint(1,7)

##MODELISATION D'UNE PARTIE
class Game:
    def __init__(self):
        self.__plateau=Board(VALEURS_PLATEAU["CASES"]["Nombre"],VALEURS_PLATEAU["HOUSE"]["Nombre"],VALEURS_PLATEAU["DOLLAR"]["Nombre"],VALEURS_PLATEAU["GO_PRISON"]["Nombre"],VALEURS_PLATEAU["PRISON"]["Position"],VALEURS_PLATEAU["PRISON"]["Tours"])
        self.__j1=Player(JOUEURS["J1"]["Argent"],JOUEURS["J1"]["Comportement"],JOUEURS["J1"]["Couleur"])
        self.__j2=Player(JOUEURS["J2"]["Argent"],JOUEURS["J2"]["Comportement"],JOUEURS["J2"]["Couleur"])
        self.__richesses=[[self.__j1.getMoney()],[self.__j2.getMoney()]]
    ### Définition des méthodes ###
    def getBoard(self):
        '''Renvoie l'objet de type "Board" modélisant le plateau'''
        return self.__plateau
    def getPlayer1(self):
        '''Renvoie l'objet de type "Player" modélisant le joueur 1'''
        return self.__j1
    def getPlayer2(self):
        '''Renvoie l'objet de type "Player" modélisant le joueur 2'''
        return self.__j2
    def getWealth(self):
        '''Renvoie la liste des richesses'''
        return self.__richesses
    def modifyWealth(self,value1,value2):
        '''Modifie la liste des richesses'''
        self.__richesses[0].append(value1)
        self.__richesses[1].append(value2)
    def roundOfPlay(self):
        '''Simule un tour de Monopoly'''
        #Conservation de la position initiale des joueurs
        j1_old_position=self.getPlayer1().getPosition()
        j2_old_position=self.getPlayer2().getPosition()

        #Tour du joueur 1
        if self.getPlayer1().getPrisonTurnsLeft()==0:
            self.getPlayer1().modifyPosition(self.getPlayer1().diceRoll(),self.getBoard().getNbCell())
            if self.getBoard().getCell(self.getPlayer1().getPosition()).getNature()=="~DOLLAR~":
                self.getPlayer1().modifyMoney(self.getBoard().getCell(self.getPlayer1().getPosition()).getWorth())
            elif self.getBoard().getCell(self.getPlayer1().getPosition()).getNature()=="~HOUSE~":
                if self.getBoard().getCell(self.getPlayer1().getPosition()).getOwner()=="J2":
                    self.getPlayer1().modifyHousePass()
                    self.getPlayer1().modifyMoney(-(self.getBoard().getCell(self.getPlayer1().getPosition()).getWorth()["Gain"]))
                    self.getPlayer2().modifyMoney(self.getBoard().getCell(self.getPlayer1().getPosition()).getWorth()["Gain"])
                elif self.getBoard().getCell(self.getPlayer1().getPosition()).getOwner()=="None" and self.getPlayer1().getBehaviour()=="INVESTISSEUR":
                    self.getPlayer1().modifyMoney(-(self.getBoard().getCell(self.getPlayer1().getPosition()).getWorth()["Prix"]))
                    self.getPlayer1().modifyProperties(self.getPlayer1().getPosition())
                    self.getBoard().getCell(self.getPlayer1().getPosition()).modifyOwner("J1")
                elif self.getBoard().getCell(self.getPlayer1().getPosition()).getOwner()=="None" and self.getPlayer1().getMoney()>self.getBoard().getCell(self.getPlayer1().getPosition()).getWorth()["Prix"]:
                    if (self.getPlayer1().getBehaviour()=="RENTABILITE" and self.getBoard().getCell(self.getPlayer1().getPosition()).getWorth()["Gain"]>=SEUIL_DE_RENTABILITE) or (self.getPlayer1().getBehaviour()=="SECURITE" and self.getBoard().getCell(self.getPlayer1().getPosition()).getWorth["Prix"]<=SEUIL_DE_SECURITE) or (self.getPlayer1().getBehaviour()=="MOYENNE" and self.getPlayer1().getMoney()>=2*(self.getBoard().getCell(self.getPlayer1().getPosition()).getWorth()["Prix"])):
                        self.getPlayer1().modifyMoney(-(self.getBoard().getCell(self.getPlayer1().getPosition()).getWorth()["Prix"]))
                        self.getPlayer1().modifyProperties(self.getPlayer1().getPosition())
                        self.getBoard().getCell(self.getPlayer1().getPosition()).modifyOwner("J1")
            elif self.getBoard().getCell(self.getPlayer1().getPosition()).getNature()=="~GO_PRISON~":
                self.getPlayer1().modifyPrisonPass()
                self.getPlayer1().setPosition(self.getBoard().getPosPrison())
                self.getPlayer1().modifyPrisonTurnsLeft(self.getBoard().getPrisonTurns())
        else:
            self.getPlayer1().modifyPrisonTurnsLeft(self.getPlayer1().getPrisonTurnsLeft()-1)

        #Tour du joueur 2
        if self.getPlayer2().getPrisonTurnsLeft()==0:
            self.getPlayer2().modifyPosition(self.getPlayer2().diceRoll(),self.getBoard().getNbCell())
            if self.getBoard().getCell(self.getPlayer2().getPosition()).getNature()=="~DOLLAR~":
                self.getPlayer2().modifyMoney(self.getBoard().getCell(self.getPlayer2().getPosition()).getWorth())
            elif self.getBoard().getCell(self.getPlayer2().getPosition()).getNature()=="~HOUSE~":
                if self.getBoard().getCell(self.getPlayer2().getPosition()).getOwner()=="J1":
                    self.getPlayer2().modifyHousePass()
                    self.getPlayer2().modifyMoney(-(self.getBoard().getCell(self.getPlayer2().getPosition()).getWorth()["Gain"]))
                    self.getPlayer1().modifyMoney(self.getBoard().getCell(self.getPlayer2().getPosition()).getWorth()["Gain"])
                elif self.getBoard().getCell(self.getPlayer2().getPosition()).getOwner()=="None" and self.getPlayer2().getBehaviour()=="INVESTISSEUR":
                    self.getPlayer2().modifyMoney(-(self.getBoard().getCell(self.getPlayer2().getPosition()).getWorth()["Prix"]))
                    self.getPlayer2().modifyProperties(self.getPlayer2().getPosition())
                    self.getBoard().getCell(self.getPlayer2().getPosition()).modifyOwner("J2")
                elif self.getBoard().getCell(self.getPlayer2().getPosition()).getOwner()=="None" and self.getPlayer2().getMoney()>self.getBoard().getCell(self.getPlayer2().getPosition()).getWorth()["Prix"]:
                    if (self.getPlayer2().getBehaviour()=="RENTABILITE" and self.getBoard().getCell(self.getPlayer2().getPosition()).getWorth()["Gain"]>=SEUIL_DE_RENTABILITE) or (self.getPlayer2().getBehaviour()=="SECURITE" and self.getBoard().getCell(self.getPlayer2().getPosition()).getWorth["Prix"]<=SEUIL_DE_SECURITE) or (self.getPlayer2().getBehaviour()=="MOYENNE" and self.getPlayer2().getMoney()>=2*(self.getBoard().getCell(self.getPlayer2().getPosition()).getWorth()["Prix"])):
                        self.getPlayer2().modifyMoney(-(self.getBoard().getCell(self.getPlayer2().getPosition()).getWorth()["Prix"]))
                        self.getPlayer2().modifyProperties(self.getPlayer2().getPosition())
                        self.getBoard().getCell(self.getPlayer2().getPosition()).modifyOwner("J2")
            elif self.getBoard().getCell(self.getPlayer2().getPosition()).getNature()=="~GO_PRISON~":
                self.getPlayer2().modifyPrisonPass()
                self.getPlayer2().setPosition(self.getBoard().getPosPrison())
                self.getPlayer2().modifyPrisonTurnsLeft(self.getBoard().getPrisonTurns())
        else:
            self.getPlayer2().modifyPrisonTurnsLeft(self.getPlayer2().getPrisonTurnsLeft()-1)

        #Gain de la case départ
        if self.getPlayer1().getPosition()<j1_old_position and self.getPlayer1().getPosition()!=self.getBoard().getPosPrison():
            self.getPlayer1().modifyMoney(self.getBoard().getCell(0).getWorth())
        if self.getPlayer2().getPosition()<j2_old_position and self.getPlayer2().getPosition()!=self.getBoard().getPosPrison():
            self.getPlayer2().modifyMoney(self.getBoard().getCell(0).getWorth())

        #Mise à jour de la liste des richesses
        self.modifyWealth(self.getPlayer1().getMoney(),self.getPlayer2().getMoney())
    def gameOver(self):
        '''Vérifie si la partie est terminée et indique le gagnant'''
        if self.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or self.getPlayer2().getMoney()<=0:
            print("*** J1 a gagné ! ***")
            return True
        elif self.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or self.getPlayer1().getMoney()<=0:
            print("*** J2 a gagné ! ***")
            return True
        else:
            return False

##FONCTIONS DE SIMULATIONS DE PARTIES
def partiesGraphes(n):
    '''Effectue n simulations et affiche les graphes des richesses associés'''
    for k in range(n):
        #Lancement de la partie
        partie=Game()
        partie.getBoard().initializeBoard()

        #Déroulement de la partie
        while not(partie.gameOver()):
            partie.roundOfPlay()

        #Affichage du graphe des richesses au cours de la partie
        plt.plot(np.array([k for k in range(len(partie.getWealth()[0]))]),np.array(partie.getWealth()[0]),partie.getPlayer1().getColour(),label=partie.getPlayer1().getBehaviour())
        plt.plot(np.array([k for k in range(len(partie.getWealth()[1]))]),np.array(partie.getWealth()[1]),partie.getPlayer2().getColour(),label=partie.getPlayer2().getBehaviour())
        plt.xlabel("Nombre de tours")
        plt.ylabel("Argent du joueur")
        plt.title("Evolution des richesses au cours de la partie")
        plt.legend()
        plt.show()

def partiesPourcentages(n):
    '''Effectue n simulations et affiche le pourcentage de victoire des deux joueurs'''
    j1_victoires=0
    j2_victoires=0
    for k in range(n):
        #Lancement de la partie
        partie=Game()
        partie.getBoard().initializeBoard()

        #Initialisation des conditions de victoire
        j1_gagnant=partie.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer2().getMoney()<=0
        j2_gagnant=partie.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer1().getMoney()<=0

        #Déroulement de la partie
        while not(j1_gagnant or j2_gagnant):
            partie.roundOfPlay()
            j1_gagnant=partie.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer2().getMoney()<=0
            j2_gagnant=partie.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer1().getMoney()<=0

        #Mise à jour des victoires
        if j1_gagnant:
            j1_victoires=j1_victoires+1
        else:
            j2_victoires=j2_victoires+1

    print("Le joueur 1 a gagné",j1_victoires,"parties sur",n)
    print("Pourcentage de victoire : "+str((j1_victoires/n)*100)+"%")
    print("Le joueur 2 a gagné",j2_victoires,"parties sur",n)
    print("Pourcentage de victoire : "+str((j2_victoires/n)*100)+"%")

def grapheVictoire_Parties(n):
    '''Affiche le graphe du pourcentage de victoire en fonction du nombre de parties jouées (n max)'''
    x=[k for k in range(n+1)]
    y_j1=[0]
    y_j2=[0]
    i=1
    while i<=n:
        j1_victoires=0
        j2_victoires=0
        for k in range(i):
            #Lancement de la partie
            partie=Game()
            partie.getBoard().initializeBoard()

            #Initialisation des conditions de victoire
            j1_gagnant=partie.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer2().getMoney()<=0
            j2_gagnant=partie.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer1().getMoney()<=0

            #Déroulement de la partie
            while not(j1_gagnant or j2_gagnant):
                partie.roundOfPlay()
                j1_gagnant=partie.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer2().getMoney()<=0
                j2_gagnant=partie.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer1().getMoney()<=0

            #Mise à jour des victoires
            if j1_gagnant:
                j1_victoires=j1_victoires+1
            else:
                j2_victoires=j2_victoires+1

        #Mise à jour des données
        y_j1.append(j1_victoires/i)
        y_j2.append(j2_victoires/i)
        i=i+1

    plt.plot(np.array(x),np.array(y_j1),partie.getPlayer1().getColour(),label=partie.getPlayer1().getBehaviour())
    plt.plot(np.array(x),np.array(y_j2),partie.getPlayer2().getColour(),label=partie.getPlayer2().getBehaviour())
    plt.xlabel("Nombre de parties jouées")
    plt.ylabel("Pourcentage de victoire")
    plt.title("Influence du nombre de parties jouées")
    plt.legend()
    plt.show()

def grapheVictoire_Maisons(n):
    '''Affiche le graphe du pourcentage de victoire en fonction du nombre de fois que le joueur est passé sur une maison (n simulations)'''
    j1_values={}
    j2_values={}
    for k in range(n):
        #Lancement de la partie
        partie=Game()
        partie.getBoard().initializeBoard()

        #Initialisation des conditions de victoire
        j1_gagnant=partie.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer2().getMoney()<=0
        j2_gagnant=partie.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer1().getMoney()<=0

        #Déroulement de la partie
        while not(j1_gagnant or j2_gagnant):
            partie.roundOfPlay()
            j1_gagnant=partie.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer2().getMoney()<=0
            j2_gagnant=partie.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer1().getMoney()<=0

        #Mise à jour des données
        if partie.getPlayer1().getHousePass() not in j1_values.keys():
            j1_values[partie.getPlayer1().getHousePass()]={"Victoires":0,"Parties":0}
        if partie.getPlayer2().getHousePass() not in j2_values.keys():
            j2_values[partie.getPlayer2().getHousePass()]={"Victoires":0,"Parties":0}
        j1_values[partie.getPlayer1().getHousePass()]["Victoires"]=j1_values[partie.getPlayer1().getHousePass()]["Victoires"]+j1_gagnant
        j1_values[partie.getPlayer1().getHousePass()]["Parties"]=j1_values[partie.getPlayer1().getHousePass()]["Parties"]+1
        j2_values[partie.getPlayer2().getHousePass()]["Victoires"]=j2_values[partie.getPlayer2().getHousePass()]["Victoires"]+j2_gagnant
        j2_values[partie.getPlayer2().getHousePass()]["Parties"]=j2_values[partie.getPlayer2().getHousePass()]["Parties"]+1

    #Abscisse et ordonnée du joueur 1
    x_j1=[]
    y_j1=[]
    for k in range(max(j1_values.keys())+1):
        if k in j1_values.keys():
            x_j1.append(k)
            y_j1.append(j1_values[k]["Victoires"]/j1_values[k]["Parties"])

    #Abscisse et ordonnée du joueur 2
    x_j2=[]
    y_j2=[]
    for k in range(max(j2_values.keys())+1):
        if k in j2_values.keys():
            x_j2.append(k)
            y_j2.append(j2_values[k]["Victoires"]/j2_values[k]["Parties"])

    plt.plot(np.array(x_j1),np.array(y_j1),partie.getPlayer1().getColour(),label=partie.getPlayer1().getBehaviour())
    plt.xlabel("Nombre de passages sur une maison adverse")
    plt.ylabel("Pourcentage de victoire")
    plt.title("Influence du nombre de passages sur les maisons adverses")
    plt.legend()
    plt.show()

    plt.plot(np.array(x_j2),np.array(y_j2),partie.getPlayer2().getColour(),label=partie.getPlayer2().getBehaviour())
    plt.xlabel("Nombre de passages sur une maison adverse")
    plt.ylabel("Pourcentage de victoire")
    plt.title("Influence du nombre de passages sur les maisons adverses")
    plt.legend()
    plt.show()

def grapheVictoire_Proprietes(n):
    '''Affiche le graphe du pourcentage de victoire en fonction des propriétés du joueur (n simulations)'''
    j1_values={}
    j2_values={}
    for k in range(n):
        #Lancement de la partie
        partie=Game()
        partie.getBoard().initializeBoard()

        #Initialisation des conditions de victoire
        j1_gagnant=partie.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer2().getMoney()<=0
        j2_gagnant=partie.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer1().getMoney()<=0

        #Déroulement de la partie
        while not(j1_gagnant or j2_gagnant):
            partie.roundOfPlay()
            j1_gagnant=partie.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer2().getMoney()<=0
            j2_gagnant=partie.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer1().getMoney()<=0

        #Mise à jour des données
        if len(partie.getPlayer1().getProperties()) not in j1_values.keys():
            j1_values[len(partie.getPlayer1().getProperties())]={"Victoires":0,"Parties":0}
        if len(partie.getPlayer2().getProperties()) not in j2_values.keys():
            j2_values[len(partie.getPlayer2().getProperties())]={"Victoires":0,"Parties":0}
        j1_values[len(partie.getPlayer1().getProperties())]["Victoires"]=j1_values[len(partie.getPlayer1().getProperties())]["Victoires"]+j1_gagnant
        j1_values[len(partie.getPlayer1().getProperties())]["Parties"]=j1_values[len(partie.getPlayer1().getProperties())]["Parties"]+1
        j2_values[len(partie.getPlayer2().getProperties())]["Victoires"]=j2_values[len(partie.getPlayer2().getProperties())]["Victoires"]+j2_gagnant
        j2_values[len(partie.getPlayer2().getProperties())]["Parties"]=j2_values[len(partie.getPlayer2().getProperties())]["Parties"]+1

    #Abscisses et ordonnées des joueurs 1 et 2
    x_j1=[]
    x_j2=[]
    y_j1=[]
    y_j2=[]
    for k in range(VALEURS_PLATEAU["HOUSE"]["Nombre"]+1):
        if k in j1_values.keys():
            x_j1.append(k)
            y_j1.append(j1_values[k]["Victoires"]/j1_values[k]["Parties"])
        if k in j2_values.keys():
            x_j2.append(k)
            y_j2.append(j2_values[k]["Victoires"]/j2_values[k]["Parties"])

    plt.plot(np.array(x_j1),np.array(y_j1),partie.getPlayer1().getColour(),label=partie.getPlayer1().getBehaviour())
    plt.xlabel("Nombre de propriétés possédées")
    plt.ylabel("Pourcentage de victoire")
    plt.title("Influence du nombre de propriétés possédées")
    plt.legend()
    plt.show()

    plt.plot(np.array(x_j2),np.array(y_j2),partie.getPlayer2().getColour(),label=partie.getPlayer2().getBehaviour())
    plt.xlabel("Nombre de propriétés possédées")
    plt.ylabel("Pourcentage de victoire")
    plt.title("Influence du nombre de propriétés possédées")
    plt.legend()
    plt.show()

def grapheVictoire_Prison(n):
    '''Affiche le graphe du  pourcentage de victoire en fonction du nombre de passage en prison du joueur (n simulations)'''
    j1_values={}
    j2_values={}
    for k in range(n):
        #Lancement de la partie
        partie=Game()
        partie.getBoard().initializeBoard()

        #Initialisation des conditions de victoire
        j1_gagnant=partie.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer2().getMoney()<=0
        j2_gagnant=partie.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer1().getMoney()<=0

        #Déroulement de la partie
        while not(j1_gagnant or j2_gagnant):
            partie.roundOfPlay()
            j1_gagnant=partie.getPlayer1().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer2().getMoney()<=0
            j2_gagnant=partie.getPlayer2().getMoney()>=CONDITION_DE_VICTOIRE or partie.getPlayer1().getMoney()<=0

        #Mise à jour des données
        if partie.getPlayer1().getPrisonPass() not in j1_values.keys():
            j1_values[partie.getPlayer1().getPrisonPass()]={"Victoires":0,"Parties":0}
        if partie.getPlayer2().getPrisonPass() not in j2_values.keys():
            j2_values[partie.getPlayer2().getPrisonPass()]={"Victoires":0,"Parties":0}
        j1_values[partie.getPlayer1().getPrisonPass()]["Victoires"]=j1_values[partie.getPlayer1().getPrisonPass()]["Victoires"]+j1_gagnant
        j1_values[partie.getPlayer1().getPrisonPass()]["Parties"]=j1_values[partie.getPlayer1().getPrisonPass()]["Parties"]+1
        j2_values[partie.getPlayer2().getPrisonPass()]["Victoires"]=j2_values[partie.getPlayer2().getPrisonPass()]["Victoires"]+j2_gagnant
        j2_values[partie.getPlayer2().getPrisonPass()]["Parties"]=j2_values[partie.getPlayer2().getPrisonPass()]["Parties"]+1

    #Abscisse et ordonnée du joueur 1
    x_j1=[]
    y_j1=[]
    for k in range(max(j1_values.keys())+1):
        if k in j1_values.keys():
            x_j1.append(k)
            y_j1.append(j1_values[k]["Victoires"]/j1_values[k]["Parties"])

    #Abscisse et ordonnée du joueur 2
    x_j2=[]
    y_j2=[]
    for k in range(max(j2_values.keys())+1):
        if k in j2_values.keys():
            x_j2.append(k)
            y_j2.append(j2_values[k]["Victoires"]/j2_values[k]["Parties"])

    plt.plot(np.array(x_j1),np.array(y_j1),partie.getPlayer1().getColour(),label=partie.getPlayer1().getBehaviour())
    plt.xlabel("Nombre de passages en prison")
    plt.ylabel("Pourcentage de victoire")
    plt.title("Influence du nombre de passages en prison")
    plt.legend()
    plt.show()

    plt.plot(np.array(x_j2),np.array(y_j2),partie.getPlayer2().getColour(),label=partie.getPlayer2().getBehaviour())
    plt.xlabel("Nombre de passages en prison")
    plt.ylabel("Pourcentage de victoire")
    plt.title("Influence du nombre de passages en prison")
    plt.legend()
    plt.show()

##ZONE DE SIMULATIONS
#Données relatives aux parties jouées
#partiesGraphes(1)
#partiesPourcentages(100)

#Influence des paramètres sur le pourcentage de victoire
#grapheVictoire_Parties(400)
grapheVictoire_Maisons(100)
#grapheVictoire_Proprietes(100)
#grapheVictoire_Prison(100)