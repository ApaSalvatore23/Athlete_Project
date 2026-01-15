import numpy as np
import matplotlib.pyplot as plt
import math

class Workout:
    def __init__(self):
        self.base = 5
        self.exponent = 0.10
        self.reps = 0
        self.load = 0
        self.max_weight = 0
        self.epley = 0
        self.brzycki = 0
        self.lombardi = 0
        self.k_min = 48  # 50=intermediate athlete, 55=explosive athlete
        self.k_max = 53
        self.min_jump = 0
        self.max_jump = 0
        self.body_weight = 0
        self.relative_strength = 0
        self.level = ""
        self.standing_reach = 0
        self.current_jump = 0

    def _calculate_1rm(self, load, reps):
        epley = load * (1 + 0.0333 * reps)
        brzycki = load * (36 / (37 - reps))
        lombardi = load * math.pow(reps, 0.10)
        return (epley + brzycki + lombardi) / 3

    def squat(self):
        self.body_weight = float(input("Enter your current body weight (kg):\n"))
        self.load = float(input("Enter your Squat load (kg):\n"))
        self.reps = float(input("Enter number of Squat reps:\n"))

        self.max_weight = self._calculate_1rm(self.load, self.reps)
        self.relative_strength = self.max_weight / self.body_weight

        print(f"Estimated Squat 1RM: {round(self.max_weight)} kg")
        print(f"You lift approximately {round(self.relative_strength * 10)/10} times your body weight")

    def jump(self):
        self.body_weight = float(input("Enter your current body weight (kg):\n"))
        self.standing_reach = float(input("Enter Standing Reach (cm):\n"))
        self.load = float(input("Enter your Squat load (kg):\n"))
        self.reps = float(input("Enter number of Squat reps:\n"))
        self.current_jump = float(input("Enter your current vertical jump (cm):\n"))

        self.max_weight = self._calculate_1rm(self.load, self.reps)

        self.min_jump = self.k_min * (self.max_weight / self.body_weight)
        self.max_jump = self.k_max * (self.max_weight / self.body_weight)
        self.relative_strength = round((self.max_weight / self.body_weight) * 10) / 10

        print(f"Your potential vertical jump is: {round(self.min_jump)}-{round(self.max_jump)} cm")
        print(f"Potential reach height: {round(self.standing_reach + self.min_jump)}-{round(self.standing_reach + self.max_jump)} cm")

        # --- Jump Subplots ---
        plt.figure(figsize=(8,10))

        plt.subplot(2,1,1)
        plt.xlim(0,3)
        plt.ylim(0,120)
        plt.plot([0,3],[50,50], label="Beginner (50-65cm)")
        plt.plot([0,3],[70,70], label="Intermediate (70-80cm)")
        plt.plot([0,3],[80,80], label="Excellent (80-90cm)")
        plt.plot([0,3],[90,90], label="Advanced (90-105cm)")
        plt.plot([0,3],[105,105], label="Elite (105+cm)")
        plt.plot(2.5, self.min_jump, 'ro', label="Min Potential Jump")
        plt.plot(2.5, self.max_jump, 'go', label="Max Potential Jump")
        plt.plot(1.5, self.current_jump, 'bo', label="Current Jump")
        plt.title("Jump Performance Chart")
        plt.ylabel("Height (cm)")
        plt.grid()
        plt.legend()

        plt.subplot(2,1,2)
        plt.xlim(0, 2.5)
        plt.ylim(0, 120)
        plt.fill([2,2.5,2.5,2],[95,95,120,120], color='#90EE90', label="Ideal Ratio")
        plt.fill([2,2.5,2.5,2],[95,95,0,0], color='#FFF44F', label="Ideal Strength")
        plt.fill([0,0,2,2],[120,95,95,120], color='#87CEFA', label="Ideal Jump")
        plt.plot(self.relative_strength, self.current_jump, 'ro', label="Current Jump")
        plt.title("Jump vs Relative Strength Chart")
        plt.xlabel("Relative Strength (BW)")
        plt.ylabel("Jump Height (cm)")
        plt.grid()
        plt.legend()

        plt.tight_layout()
        plt.show()

    def bench_press(self):
        self.body_weight = float(input("Enter your current body weight (kg):\n"))
        self.load = float(input("Enter Bench Press load (kg):\n"))
        self.reps = float(input("Enter number of Bench Press reps:\n"))

        self.max_weight = self._calculate_1rm(self.load, self.reps)
        self.relative_strength = self.max_weight / self.body_weight

        print(f"Estimated Bench Press 1RM: {round(self.max_weight)} kg")
        print(f"You lift approximately {round(self.relative_strength * 10)/10} times your body weight")

    def power(self):
        self.body_weight = float(input("Enter your current body weight (kg):\n"))
        self.load = float(input("Enter Squat load (kg):\n"))
        time = float(input("Enter concentric phase time (s):\n"))

        self.relative_strength = round((self.load / self.body_weight) * 10) / 10
        power_index = self.relative_strength / time

        if power_index < 0.8:
            power_level = "Low"
        elif 0.8 <= power_index < 1.5:
            power_level = "Medium"
        elif 1.5 <= power_index < 2.5:
            power_level = "High"
        else:
            power_level = "Elite"

        print(f"Your Power Level is: {power_level}")

        # --- Power Subplots ---
        plt.figure(figsize=(8,10))

        plt.subplot(2,1,1)
        plt.xlim(0,3)
        plt.ylim(0,2)
        plt.plot([0,3],[0.7,0.7], label="Low")
        plt.plot([0,3],[1.0,1.0], label="Medium")
        plt.plot([0,3],[1.5,1.5], label="Advanced")
        plt.plot(1.5, power_index, 'ro', label="You")
        plt.title("Power Level Chart")
        plt.xlabel("Measurements")
        plt.ylabel("Power Index")
        plt.grid()
        plt.legend()

        plt.subplot(2,1,2)
        plt.xlim(0,2.5)
        plt.ylim(0,2)
        plt.plot(time, self.relative_strength, 'ro', label="You")
        plt.fill([0,0.8,0.8,0],[2,2,1.25,1.25], color='#90EE90', label="Ideal Ratio")
        plt.fill([0,0.8,0.8,0],[1.25,1.25,0,0], color="#87CEFA", label="Ideal Time")
        plt.fill([0.8,0.8,2.5,2.52],[1.25,2,2,1.25], color="#FFF44F", label="Ideal Strength")
        plt.title("Strength vs Time Chart")
        plt.xlabel("Time (s)")
        plt.ylabel("Relative Strength (BW)")
        plt.grid()
        plt.legend()

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    n = 1
    user_workout = Workout()
    while n > 0:
        print("What would you like to calculate?")
        print("1) Squat 1RM and Level")
        print("2) Potential Vertical Jump")
        print("3) Bench Press 1RM and Level")
        print("4) Calculate Power")
        print("0) Exit")

        try:
            choice = int(input("Choice: "))
            if choice == 1:
                user_workout.squat()
            elif choice == 2:
                user_workout.jump()
            elif choice == 3:
                user_workout.bench_press()
            elif choice == 4:
                user_workout.power()
            elif choice == 0:
                break
        except ValueError:
            print("Please enter a valid number.")
        print("")