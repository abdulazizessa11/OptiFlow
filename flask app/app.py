from flask import Flask, request, render_template
import random

app = Flask(__name__)

# الخوارزمية الجينية
DEPARTMENTS = ["A", "B", "C", "D"]
MAX_HOURS = 8

def fitness(individual):
    balance = -sum(abs(sum(hours[dep] for hours in individual.values()) - EMPLOYEES * MAX_HOURS / len(DEPARTMENTS))
                   for dep in DEPARTMENTS)
    coverage = sum(min(sum(hours[dep] for hours in individual.values()), EMPLOYEES * MAX_HOURS / len(DEPARTMENTS))
                   for dep in DEPARTMENTS)
    fairness = -sum(abs(sum(hours.values()) - MAX_HOURS) for hours in individual.values())
    overlap = sum(1 for hours in individual.values() if sum(1 for dep2 in DEPARTMENTS if hours[dep2] > 0) > 1)
    return 0.4 * balance + 0.4 * coverage + 0.2 * fairness - overlap

def generate_initial_population(pop_size, employees):
    population = []
    for _ in range(pop_size):
        individual = {f"Emp{i}": {dep: random.randint(0, MAX_HOURS) for dep in DEPARTMENTS} for i in range(employees)}
        population.append(individual)
    return population

def genetic_algorithm(pop_size, generations, employees):
    population = generate_initial_population(pop_size, employees)
    for _ in range(generations):
        population = sorted(population, key=fitness, reverse=True)[:pop_size//2]
        next_population = []
        for _ in range(pop_size):
            parent1, parent2 = random.sample(population, 2)
            child = {key: (random.choice([parent1[key][dep], parent2[key][dep]]) for dep in DEPARTMENTS)
                     for key in parent1.keys()}
            next_population.append(child)
        population = next_population
    return sorted(population, key=fitness, reverse=True)[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_algorithm():
    try:
        employees = int(request.form['employees'])
        generations = int(request.form['generations'])
        pop_size = int(request.form['population_size'])
        if employees <= 0 or generations <= 0 or pop_size <= 0:
            raise ValueError("Values must be positive integers.")

        best_solution = genetic_algorithm(pop_size, generations, employees)
        return render_template('result.html', solution=best_solution)

    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
