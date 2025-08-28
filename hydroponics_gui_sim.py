import tkinter as tk
import random

# Lettuce ideal ranges and target values
lettuce_profile = {
    'pH': (5.5, 6.5),
    'EC': (1.2, 2.0),
    'water_level_min': 1.0,
}

nutrients_profile = {
    'Nitrogen': 150,
    'Phosphorus': 50,
    'Potassium': 200,
}

# Initial environment state
environment = {
    'pH': 5.0,
    'EC': 1.0,
    'water_level': 0.8,
    'Nitrogen': 120,
    'Phosphorus': 40,
    'Potassium': 180,
}

def simulate_environment_change(env):
    env['pH'] += random.uniform(-0.05, 0.05)
    env['EC'] += random.uniform(-0.05, 0.05)
    env['water_level'] -= random.uniform(0.01, 0.03)
    env['Nitrogen'] -= random.uniform(1, 3)
    env['Phosphorus'] -= random.uniform(0.5, 2)
    env['Potassium'] -= random.uniform(1, 4)
    
    env['pH'] = max(4.0, min(env['pH'], 8.0))
    env['EC'] = max(0.5, min(env['EC'], 3.0))
    env['water_level'] = max(0, env['water_level'])
    for nut in ['Nitrogen', 'Phosphorus', 'Potassium']:
        env[nut] = max(0, env[nut])

def calculate_adjustments(env):
    adjustments = {}
    if env['water_level'] < lettuce_profile['water_level_min']:
        adjustments['water'] = round(lettuce_profile['water_level_min'] - env['water_level'], 2)
    if env['pH'] < lettuce_profile['pH'][0]:
        diff = lettuce_profile['pH'][0] - env['pH']
        adjustments['add_base_ml'] = round(diff * 10, 2)
    elif env['pH'] > lettuce_profile['pH'][1]:
        diff = env['pH'] - lettuce_profile['pH'][1]
        adjustments['add_acid_ml'] = round(diff * 10, 2)
    if env['EC'] < lettuce_profile['EC'][0]:
        diff = lettuce_profile['EC'][0] - env['EC']
        adjustments['add_nutrients_ml'] = round(diff * 50, 2)
    elif env['EC'] > lettuce_profile['EC'][1]:
        diff = env['EC'] - lettuce_profile['EC'][1]
        adjustments['dilute_water_l'] = round(diff * 0.5, 2)
    for nut in ['Nitrogen', 'Phosphorus', 'Potassium']:
        ideal = nutrients_profile[nut]
        actual = env[nut]
        if actual < ideal * 0.9:
            amt = round(ideal - actual, 2)
            adjustments[f'add_{nut}_mg_per_l'] = amt
    return adjustments

def apply_adjustments(env, adjustments):
    if 'water' in adjustments:
        env['water_level'] += adjustments['water']
    if 'add_base_ml' in adjustments:
        env['pH'] += adjustments['add_base_ml'] * 0.01
    if 'add_acid_ml' in adjustments:
        env['pH'] -= adjustments['add_acid_ml'] * 0.01
    if 'add_nutrients_ml' in adjustments:
        env['EC'] += adjustments['add_nutrients_ml'] * 0.01
    if 'dilute_water_l' in adjustments:
        env['water_level'] += adjustments['dilute_water_l']
        env['EC'] -= adjustments['dilute_water_l'] * 0.05
    for nut in ['Nitrogen', 'Phosphorus', 'Potassium']:
        key = f'add_{nut}_mg_per_l'
        if key in adjustments:
            env[nut] += adjustments[key]

# Tkinter GUI setup
root = tk.Tk()
root.title("Hydroponics Simulation")

labels = {}
for param in ['pH', 'EC', 'Water Level (L)', 'Nitrogen (mg/L)', 'Phosphorus (mg/L)', 'Potassium (mg/L)']:
    tk.Label(root, text=param + ": ", font=("Helvetica", 14)).pack()
    labels[param] = tk.Label(root, text="--", font=("Helvetica", 14, "bold"))
    labels[param].pack()

tk.Label(root, text="Adjustments Needed:", font=("Helvetica", 14, "underline")).pack(pady=(10,0))
adjustments_text = tk.Text(root, height=8, width=50, font=("Helvetica", 12))
adjustments_text.pack()

def update_gui():
    # Show current environment values
    labels['pH'].config(text=f"{environment['pH']:.2f}")
    labels['EC'].config(text=f"{environment['EC']:.2f}")
    labels['Water Level (L)'].config(text=f"{environment['water_level']:.2f}")
    labels['Nitrogen (mg/L)'].config(text=f"{environment['Nitrogen']:.2f}")
    labels['Phosphorus (mg/L)'].config(text=f"{environment['Phosphorus']:.2f}")
    labels['Potassium (mg/L)'].config(text=f"{environment['Potassium']:.2f}")

    # Calculate adjustments and apply
    adjustments = calculate_adjustments(environment)
    apply_adjustments(environment, adjustments)

    # Show adjustments text
    adjustments_text.delete(1.0, tk.END)
    if adjustments:
        for k, v in adjustments.items():
            adjustments_text.insert(tk.END, f"{k}: {v}\n")
    else:
        adjustments_text.insert(tk.END, "No adjustments needed. Environment is stable.\n")

    # Simulate environment changes
    simulate_environment_change(environment)

    # Schedule next update in 3 seconds (3000 ms)
    root.after(3000, update_gui)

# Start the loop
update_gui()
root.mainloop()
