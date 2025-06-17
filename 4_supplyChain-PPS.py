"""
Simulation of a process plant
"""
import simpy

simulationTime = 20

class ProcessPlant():
    def __init__(self, env):
        self.env = env
        self.tankIsEmpty = True
        self.start = env.process(self.run())

    def run(self):
        while True:
            if self.tankIsEmpty:
                print(f'Refilling tank at {self.env.now} mins')
                yield self.env.process(self.fillTank())
            else:
                print(f"Tank is full at {self.env.now} mins")
                yield self.env.timeout(1)

    def fillTank(self):
        print('Refilling the tank')
        yield self.env.timeout(10)
        self.tankIsEmpty = False

class Sim():
    def __init__(self, env):
        self.env = env
        self.processPlant = ProcessPlant(self.env)

env = simpy.Environment()
sim = Sim(env)
env.run(until=simulationTime)
