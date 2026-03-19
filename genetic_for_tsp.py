from math import radians, cos, sin, sqrt, atan2
import json, haversine, random, itertools


# haversine distance
def haversine_distance(ville1, ville2):
    return haversine.haversine(
        (ville1.latitude, ville1.longitude), (ville2.latitude, ville2.longitude)
    )


def distance(individu):
    d = 0
    for i in range(len(individu) - 1):
        d += haversine_distance(individu[i], individu[i + 1])
    d += haversine_distance(individu[-1], individu[0])
    return d


# CLASSE VILLE


class Ville:
    def __init__(self, nom, latitude, longitude):
        self.nom = nom
        self.latitude = latitude
        self.longitude = longitude


def generate_random_villes(n):
    with open("villes_france.json", "r", encoding="utf-8") as f:
        donnees_json = json.load(f)

    selection = random.sample(donnees_json, n)

    return [
        Ville(item["nom"], item["latitude"], item["longitude"]) for item in selection
    ]


def generate_individu(villes):
    return random.sample(villes, len(villes))


def generate_population(villes, taille):
    pop = []
    for _ in range(taille):
        pop.append(generate_individu(villes))
    return pop


# selection tournoi
def selection_tournoi(population, k=3):
    participants = random.sample(population, k)
    participants.sort(key=distance)
    return participants[0], participants[1]


# order crossover
def ox_crossover(parent1, parent2):
    taille = len(parent1)
    enfant = [None] * taille

    i, j = sorted(random.sample(range(taille), 2))
    enfant[i:j] = parent1[i:j]

    villes_presentes = set(enfant)

    p2_index = 0
    for k in range(taille):
        if enfant[k] is None:
            while parent2[p2_index] in villes_presentes:
                p2_index += 1
            enfant[k] = parent2[p2_index]
            villes_presentes.add(parent2[p2_index])

    return enfant


# swap mutation
def swap_mutation(individu, p=0.02):
    if random.random() < p:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu


# nouvelle population
def new_population(population, taille):
    nouvelle = []

    for _ in range(taille):
        p1, p2 = selection_tournoi(population)
        enfant = ox_crossover(p1, p2)
        enfant = swap_mutation(enfant)
        nouvelle.append(enfant)

    return nouvelle


# fonction principale
def tsp_algorithm(villes, taille_pop=100, gens=500):
    pop = generate_population(villes, taille_pop)
    best = min(pop, key=distance)

    for _ in range(gens):
        pop = new_population(pop, taille_pop)
        current_best = min(pop, key=distance)

        if distance(current_best) < distance(best):
            best = current_best

    return best, distance(best)


# analyse combinatoire brute-force pour tester et valider
def brute_force(villes):
    best = float("inf")
    best_tour = None

    for perm in itertools.permutations(villes[1:]):
        tour = [villes[0]] + list(perm)
        d = distance(tour)

        if d < best:
            best = d
            best_tour = tour

    return best, best_tour


# main
if __name__ == "__main__":
    random.seed(42)  # Pour des résultats reproductibles

    # villes
    villes = generate_random_villes(100)

    print("Calcul optimum (bruteforce)...")
    # opt, _ = brute_force(villes)

    print("Algo génétique...")
    sol, dist = tsp_algorithm(villes)

    print("\nRésultats :")
    # print("Résultat bruteforce :", opt)
    print("Résultat algo génétique :", dist)
    # print("Taux d'erreur (%) :", (dist - opt) / opt * 100) #calcul du taux d'erreur

    print("\nTour trouvé :")
    for v in sol:
        print(v.nom, "->", end="")
