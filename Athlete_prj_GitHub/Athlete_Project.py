import numpy as np
import matplotlib.pyplot as plt
import math

class Allenamento:
    def _init_(self):
        self.base = 5
        self.esponente = 0.10
        self.reps = 0
        self.carico = 0
        self.max = 0
        self.epley = 0
        self.brzycki = 0
        self.lombardi = 0
        self.k_min = 46  # 50=atleta intermedio, 55=atleta esplosivo
        self.k_max = 52
        self.salto_min = 0
        self.salto_max = 0
        self.peso = 0
        self.forza = 0
        self.livello = ""
        self.standing_reach=0
        self.salto_attuale=0

    def squat(self):
        self.peso = float(input("Inserisci il tuo peso attuale:\n"))
        self.carico = float(input("Inserisci il carico(kg) di Squat:\n"))
        self.reps = float(input("Inserisci n° reps di Squat:\n"))

        self.epley = self.carico * (1 + 0.0333 * self.reps)
        self.brzycki = self.carico * (36 / (37 - self.reps))
        x = math.pow(self.reps, 0.10)
        self.lombardi = self.carico * x
        self.max = (self.epley + self.brzycki + self.lombardi) / 3
        self.forza = self.max / self.peso

        print(f"Massimale di Squat stimato: {round(self.max)} kg")
        print(f"Sollevi circa {round(self.forza * 10)/10} volte il tuo peso corporeo")

    def salto(self):
        self.peso = float(input("Inserisci il tuo peso attuale:\n"))
        self.standing_reach= float(input("inserisci Standing Reach(cm):\n"))
        self.carico = float(input("Inserisci il carico(kg) di Squat:\n"))
        self.reps = float(input("Inserisci n° reps di Squat:\n"))
        self.salto_attuale = float(input("inserisci il tuo salto attuale(cm):\n"))

        self.epley = self.carico * (1 + 0.0333 * self.reps)
        self.brzycki = self.carico * (36 / (37 - self.reps))
        x = math.pow(self.reps, 0.10)
        self.lombardi = self.carico * x
        self.max = (self.epley + self.brzycki + self.lombardi) / 3

        self.salto_min = self.k_min * (self.max / self.peso)
        self.salto_max = self.k_max * (self.max / self.peso)
        self.forza = round((self.max / self.peso) * 10) / 10

        print(f"Il tuo salto potenziale è: {round(self.salto_min)}-{round(self.salto_max)} cm")
        print(f"altezza potenziale: {round(self.standing_reach+self.salto_min)}-{round(self.standing_reach+self.salto_max)}")

        # --- Subplot per Salto ---
        plt.figure(figsize=(8,10))

        # Grafico 1: Salto
        plt.subplot(2,1,1)
        plt.xlim(0,3)
        plt.ylim(0,120)
        plt.plot([0,3],[50,50], label="Principiante(50-65cm)")
        plt.plot([0,3],[70,70], label="Intermedio(70-80cm)")
        plt.plot([0,3],[80,80], label="Eccellente(80-90cm)")
        plt.plot([0,3],[90,90], label="Avanzato(90-105cm)")
        plt.plot([0,3],[105,105], label="Elite(105+cm)")
        plt.plot(2.5, self.salto_min, 'ro', label="salto minimo potenziale")
        plt.plot(2.5, self.salto_max, 'go', label="salto massimo potenziale")
        plt.plot(1.5, self.salto_attuale, 'bo', label="salto attuale")
        plt.title("Grafico Salti")
        plt.ylabel("Altezza(cm)")
        plt.grid()
        plt.legend()

        # Grafico 2: Salto vs Forza Relativa
        plt.subplot(2,1,2)
        plt.xlim(0, 2.5)
        plt.ylim(0, 120)
        plt.fill([2,2.5,2.5,2],[95,95,120,120], color='#90EE90', label="rapporto ideale")
        plt.fill([2,2.5,2.5,2],[95,95,0,0], color='#FFF44F', label="Forza ideale")
        plt.fill([0,0,2,2],[120,95,95,120], color='#87CEFA', label="Salto ideale")
        plt.plot(self.forza, self.salto_attuale, 'ro', label="salto attuale")
        plt.title("Grafico Salto-Forza_R")
        plt.xlabel("Forza Relativa(BW)")
        plt.ylabel("H_Salto(cm)")
        plt.grid()
        plt.legend()

        plt.tight_layout()
        plt.show()

    def panca_piana(self):
        self.peso = float(input("Inserisci il tuo peso attuale:\n"))
        self.carico = float(input("Inserisci il carico(kg) di Panca Piana:\n"))
        self.reps = float(input("Inserisci n° reps di Panca Piana:\n"))

        self.epley = self.carico * (1 + 0.0333 * self.reps)
        self.brzycki = self.carico * (36 / (37 - self.reps))
        x = math.pow(self.reps, 0.10)
        self.lombardi = self.carico * x
        self.max = (self.epley + self.brzycki + self.lombardi) / 3
        self.forza = self.max / self.peso

        print(f"Massimale di Panca Piana stimato: {round(self.max)} kg")
        print(f"Sollevi circa {round(self.forza * 10)/10} volte il tuo peso corporeo")

    def potenza(self):
        self.peso = float(input("Inserisci il tuo peso attuale:\n"))
        self.carico = float(input("Inserisci carico di Squat (kg):\n"))
        tempo = float(input("Inserisci tempo di salita (s):\n"))

        self.forza = round((self.carico / self.peso) * 10) / 10
        ind_pot = self.forza / tempo

        if ind_pot < 0.8:
            liv_pot = "basso"
        elif 0.8 <= ind_pot < 1.5:
            liv_pot = "medio"
        elif 1.5 <= ind_pot < 2.5:
            liv_pot = "alto"
        else:
            liv_pot = "Elite"

        print(f"Il tuo livello di Potenza è: {liv_pot}")

        # --- Subplot per potenza ---
        plt.figure(figsize=(8,10))

        # Grafico 1: Livello Potenza
        plt.subplot(2,1,1)
        plt.xlim(0,3)
        plt.ylim(0,2)
        plt.plot([0,3],[0.7,0.7], label="Basso")
        plt.plot([0,3],[1.0,1.0], label="Medio")
        plt.plot([0,3],[1.5,1.5], label="Avanzato")
        plt.plot(1.5, ind_pot, 'ro', label="Tu")
        plt.title("Grafico Livello Potenza")
        plt.xlabel("Misurazioni")
        plt.ylabel("Indice di Potenza")
        plt.grid()
        plt.legend()

        # Grafico 2: Forza Relativa vs Tempo
        plt.subplot(2,1,2)
        plt.xlim(0,2.5)
        plt.ylim(0,2)
        plt.plot(tempo, self.forza, 'ro', label="Tu")
        plt.fill([0,0.8,0.8,0],[2,2,1.25,1.25], color='#90EE90', label="Rapporto Ideale")
        plt.fill([0,0.8,0.8,0],[1.25,1.25,0,0], color="#87CEFA", label="Tempo ideale")
        plt.fill([0.8,0.8,2.5,2.52],[1.25,2,2,1.25], color="#FFF44F", label="Forza ideale")
        plt.title("Grafico ForzaR-Tempo")
        plt.xlabel("Tempo(s)")
        plt.ylabel("Forza Relativa(BW)")
        plt.grid()
        plt.legend()

        plt.tight_layout()
        plt.show()


# --- Main Program ---
if _name_ == "_main_":
    n=1
    Salvatore = Allenamento()
    while n>0:
       print("Cosa vuoi che calcoli?")
       print("1) Massimale e Livello di Squat")
       print("2) Salto Potenziale")
       print("3) Massimale e Livello di Panca Piana")
       print("4) Calcola Potenza")

       scelta = int(input())
       if scelta == 1:
          Salvatore.squat()
       elif scelta == 2:
          Salvatore.salto()
       elif scelta == 3:
          Salvatore.panca_piana()
       elif scelta == 4:
          Salvatore.potenza()
       print("")