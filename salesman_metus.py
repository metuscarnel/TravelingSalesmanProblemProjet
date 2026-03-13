from math import radians, cos, sin, sqrt, atan2
import plotly.graph_objects as go
import pandas as pd
import json, haversine, random
def haversine_distance(ville1, ville2):
  return haversine.haversine((ville1.latitude, ville1.longitude), (ville2.latitude, ville2.longitude))

class Ville:
    def __init__(self, nom, latitude, longitude):
        self.nom = nom
        self.latitude = latitude
        self.longitude = longitude

def generate_random_villes(n):
    villes = []
    donnees_json = json.load(open("villes_france.json", "r", encoding="utf-8"))
    
    selection_aleatoire = random.sample(donnees_json, n)

    for item in selection_aleatoire:
        nouvelle_ville = Ville(
            nom=item["nom"],
            latitude=item["latitude"],
            longitude=item["longitude"]
        )
        villes.append(nouvelle_ville)

    return villes
def generate_individu(villes):
    individu = random.sample(villes, len(villes)) # Crée une nouvelle liste mélangée sans modifier l'originale
    return individu
def generate_genese(villes, taille_population):
    population = []
    for _ in range(taille_population):
        individu = generate_individu(villes)
        population.append(individu)
    return population


def fitness(individu):
    distance_totale = 0
    for i in range(len(individu) - 1):
        distance_totale += haversine_distance(
            individu[i],
            individu[i+1]
        )
    # On ajoute le retour à la ville de départ ici, pas dans l'individu
    distance_totale += haversine_distance(
        individu[-1],
        individu[0]
    )
    return 1 / distance_totale


def selection_tournoi(population, k=3):
    population_tournoi = random.sample(population, k) # Sélectionne k individus au hasard
    deux_parents = sorted(population_tournoi, key=fitness, reverse=True)[:2] # Garde les 2 meilleurs
    return deux_parents

def ox_crossover(parent1, parent2):
    
    
    taille = len(parent1)
    enfant = [None] * taille

    # 1. Sélection des segments
    p1_idx, p2_idx = sorted(random.sample(range(taille), 2))

    # 2. Copie du segment du parent 1
    enfant[p1_idx:p2_idx] = parent1[p1_idx:p2_idx]
    
    # On utilise un set pour que la recherche "in" soit instantanée (O(1))
    villes_presentes = set(enfant)

    # 3. Remplissage avec le parent 2
    # On commence à remplir APRES le segment copié pour respecter la logique OX
    p2_index = 0
    for i in range(taille):
        if enfant[i] is None:
            while parent2[p2_index] in villes_presentes:
                p2_index += 1
            enfant[i] = parent2[p2_index]
            villes_presentes.add(parent2[p2_index])
    
    return enfant

def swap_mutation(individu, p_mutation=0.02):
    # On décide SI on mute en fonction de la probabilité p
    if random.random() < p_mutation:
        idx1, idx2 = random.sample(range(len(individu)), 2)
        individu[idx1], individu[idx2] = individu[idx2], individu[idx1]
    return individu

def new_population(population, taille_population):
    nouvelle_population = []
    for _ in range(taille_population):
        parent1, parent2 = selection_tournoi(population)
        enfant = ox_crossover(parent1, parent2)
        enfant_muté = swap_mutation(enfant)
        nouvelle_population.append(enfant_muté)
    return nouvelle_population
global nb_gens

def tsp_algorithm(n_villes=5, taille_pop=100, gens=500):
    # Entrée : Nombre de points aléatoires [cite: 6]
    global nb_gens
    nb_gens = 0
    villes = generate_random_villes(n_villes)
    pop = generate_genese(villes, taille_pop)
    
    # On initialise le record avec le premier individu de la genèse
    meilleur_absolu = pop[0]
    for _ in range(gens):
        # 1. On crée la génération n+1 à partir de la n
        nouvelle_pop = new_population(pop, taille_pop)
        
        # 2. On cherche si un nouveau champion est apparu
        champion_gen = max(nouvelle_pop, key=fitness)
        if fitness(champion_gen) > fitness(meilleur_absolu):
            meilleur_absolu = champion_gen
        
        # 3. TRANSITION : La nouvelle génération devient la base de la suivante
        pop = nouvelle_pop 
        nb_gens += 1
        # Si auc une amélioration n'est trouvée, on peut arrêter plus tôt  
    # Sortie : Valeur totale de la distance (coût) [cite: 9]
    return villes, meilleur_absolu, 1 / fitness(meilleur_absolu)
            
                
print( "Résultat du TSP avec l'algorithme génétique :")
villes, chemin_optimal, distance = tsp_algorithm()
print("Ville de départ :", chemin_optimal[0].nom)
print("Distance totale :", distance, "km")
print("Chemin optimal :")
print("Test obtenu au bout de " + str(nb_gens) + " générations.")
for ville in chemin_optimal:
    print(ville.nom+" -> ", end="")

print(chemin_optimal[0].nom) # Retour à la ville de départ pour fermer le cycle