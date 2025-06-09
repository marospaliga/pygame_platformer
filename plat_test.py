import pygame
import time

clock = pygame.time.Clock()
counter = 0
start_time = time.time()

while True:
    print("Tick")
    counter += 1
    clock.tick(120)
    
    if time.time() - start_time >= 1:
        print(f"Ticks in last second: {counter}")
        counter = 0
        start_time = time.time()

#testing comment