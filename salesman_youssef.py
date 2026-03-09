import random
import math
import tkinter as tk
from tkinter import ttk

# Générer des points aléatoir
def generate_points(n):
    return [(random.uniform(50, 450), random.uniform(50, 450)) for _ in range(n)]

# Calculer la distance euclidienne entre deux points
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Calculer la distance totale d'un chemin
def total_distance(path, points):
    return sum(distance(points[path[i]], points[path[i+1]]) for i in range(len(path)-1)) + distance(points[path[-1]], points[path[0]])

# Générer un individu aléatoire
def generate_individual(n):
    return random.sample(range(n), n)

# Générer une population initiale
def generate_population(pop_size, n):
    return [generate_individual(n) for _ in range(pop_size)]

# Sélectionner deux parents
def select_parents(population, points):
    fitness = [1 / total_distance(ind, points) for ind in population]
    return random.choices(population, weights=fitness, k=2)

# Croisement (Ordered Crossover)
def crossover(parent1, parent2):
    size = len(parent1)
    a, b = sorted(random.sample(range(size), 2))
    child1 = parent1[a:b]
    child1 += [item for item in parent2 if item not in child1]
    child2 = parent2[a:b]
    child2 += [item for item in parent1 if item not in child2]
    return child1, child2

# Mutation
def mutate(individual):
    a, b = random.sample(range(len(individual)), 2)
    individual[a], individual[b] = individual[b], individual[a]
    return individual

# Algorithme génétique
def genetic_algorithm(n_points, pop_size=100, generations=1000):
    points = generate_points(n_points)
    population = generate_population(pop_size, n_points)

    for _ in range(generations):
        new_population = []
        for _ in range(pop_size // 2):
            parent1, parent2 = select_parents(population, points)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])
        population = new_population

    best_individual = min(population, key=lambda ind: total_distance(ind, points))
    best_distance = total_distance(best_individual, points)
    return best_individual, points, best_distance

# Interface graphique avec Tkinter
class TSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Problème du Voyageur de Commerce (TSP)")

        # Paramètres
        self.n_points = tk.IntVar(value=10)
        self.pop_size = tk.IntVar(value=100)
        self.generations = tk.IntVar(value=1000)

        # Interface
        ttk.Label(root, text="Nombre de villes:").grid(column=0, row=0, padx=5, pady=5)
        ttk.Entry(root, textvariable=self.n_points).grid(column=1, row=0, padx=5, pady=5)

        ttk.Label(root, text="Taille de la population:").grid(column=0, row=1, padx=5, pady=5)
        ttk.Entry(root, textvariable=self.pop_size).grid(column=1, row=1, padx=5, pady=5)

        ttk.Label(root, text="Nombre de générations:").grid(column=0, row=2, padx=5, pady=5)
        ttk.Entry(root, textvariable=self.generations).grid(column=1, row=2, padx=5, pady=5)

        ttk.Button(root, text="Exécuter", command=self.run_algorithm).grid(column=0, row=3, columnspan=2, pady=10)

        self.canvas = tk.Canvas(root, width=500, height=500, bg='white')
        self.canvas.grid(column=0, row=4, columnspan=2, padx=5, pady=5)

        self.result_label = ttk.Label(root, text="")
        self.result_label.grid(column=0, row=5, columnspan=2, pady=5)

    def run_algorithm(self):
        n_points = self.n_points.get()
        pop_size = self.pop_size.get()
        generations = self.generations.get()

        best_path, points, best_distance = genetic_algorithm(n_points, pop_size, generations)

        self.canvas.delete("all")
        self.draw_path(best_path, points)
        self.result_label.config(text=f"Distance totale optimale: {best_distance:.2f}")

    def draw_path(self, path, points):
        for i, (x, y) in enumerate(points):
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='red')
            self.canvas.create_text(x, y-10, text=str(i))

        for i in range(len(path)):
            p1 = points[path[i]]
            p2 = points[path[(i+1) % len(path)]]
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill='blue')

# Exécuter l'application
root = tk.Tk()
app = TSPApp(root)
root.mainloop()
