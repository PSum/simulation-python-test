import simpy
import numpy as np

# Total number of cutomers
NUM = 20

# Probability of arrival (5 %)
ARR = 0.05

# Collect data
interval = np.zeros(NUM)

def purchase (env, probArrival = 0.1):
    #Start timer
    minutes = 0
    while True:
        # Random number between 0 and 1 (or 0 % - 100 %)
        probability = np.random.rand()
        minutes += 1
        if probability < probArrival:
            print(f'Customer number {env.now} arrived.')
            print(f'It took {minutes} minutes.')
            # Add data
            interval[env.now-1] = minutes
            # Reset timer
            minutes = 0
            yield env.timeout(1)

env = simpy.Environment()

env.process(purchase(env, probArrival = ARR))
env.run(until = NUM +1)

print(interval)
