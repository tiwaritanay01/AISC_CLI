import random
import math

def fitness(x):
    # Sphere function: global minimum at x = 0
    return x ** 2

def run_genetic_algorithm(pop_size=20, generations=50, mutation_rate=0.1):
    population = [random.uniform(-10, 10) for _ in range(pop_size)]

    for gen in range(generations):
        population.sort(key=fitness)
        parents = population[:2]

        # Crossover
        child = (parents[0] + parents[1]) / 2.0

        # Mutation
        if random.random() < mutation_rate:
            child += random.uniform(-1.0, 1.0)
        child = max(-10.0, min(10.0, child))

        population[-1] = child

    best = min(population, key=fitness)
    return best, fitness(best)

def run_simulated_annealing(initial_temp=100.0, cooling_rate=0.95, iterations=100):
    current = random.uniform(-10, 10)
    current_cost = fitness(current)
    temp = initial_temp

    for _ in range(iterations):
        neighbor = current + random.uniform(-1.0, 1.0)
        neighbor_cost = fitness(neighbor)
        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / max(temp, 1e-6)):
            current = neighbor
            current_cost = neighbor_cost

        temp *= cooling_rate

    return current, current_cost

if __name__ == "__main__":
    print("=" * 60)
    print(" LabX Exp 11: Genetic Algorithm & Simulated Annealing")
    print("=" * 60)

    ga_x, ga_fit = run_genetic_algorithm()
    print(f"Genetic Algorithm Result       : x = {ga_x:.6f}, f(x) = {ga_fit:.6f}")

    sa_x, sa_fit = run_simulated_annealing()
    print(f"Simulated Annealing Result     : x = {sa_x:.6f}, f(x) = {sa_fit:.6f}")
    print("=" * 60)

# ============================================================================
# EXPERIMENT THEORY (from AISC Laboratory Submission):
# ============================================================================
# Genetic algorithms mimic biological evolution: a population of candidate
# solutions is evolved through selection, crossover, and mutation to
# optimize a fitness function. Simulated annealing mimics physical
# annealing: a single solution is iteratively perturbed and accepted with a
# probability that decreases with temperature, allowing escape from local
# optima. Both methods rely on stochastic search and balance exploration
# with exploitation. Key parameters: population size, crossover/mutation
# rates for GA; cooling schedule and acceptance probability for SA.
# ============================================================================
