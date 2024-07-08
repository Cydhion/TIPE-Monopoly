import numpy as np
import matplotlib.pyplot as plt

## Courbe de Base
x = np.arange(0,110,1)
y0 = 0*x

## Terrain

Plateau1 = np.array(
[
[0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6,1/6,0  ,1/6,1/6],
[1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6,0  ,1/6,1/6],
[1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6,0  ,1/6,1/6],
[1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6],
[1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6],
[1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6],
[1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,1  ,0  ,0  ],
[0  ,1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ],
[0  ,0  ,1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ],
[0  ,0  ,0  ,1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ],
[0  ,0  ,0  ,0  ,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ],
[0  ,0  ,0  ,0  ,0  ,1/6,1/6,1/6,1/6,0  ,1/6,0  ],
])

def Plateau(Ch):
    Plateau2 = np.array(
    [
    [0  ,0         ,0  ,0  ,0  ,0  ,1/6,1/6,1/6,0  ,1/6,1/6,0    ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ],
    [1/6,0         ,0  ,0  ,0  ,0  ,0  ,1/6,1/6,0  ,1/6,1/6,0    ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ],
    [1/6,1/6*(1-Ch),0  ,0  ,0  ,0  ,0  ,0  ,1/6,0  ,1/6,1/6,0    ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ],
    [1/6,1/6*(1-Ch),1/6,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6,0    ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ],
    [1/6,1/6*(1-Ch),1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6,0    ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ],
    [1/6,1/6*(1-Ch),1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6,0    ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ],
    [1/6,1/6*(1-Ch),1/6,1/6,1/6,1/6,0  ,0  ,0  ,1  ,0  ,0  ,0    ,1  ,0    ,0    ,1/6  ,1/6  ,1/6  ,1/6  ,1/6  ,1/6  ],
    [0  ,1/6*(1-Ch),1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ,0    ,0  ,0    ,0    ,0    ,1/6  ,1/6  ,1/6  ,1/6  ,1/6  ],
    [0  ,0         ,1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ,0    ,0  ,0    ,0    ,0    ,0    ,1/6  ,1/6  ,1/6  ,1/6  ],
    [0  ,0         ,0  ,1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0    ,0  ,0    ,0    ,0    ,0    ,0    ,1/6  ,1/6  ,1/6  ],
    [0  ,0         ,0  ,0  ,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0    ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,1/6  ,1/6  ],
    [0  ,0         ,0  ,0  ,0  ,1/6,1/6,1/6,1/6,0  ,1/6,0  ,0    ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,1/6  ],
    [0  ,Ch        ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0    ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ],
    [0  ,0         ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1/6  ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ],
    [0  ,0         ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1/6  ,0  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ,0    ],
    [0  ,0         ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1/6  ,0  ,1/6  ,0    ,0    ,0    ,0    ,0    ,0    ,0    ],
    [0  ,0         ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1/6  ,0  ,1/6  ,1/6  ,0    ,0    ,0    ,0    ,0    ,0    ],
    [0  ,0         ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1/6  ,0  ,1/6  ,1/6  ,1/6  ,0    ,0    ,0    ,0    ,0    ],
    [0  ,0         ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,1/6  ,0  ,1/6  ,1/6  ,1/6  ,1/6  ,0    ,0    ,0    ,0    ],
    [0  ,0         ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0    ,0  ,1/6  ,1/6  ,1/6  ,1/6  ,1/6  ,0    ,0    ,0    ],
    [0  ,0         ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0    ,0  ,1/6  ,1/6  ,1/6  ,1/6  ,1/6  ,1/6  ,0    ,0    ],
    [0  ,0         ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0    ,0  ,0    ,1/6  ,1/6  ,1/6  ,1/6  ,1/6  ,1/6  ,0    ],
    ])
    return Plateau2
'''Attention Ch = choix de passer dans l'autre branche 1 = tu change de branche sinon 0'''

Test1 = np.array(
[
[0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6,1/6,1/6,1/6,1/6],
[1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6,1/6,1/6,1/6],
[1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6,1/6,1/6],
[1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6,1/6],
[1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6,1/6],
[1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ,1/6],
[1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ,0  ],
[0  ,1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ,0  ],
[0  ,0  ,1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ,0  ],
[0  ,0  ,0  ,1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ,0  ],
[0  ,0  ,0  ,0  ,1/6,1/6,1/6,1/6,1/6,1/6,0  ,0  ],
[0  ,0  ,0  ,0  ,0  ,1/6,1/6,1/6,1/6,1/6,1/6,0  ],
])

## Impact du Choix

choix = 1

## Maison/rentablité ; Coût par Gain
M2 = [15,2]
M6 = [40,5]
M9 = [100,10]
M12 = [90,10]
M20 = [50,30]

