""":
Simulation of a process plant
"""

import simpy

simulationTime = 120

class Tank:
    def __init__(self, name):
        self.name = name
        self.empty = True

class ProcessPlant():
    def __init__(self, env):
        self.env = env
        self.conti = simpy.Resource(env, capacity=1)
        self.liquidPump = simpy.Resource(env, capacity=1)
        self.tankEmpty = True
        self.powderInductionFinished = False

        # tanks
        self.tank1 = Tank('Tank1')
        self.tank2 = Tank('Tank2')

        # times
        self.transferTime = 20
        self.inductionTime = 30
        self.dispersingTime = 10
        self.bufferTime = 3
        self.dosingTime = 15
        self.batchFinished = False

        self.env.process(self.cycle_tank1())
        self.env.process(self.cycle_tank2())

    def cycle_tank1(self):
        while True:
            if self.tank1.empty:
                yield self.env.process(self.liquidDosing(self.tank1))
            yield self.env.process(self.inductPowder(self.tank1))
            yield self.env.process(self.disperse(self.tank1))
            yield self.env.process(self.transfer(self.tank1))

    def cycle_tank2(self):
        while True:
            if self.tank2.empty:
                yield self.env.process(self.liquidDosing(self.tank2))
            yield self.env.process(self.inductPowder(self.tank2))
            yield self.env.process(self.disperse(self.tank2))
            yield self.env.process(self.transfer(self.tank2))

    def liquidDosing(self, tank):
        with self.liquidPump.request() as req:
            yield req
            print(f'{self.env.now} min: {tank.name} filling liquid')
            yield self.env.timeout(self.dosingTime)
            tank.empty = False
            print(f'{self.env.now} min: {tank.name} liquid filled')

    def inductPowder(self, tank):
        with self.conti.request() as req:
            yield req
            print(f'{self.env.now} min: {tank.name} powder induction started')
            yield self.env.timeout(self.inductionTime)
            print(f'{self.env.now} min: {tank.name} powder induction finished')

    def disperse(self, tank):
        with self.conti.request() as req:
            yield req
            print(f'{self.env.now} min: {tank.name} dispersing started')
            yield self.env.timeout(self.dispersingTime)
            print(f'{self.env.now} min: {tank.name} dispersing finished')

    def transfer(self, tank):
        with self.conti.request() as req:
            yield req
            print(f'{self.env.now} min: {tank.name} transfer started')
            yield self.env.timeout(self.transferTime)
            print(f'{self.env.now} min: {tank.name} transfer finished')
            tank.empty = True
    

env = simpy.Environment()
plant = ProcessPlant(env)
env.run(until=simulationTime)
