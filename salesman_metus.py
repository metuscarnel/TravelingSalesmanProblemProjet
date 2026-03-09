class City  :
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5


def departure_city():
    return 

def generate_cities(n):
    import random
    return [City(random.uniform(0, 100), random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
cities = generate_cities(n) 

def traveling_salesman(cities):
    import random
    best_route = None
    best_distance = float('inf')

    for _ in range(1000):  # Nombre d'itérations
        route = cities[:]
        random.shuffle(route)
        distance = sum(route[i].distance_to(route[i + 1]) for i in range(len(route) - 1)) + route[-1].distance_to(route[0])
        
        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance