import random

import musicalbeeps as musicalbeeps
from deap import base
from deap import creator
from deap import tools
from deap import algorithms


basic_notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # List of all existing notes
find_melody = ['E', 'D', 'C', 'D', 'E', 'E', 'E', 'D', 'D', 'D', 'E', 'G', 'G', 'E', 'D', 'C', 'D', 'E', 'E', 'E', 'D',
               'D', 'D', 'E', 'G', 'G', 'E', 'D', 'C', 'D', 'E', 'E', 'E', 'D', 'D', 'D', 'E', 'G', 'G', 'E', 'D', 'C',
               'D', 'E', 'E', 'E', 'D', 'D', 'D', 'E', 'G', 'G']  # Melody that is trying to be found
test_melody = ['E', 'D', 'C', 'D', 'E', 'E', 'E', 'D', 'D', 'D', 'E', 'G', 'G']  # Melody that is incorrect
note_pos_dict = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': []}  # Position dictionary for each note
IND_SIZE = len(find_melody)  # Size of the target melody
note_amount = len(basic_notes)  # Size of the existing notes list


def note_pos(note_pos_dict):
    counter_pos = 0
    for i in find_melody:
        match i:
            case 'A':
                note_pos_dict['A'].append(counter_pos)
            case 'B':
                note_pos_dict['B'].append(counter_pos)
            case 'C':
                note_pos_dict['C'].append(counter_pos)
            case 'D':
                note_pos_dict['D'].append(counter_pos)
            case 'E':
                note_pos_dict['E'].append(counter_pos)
            case 'F':
                note_pos_dict['F'].append(counter_pos)
            case 'G':
                note_pos_dict['G'].append(counter_pos)
        counter_pos += 1

    return note_pos_dict


note_pos_dict = note_pos(note_pos_dict)
print(note_pos_dict)


def random_note():
    note = basic_notes[random.randint(0, note_amount - 1)]
    return note


def find_difference_pos(note, counter_pos):
    lst = note_pos_dict.get(note)

    if counter_pos in lst:
        return 0
    elif len(lst) == 0:
        return IND_SIZE * 2
    else:
        retValue = lst[min(range(len(lst)), key=lambda i: abs(lst[i] - counter_pos))]
        return retValue


def evaluate_melody(individual):
    fitness_value = 0
    counter_pos = 0

    # | (broj_nota - razlika_pozicija)/broj_nota - razlika_ascii | = 169
    for note in individual:
        fitness_value += ((IND_SIZE - find_difference_pos(note, counter_pos) / IND_SIZE -
                           abs(ord(find_melody[counter_pos]) - ord(note))))

        counter_pos += 1
    return fitness_value,


def mutMelody(individual, mutperc):
    tmpList = []
    for i in range(len(individual)):
        tmpList.append(individual[i])
    mut_count = round(len(individual) * mutperc)

    for i in range(mut_count):
        var = random.randint(0, len(tmpList) - 1)
        del tmpList[var]

        new_note = random.randint(0, note_amount - 1)
        tmpList.append(basic_notes[new_note])

    return tmpList,


creator.create("Fitness", base.Fitness, weights=(1,))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("attr_note", random_note)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_note, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# print(evaluate_melody(test_melody))

toolbox.register("evaluate", evaluate_melody)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutMelody, mutperc=0.2)  # tools.mutGaussian, mu=0.5, sigma=1.2,
# indpb=0.2
toolbox.register("select", tools.selNSGA2)


def main():
    MU = 120
    CXPB = 0.7
    MUTPB = 0.3

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)

    print("Start of evolution")

    # Evaluate entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while max(fits) < pow(IND_SIZE, 2):
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))


if __name__ == "__main__":
    main()

player = musicalbeeps.Player(volume=0.1, mute_output=False)

# To play an A on default octave n°4 for 0.2 seconds
for i in find_melody:
    player.play_note(i)
