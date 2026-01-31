import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# CONFIG
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "../results/grid_results_day20.csv")

def run_winning_race():
    if not os.path.exists(DATA_FILE):
        print(f"❌ Error: {DATA_FILE} not found.")
        return

    # Load Data and extract the comparison points for L=0.10
    df = pd.read_csv(DATA_FILE)
    
    # We filter for the Small Robot (L=0.1)
    # 1. The "Designed" Case (1.0 Hz) -> Usually fails or is slow
    row_dumb = df[(df["LegLength"] == 0.1) & (df["Frequency"] == 1.0)].iloc[0]
    
    # 2. The "Desire Path" Case (2.25 Hz) -> The Discovery
    row_smart = df[(df["LegLength"] == 0.1) & (df["Frequency"] == 2.25)].iloc[0]

    names = ["Standard Control (1.0Hz)", "Resonance Discovery (2.25Hz)"]
    speeds = [row_dumb["Speed"], row_smart["Speed"]]
    colors = ['#FF4444', '#44FF44'] # Red vs Green

    # Setup Plot
    fig, ax = plt.subplots(figsize=(10, 4))
    plt.style.use('dark_background')
    
    duration = 10.0
    fps = 30
    frames = int(duration * fps)
    
    bars = ax.barh(names, [0, 0], color=colors)
    
    # Set limit to the winner's distance
    max_dist = max(speeds) * duration * 1.2
    ax.set_xlim(0, max_dist)
    
    ax.set_title(f"The 'Desire Path' Effect (Robot L=0.10m)", fontsize=18, color='white', pad=20)
    ax.set_xlabel("Distance Traveled (m)", fontsize=12)
    
    # Add vertical line for "Start"
    ax.axvline(0, color='white', linewidth=1)

    def update(frame):
        t = (frame / frames) * duration
        current_dists = [s * t for s in speeds]
        
        for bar, dist, speed in zip(bars, current_dists, speeds):
            bar.set_width(dist)
            # Add text label at end of bar
            val = f"{dist:.2f}m"
            # We can't easily update text objects in blit mode without managing them, 
            # so we just update the bars.
            
        return list(bars)

    print(f"🏎️  Racing: Standard ({speeds[0]:.2f} m/s) vs Resonance ({speeds[1]:.2f} m/s)")
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=1000/fps, repeat=True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_winning_race()