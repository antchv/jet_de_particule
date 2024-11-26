import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random as rd
from math import *
import numpy as np
from tkinter import *
import tkinter as tk
import pylab as plb
from tqdm import tqdm

# Fonction pour recalculer et afficher la figure à chaque lancement
def jet():
    # On ferme la figure du lancement précédent
    plb.close()
    x_final = []
    y_final = []
    # On récupère les valeurs des curseurs
    nb_particules = curseur_nb_particules.get()
    temperature = curseur_temperature.get()
    jet = afficher_jet.get()

    # Préparation des données
    ecran_y = []
    ecran_z = []
    hist_vitesse_part = []

    # dt
    temps_final = 25
    pas_de_temps = 1200
    dt = temps_final / (temps_final * pas_de_temps)
    temps = np.linspace(0, temps_final, temps_final * 10 + 1)

    # valeurs numériques / constantes comme ça tout le monde est ok
    m = 3.0 * 10 ** (-26)
    T = temperature
    k = 1.38 * 10 ** (-23)
    alpha = (m) / (2 * k * T)
    a = alpha * 2
    N = nb_particules
    Lx = 25
    Ly = 10
    Lz = 10
    taille_ecran_y = 15
    taille_ecran_z = 15
    distance_ecran = 2
    acceleration_y = -9.81
    division = 10

    if jet == True:
        """
        plt.figure()
        ax = plt.subplot()
        ax.set_xlim(0, 40)
        ax.set_ylim(-15, 25)
        line, = ax.plot([], [], linewidth=1)  # Ajoutez une ligne vide pour l'animation

        # affiche les bords de la boîte et de la fente
        x1, y1 = [Lx, Lx], [4.5, 4.5]
        x2, y2 = [Lx, Lx], [4.5, 5.5]
        x3, y3 = [Lx, Lx], [5.5, 5.5]
        x4, y4 = [Lx, Lx], [5.5, 4.5]

        ax.plot(x1, y1, 'k', linewidth=6)
        ax.plot(x2, y2, 'k', linewidth=6)
        ax.plot(x3, y3, 'k', linewidth=6)
        ax.plot(x4, y4, 'k', linewidth=6)
        """
    # explication
    ###### idée optimisation simple : calculer les traj seulement des particules sortantes -> if x>10 and fente<y<fente : on continue de calcul, else : on stop
    with tqdm(total=N, desc="Traitement en cours", unit="iteration") as pbar:
        for i in range(N):
            # tirage aléatoire vitesse selon distribution de Maxwell-Boltzmann

            # tirage vitesse en x
            vitesse_x = abs((sqrt(-(log(1 - rd.random())) * 2 / a)) * cos(rd.uniform(0, pi * 2)))

            # tirage vitesse en y
            vitesse_y = (sqrt(-(log(1 - rd.random())) * 2 / a)) * cos(rd.uniform(0, pi * 2))

            # calcul des vitesses 3D
            vitesse_part = sqrt(vitesse_x ** 2 + vitesse_y ** 2)
            hist_vitesse_part.append(vitesse_part)

            # angle_part =  np.arctan (vitesse_y/vitesse_x)

            # tirage aléatoire positions
            position_x = rd.uniform(0, Lx)
            position_y = rd.uniform(0, Ly)

            x = [position_x]
            y = [position_y]

            x2 = []
            y2 = []

            for t in temps:
                if position_x < 30 :
                    vtx = vitesse_x
                    vty = vitesse_y + acceleration_y * dt

                    ptx = position_x + (vitesse_x * dt)
                    pty = position_y + (vitesse_y * dt) + (acceleration_y * dt ** 2) / 2

                    vitesse_x = vtx
                    vitesse_y = vty

                    position_x = ptx
                    position_y = pty

                    x.append(ptx)
                    y.append(pty)
                else :
                    vtx = vitesse_x * 0.9
                    vty = (vitesse_y + acceleration_y * dt) * 0.9

                    ptx = position_x + (vitesse_x * dt)
                    pty = position_y + (vitesse_y * dt) + (acceleration_y * dt ** 2) / 2

                    vitesse_x = vtx
                    vitesse_y = vty

                    position_x = ptx
                    position_y = pty

                    x.append(ptx)
                    y.append(pty)

            for j in range(len(y)):
                if 25 < x[j] < 25.005:
                    if 4.95 < y[j] < 5.05:
                        if jet == True:
                            x_final.append(x)
                            y_final.append(y)
            pbar.update(1)  # Met à jour la barre de défilement


        print(len(x_final))

        # Appel de la fonction pour afficher l'animation
        afficher_animation(x_final, y_final)
############
# idée : créer quelques threads qui appelle la fonction jet(), exemple : N=1000, nb_thread=4 --> on appelle jet(250) sur chacun des threads
# on concatene les listes de resultats obtenues

# Fonction pour afficher l'animation
def afficher_animation(x_final, y_final):
    fig, ax = plt.subplots()
    num_particules = len(x_final)
    num_steps = len(x_final[0])
    lines = [ax.plot([], [])[0] for _ in range(len(x_final))]
    ax.set_xlim(0, 60)
    ax.set_ylim(-15, 25)
    taille_boite=25
    #affiche les bords de la boîte et de la fente
    x1, y1 = [taille_boite, taille_boite], [0, 4.5]
    x2, y2 = [taille_boite, taille_boite], [5.5, 10]
    x3, y3 = [taille_boite, 0], [10, 10]
    x4, y4 = [0, 0], [10, 0]
    x5, y5 = [0, taille_boite], [0, 0]
    x6, y6 = [30, 30], [-15, 25]
    

    ax.plot(x1, y1, 'k', linewidth=3)
    ax.plot(x2, y2, 'k', linewidth=3)
    ax.plot(x3, y3, 'k', linewidth=3)
    ax.plot(x4, y4, 'k', linewidth=3)
    ax.plot(x5, y5, 'k', linewidth=3)
    ax.plot(x6, y6, 'k', linewidth=3)

    def init():
        for line in lines :
            line.set_data([], [])
        return lines

    def animate(frame):
        for i in range(num_particules):
            x = x_final[i][:frame]  # Coordonnées X jusqu'au pas actuel
            y = y_final[i][:frame]  # Coordonnées Y jusqu'au pas actuel
            lines[i].set_data(x, y)
        return lines

    ani = FuncAnimation(fig, animate, init_func=init, frames=num_steps, interval=20, blit=True)
    plt.show()





# Création de la fenêtre principale
interface = tk.Tk()
interface.geometry("800x800")
interface.title("Jet de particules")

# 1er curseur pour le nombre de particules
curseur_nb_particules = tk.Scale(interface, orient='horizontal', from_=1,
                                  to=5000000, length=600,
                                  label="Nombre de particules")
curseur_nb_particules.place(x=10, y=50)

# 2e curseur pour la température
curseur_temperature = tk.Scale(interface, orient='horizontal', from_=1, to=1000, length=400,
                                label="température en kelvin")
curseur_temperature.place(x=10, y=150)
curseur_temperature.set(273)

# Afficher ou non le jet
afficher_jet = BooleanVar()
afficher_jet.set(False)

case_jet = Checkbutton(interface, text='jet de particules', var=afficher_jet)
case_jet.place(x=10, y=250)

# Bouton pour re calculer le jet
b1 = tk.Button(interface, text='Lancer', command=lambda: jet())
b1.place(x=10, y=650)

# Bouton pour arrêter la simulation
b4 = tk.Button(interface, text='Quitter', command=interface.destroy)
b4.pack(side=RIGHT, padx=10, pady=10)
b4.place(x=10, y=750)

interface.mainloop()
