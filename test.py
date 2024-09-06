import tkinter as tk
from tkinter import ttk
import pygame
import math
import threading

# Initialize Pygame and setup screen
pygame.init()
simWidth, simHeight = 800, 600
screen = pygame.display.set_mode((simWidth, simHeight), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Initial parameters
parameters = {
    'noOfMics': 4,
    'micRadius': 7,
    'micArrayRadius': 50,
    'micArrayWidth': 3,
    'soundWaveWidth': 10,
    'soundWaveSpeed': 5,
    'lineLen': 100,
    'lineWidth': 3,
    'lineRotationSpeed': 120,  # Degree per second
}

# Drawing the Pygame visualization
def draw_visualization():
    angle = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))

        # Draw radar circle
        pygame.draw.circle(screen, pygame.Color('lightgrey'), (simWidth // 2, simHeight // 2), parameters['micArrayRadius'], parameters['micArrayWidth'])

        # Draw microphones
        for i in range(parameters['noOfMics']):
            angle_deg = (360 / parameters['noOfMics']) * i
            angle_rad = math.radians(angle_deg)
            mic_x = int(simWidth // 2 + parameters['micArrayRadius'] * math.cos(angle_rad))
            mic_y = int(simHeight // 2 + parameters['micArrayRadius'] * math.sin(angle_rad))
            pygame.draw.circle(screen, pygame.Color('grey'), (mic_x, mic_y), parameters['micRadius'])

        # Draw rotating radar line
        end_x = simWidth // 2 + parameters['lineLen'] * math.cos(math.radians(angle))
        end_y = simHeight // 2 + parameters['lineLen'] * math.sin(math.radians(angle))
        pygame.draw.line(screen, pygame.Color('red'), (simWidth // 2, simHeight // 2), (end_x, end_y), parameters['lineWidth'])

        # Update the angle
        angle = (angle + parameters['lineRotationSpeed'] * (clock.get_time() / 1000)) % 360

        pygame.display.flip()
        clock.tick(60)

# Tkinter GUI for controlling parameters
def run_tkinter_interface():
    root = tk.Tk()
    root.title("Control Panel")

    def update_parameter(name, value):
        try:
            parameters[name] = int(float(value))  # Corrected conversion to handle float string
        except ValueError:
            pass  # Handle or log error if needed

    # Sliders and controls
    sliders = {
        'Number of Mics': ('noOfMics', 1, 10),
        'Mic Radius': ('micRadius', 1, 20),
        'Mic Array Radius': ('micArrayRadius', 10, 200),
        'Sound Wave Width': ('soundWaveWidth', 1, 20),
        'Sound Wave Speed': ('soundWaveSpeed', 1, 20),
        'Radar Line Length': ('lineLen', 50, 300),
        'Radar Line Width': ('lineWidth', 1, 10),
        'Line Rotation Speed': ('lineRotationSpeed', 10, 360)
    }

    # Create sliders for each parameter
    for label, (param, min_val, max_val) in sliders.items():
        frame = ttk.Frame(root)
        frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(frame, text=label).pack(side='left')
        scale = ttk.Scale(frame, from_=min_val, to=max_val, orient='horizontal', command=lambda value, p=param: update_parameter(p, value))
        scale.set(parameters[param])
        scale.pack(side='right', fill='x', expand=True)

    root.mainloop()

# Run Tkinter interface in a separate thread
tk_thread = threading.Thread(target=run_tkinter_interface)
tk_thread.daemon = True
tk_thread.start()

# Run Pygame visualization
draw_visualization()
