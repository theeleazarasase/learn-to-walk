import os

# CONFIG
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "generated")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "final_demo.xml")

# PARAMETERS FOR THE 0.10m ROBOT
L = 0.10
Z_START = L + 0.15

def generate_nuclear_option():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Generating FINAL Monolith File: {OUTPUT_FILE}")

    # ONE SINGLE STRING. NO INCLUDES. NO COMPLEXITY.
    xml_content = f"""
<mujoco>
    <option timestep="0.005" gravity="0 0 -9.81"/>
    
    <asset>
        <texture type="2d" name="tex_track" builtin="checker" rgb1="0.2 0.2 0.2" rgb2="0.3 0.3 0.3" width="512" height="512"/>
        <material name="mat_track" texture="tex_track" texrepeat="10 1" reflectance="0.0"/>
        <material name="mat_line" rgba="1 1 1 0.5"/>
        <material name="mat_post" rgba="0.9 0.2 0.2 1"/>
        <material name="robot_mat" rgba="0.9 0.1 0.1 1"/>
        <material name="leg_mat" rgba="0.1 0.1 0.1 1"/>
    </asset>

    <visual>
        <headlight diffuse="0.6 0.6 0.6" ambient="0.3 0.3 0.3" specular="0 0 0"/>
        <rgba haze="0.15 0.25 0.35 1"/>
    </visual>

    <worldbody>
        <light pos="0 0 4" dir="0 0 -1" directional="true" castshadow="true"/>
        
        <geom name="floor" type="plane" material="mat_track" size="20 2 0.1"/>
        
        <geom type="box" pos="1 -1.2 0.5" size="0.02 0.02 0.5" material="mat_post"/>
        <geom type="box" pos="2 -1.2 0.5" size="0.02 0.02 0.5" material="mat_post"/>
        <geom type="box" pos="3 -1.2 0.5" size="0.02 0.02 0.5" material="mat_post"/>
        <geom type="box" pos="4 -1.2 0.5" size="0.02 0.02 0.5" material="mat_post"/>
        <geom type="box" pos="5 -1.2 0.5" size="0.02 0.02 0.5" material="mat_post"/>
        
        <geom type="box" pos="1 0 0.001" size="0.02 1 0.001" material="mat_line"/>
        <geom type="box" pos="2 0 0.001" size="0.02 1 0.001" material="mat_line"/>
        <geom type="box" pos="3 0 0.001" size="0.02 1 0.001" material="mat_line"/>
        <geom type="box" pos="4 0 0.001" size="0.02 1 0.001" material="mat_line"/>
        <geom type="box" pos="5 0 0.001" size="0.02 1 0.001" material="mat_line"/>

        <body name="torso" pos="0 0 {Z_START:.3f}">
            <joint type="free"/>
            <geom name="torso_geom" type="box" size="0.05 0.05 0.05" material="robot_mat" mass="1"/>
            <geom name="head_geom" type="box" pos="0.03 0 0.06" size="0.03 0.03 0.03" rgba="1 1 1 0.8"/>
            
            <body name="left_leg" pos="0 0.06 0">
                <joint name="hip_left" type="hinge" axis="0 1 0" damping="0.5" range="-100 100"/>
                <geom type="capsule" fromto="0 0 0 0 0 -{L:.2f}" size="0.015" material="leg_mat"/>
            </body>
            
            <body name="right_leg" pos="0 -0.06 0">
                <joint name="hip_right" type="hinge" axis="0 1 0" damping="0.5" range="-100 100"/>
                <geom type="capsule" fromto="0 0 0 0 0 -{L:.2f}" size="0.015" material="leg_mat"/>
            </body>
        </body>
    </worldbody>
    
    <actuator>
        <motor joint="hip_left" gear="12" ctrllimited="true" ctrlrange="-1.0 1.0"/>
        <motor joint="hip_right" gear="12" ctrllimited="true" ctrlrange="-1.0 1.0"/>
    </actuator>
</mujoco>
"""
    with open(OUTPUT_FILE, "w") as f:
        f.write(xml_content)
    print("✅ Success! 'final_demo.xml' is ready.")

if __name__ == "__main__":
    generate_nuclear_option()