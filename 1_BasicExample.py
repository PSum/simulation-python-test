# Code according to link below
# https://simpy.readthedocs.io/en/latest/topical_guides/simpy_basics.html
import simpy  # Import SimPy simulation library

def example(env):
    # Pause the simulation for 1 unit of time, then return value 42
    value = yield env.timeout(1, value=42)
    # After the timeout, print the current simulation time and received value
    print('now=%d, value=%d' % (env.now, value))

env = simpy.Environment()  # Create a new simulation environment
p = env.process(example(env))  # Register the example() generator as a process
env.run()  # Run the simulation until all processes finish
