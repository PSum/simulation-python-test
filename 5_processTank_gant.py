"""
Gantt-style visualization of a two-tank process plant
"""

import simpy
import matplotlib.pyplot as plt
import pandas as pd

SIMULATION_TIME = 200


class Tank:
    def __init__(self, name):
        self.name = name
        self.empty = True


class ProcessPlant:
    def __init__(self, env):
        self.env = env
        self.conti = simpy.Resource(env, capacity=1)       # shared machine
        self.liquidPump = simpy.Resource(env, capacity=1)  # shared pump

        self.tank1 = Tank('Tank1')
        self.tank2 = Tank('Tank2')

        # times
        self.transferTime = 20
        self.inductionTime = 30
        self.dispersingTime = 10
        self.dosingTime = 15

        # logging
        self.log = []   # (resource, start, finish, task, tank)

    def record(self, resource, start, finish, task, tank):
        self.log.append({
            'resource': resource,
            'start': start,
            'finish': finish,
            'task': task,
            'tank': tank
        })

    def cycle_tank(self, tank):
        while True:
            if tank.empty:
                yield self.env.process(self.liquidDosing(tank))
            yield self.env.process(self.inductPowder(tank))
            yield self.env.process(self.disperse(tank))
            yield self.env.process(self.transfer(tank))

    def liquidDosing(self, tank):
        with self.liquidPump.request() as req:
            yield req
            start = self.env.now
            yield self.env.timeout(self.dosingTime)
            finish = self.env.now
            tank.empty = False
            self.record('Pump', start, finish, 'Liquid dosing', tank.name)

    def inductPowder(self, tank):
        with self.conti.request() as req:
            yield req
            start = self.env.now
            yield self.env.timeout(self.inductionTime)
            finish = self.env.now
            self.record('Machine', start, finish, 'Powder induction', tank.name)

    def disperse(self, tank):
        with self.conti.request() as req:
            yield req
            start = self.env.now
            yield self.env.timeout(self.dispersingTime)
            finish = self.env.now
            self.record('Machine', start, finish, 'Dispersing', tank.name)

    def transfer(self, tank):
        with self.conti.request() as req:
            yield req
            start = self.env.now
            yield self.env.timeout(self.transferTime)
            finish = self.env.now
            tank.empty = True
            self.record('Machine', start, finish, 'Transfer', tank.name)


# run simulation
env = simpy.Environment()
plant = ProcessPlant(env)
env.process(plant.cycle_tank(plant.tank1))
env.process(plant.cycle_tank(plant.tank2))
env.run(until=SIMULATION_TIME)

# prepare dataframe
df = pd.DataFrame(plant.log)
df['duration'] = df['finish'] - df['start']

# assign y-positions for resources
resources = ['Machine', 'Pump']
ypos = {res: i * 10 for i, res in enumerate(resources)}

# plot
fig, ax = plt.subplots(figsize=(10, 4))
for _, row in df.iterrows():
    ax.broken_barh([(row['start'], row['duration'])],
                   (ypos[row['resource']], 8),
                   facecolors=('tab:blue' if row['tank'] == 'Tank1' else 'tab:orange'),
                   label=row['tank'])

# axes and labels
ax.set_yticks([y + 4 for y in ypos.values()])
ax.set_yticklabels(resources)
ax.set_xlabel("Time")
ax.set_ylabel("Resource")
ax.set_title("Process timeline")

# legend (unique tank colors)
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

plt.tight_layout()
plt.show()
