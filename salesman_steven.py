import random
import numpy as np
import matplotlib.pyplot as plt 


# Une ville est définie par ses coordonnées (x, y) dans un plan
class Ville:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self is other


# Générer un ensemble de villes
def generer_villes(nbr_villes):
    villes = []
    for i in range(nbr_villes):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        villes.append(Ville(x, y))
    return villes


# Un individu représente une solution possible au problème : un ordre de visite des villes
class Individu:
    def __init__(self, villes):
        self.liste_villes = villes.copy()
        random.shuffle(self.liste_villes)


# Une population est un ensemble d'individus
class Population:
    def __init__(self, taille_population, villes):
        self.liste_individus = []
        for i in range(taille_population):
            self.liste_individus.append(Individu(villes))


# Calcul de la distance entre deux villes
def distance(ville1, ville2):
    return np.sqrt((ville1.x - ville2.x)**2 + (ville1.y - ville2.y)**2)


# Calcul de la distance totale d'un individu (le chemin complet)
def distance_totale(individu):    
    distance_totale = 0
    for i in range(len(individu.liste_villes) - 1):
        distance_totale += distance(individu.liste_villes[i], individu.liste_villes[i+1])
    distance_totale += distance(individu.liste_villes[-1], individu.liste_villes[0])
    return distance_totale


# Validation d'un individu
def valider_individu(individu, villes_originales):
    if len(individu.liste_villes) != len(villes_originales):
        return False
    for ville in individu.liste_villes:
        if ville not in villes_originales:
            return False
    # Vérifier qu'il n'y a pas de doublons.
    if len(individu.liste_villes) != len(set(id(ville) for ville in individu.liste_villes)):
        return False
    return True


# Evaluation des individus : on trie la population en fonction de la distance totale (le plus court est le meilleur)
def evaluation(population):
    population.sort(key=lambda individu: distance_totale(individu))


# Croisement d'un individu avec un autre
def croisement(parent1, parent2, villes_originales):
    taille_chemin = len(parent1.liste_villes)
    start, end = sorted(random.sample(range(taille_chemin), 2))
    
    enfant_villes = [None] * taille_chemin
    enfant_villes[start:end] = parent1.liste_villes[start:end]
    
    # Marquer les villes déjà utilisées
    villes_utilisees = set(id(ville) for ville in enfant_villes if ville is not None)
    
    # Ajouter les villes du parent2 qui ne sont pas encore dans l'enfant
    for ville in parent2.liste_villes:
        if id(ville) not in villes_utilisees:
            for i in range(taille_chemin):
                if enfant_villes[i] is None:
                    enfant_villes[i] = ville
                    villes_utilisees.add(id(ville))
                    break
    
    # Vérification de sécurité : s'il reste des None, compléter avec les villes manquantes
    villes_manquantes = [ville for ville in villes_originales if id(ville) not in villes_utilisees]
    for i in range(taille_chemin):
        if enfant_villes[i] is None and villes_manquantes:
            enfant_villes[i] = villes_manquantes.pop(0)
    
    enfant = Individu([])
    enfant.liste_villes = enfant_villes
    
    # Validation finale
    if not valider_individu(enfant, villes_originales):
        # En cas d'erreur, retourner une copie du parent1
        print("!!! Croisement invalide détecté, utilisation du parent1")
        enfant = Individu(parent1.liste_villes)
    
    return enfant


# Mutation d'un individu 
def mutation(individu: Individu, taux_mutation):
    if random.random() < taux_mutation:
        i, j = random.sample(range(len(individu.liste_villes)), 2)
        temp = individu.liste_villes[i]
        individu.liste_villes[i] = individu.liste_villes[j]
        individu.liste_villes[j] = temp
    return individu


# Algorithme génétique 
def algorithme_genetique(generation, taille_population, villes, taux_mutation):
    population = Population(taille_population, villes)
    
    # Stocker le meilleur individu de chaque génération pour l'animation
    evolution_best_individuals = []
    evolution_distances = []

    for gen in range(generation):
        evaluation(population.liste_individus)
        
        # Sauvegarder le meilleur de cette génération
        meilleur_actuel = population.liste_individus[0]
        evolution_best_individuals.append(meilleur_actuel)
        evolution_distances.append(distance_totale(meilleur_actuel))
        
        nouvelle_population = population.liste_individus[:taille_population//2]

        while len(nouvelle_population) < taille_population:
            parent1, parent2 = random.sample(population.liste_individus[:taille_population//2], 2)
            enfant = croisement(parent1, parent2, villes)
            enfant = mutation(enfant, taux_mutation)
            nouvelle_population.append(enfant)

        population.liste_individus = nouvelle_population

    return evolution_best_individuals, evolution_distances


# Interface graphique - Animation de l'évolution
def animation_evolution(liste_individus, liste_distances, pause=0.5):
    for i, individu in enumerate(liste_individus):
        x = [ville.x for ville in individu.liste_villes] + [individu.liste_villes[0].x]
        y = [ville.y for ville in individu.liste_villes] + [individu.liste_villes[0].y]

        plt.clf()
        plt.plot(x, y, 'bo-', label="Chemin")
        plt.scatter(x[0], y[0], color='red', s=80, zorder=5, label="Départ/Arrivée")
        plt.title(f"Génération {i+1} | Distance: {liste_distances[i]:.2f}")
        plt.legend()
        plt.grid(True)
        plt.xlim(-5, 105)
        plt.ylim(-5, 105)
        plt.gca().set_aspect('equal')
        plt.pause(pause)

    plt.show()

def animation_graphique_évolution_distance(evolution_distances):
    # Graphique supplémentaire : évolution de la distance sur les générations
    plt.figure(figsize=(10, 5))
    plt.plot(evolution_distances, 'b-', linewidth=2, label="Distance minimale")
    plt.axhline(y=evolution_distances[-1], color='r', linestyle='--', alpha=0.5, 
                label=f"Final: {evolution_distances[-1]:.2f}")
    plt.xlabel("Génération")
    plt.ylabel("Distance totale")
    plt.title("Évolution de la distance minimale sur les générations")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def main():
    
    # PARAMÈTRES MODIFIABLES 

    # Nombre de villes 
    nbr_villes = 10
    
    # Taille de la population 
    taille_population = 100
    
    # Nombre de générations 
    generation = 100
    
    # Taux de mutation (0.1 = 10%)
    taux_mutation = 0.1
    
    # Temps de pause entre chaque génération (en secondes)
    pause_animation = 0.3

    #LANCEMENT DU PROGRAMME 

    # Générer les villes une seule fois
    villes = generer_villes(nbr_villes)
    print(f" {nbr_villes} villes générées")

    # Lancement de l'algorithme génétique
    print("- Démarrage de l'algorithme génétique...")
    evolution_best_individuals, evolution_distances = algorithme_genetique(
        generation, taille_population, villes, taux_mutation
    )
    
    meilleur_final = evolution_best_individuals[-1]
    
    print(f"- Distance totale finale : {distance_totale(meilleur_final):.2f}")
    

    # Animation de l'évolution génération par génération
    print("\n - Lancement de l'animation...")
    animation_evolution(evolution_best_individuals, evolution_distances, pause=pause_animation)

    # Graphique supplémentaire : évolution de la distance sur les générations (optionel)
    print("\n - Affichage du graphique...")
    animation_graphique_évolution_distance(evolution_distances)
    

if __name__ == "__main__":    
    main()
