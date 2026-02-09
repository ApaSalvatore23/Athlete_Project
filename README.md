# Athletic Performance & Power Calculator
# Website Link: https://athleteproject-eys2o38hbmaxp7cyfzik4f.streamlit.app/
A Python tool designed for athletes and strength coaches to estimate **One Repetition Maximum (1RM)**, **Vertical Jump Potential**, and **Explosive Power** using validated scientific formulas.

- **1RM Estimation:** Calculates a reliable Squat and Bench Press maximum by averaging **Epley**, **Brzycki**, and **Lombardi** formulas.
- **Vertical Jump Prediction:** Estimates potential jump height based on relative strength and explosive factors.
- **Power Indexing:** Analyzes the quality of a lift by calculating the ratio between relative strength and movement speed (concentric time).
- **Data Visualization:** Generates dual-plot dashboards using `matplotlib` to compare user results against athletic standards (Beginner to Elite).

## 📊 Scientific Framework
To ensure accuracy, the tool calculates the 1RM as the mean of three industry-standard models:
1. **Epley:** 1RM = load * (1 + 0.0333 * reps)
2. **Brzycki:** 1RM = load * (36 / (37 - reps))
3. **Lombardi:** 1RM = load * reps^^0.10
*(Where Load is the weight lifted and reps is the number of repetitions)*

The **Jump Potential** is calculated using an explosive coefficient (k) correlated with the athlete's relative strength:  **45-48**-> not very explosive athlete, **52-55**->very Explosive Athlete
Jump = k \cdot (\frac{1RM}{Bodyweight})

## 🛠️ Tech Stack & Requirements:
- **Language:** Python 3.x
- **Libraries:**
  - `numpy`: For numerical operations.
  - `matplotlib`: For data visualization and performance plotting.
-**Website Libraries:**
  - 'streamlit' : for Website scripts in Python
  - 'plotly' : for better and mmore interactive Graphs
    

