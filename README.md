# Learn to Walk: Mapping the Desire Paths of Physics

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Physics-MuJoCo-orange)](https://mujoco.org/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-yellow)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Hackathon-Spartan%20Hack%202026-red)](https://devpost.com/)

> **"Engineers design control. Physics dictates resonance. We mapped the gap."**

![Desire Path Heatmap](<assets/desire to heatmap.png>) 
*The "Desire Path" Heatmap: Yellow zones indicate where mechanical resonance creates free speed. Black zones indicate physics failure modes.*

## 🎥 The Demo (Watch this first!)
**[▶️ CLICK HERE TO WATCH THE DEMO VIDEO](https://youtu.be/placeholder)**
*(We achieved a 3,000% speed increase by tuning resonance frequency live)*
---

## The Discovery

Traditional robotics forces robots to move at arbitrary frequencies (e.g., "1.0 Hz is standard"). This project proves that approach fights physics.

By sweeping the **Phase Space** of Body Morphology vs. Control Frequency, we discovered hidden **"Desire Paths"**—specific frequencies where the robot's mechanical resonance creates high-speed locomotion for free.

### The "A/B" Test Results (Robot L=0.1m)

| Control Mode | Frequency | Distance (10s) | Speed | Outcome |
|:-------------|:----------|:---------------|:------|:--------|
| 🔴 **Designed Path** | 1.00 Hz | 0.02 m | 0.002 m/s | **FAILURE** (Vibration) |
| 🟢 **Desire Path** | 2.25 Hz | 0.65 m | 0.065 m/s | **SUCCESS** (Resonance) |

**Result:** 3,000% performance increase without changing a single hardware component.

---
## Gallery & Results

### 1. The "Valley of Failure" (1.0 Hz)
*At standard frequencies, the robot fights its own mass. It vibrates in place.*
![Struggling Robot](<assets/Valley of Failure.png>)

### 2. The "Ridge of Agility" (2.25 Hz)
*At resonance, the robot enters a stable limit cycle. Speed increases by 30x.*
![Running Robot](<assets/Ridge of agility.png>)

### 3. The Data Proof
*Live telemetry confirms the massive performance gap.*
![Data Chart](<assets/Data Chart.png>)

---

## 🛠 Tech Stack & Libraries
We avoided "Black Box" AI and used pure physics-based optimization.

* **Simulation Engine:** [MuJoCo](https://mujoco.org/) (Multi-Joint dynamics with Contact)
* **Language:** Python 3.13
* **Data Analysis:** Pandas & NumPy
* **Visualization:** Plotly (Heatmaps) & Matplotlib (Animation)

---
## Quick Start

### 1. Installation
```bash
pip install mujoco matplotlib pandas numpy plotly
```

### 2. Build the Environment

Generate the "Monolith" XML file with physics baked into a single, schema-compliant simulation:

```bash
python src/make_final_demo.py
```
### 3.  Run the Live Simulation

Launch the MuJoCo viewer. The robot automatically toggles between Struggle Mode (Red) and Resonance Mode (Green) every 8 seconds:
```bash
python src/demo_live_showcase.py
```

**Watch the console!** Real-time speed and distance metrics display while the robot runs.

### 4. View the "Winning Race" Data

Launch an animated bar chart comparing the "Dumb" vs. "Smart" robot:

python src/viz_winning_race.py


## The Math & Theory

We utilized a Central Pattern Generator (CPG) approach to drive a simple bipedal morphology.

For the complete breakdown of Control Theory, Power Equations ($P = \tau \omega$), and Cost of Transport calculations, see:

**[THEORY.md](THEORY.md)**

---

## Repository Structure
```
LEARN_TO_WALK/
├── README.md                          # You are here
├── THEORY.md                          # Physics & Math Documentation
├── dashboard_desire_path.html         # Interactive Data Visualization
├── LICENSE                            # GNU GPLv3 Copyleft License
├── assets/
|      └──robot_template.xml           # template to generate robot morphology
├── results/
|      └── grid_results_day20.csv       # Raw experimental data
└── src/
    ├── demo_live_showcase.py          # MAIN DEMO: Physics engine & HUD
    ├── viz_winning_race.py            # ANIMATION: Bar chart race
    ├── viz_interactive.py             # TOOL: Generates heatmap dashboard
    ├── make_final_demo.py             # BUILDER: Creates XML environment
    ├── robot_generator.py             # ASSETS: Procedural robot generation
    ├── scene_builder.py               # ASSETS: Track generation
    ├── experiment_runner.py           # RESEARCH ENGINE: Runs the grid sweep to generate data
    ├── controllers.py                 # THE BRAIN: Defines the SineWaveController class
    ├── failure_check.py               # VALIDATION: Detects falls/instability during experiments 
    └── generated/                     # Compiled XML simulation files
```

---

## License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.

- **Copyleft:** Modified and distributed versions must be open-sourced under the same license
- **Freedom:** You are free to run, study, share, and modify the software

---

**Built for Spartan Hack 2026** 