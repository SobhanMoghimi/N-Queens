import random

import matplotlib.pyplot as plt


def generate_chromosome(n):
    return [random.randint(0, n - 1) for _ in range(n)]


def fitness(chromosome):
    conflicts = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            if chromosome[i] == chromosome[j] or abs(chromosome[i] - chromosome[j]) == abs(i - j):
                conflicts += 1
    return -conflicts


def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child


def mutate(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = random.randint(0, len(chromosome) - 1)
    return chromosome


def genetic_algorithm(n, population_size=100, mutation_rate=0.1, max_generations=4000):
    population = [generate_chromosome(n) for _ in range(population_size)]

    for generation in range(max_generations):
        population = sorted(population, key=fitness, reverse=True)

        if not generation % 25:
            print("Generation: {}. Fitness: {}".format(generation, fitness(population[0])))
        if fitness(population[0]) == 0:
            print("Found Answer on Generation: {}. Fitness: {}".format(generation, fitness(population[0])))
            return population[0]

        next_generation = population[:2]
        for _ in range(population_size - 2):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            next_generation.append(child)
        population = next_generation
    return None


def plot_solution(solution):
    def create_board(solution):
        n = len(solution)
        board = [[0] * n for _ in range(n)]
        for row, col in enumerate(solution):
            board[row][col] = 1
        return board

    def draw_board(board):
        n = len(board)
        fig, ax = plt.subplots()
        ax.imshow(board, cmap='binary', extent=(0, n, 0, n), origin='lower')

        for row in range(n):
            for col in range(n):
                if board[row][col] == 1:
                    ax.text(col, row, '', fontsize=12, ha='center', va='center', color='black')

        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(True, which='both', color='black', linewidth=1)
        plt.show()

    board = create_board(solution)
    draw_board(board)


if __name__ == '__main__':
    N = int(input('Set the board size: '))
    solution = genetic_algorithm(N)
    if solution:
        print(f"Solution for {N}x{N} board:")
        plot_solution(solution)
    else:
        print(f"No solution found for {N}x{N} board")
