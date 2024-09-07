import serial  # For serial communication with ESP32
import pygame
from pygame.locals import *
from Output_radar import Radar
from output_config import *

# Initialize Pygame and radar display
pygame.init()
radar = Radar(screen, width, height)
clock = pygame.time.Clock()

# Serial port setup (adjust 'COM3' and baudrate accordingly)
ser = serial.Serial('COM8', 115200, timeout=1)  # Replace 'COM3' with your port
ser.flush()  # Clear any existing data in the serial buffer

def addBlip(angle):
    radar.addBlip(angle)

running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    # Read data from ESP32
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip()
            if data:  # If there's any data, interpret it as an angle
                angle = float(data)  # Convert the single value to a float
                addBlip(angle)  # Add blip at the received angle
        except Exception as e:
            print(f"Error processing data: {e}")

    # Update radar
    radar.draw()
    radar.update()
    clock.tick(frameRate)
    pygame.display.update()

# Cleanup
ser.close()
pygame.quit()
