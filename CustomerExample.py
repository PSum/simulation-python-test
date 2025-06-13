import simpy

def customer(env, name, service_time, bank_counter):
    print(f'{name} arrives at the bank at {env.now}')
    with bank_counter.request() as req:
        yield req
        print(f'{name} starts being served at {env.now}')
        yield env.timeout(service_time)
        print(f'{name} leaves the bank at {env.now}')

# Create environment and resource
env = simpy.Environment()
bank_counter = simpy.Resource(env, capacity=1)

# Add customers to the environment
env.process(customer(env, 'Customer 1', 5, bank_counter))
env.process(customer(env, 'Customer 2', 3, bank_counter))

# Run the simulation
env.run(until=20)
