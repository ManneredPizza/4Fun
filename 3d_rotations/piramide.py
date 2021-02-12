import numpy as np
import math as m
import random as r
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def proiezione_punto(P):
    #f:R^3->R^2 t.c. (x,y,z)|->(x,y)
    return np.array((P[0],P[1]))

massimo = 100
rotazioni = 1000

#prendo tre punti randomici nello spazio affine su R di dimensione 3
A = np.random.randint(massimo, size=3)
B = np.random.randint(massimo, size=3)
C = np.random.randint(massimo, size=3)

v1 = B - A
v2 = B - C

#prendo il vettore normale ai due trovati
cp = np.cross(v1,v2)
a, b, c = cp #assegno le tre coordinate del vettore normale a 3 variabili

#calcolo la d per definite a*xB+b*yB+c*zB=d, questo non è altro che il prodotto scalare tra B e cp
d = np.dot(cp, B)

#ora so che l'equazione del piano è ax+by+cz=d
#so che il piano è dato da L(B, <B-A>+<B-C>), devo prenderne uno che non apartiene al piano, vista la bassa probabilità che prso randomicamente appartenga al piano, ne prendo
#uno e testo se appartiene
P = np.random.randint(massimo, size=3)
while(a*P[0]+b*P[1]+c*P[2]==d):
    P = np.random.randint(massimo, size=3)

#Ora che ho 4 punti non sullo stesso piano ho un una piramide, mi serve la superficie
#è data dall'area dei 4 triangoli delle facce che posso calcolare per mezzo del prodotto vettoriale tra i vettori di distanza tra i vertici
v3 = B - P
v4 = A - P
v5 = A - C

S = 0.5*(np.linalg.norm(np.cross(v1,v2))+np.linalg.norm(np.cross(v3,v2))+np.linalg.norm(np.cross(v3,v1))+np.linalg.norm(np.cross(v4,v5)))

#ora che ho tutti i dati fissi effettuo dei loop per le rotazioni

area = []

for i in range(rotazioni):

    theta_x = r.uniform(0,2*m.pi)
    theta_y = r.uniform(0,2*m.pi)
    theta_z = r.uniform(0,2*m.pi)

    #prendo il trasposto dei vettori per poterli moltiplicare per le matrici di rotazione
    A_t = np.transpose(np.atleast_2d(A))
    B_t = np.transpose(np.atleast_2d(B))
    C_t = np.transpose(np.atleast_2d(C))
    P_t = np.transpose(np.atleast_2d(P))

    #calcolo le matrici di rotazione
    R_x = np.array(((1, 0, 0), (0, m.cos(theta_x), (-1)*m.sin(theta_x)), (0, m.sin(theta_x), m.cos(theta_x))))
    R_y = np.array(((m.cos(theta_y), 0, m.sin(theta_y)), (0, 1, 0), ((-1)*m.sin(theta_y), 0, m.cos(theta_y))))
    R_z = np.array(((m.cos(theta_z), (-1)*m.sin(theta_z), 0), (m.sin(theta_z), m.cos(theta_z), 0), (0,0,1)))

    #ruoto tutti i punti
    R = np.matmul(R_z, np.matmul(R_y, R_x))
    A = np.transpose(np.atleast_2d(np.matmul(R, A_t)))[0]
    B = np.transpose(np.atleast_2d(np.matmul(R, B_t)))[0]
    C = np.transpose(np.atleast_2d(np.matmul(R, C_t)))[0]
    P = np.transpose(np.atleast_2d(np.matmul(R, P_t)))[0]


    #prendo le proiezioni dei punti sul piano x,y
    A_xy = proiezione_punto(A)
    B_xy = proiezione_punto(B)
    C_xy = proiezione_punto(C)
    P_xy = proiezione_punto(P)

    punti = np.array((A_xy, B_xy, C_xy, P_xy))

    #devo calcolare l'area dell'ombra (la proiezione) che ho creato
    #se un punto è contenuto all'interno del triangolo formato dagli altri 3, la proiezione è il triangolo
    #per vedere se è interno prtendo, nello spazio affine dimensione 2, 2 punti (A_xy,B_xy) e definisco la retta passante r, prendo t la retta passante per gli altri due punti (C_xy,P_xy)
    #prendo T_xy l'intersezione tra t e r, se |C_xy-T_xy|>=|C_xy-P_xy|, P_xy è interno o sul bordo del triangolo ABC

    is_triangle = 0
    skip = 0

    #le combinazioni sono i primi 3 -> vertici, il 4 -> il vertice da controllare se dentro o meno, 5 -> valutazione finale se è un triangolo 
    combs = np.array(((0,1,2,3,0),(1,2,3,0,0),(2,3,0,1,0),(3,0,1,2,0)))
    for comb in combs:
        #controllo se il punto è interno o sul bordo al triangolo
        punto_interno = Point(punti[comb[3]])
        triangolo = Polygon([punti[comb[0]], punti[comb[1]], punti[comb[2]]])

        if(triangolo.intersects(punto_interno)):
            is_triangle = 1
            comb[4]=1
            break


    if(is_triangle):
        for comb in combs:
            if(comb[4]==1):
                area.append(0.5*np.linalg.norm(np.cross(punti[comb[0]]-punti[comb[1]],punti[comb[0]]-punti[comb[2]])))
    else:
        #non è un triangolo quindi devo calcolare l'area del quadrilatero, bisogna capire quale è l'ordine dei punti (in senso orario o antiorario) per poter poi usare la formula di Gauss
        #per fare ciò controllo l'angolo tra i vettori che costruisco (punto fissato), l'angolo maggiore mi definisce i punti a cui collegare il punto fissato
        angolo_massimo = 0

        #fisso il primo punto che è A_xy
        #i primi due valori sono i vertici che confronto, il terzo valore è il vertice mancante
        combs = ((1,2,3), (1,3,2), (2,3,1))
        for comb in combs:   
            angolo = m.acos(np.dot(A_xy-punti[comb[0]], A_xy-punti[comb[1]])/(np.linalg.norm(A_xy-punti[comb[0]])*np.linalg.norm(A_xy-punti[comb[1]])))
            if angolo_massimo < angolo:
                angolo_massimo = angolo
                vincente = comb

        punti_ordinati = np.array((A_xy, punti[vincente[0]], punti[vincente[2]], punti[vincente[1]]))

        x = []
        y = []

        for punto in punti_ordinati:
            x.append(punto[0])
            y.append(punto[1])

        x = np.asanyarray(x)
        y = np.asanyarray(y)
        n = len(x)
        shift_up = np.arange(-n+1, 1)
        shift_down = np.arange(-1, n-1)    
        area.append(abs((x * (y.take(shift_up) - y.take(shift_down))).sum() / 2.0))

    #ora ho calcolato l'area sia se è un triangolo sia se è un quadrilatero
    #stampo per confronto la superficie e 4 volte la media delle aree che è quello che voglio raggiungere
    area_np = np.array(area)
    print("Superficie: " + str(S) + " Area media * 4: " + str(4*np.mean(area_np)) + " (area media: " + str(np.mean(area_np)) + ")")