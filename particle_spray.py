import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import random as rd
from math import *
import numpy as np
from tkinter import *
import tkinter as tk
import pylab as plb


# Fonction pour re calculer et afficher la figure à chaque lancement
def jet():
    # On ferme la figure du lancement précédent
    plb.close()
    
    # On récupère les valeurs des curseurs
    nb_particules=curseur_nb_particules.get()
    temperature=curseur_temperature.get()
    jet = afficher_jet.get()
    
    # Préparation des données
 
    ecran_y=[]
    ecran_z=[]
    hist_vitesse_part=[]
    
    #dt
    temps_final=8
    pas_de_temps=1200
    dt = temps_final/(temps_final*pas_de_temps)
    temps=np.linspace(0,temps_final,temps_final*10+1)
    
    
    #valeurs numériques / constantes comme ca tout le monde est ok
    m=3.0*10**(-26)
    T=temperature
    k=1.38*10**(-23)
    alpha=(m)/(2*k*T)
    a=alpha*2
    N=nb_particules
    Lx=10
    Ly=10
    Lz=10
    taille_ecran_y=15
    taille_ecran_z=15
    distance_ecran=2
    acceleration_y=-9.81 
    division=10
    
    
   
    if jet == True :
        plt.figure()
        ax = plt.axes(projection='3d')

        ax.set_xlim(0, 40)
        ax.set_ylim(-15, 25)
        ax.set_zlim(-15,25)
            
        
        #affiche les bords de la boite et de la fente
        x1, y1, z1 = [Lx, Lx], [4.5, 4.5], [4.5,5.5]
        x2, y2, z2= [Lx, Lx], [4.5, 5.5], [5.5,5.5]
        x3, y3, z3 = [Lx,Lx], [5.5, 5.5], [5.5,4.5]
        x4, y4, z4 = [Lx, Lx], [5.5, 4.5], [4.5,4.5]
        
        
        ax.plot(x1, y1, z1, 'k',linewidth=6)
        ax.plot(x2, y2, z2,'k',linewidth=6)
        ax.plot(x3, y3, z3, 'k',linewidth=6)
        ax.plot(x4, y4, z4, 'k',linewidth=6)
        
        
        # Create axis
        axes = [10, 10, 10]
          
        # Create Data
        data = np.ones(axes, dtype=np.bool)
          
        # Controll Tranperency
        alpha = 0.7
          
        # Control colour
        colors = np.empty(axes + [4], dtype=np.float32)
          
        colors[:] = [1, 1, 1, alpha]  # grey
          
        # Voxels is used to customizations of the
        # sizes, positions and colors.
        ax.voxels(data, facecolors=colors)
   
    
    #explication
    for i in range(N):
        #tirage aléatoire vitesse selon distribution de Maxwell-Boltzmann
        
        #tirage vitesse en x
        vitesse_x = abs((sqrt(-(log(1-rd.random()))*2/a)) * cos(rd.uniform(0,pi*2)))
        
        #tirage vitesse en y
        vitesse_y = (sqrt(-(log(1-rd.random()))*2/a)) * cos(rd.uniform(0,pi*2))
        
        #tirage vitesse en z
        vitesse_z = (sqrt(-(log(1-rd.random()))*2/a)) * cos(rd.uniform(0,pi*2))
        
        #calcul des vitesses 3D
        vitesse_part = sqrt( vitesse_x**2 + vitesse_y**2 + vitesse_z**2)
        hist_vitesse_part.append(vitesse_part)
     
        #angle_part =  np.arctan (vitesse_y/vitesse_x)
        
        #tirage aléatoire positions
        position_x=rd.uniform(0,Lx)
        position_y=rd.uniform(0,Ly)
        position_z=rd.uniform(0,Lz)
            
        x=[position_x]
        y=[position_y]
        z=[position_z]
        
        x2=[]
        y2=[]
        z2=[]
       
        for t in temps :
            vtx = vitesse_x 
            vty = vitesse_y + acceleration_y*dt
            vtz = vitesse_z
            
            ptx = position_x + (vitesse_x * dt) 
            pty = position_y + (vitesse_y * dt) + (acceleration_y*dt**2)/2
            ptz = position_z + (vitesse_z * dt) 
            
            vitesse_x = vtx
            vitesse_y = vty
            vitesse_z = vtz
            
            position_x = ptx
            position_y = pty
            position_z = ptz
            
            x.append(ptx)
            y.append(pty)
            z.append(ptz)
           
        for j in range (len(y)) :
            if 10<x[j]<10.01:
                if 4.5<y[j]<5.5:
                    if 4.5<z[j]<5.5:
                        if jet == True : 
                            ax.plot3D(x,y,z,linewidth=1)
                          
                        for p in range(len(x)):
                            if Lx+distance_ecran <x[p]< Lx + distance_ecran + 0.2 :
                                if -taille_ecran_y + 5 <y[p]< taille_ecran_y + 5:
                                    if -taille_ecran_z+5<z[p] < taille_ecran_z + 5:
                                        ecran_y.append(y[p])
                                        ecran_z.append(z[p])
        
                                   
 
    histo_initial = histo_ini.get()
    if histo_initial == True :
        plt.figure()
        plt.hist(hist_vitesse_part,range=(0,2000), bins=500, histtype='step')
        plt.grid(True)
        
        
    histo_ecran = histo_ec.get()
    if histo_ecran == True :
        # Affichage
        plt.figure(figsize=(15,15))
        ax2 = plt.axes(projection='3d')
        
        
        dy=2
        hist, xedges, yedges = np.histogram2d(ecran_y, ecran_z, bins=30, 
                                              range=[[-10, 20], [-10, 20]])
        
        # Construct arrays for the anchor positions of the 16 bars.
        xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
        xpos = xpos.ravel()
        ypos = ypos.ravel()
        zpos = 0
        
        dz=hist.ravel()
        ax2.bar3d(xpos ,ypos, zpos , dy , dy , dz , zsort='average')
        
        
    impact_ecran = impact_ec.get()
    if impact_ecran == True :
        plt.figure()
        plt.scatter(ecran_y,ecran_z)
           
    plt.show()
   


