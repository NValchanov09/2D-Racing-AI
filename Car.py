import math
import pygame

sensor_color = (255, 255, 0)
border_color = (37, 112, 42, 255)

screen_width = 2560
screen_height = 1440

car_width = 100
car_height = 100

def calculate_distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return int(math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)))

def clamp(x, lb, ub):
    if lb > ub:
        return

    if x < lb:
        x = lb
    
    if x > ub:
        x = ub

class Car:
    def __init__(self, x, y, image_path, acceleration, braking_acceleration, angle_change):

        self.sprite = pygame.image.load(image_path)
        self.sprite = pygame.transform.scale(self.sprite, (car_width, car_height))
        self.rotated_sprite = self.sprite

        self.position = [x, y]
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.corners = []
        self.angle = 0
        self.velocity = 0
        self.angle_change = angle_change
        self.acceleration = acceleration
        self.braking_acceleration = braking_acceleration
        self.center = [self.position[0] + car_width / 2, self.position[1] + car_height / 2]
        self.sensors = []
        self.alive = True
        self.distance = 0
        self.time_elapsed = 0
        self.laps = 0

    def draw(self, screen):

        screen.blit(self.rotated_sprite, self.position)
        # self.draw_sensors(screen)

    def draw_sensors(self, screen):

        for sensor in self.sensors:
            position, distance = sensor
            pygame.draw.line(screen, sensor_color, self.center, position, 1)
            pygame.draw.circle(screen, sensor_color, position, 6)

    def collision_check(self, map):

        self.alive = True
        for corner in self.corners:
            if map.get_at((int(corner[0]), int(corner[1]))) == border_color:
                self.alive = False
                self.time_elapsed = 0
                break

    def update_sensor(self, sensor_angle, map):

        length = 0
        x = int(self.center[0])
        y = int(self.center[1])

        while not map.get_at((x, y)) == border_color:
            length += 1
            x = int(self.center[0] + math.cos(math.radians(360 - self.angle - sensor_angle)) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - self.angle - sensor_angle)) * length)

        distance = calculate_distance(self.center[0], self.center[1], x, y)
        self.sensors.append([(x, y), distance])

    def rotate_sprite(self):

        rectangle = self.sprite.get_rect()
        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_sprite.get_rect().center
        rotated_sprite = rotated_sprite.subsurface(rotated_rectangle).copy()

        self.rotated_sprite = rotated_sprite

    def update(self, map):

        self.velocity = max(5, self.velocity)

        self.rotate_sprite()

        self.distance += self.velocity
        self.time_elapsed += 1

        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.velocity
        clamp(self.position[0], 0, screen_width)
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.velocity
        clamp(self.position[1], 0, screen_height)


        self.center = [self.position[0] + car_width / 2, self.position[1] + car_height / 2]

        length = car_width / 2
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        self.collision_check(map)

        self.sensors.clear()

        for sensor_angle in range(-90, 120, 45):
            self.update_sensor(sensor_angle, map)

    def is_alive(self):

        return self.alive
    
    def get_fitness(self):

        return self.distance / self.time_elapsed
    
    def get_inputs(self):
        
        sensors = self.sensors
        inputs = [0, 0, 0, 0, 0]

        for i, sensor in enumerate(sensors):
            inputs[i] = int(sensor[1] / 30)

        return inputs
    
    def rotate(self, direction):

        if direction == True:
            self.angle += self.angle_change
        else:
            self.angle -= self.angle_change
    
    def move(self, direction):

        if direction == True:
            self.velocity += self.acceleration
        else:
            self.velocity -= self.braking_acceleration

    def perform(self, choice):

        if choice == 0:
            self.move(True)
        elif choice == 1:
            self.move(False)
        elif choice == 2:
            self.rotate(True)
        else:
            self.rotate(False)
    