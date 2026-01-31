import pandas as pd
import numpy as np  # <--- Added NumPy for dstack
import plotly.graph_objects as go
import os

# CONFIG
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "../results/grid_results_day20.csv")
OUTPUT_HTML = os.path.join(SCRIPT_DIR, "../dashboard_desire_path.html")

def create_dashboard():
    if not os.path.exists(DATA_FILE):
        print(f" Error: {DATA_FILE} not found.")
        return

    print(f"📊 Loading data for Interactive Dashboard...")
    df = pd.read_csv(DATA_FILE)

    # 1. Prepare Matrices for the Heatmap
    speed_matrix = df.pivot(index="LegLength", columns="Frequency", values="Speed")
    cot_matrix = df.pivot(index="LegLength", columns="Frequency", values="CoT")
    dist_matrix = df.pivot(index="LegLength", columns="Frequency", values="Distance")
    
    # Sort index (Short legs at bottom)
    speed_matrix = speed_matrix.sort_index(ascending=True)
    cot_matrix = cot_matrix.sort_index(ascending=True)
    dist_matrix = dist_matrix.sort_index(ascending=True)

    # 2. Build the Interactive Heatmap
    # FIX: Use np.dstack, not pd.dstack
    custom_data = np.dstack((cot_matrix.values, dist_matrix.values))

    fig = go.Figure(data=go.Heatmap(
        z=speed_matrix.values,
        x=speed_matrix.columns,
        y=speed_matrix.index,
        colorscale='Inferno', 
        zmin=0,
        zmax=0.20,
        colorbar=dict(title='Speed (m/s)'),
        
        # Hover Data
        customdata=custom_data,
        hovertemplate=(
            "<b>Leg Length: %{y}m</b><br>" +
            "<b>Frequency: %{x} Hz</b><br>" +
            "<br>" +
            "🚀 Speed: <b>%{z:.3f} m/s</b><br>" +
            "🔋 CoT: %{customdata[0]:.2f}<br>" +
            "📏 Dist: %{customdata[1]:.2f}m<br>" +
            "<extra></extra>"
        )
    ))

    # 3. Layout & Style
    fig.update_layout(
        title={
            'text': "<b>The Desire Path:</b> Resonance Frequency vs. Agility",
            'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top',
            'font': dict(size=24, color='white')
        },
        xaxis_title="Control Frequency (Hz)",
        yaxis_title="Leg Length (m)",
        template="plotly_dark",
        width=1200,
        height=800,
        margin=dict(t=100, b=100, l=100, r=100)
    )

    # 4. Save
    print(f"💾 Saving Interactive Dashboard to: {OUTPUT_HTML}")
    fig.write_html(OUTPUT_HTML)
    print("✅ Done! Open the HTML file in your browser.")

if __name__ == "__main__":
    create_dashboard()