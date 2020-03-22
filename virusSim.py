import pygame,random

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

populations = []

class city():
    def __init__(self,parent,x,y):
        self.parentPopulation = parent
        self.infectionTime = 0
        self.x, self.y = x,y
        self.populationTotal = 25000
        self.populationInfected = 0
        self.populationHealthy = 25000
        self.populationCured = 0
        self.populationDead = 0
        self.infected = False

    def draw_self(self):
        if self.infected == False:
            pygame.draw.rect(screen, (0,255,0), pygame.Rect(self.x,self.y,10,10)) 
        else:
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.x,self.y,10,10))

class population():
    # Popluation limit between 0-16
    # Population = 100,000 * number
    def __init__(self,population, x, y):
        self.x, self.y = x,y
        self.popNum = population
        self.populationTotal = population*100000
        self.populationInfected = 0
        self.populationHealthy = population*100000
        self.populationCured = 0
        self.populationDead = 0
        self.cities = []
        populations.append(self)
        self.create_population_cubes()

    def create_population_cubes(self):
        # Each population will be made of cubes
        # Each cube will be 25,000 people
        # One population is 4 cubes
        g = 0
        for b in range(8):
            for a in range(8):
                x,y = (self.x + (15*a)), (self.y + (15*b))
                c = city(self,x,y)
                self.cities.append(c)
                g += 25000
                if g == self.populationTotal:
                    break
            if g == self.populationTotal:
                break

class virus():
    def __init__(self, infectRate, mortalityRate, infectionPeriod):
        # Infect Rate is how likely a person is to spread the virus
        # Morality Rate is how likely an infected person is to die as a result of the virus
        # Infection Period is how long before the virus "wears off" - 1 tick = 1 day
        # Infect and Morality rate value between 0-10
        # Infection Period has no limit, put 0 for virus that can't be cured
        self.infectRate = infectRate
        self.mortalityRate = mortalityRate
        self.infectionPeriod = infectionPeriod
        self.infectedCities = []
        self.infectedPopulations = []
        self.totalInfected = 0
        self.totalKilled = 0

    def virusRun(self):
        # Main function for the virus
        # Controls infection, falalities, spread, etc
        
        # Infect more people
        for c in self.infectedCities:
            for i in range(c.populationInfected):
                if c.populationHealthy > 0:
                    x = random.choice(range(11))
                    if x <= self.infectRate:
                        c.populationInfected += 1
                        c.populationHealthy -= 1
                        c.parentPopulation.populationInfected += 1
                        c.parentPopulation.populationHealthy -= 1
                        self.totalInfected += 1

        # Kill Infected
        for c in self.infectedCities:
            for i in range(c.populationInfected):
                if c.populationTotal > 0:
                    x = random.choice(range(11))
                    if x <= self.mortalityRate and self.mortalityRate != 0:
                        c.populationInfected -= 1
                        c.populationTotal -= 1
                        c.populationDead += 1
                        c.parentPopulation.populationInfected -= 1
                        c.parentPopulation.populationTotal -= 1
                        c.parentPopulation.populationDead += 1
                        self.totalKilled += 1

        # Spread to other Cities
        for p in self.infectedPopulations:
            for c in p.cities:
                if c in self.infectedCities:
                    pass
                else:
                    x = random.choice(range(11))
                    if x <= self.infectRate/2:
                        self.infectedCities.append(c)
                        c.infected = True
                        c.infectionTime = simCurrentTick
                        c.populationInfected += 1
                        c.populationHealthy += 1
                        p.populationInfected += 1
                        p.populationHealthy += 1
                        self.totalInfected += 1

        # Spread to other populations
        for p in populations:
            if p in self.infectedPopulations:
                break
            else:
                x = random.choice(range(11))
                if x == 0:
                    self.infectedPopulations.append(p)
                    p.populationInfected += 1
                    p.populationHealthy -= 1
                    c = random.choice(p.cities)
                    c.infected = True
                    c.infectionTime = simCurrentTick
                    c.populationInfected += 1
                    c.populationHealthy -= 1
                    self.totalInfected += 1

        # Cure Infected
        if self.infectionPeriod > 0:
            for c in self.infectedCities:
                for i in range(c.populationInfected):
                    if c.populationInfected > 0:
                        if (simCurrentTick - c.infectionTime) >= self.infectionPeriod:
                            x = random.choice(range(2))
                            if x == 0:
                                c.populationInfected -= 1
                                c.populationCured += 1
                                c.populationHealthy += 1
                                c.parentPopulation.populationInfected -= 1
                                c.parentPopulation.populationCured += 1
                                c.parentPopulation.populationHealthy += 1
                                if c.populationInfected <= 0:
                                    c.infected = False

populationA = population(4,50,50)
populationA.name = "A"
populationB = population(8,200,200)
populationB.name = "B"
populationC = population(10,400,500)
populationC.name = "C"
populationD = population(3,500,100)
populationD.name = "D"
populationE = population(2,100,500)
populationE.name = "E"

TestVirus = virus(5,0,14)

hostPop = random.choice(populations)
hostCity = random.choice(hostPop.cities)
hostCity.infected = True
hostCity.infectionTime = 0
hostCity.populationInfected += 1
hostCity.populationHealthy -= 1
hostCity.parentPopulation.populationInfected += 1
hostCity.parentPopulation.populationHealthy -= 1
TestVirus.totalInfected += 1
TestVirus.infectedCities.append(hostCity)
TestVirus.infectedPopulations.append(hostPop)

simCurrentTick = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    print("Time: " + str(simCurrentTick))

    for p in populations:
        for c in p.cities:
            c.draw_self()
        print(p.name + "(" + str(p.popNum*100000) + ")" + ": " + str(p.populationInfected) + " Infected, " + str(p.populationDead) + " Dead, " + str(p.populationCured) + " Cured")

    TestVirus.virusRun()

    print("\n")

    clock.tick(1)
    simCurrentTick += 1
    pygame.display.update()
