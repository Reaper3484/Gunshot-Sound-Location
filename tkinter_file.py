import tkinter as tk
from tkinter import ttk, colorchooser

# Function to handle color selection
def choose_color(entry, label):
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        entry.delete(0, tk.END)
        entry.insert(0, color_code)
        label.config(text=f"Current Value: {color_code}")

# Function to update parameters and display changes
def update_parameter(name, value, label):
    try:
        # Convert value if needed, handle floats and ints
        if '.' in str(value):
            new_value = float(value)
        else:
            new_value = int(value)
        label.config(text=f"Current Value: {new_value}")
    except ValueError:
        label.config(text="Invalid input")  # Handle invalid input gracefully

# Create the main window
root = tk.Tk()
root.title("Simulation Control Panel")
root.geometry("600x800")  # Set a size that fits all controls comfortably

# Create a notebook for organized tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

# Create a tab for each group of related settings
mic_tab = ttk.Frame(notebook)
array_tab = ttk.Frame(notebook)
source_tab = ttk.Frame(notebook)
sound_wave_tab = ttk.Frame(notebook)
radar_tab = ttk.Frame(notebook)

notebook.add(mic_tab, text="Microphones")
notebook.add(array_tab, text="Mic Array")
notebook.add(source_tab, text="Source")
notebook.add(sound_wave_tab, text="Sound Wave")
notebook.add(radar_tab, text="Radar")

# Define a helper function to create labeled sliders with value display
def create_slider(parent, label, var, min_val, max_val, callback):
    frame = ttk.Frame(parent)
    frame.pack(fill='x', padx=5, pady=5)
    ttk.Label(frame, text=label).pack(side='left', padx=5)
    value_label = ttk.Label(frame, text=f"Current Value: {var.get()}")
    value_label.pack(side='right')
    slider = ttk.Scale(frame, from_=min_val, to=max_val, orient='horizontal', variable=var, 
                       command=lambda v: callback(label, var.get(), value_label))
    slider.pack(side='right', fill='x', expand=True)

# Define a helper function to create labeled entry fields with value display
def create_entry(parent, label, var, callback):
    frame = ttk.Frame(parent)
    frame.pack(fill='x', padx=5, pady=5)
    ttk.Label(frame, text=label).pack(side='left', padx=5)
    entry = ttk.Entry(frame, textvariable=var)
    entry.pack(side='right', fill='x', expand=True)
    value_label = ttk.Label(frame, text=f"Current Value: {var.get()}")
    value_label.pack(side='right', padx=5)
    entry.bind('<Return>', lambda event: callback(label, var.get(), value_label))

# Define a helper function to create color pickers with value display
def create_color_picker(parent, label, var):
    frame = ttk.Frame(parent)
    frame.pack(fill='x', padx=5, pady=5)
    ttk.Label(frame, text=label).pack(side='left', padx=5)
    entry = ttk.Entry(frame, textvariable=var)
    entry.pack(side='left', fill='x', expand=True, padx=5)
    value_label = ttk.Label(frame, text=f"Current Value: {var.get()}")
    value_label.pack(side='right', padx=5)
    button = ttk.Button(frame, text="Choose Color", command=lambda: choose_color(entry, value_label))
    button.pack(side='right')

# Variables for microphone settings
no_of_mics = tk.IntVar(value=4)
mic_radius = tk.IntVar(value=7)
mic_idle_color = tk.StringVar(value='grey')
mic_detected_color = tk.StringVar(value='green')

# Microphones tab
create_slider(mic_tab, "Number of Mics", no_of_mics, 1, 10, update_parameter)
create_slider(mic_tab, "Mic Radius", mic_radius, 1, 20, update_parameter)
create_color_picker(mic_tab, "Mic Idle Color", mic_idle_color)
create_color_picker(mic_tab, "Mic Detected Color", mic_detected_color)

# Variables for mic array settings
mic_array_radius = tk.IntVar(value=50)
mic_array_width = tk.IntVar(value=3)
array_color = tk.StringVar(value='light grey')

# Mic Array tab
create_slider(array_tab, "Mic Array Radius", mic_array_radius, 10, 200, update_parameter)
create_slider(array_tab, "Mic Array Width", mic_array_width, 1, 20, update_parameter)
create_color_picker(array_tab, "Array Color", array_color)

# Variables for source settings
source_pos_x = tk.IntVar(value=500)
source_pos_y = tk.IntVar(value=0)
source_color = tk.StringVar(value='red')
source_size = tk.IntVar(value=10)

# Source tab
create_entry(source_tab, "Source X Position", source_pos_x, update_parameter)
create_entry(source_tab, "Source Y Position", source_pos_y, update_parameter)
create_slider(source_tab, "Source Size", source_size, 1, 100, update_parameter)
create_color_picker(source_tab, "Source Color", source_color)

# Variables for sound wave settings
sound_wave_color = tk.StringVar(value='white')
sound_wave_width = tk.IntVar(value=10)
sound_wave_speed = tk.IntVar(value=5)

# Sound Wave tab
create_slider(sound_wave_tab, "Sound Wave Width", sound_wave_width, 1, 50, update_parameter)
create_slider(sound_wave_tab, "Sound Wave Speed", sound_wave_speed, 1, 50, update_parameter)
create_color_picker(sound_wave_tab, "Sound Wave Color", sound_wave_color)

# Variables for radar settings
radar_radius = tk.IntVar(value=80)
line_len = tk.IntVar(value=80)
line_color = tk.StringVar(value='red')
line_width = tk.IntVar(value=3)
line_rotation_speed = tk.IntVar(value=120)
line_trail_alpha = tk.IntVar(value=100)

# Radar tab
create_slider(radar_tab, "Radar Radius", radar_radius, 10, 200, update_parameter)
create_slider(radar_tab, "Line Length", line_len, 10, 200, update_parameter)
create_slider(radar_tab, "Line Width", line_width, 1, 20, update_parameter)
create_slider(radar_tab, "Line Rotation Speed", line_rotation_speed, 10, 360, update_parameter)
create_slider(radar_tab, "Line Trail Alpha", line_trail_alpha, 0, 255, update_parameter)
create_color_picker(radar_tab, "Line Color", line_color)

# Run the application
root.mainloop()
