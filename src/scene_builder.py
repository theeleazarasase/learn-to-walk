import os

# CONFIG
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "generated")

def build_track_scene():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("🏗️ Building Race Track Environment...")

    # 1. HEADER & ASSETS
    xml = """
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
    """

    # 3. PROCEDURAL MARKERS (The "Indicator Points")
    # We add lines every 0.5m and Posts every 1.0m
    for x in range(1, 11): # 1m to 10m
        # White Floor Line
        xml += f'        <geom type="box" pos="{x} 0 0.001" size="0.02 1 0.001" material="mat_line"/>\n'
        
        # Vertical Distance Post (The "Flag")
        # Placed slightly to the side (y=-1.2) so the robot doesn't hit it
        xml += f'        <geom type="cylinder" pos="{x} -1.2 0.5" size="0.05 0.5" material="mat_post"/>\n'
        
        # Add a "Crossbar" to make it look like a finish line marker
        xml += f'        <geom type="box" pos="{x} -1.2 1.0" size="0.02 0.4 0.05" rgba="1 1 1 1"/>\n'

    # 4. INCLUDE THE ROBOT
    # This is the "Correct Way": We use an <include> tag.
    # The simulation will look for 'robot_body.xml' in the same folder.
    xml += """
            <include file="robot_body.xml"/>
            
        </worldbody>
    </mujoco>
    """

    # Write the Scene File
    with open(os.path.join(OUTPUT_DIR, "track_scene.xml"), "w") as f:
        f.write(xml)
    print("✅ Created 'track_scene.xml' (Environment)")

if __name__ == "__main__":
    build_track_scene()