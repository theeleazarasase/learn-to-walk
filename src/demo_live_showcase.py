import mujoco
import mujoco.viewer
import numpy as np
import os
import time
import sys

# CONFIG
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# POINT TO THE FINAL DEMO FILE
ROBOT_FILE = os.path.join(SCRIPT_DIR, "generated/final_demo.xml")

SWITCH_INTERVAL = 8.0 
MODE_A_FREQ = 1.0   
MODE_A_AMP = 0.5    
MODE_B_FREQ = 2.25  
MODE_B_AMP = 1.0    

def run_live_showcase():
    if not os.path.exists(ROBOT_FILE):
        print(f"❌ Error: {ROBOT_FILE} not found. Run 'src/make_final_demo.py' first!")
        return

    model = mujoco.MjModel.from_xml_path(ROBOT_FILE)
    data = mujoco.MjData(model)
    
    try:
        torso_mat_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_MATERIAL, "robot_mat")
    except:
        torso_mat_id = -1

    current_freq = MODE_A_FREQ
    current_amp = MODE_A_AMP
    last_switch_time = time.time()
    mode_name = "STRUGGLING"
    
    print("\n\n")
    print("🎥 LAUNCHING LIVE DEMO...")
    print("   (Keep this terminal visible next to the MuJoCo window for metrics)")
    print("\n")

    with mujoco.viewer.launch_passive(model, data) as viewer:
        mujoco.mj_resetData(model, data)
        start_pos = np.array([data.qpos[0], data.qpos[1]])
        
        # Camera Setup (Side View for Race)
        viewer.cam.azimuth = 90
        viewer.cam.distance = 4.0
        viewer.cam.elevation = -10
        viewer.cam.lookat[0] = 2.0
        
        while viewer.is_running():
            step_start = time.time()
            now = time.time()

            # --- SWITCH LOGIC ---
            if now - last_switch_time > SWITCH_INTERVAL:
                if current_freq == MODE_A_FREQ:
                    current_freq = MODE_B_FREQ
                    current_amp = MODE_B_AMP
                    mode_name = "RESONANCE SPRINT"
                    if torso_mat_id >= 0: model.mat_rgba[torso_mat_id] = [0.1, 1.0, 0.1, 1.0] 
                else:
                    current_freq = MODE_A_FREQ
                    current_amp = MODE_A_AMP
                    mode_name = "STRUGGLING"
                    if torso_mat_id >= 0: model.mat_rgba[torso_mat_id] = [1.0, 0.1, 0.1, 1.0]
                
                mujoco.mj_resetData(model, data) 
                start_pos = np.array([data.qpos[0], data.qpos[1]])
                last_switch_time = now
                viewer.sync()
                continue

            target = current_amp * np.sin(2 * np.pi * current_freq * data.time)
            data.ctrl[:] = [target, -target]
            mujoco.mj_step(model, data)
            
            # Metrics
            current_pos = np.array([data.qpos[0], data.qpos[1]])
            dist = np.linalg.norm(current_pos - start_pos)
            elapsed = now - last_switch_time
            speed = dist / elapsed if elapsed > 0.1 else 0.0
            
            # Camera Tracking
            viewer.cam.lookat[0] = data.qpos[0] + 1.0 
            viewer.sync()
            
            # --- CONSOLE HUD (Replaces the broken Overlay) ---
            # We use ANSI colors to make it pop in the terminal
            icon = "🟢" if "SPRINT" in mode_name else "🔴"
            
            # \r overwrites the same line, creating a "Dashboard" effect
            sys.stdout.write(f"\r {icon} [{mode_name}]  Freq: {current_freq}Hz  |  Dist: {dist:.2f}m  |  Speed: {speed:.2f} m/s    ")
            sys.stdout.flush()

            # Sync Speed
            time_until_next = model.opt.timestep - (time.time() - step_start)
            if time_until_next > 0: time.sleep(time_until_next)

if __name__ == "__main__":
    run_live_showcase()