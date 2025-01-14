import random

# إعداد بيانات أولية
DEPARTMENTS = ["A", "B", "C", "D"]  # الأقسام
EMPLOYEES = 20  # عدد الموظفين
MAX_HOURS = 8  # الحد الأقصى لساعات العمل اليومية
MIN_HOURS = 4  # الحد الأدنى لساعات العمل اليومية
GENERATIONS = 100  # عدد الأجيال
POPULATION_SIZE = 50  # حجم السكان (عدد الحلول في كل جيل)
MUTATION_RATE = 0.1  # نسبة الطفرة

# إنشاء فرد
def create_individual():
    return {emp: {dep: random.randint(0, MAX_HOURS) for dep in DEPARTMENTS} for emp in range(EMPLOYEES)}

# إنشاء الجيل الأول
def initialize_population():
    return [create_individual() for _ in range(POPULATION_SIZE)]

# وظيفة التقييم
def fitness(individual):
    balance = -sum(abs(sum(hours[dep] for hours in individual.values()) - EMPLOYEES * MAX_HOURS / len(DEPARTMENTS))
                   for dep in DEPARTMENTS)
    coverage = sum(min(sum(hours[dep] for hours in individual.values()), EMPLOYEES * MAX_HOURS / len(DEPARTMENTS))
                   for dep in DEPARTMENTS)
    fairness = -sum(abs(sum(hours.values()) - MAX_HOURS) for hours in individual.values())
    overlap = sum(1 for hours in individual.values() if sum(1 for dep2 in DEPARTMENTS if hours[dep2] > 0) > 1)
    return 0.4 * balance + 0.4 * coverage + 0.2 * fairness - overlap

# الانتقاء
def selection(population):
    sorted_population = sorted(population, key=fitness, reverse=True)
    return sorted_population[:POPULATION_SIZE // 2]

# التزاوج
def crossover(parent1, parent2):
    child = {}
    for emp in parent1:
        child[emp] = parent1[emp] if random.random() < 0.5 else parent2[emp]
    return child

# الطفرة
def mutate(individual):
    if random.random() < MUTATION_RATE:
        emp = random.choice(list(individual.keys()))
        dep = random.choice(DEPARTMENTS)
        individual[emp][dep] = random.randint(MIN_HOURS, MAX_HOURS)
    return individual

# الجيل الجديد
def create_new_generation(population):
    new_generation = []
    selected = selection(population)
    while len(new_generation) < POPULATION_SIZE:
        parent1, parent2 = random.sample(selected, 2)
        child = crossover(parent1, parent2)
        child = mutate(child)
        new_generation.append(child)
    return new_generation

# الخوارزمية الجينية
def genetic_algorithm():
    population = initialize_population()
    for generation in range(GENERATIONS):
        population = create_new_generation(population)
        best_individual = max(population, key=fitness)
        print(f"Generation {generation + 1}: Best Fitness = {fitness(best_individual)}")
    return max(population, key=fitness)

# تشغيل الخوارزمية
best_solution = genetic_algorithm()

# عرض النتائج
print("\n")
for emp, schedule in best_solution.items():
    print(f"Employee {emp}: {schedule}")
