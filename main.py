import pygame
from Car import Car

pygame.init()

screen_width = 2560
screen_height = 1440

car_starting_x = 900
car_starting_y = 1200

car_acceleration = 0.2
car_braking_acceleration = 0.1
car_angle_change = 5

generation = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Racing AI")

circuit = pygame.image.load("circuit.png")
circuit = pygame.transform.scale(circuit, (screen_width, screen_height))

car = Car(car_starting_x, car_starting_y, "car.png", car_acceleration, car_braking_acceleration, car_angle_change)

clock = pygame.time.Clock()
run = True

while run:
    clock.tick(60)
    screen.blit(circuit, (0, 0))
    car.draw(screen)
    pygame.display.update()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        car.rotate(True)
    if keys[pygame.K_d]:
        car.rotate(False)
    if keys[pygame.K_w]:
        car.move(True)
    if keys[pygame.K_s]:
        car.move(False)
    if keys[pygame.K_q]:
        run = False

    car.update(circuit)

    if car.is_alive() == False:
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()