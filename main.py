import neat
import pygame
from Car import Car
from simulation import Simulation

screen_width = 2560
screen_height = 1440

car_starting_x = 1050
car_starting_y = 1200

car_acceleration = 0.2
car_braking_acceleration = 0.1
car_angle_change = 5
 
generation_time_limit = 30 * 1000 # in milliseconds

finish_x = 1000
finish_y = 1100

car_image_path = "car.png"
circuit_image_path = "circuit.png"

if __name__ == "__main__":

    config_path = "config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)
    
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    sim = Simulation(car_starting_x, car_starting_y, car_image_path, car_acceleration, car_braking_acceleration, car_angle_change, screen_width, screen_height, circuit_image_path, finish_x, finish_y, generation_time_limit)

    population.run(sim.simulate, 1000)