# Création de la fenêtre principale
interface = tk.Tk()
interface.geometry("800x800")
interface.title("Jet de particules")

# 1er curseur pour le nombre de particules
curseur_nb_particules= tk.Scale(interface, orient='horizontal', from_=1, 
                                to=1000000, length=600, 
                                label="Nombre de particules")
curseur_nb_particules.place(x=10,y=50)

# 2e curseur pour la température
curseur_temperature= tk.Scale(interface, orient='horizontal', from_=1, to=1000, length=400, 
             label="température en kelvin")
curseur_temperature.place(x=10,y=150)
curseur_temperature.set(273)


# Afficher ou non le jet
afficher_jet = BooleanVar() 
afficher_jet.set(False)
 
case_jet = Checkbutton(interface, text='jet de particules', var=afficher_jet)
case_jet.place(x=10, y=250)

# Afficher ou non histogramme initial
histo_ini = BooleanVar() 
histo_ini.set(False)
 
case_histo = Checkbutton(interface, text='histogramme vitesses initiales', var=histo_ini)
case_histo.place(x=10, y=350)

# Afficher ou non histogramme écran
histo_ec = BooleanVar() 
histo_ec.set(False)
 
case_histo_ecran = Checkbutton(interface, text='histogramme positions sur un écran',
                               var=histo_ec)
case_histo_ecran.place(x=10, y=450)


# Afficher ou non les impacts sur un écran
impact_ec = BooleanVar() 
impact_ec.set(False)
 
case_impact_ecran = Checkbutton(interface, text='position des impacts sur un écran',
                               var=impact_ec)
case_impact_ecran.place(x=10, y=550)



# Bouton pour re calculer le jet
b1 = tk.Button(interface, text ='Lancer', command=lambda:jet())
b1.place(x=10,y=650)

# Bouton pour arrêter la simulation
b4 = tk.Button(interface, text ='Quitter', command=interface.destroy)
b4.pack(side = RIGHT, padx = 10, pady = 10)
b4.place(x=10,y=750)


interface.mainloop()
