import os

# CONFIG
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "generated")
LEG_LENGTHS = [0.10, 0.15, 0.20, 0.25, 0.30]

def generate_robot_bodies():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"🏭 Factory: Generating {len(LEG_LENGTHS)} robot bodies...")

    for L in LEG_LENGTHS:
        # 1. Calculate safe spawn height (Body + Legs + Buffer)
        # Narrow hips (0.06) included to prevent spinning
        z_start = L + 0.15
        
        xml = f"""
    <mujoco>
        <worldbody>
            <body name="torso" pos="0 0 {z_start:.3f}">
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
        
        # 2. Write the specific file (e.g., robot_L0.10.xml)
        filename = f"robot_L{L:.2f}.xml"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w") as f:
            f.write(xml)
        print(f"   ✅ Generated: {filename}")

        # 3. SPECIAL STEP:
        # If this is the 0.10 robot, ALSO save it as 'robot_body.xml'
        # This ensures the 'track_scene.xml' (which looks for robot_body.xml)
        # has a default robot to load immediately.
        if L == 0.10:
            default_path = os.path.join(OUTPUT_DIR, "robot_body.xml")
            with open(default_path, "w") as f:
                f.write(xml)
            print(f"      ↳ (Saved as default 'robot_body.xml' for the demo)")

if __name__ == "__main__":
    generate_robot_bodies()