def transi(y,PrM,x):
    a = (y[1]-y[0])
    for i in range(len(x)):
        if PrM - x[i] > 0 :
            y[i] = 0
        else :
            y[i] = y[i] - a*np.ceil(PrM)

    return y

''' Rentabilités'''

P = Plateau(choix)
for i in range(50):
    P = np.dot(P,P)

R2 = (P[2-1][0])*M2[1]*x
R6 = (P[6-1][0])*M6[1]*x
R9 = (P[9-1][0])*M9[1]*x
R12 = (P[12-1][0])*M12[1]*x
R20 = (P[20-1][0])*M20[1]*x

    ## Proba de tomber sur une maison
plt.plot(x,P[1][0]*x,'r-',label='Maison case 2')
plt.plot(x,P[5][0]*x,'b-',label='Maison case 6')
plt.plot(x,P[8][0]*x,'k-',label='Maison case 9')
plt.plot(x,P[11][0]*x,'g-',label='Maison case 12')
plt.plot(x,P[19][0]*x,'y-',label='Maison case 20')
plt.plot(x,y0+1,'k--')
plt.grid()
plt.legend()
plt.show()

PrM2 = 1/P[1][0]
PrM6 = 1/P[5][0]
PrM9 = 1/P[8][0]
PrM12 = 1/P[11][0]
if P[19][0] == 0:
    PrM20 = 0
else:
    PrM20 = 1/P[19][0]

    ## Courbe rentabilité
y2 = R2 - M2[0]
y6 = R6 - M6[0]
y9 = R9 - M9[0]
y12 = R12 - M12[0]
y20 = R20 - M20[0]

R2tr = transi(R2,PrM2,x)
R6tr = transi(R6,PrM6,x)
R9tr = transi(R9,PrM9,x)
R12tr = transi(R12,PrM12,x)
R20tr = transi(R20,PrM20,x)

y2tr = transi(y2,PrM2,x)
y6tr = transi(y6,PrM6,x)
y9tr = transi(y9,PrM9,x)
y12tr = transi(y12,PrM12,x)
y20tr = transi(y20,PrM20,x)

        ## Affichage
plt.plot(x,y2,'r-',label='Maison case 2')
plt.plot(x,y6,'b-',label='Maison case 6')
plt.plot(x,y9,'k-',label='Maison case 9')
plt.plot(x,y12,'g-',label='Maison case 12')
plt.plot(x,y20,'y-',label='Maison case 20')
plt.plot(x,y0,'k--')
plt.legend()
plt.show()

## Argent
GainDepart = 20
NbLancerParTour = 12/3.5

Atour = 150 + (GainDepart/NbLancerParTour)*x


RevenueInvestisseur = y2tr + y6tr + y9tr + y12tr + y20tr
RevenueConservateur = - (R2tr + R6tr +R9tr + R12tr - R20tr)
RevenueRentabilité = y9tr + y12tr - (R2tr + R6tr)  + y20tr
RevenueSécurité = y2tr + y6tr - (R9tr + R12tr)  - R20tr
RevenueMoyenne = 0 ## ??????

  ## Affichage
A1 = Atour + RevenueRentabilité
A2 = Atour + RevenueSécurité

plt.plot(x,A1,color='yellow',label='Rentabilité')
plt.plot(x,A2,color='brown',label='Sécurité')
plt.plot(x,0*x + 500,'k--')
plt.grid()
plt.legend()
plt.show()

  ## Croisement

a1 = np.polyfit(x,A1,1)
a2 = np.polyfit(x,A2,1)
t = (a2[1] - a1[1])/(a1[0] - a2[0])

print( "Nombre de tour avant le changement d'avantage : ", t )
print( "Argent obtenu par les deux joueurs en même temps : ", a1[0]*t + a1[1] )

## Chance Max
print(np.max(Plateau(choix)))
T = Plateau(choix)
for i in range(50):
    T = np.dot(T,Plateau(choix))
    print(np.max(T),"\n")
## Variation Plateau
print(Plateau(choix),"\n")
T = Plateau(choix)
for i in range(50):
    T = np.dot(T,Plateau(choix))
print(np.round(T,3),"\n")

### Test
P = Plateau(choix)
for i in range(50):
    P = np.dot(P,P)
print(np.round(P[3-1][0],3))
print(np.round(P[6-1][0],3))
print(np.round(P[20-1][0],3),"\n")
print(P[20-1][0]*M20[1])
print((P[2-1][0]*M20[1] + P[6-1][0]*M20[1])/2)
