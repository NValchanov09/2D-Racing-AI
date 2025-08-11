import sys
import pygame
import neat
from Car import Car

class Simulation:
    
    def __init__(self, car_starting_x, car_starting_y, car_width, car_height, car_image_path, car_acceleration, car_braking_acceleration, car_angle_change, screen_width, screen_height, circuit_image_path, finish_x, finish_y, generation_time_limit, laps_multiplier, alive_multiplier):

        self.car_starting_x = car_starting_x
        self.car_starting_y = car_starting_y
        self.car_width = car_width
        self.car_height = car_height
        self.car_image_path = car_image_path
        self.car_acceleration = car_acceleration
        self.car_braking_acceleration = car_braking_acceleration
        self.car_angle_change = car_angle_change
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.circuit_image_path = circuit_image_path
        self.generation_time_limit = generation_time_limit
        self.finish_x = finish_x
        self.finish_y = finish_y
        self.laps_multiplier = laps_multiplier
        self.alive_multiplier = alive_multiplier

        self.generation = -1

    def draw_screen(self, alive_counter, laps_all, cars, finish, screen, circuit, generation_font, standard_font, clock):

        screen.blit(circuit, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)

        text = generation_font.render("Generation: " + str(self.generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = standard_font.render("Alive: " + str(alive_counter), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 520)
        screen.blit(text, text_rect)

        text = standard_font.render("Laps sum: " + str(laps_all), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 570)
        screen.blit(text, text_rect)

        text = standard_font.render("Laps average: " + str(int(laps_all / alive_counter)), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 620)
        screen.blit(text, text_rect)

        #pygame.draw.rect(screen, (255, 255, 0), finish)

        pygame.display.flip()
        clock.tick(60) 

    def update_cars(self, cars, genomes, circuit, finish):

        alive_counter = 0
        laps_all = 0

        for i, car in enumerate(cars):
            if car.is_alive():
                car.update(circuit, finish)
                alive_counter += 1
                laps_all += car.laps
            
            genomes[i][1].fitness = car.get_fitness()

        return [alive_counter, laps_all]

    def simulate(self, genomes, config):

        nets = []
        cars = []

        for id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            genome.fitness = 0

            cars.append(Car(self.car_starting_x, self.car_starting_y, self.car_width, self.car_height, self.car_image_path, self.car_acceleration, self.car_braking_acceleration, self.car_angle_change, self.laps_multiplier, self.alive_multiplier, self.generation_time_limit, self.screen_width, self.screen_height))

        pygame.init()

        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        clock = pygame.time.Clock()
        generation_font = pygame.font.SysFont("Arial", 70)
        standard_font = pygame.font.SysFont("Arial", 30)
        circuit = pygame.image.load(self.circuit_image_path)
        circuit = pygame.transform.scale(circuit, (self.screen_width, self.screen_height))
        finish = pygame.Rect(self.finish_x, self.finish_y, 30, 250)

        self.generation += 1

        time_begin = pygame.time.get_ticks()


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            for i, car in enumerate(cars):
                output = nets[i].activate(car.get_inputs())
                choice = output.index(max(output))

                car.perform(choice)

            info = self.update_cars(cars, genomes, circuit, finish)

            alive_counter = info[0]
            laps_all = info[1]

            if alive_counter == 0:
                break

            time_current = pygame.time.get_ticks()

            if time_current - time_begin > self.generation_time_limit:
                break

            self.draw_screen(alive_counter, laps_all, cars, finish, screen, circuit, generation_font, standard_font, clock)

