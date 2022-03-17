"""
This is a Solar System simulation using the pygame module 
@Khuslen Sugarbat
"""
import pygame
import math
pygame.init()

width, height = 1000, 1000
white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (100, 149, 237)
red = (188, 39, 50)
grey = (80, 78, 81)
screen = pygame.display.set_mode((width,height))
font = pygame.font.SysFont("comicsans", 16)
pygame.display.set_caption("Solar System Simulation")
class Planet:
    #Earth to Sun distance
    AU = 149.6e6*1000
    #Gravitational Constant 
    G = 6.67428e-11
    SCALE = 200/AU #1AU is 100 pixels 
    UNIT = 24 * 3600 #1 earth day 
    def __init__(self, x, y, radius, color, mass):
        #Basic constructors 
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color 
        self.mass = mass
        #Others
        self.sun = False
        self.orbit = []
        self.distance_to_sun = 0
        #Speed
        self.x_velocity = 0
        self.y_velocity = 0
    #Draws the planets
    def draw(self,win):
        x = self.x * self.SCALE + width / 2
        y = self.y * self.SCALE + height / 2
        #orbit 
        if len(self.orbit) > 2:
            new_position = []
            for position in self.orbit:
                x, y = position
                x = x * self.SCALE + width / 2
                y = y * self.SCALE + height / 2
                new_position.append((x,y))
            pygame.draw.lines(win, self.color, False, new_position, 2)
        if not self.sun:
            distance_text = font.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, white)
            screen.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))
        pygame.draw.circle(screen, self.color,(x,y),self.radius)
    #Gravitation
    def gravitation(self,other):
        x_other, y_other = other.x, other.y
        x_distance = x_other - self.x
        y_distance = y_other - self.y
        distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
        if other.sun:
            self.distance_to_sun = distance
        #Force of Gravitation
        force = self.G * self.mass * other.mass / distance ** 2
        #angle of force
        alpha = math.atan2(y_distance, x_distance)
        #force vectors
        x_force = force * math.cos(alpha)
        y_force = force * math.sin(alpha)
        return x_force, y_force
    #Movement
    def displacement(self, Planets):
        net_fx, net_fy = 0, 0
        for planet in Planets:
            if self == planet:
                continue
            fx, fy = self.gravitation(planet)
            net_fx += fx
            net_fy += fy
        # v = a * t, a = F / m, v= f /m * t
        self.x_velocity += net_fx / self.mass * self.UNIT
        self.y_velocity += net_fy / self.mass * self.UNIT
        self.x += self.x_velocity * self.UNIT
        self.y += self.y_velocity * self.UNIT
        self.orbit.append((self.x,self.y))
def main():
    condition = True 
    clock = pygame.time.Clock()
    #TheSun
    sun = Planet(0, 0, 30, yellow, 1.98892 * 10 ** 30)
    sun.sun = True
    #Mercury
    mercury = Planet(0.387 * Planet.AU, 0, 8, grey, 0.330 * 10 ** 24)
    mercury.y_velocity = -47.4 * 1000
    #Venus 
    venus = Planet(0.723 * Planet.AU, 0, 14, white, 4.865 * 10 ** 24)
    venus.y_velocity = -35.02 * 1000
    #TheEarth
    earth = Planet(-1 * Planet.AU, 0, 16, blue, 5.9742 * 10** 24)
    earth.y_velocity = 29.783 * 1000 
    #Mars
    mars = Planet(-1.524 * Planet.AU, 0, 12, red, 6.39 * 10 ** 23)
    mars.y_velocity = 24.077 * 1000
    #List of Planets
    Planets = [sun,mercury,venus,earth,mars]
    while condition:
        clock.tick(60)
        screen.fill((0, 0, 0))
        #screen.fill(WHITE)
        #pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                condition = False
        for planet in Planets:
            planet.displacement(Planets)
            planet.draw(screen)
        pygame.display.update()
    pygame.quit()
main()