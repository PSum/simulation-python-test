"""
Disruption in supply chains
"""
import simpy
import numpy as np

# Parameter für die Simulationsdauer
NUM = 1000

# Liste zur Speicherung des Lagerbestands im Zeitverlauf
stock = [100]

class Store():
	"""
	Store modelliert das Lager eines Geschäfts, das Reis führt.
	Kunden treffen zufällig ein und kaufen eine kleine Menge Reis.
	"""
	def __init__(self, env):
		"""
		env: SimPy-Umgebung (Zeitsteuerung)
		self.stock: Startlagerbestand
		self.start: Startet den Simulationsprozess für das Lager
		"""
		self.env = env
		self.stock = 100
		self.start = env.process(self.run())  # Prozess für Kundeninteraktion

	def run(self):
		"""
		Reagiert auf zufällige Kundennachfrage.
		Bei einer Wahrscheinlichkeit von 10 % pro Zeiteinheit kommt ein Kunde.
		Jeder Kunde kauft 1 oder 2 Einheiten Reis.
		"""
		while True:
			prob = np.random.rand()  # Zufallswert zwischen 0 und 1
			if prob < 0.1:
				print(f'Customer number {env.now} arrived.')
				self.stock -= np.random.randint(1, 3)  # 1 oder 2 Einheiten
				print(f'Current stock {self.stock}.')
				stock.append(self.stock)  # Lagerstand protokollieren
				yield env.timeout(1)  # Zeitfortschritt um 1 Zeiteinheit
			else:
				yield env.timeout(1)  # Auch ohne Kunde vergeht Zeit

class Ship():
	"""
	Ship bringt in regelmäßigen Abständen neue Reissendungen.
	Jede Lieferung füllt 15 Einheiten Reis auf.
	Reisezeit ist zufällig zwischen 7 und 12 Zeiteinheiten.
	"""
	def __init__(self, env, store):
		"""
		env: SimPy-Umgebung
		store: Referenz auf das Lager, um Reis dorthin zu liefern
		"""
		self.env = env
		self.capacity = 15  # Liefermenge pro Lieferung
		self.start = env.process(self.run(store))  # Startet Schiffprozess

	def run(self, store):
		"""
		Führt den Lebenszyklus eines Schiffes aus:
		- Fahrt beginnt
		- wartet die Reisezeit ab (on_sea)
		- liefert Reis im Lager ab
		"""
		while True:
			print(f"Ship starts at {env.now}")
			yield env.process(self.on_sea())  # Schiff unterwegs

			store.stock += self.capacity  # Reis wird im Lager ergänzt
			print(f"Ship reaches at {env.now}")
			print(f"Store has {store.stock} units of rice.")
			yield env.timeout(1)  # Pause nach Entladung

	def on_sea(self):
		"""
		Bestimmt zufällige Reisedauer zwischen 7 und 12 Zeiteinheiten
		"""
		time = np.random.randint(7, 13)
		yield self.env.timeout(time)  # Zeitfortschritt

class Sim():
	"""
	Initialisiert die gesamte Simulation.
	Erstellt eine Store-Instanz und eine Ship-Instanz.
	"""
	def __init__(self, env):
		self.env = env
		self.store = Store(self.env)
		self.ship = Ship(env = self.env, store = self.store)

# Erzeuge SimPy-Umgebung und starte Simulation
env = simpy.Environment()
sim = Sim(env)
env.run(until = NUM)
