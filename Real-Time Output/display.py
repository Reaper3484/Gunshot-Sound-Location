import serial  
from radar_rt import Radar
from config_rt import *


pygame.init()
radar = Radar(screen, width, height)
clock = pygame.time.Clock()


ser = serial.Serial('COM8', 115200, timeout=1)  
ser.flush()  

def addBlip(angle):
    radar.addBlip(angle)

running = True

while running:
    
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode('utf-8').strip()
            if data:  
                angle = float(data)  
                addBlip(angle)  
        except Exception as e:
            print(f"Error processing data: {e}")

    
    radar.draw()
    radar.update()
    clock.tick(frameRate)
    pygame.display.update()


ser.close()
pygame.quit()
