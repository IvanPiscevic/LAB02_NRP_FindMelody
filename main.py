#!python3
# LAB02 - FindMelodyGA
# This program was made by Tomislav Horvat and Ivan Piscevic for class Unconventional computing procedures.
# Program uses python library DEAP.
# To try different songs, comment the first find_melody list, and uncomment the other one,
# or add your own but make sure you use find_melody variable name.
# For larger melodies (length > 50) It's important to use larger mu - population size (above 500)

import random

import musicalbeeps as musicalbeeps
from deap import base
from deap import creator
from deap import tools

# ***** USAGE: *****
# It's important to change the octave or type
# flag depending on if the song you are playing
# contains visual octaves and types.
octave_flag = True
type_flag = False


basic_notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # List of all existing notes
basic_octaves = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # List of all existing octaves
basic_note_types = ['#', 'b', 'x']  # List of all existing note types

# Sample Melody #1
find_melody = ['E', 'D', 'C', 'D', 'E', 'E', 'E', 'D', 'D', 'D', 'E', 'G', 'G', 'E', 'D', 'C', 'D', 'E', 'E', 'E', 'D',
               'D', 'D', 'E', 'G', 'G', 'E', 'D', 'C', 'D', 'E', 'E', 'E', 'D', 'D', 'D', 'E', 'G', 'G', 'E', 'D', 'C',
               'D', 'E', 'E', 'E', 'D', 'D', 'D', 'E', 'G', 'G']

# # Happy Birthday x2
# find_melody = ["C4", "C4", "D4", "C4", "F4", "E4", "C4", "C4", "D4", "C4", "G4", "F4", "C4", "C4", "C5", "A4", "F4",
#                 "E4", "D4", "B4", "B4", "A4", "F4", "G4", "F4", "C4", "C4", "D4", "C4", "F4", "E4", "C4", "C4", "D4",
#                 "C4", "G4", "F4", "C4", "C4", "C5", "A4", "F4", "E4", "D4", "B4", "B4", "A4", "F4", "G4", "F4"]

# # Fur Elise Melody
# find_melody = ["E5x", "D5#", "E5x", "D5#", "E5x", "B4x", "D5x", "C5x", "A4x", "E3x", "A3x", "C4x", "E4x", "A4x", "B4x",
#                 "E3x", "G3#", "E4x", "G4#", "B4x", "C5x", "E3x", "A3x", "E4x", "E5x", "D5#", "E5x", "D5#", "E5x", "B4x",
#                 "D5x", "C5x", "A4x", "E3x", "A3x", "C4x", "E4x", "A4x", "B4x", "E3x", "G3#", "D4x", "C5x", "B4x", "A4x",
#                 "E3x", "A3x", "B4x", "C5x", "D5x", "E5x", "G3x", "C4x", "G4x", "F5x", "E5x", "D5x", "G3x", "B3x", "F4x",
#                 "E5x", "D5x", "C5x", "E3x", "A3x", "E4x", "D5x", "C5x", "B4x", "E3x", "E4x", "E4x", "E5x", "E4x", "E5x",
#                 "E5x", "E6x", "D5#", "E5x", "D5#", "E5x", "D5#", "E5x", "D5#", "E5x", "D5#", "E5x", "D5#", "E5x", "B4x",
#                 "D5x", "C5x", "A4x", "E3x", "A3x", "C4x", "E4x", "A4x", "B4x", "E3x", "G3#", "D4x", "C5x", "B4x", "A4x",
#                 "E3x", "A3x", "B4x", "C5x", "D5x", "E5x", "G3x", "C4x", "G4x", "F5x", "E5x", "D5x", "G3x", "B3x", "F4x",
#                 "E5x", "D5x", "C5x", "E3x", "A3x", "E4x", "D5x", "C5x", "B4x", "E3x", "E4x", "E4x", "E5x", "E4x", "E5x",
#                 "E5x", "E6x", "D5#", "E5x", "D5#", "E5x", "D5#", "E5x", "D5#", "E5x", "D5#", "E5x", "D5#", "E5x", "B4x",
#                 "D5x", "C5x", "A4x", "E3x", "A3x", "C4x", "E4x", "A4x", "B4x", "E3x", "G3#", "D4x", "C5x", "B4x", "A4x"]

# # Random Melody
# find_melody = ['E5x', 'A5#', 'B2b', 'C5x', 'C6x', 'D5b', 'G2#']

note_pos_dict = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': []}  # Position dictionary for each note
note_octave_dict = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': []}
note_type_dict = {'#': [], 'b': [], 'x': []}

target_melody_notes = []
target_melody_octaves = []
target_melody_types = []

IND_SIZE = len(find_melody)  # Size of the target melody
note_amount = len(basic_notes)  # Size of the existing notes list
octave_amount = len(basic_octaves)  # Size of the existing octave list
type_amount = len(basic_note_types)     # Size of the existing type list

def fill_target_melody(find_melody):
    for note in find_melody:
        for i in range(len(note)):
            if i == 0:
                target_melody_notes.append(note[i])
            elif i == 1:
                target_melody_octaves.append(note[i])
            else:
                target_melody_types.append(note[i])


fill_target_melody(find_melody)
print(target_melody_notes, target_melody_octaves, target_melody_types)


def note_pos():
    counter_pos = 0
    for i in find_melody:
        match i[0]:
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


def note_octave_pos():
    if octave_flag:
        counter_pos = 0
        for j in find_melody:
            match j[1]:
                case '0':
                    note_octave_dict['0'].append(counter_pos)
                case '1':
                    note_octave_dict['1'].append(counter_pos)
                case '2':
                    note_octave_dict['2'].append(counter_pos)
                case '3':
                    note_octave_dict['3'].append(counter_pos)
                case '4':
                    note_octave_dict['4'].append(counter_pos)
                case '5':
                    note_octave_dict['5'].append(counter_pos)
                case '6':
                    note_octave_dict['6'].append(counter_pos)
                case '7':
                    note_octave_dict['7'].append(counter_pos)
                case '8':
                    note_octave_dict['8'].append(counter_pos)
                case '9':
                    note_octave_dict['9'].append(counter_pos)
            counter_pos += 1

    return note_octave_dict


def note_type_pos():
    if type_flag:
        counter_pos = 0
        for k in find_melody:
            if len(k) > 2:
                match k[2]:
                    case '#':
                        note_type_dict['#'].append(counter_pos)
                    case 'b':
                        note_type_dict['b'].append(counter_pos)
                    case 'x':
                        note_type_dict['x'].append(counter_pos)
            counter_pos += 1

    return note_type_dict


# Filling dictionaries with the correct positions of notes, octaves and types.
note_pos()
note_octave_pos()
note_type_pos()
print(note_pos_dict)
print(note_octave_dict)
print(note_type_dict)


def random_note():
    note = basic_notes[random.randint(0, note_amount - 1)]

    if octave_flag:
        note += basic_octaves[random.randint(0, octave_amount - 1)]
    else:
        note += "x"

    if type_flag:
        # if random.randint(0, 10) < 5:
        #     note += basic_note_types[random.randint(0, type_amount - 1)]
        # else:
        #     note += "x"

        randVal = random.randint(0, 10)
        if randVal < 3:
            note += basic_note_types[0]
        elif randVal < 6:
            note += basic_note_types[1]
        else:
            note += "x"

    else:
        note += "x"

    return note


def find_difference_pos(note, current_note_position):
    existing_notes_list = note_pos_dict.get(note[0])
    if current_note_position in existing_notes_list:
        return 0  # Don't do anything if note exists and its in the correct position
    elif len(existing_notes_list) == 0:
        return IND_SIZE * 6  # Negatively score unused note
    else:
        retValue = existing_notes_list[min(range(len(existing_notes_list)), key=lambda i: abs(
            existing_notes_list[i] - current_note_position))]  # Negatively score existing notes in wrong position
        return retValue


def find_difference_octave(note, current_note_position):
    existing_octave_list = []

    if len(note_octave_dict.values()) != 0:
        if len(note) > 1:
            existing_octave_list = note_octave_dict.get(note[1])
        if current_note_position in existing_octave_list:
            return 0
        elif len(existing_octave_list) == 0:
            return IND_SIZE * 4
        else:
            retValue = existing_octave_list[min(range(len(existing_octave_list)), key=lambda i: abs(
                existing_octave_list[i] - current_note_position))]  # Negatively score existing notes in wrong position
            return retValue
    else:
        return 0


def find_difference_type(note, current_note_position):
    if len(note_type_dict.values()) != 0:
        if len(note) > 2:
            existing_notetype_list = note_type_dict.get(note[2])

            if current_note_position in existing_notetype_list:
                return 0
            elif len(existing_notetype_list) == 0:
                return IND_SIZE * 10
            else:
                retValue = existing_notetype_list[min(range(len(existing_notetype_list)), key=lambda i: abs(
                    existing_notetype_list[i] - current_note_position))]
                # Negatively score existing notes in wrong position
                return abs(current_note_position - retValue)
                # return IND_SIZE * 3
    else:
        return 0


def max_fitness(given_melody):
    fitness_value = 0
    counter_pos = 0

    for note in given_melody:
        fitness_value += (((IND_SIZE - find_difference_pos(note, counter_pos)) / IND_SIZE -
                           abs(ord(find_melody[counter_pos][0]) - ord(note[0]))))
        if octave_flag:
            fitness_value += (((IND_SIZE - find_difference_octave(note, counter_pos)) / IND_SIZE -
                               abs(ord(find_melody[counter_pos][1]) - ord(note[1]))))
        if type_flag:
            fitness_value += (((IND_SIZE - find_difference_type(note, counter_pos)) / IND_SIZE -
                               abs(ord(target_melody_types[counter_pos]) - ord(note[2]))))

        counter_pos += 1

    return fitness_value


def evaluate_melody(individual):
    fitness_value = 0
    counter_pos = 0

    # ((broj_nota - razlika_pozicija)/broj_nota - razlika_ascii) - NOTA, OKTAVA, POVISILICA
    # FITNESS = NOTA + OKTAVA + POVISILICA
    for note in individual:
        fitness_value += (((IND_SIZE - find_difference_pos(note, counter_pos)) / IND_SIZE -
                           abs(ord(target_melody_notes[counter_pos]) - ord(note[0]))))
        if octave_flag:
            fitness_value += (((IND_SIZE - find_difference_octave(note, counter_pos)) / IND_SIZE -
                               abs(ord(target_melody_octaves[counter_pos]) - ord(note[1]))))
        if type_flag:
            fitness_value += (((IND_SIZE - find_difference_type(note, counter_pos)) / IND_SIZE -
                               abs(ord(target_melody_types[counter_pos]) - ord(note[2]))))

        counter_pos += 1
    return fitness_value,


def mut_melody(individual, mutperc):
    tmpList = []
    for i in range(len(individual)):
        tmpList.append(individual[i])
    mut_count = round(len(individual) * mutperc)

    for i in range(mut_count):
        var = random.randint(0, len(tmpList) - 1)
        del tmpList[var]

        # new_note = str(basic_notes[random.randint(0, note_amount - 1)]) +\
        #         str(basic_octaves[random.randint(0, octave_amount - 1)]) + \
        #            str(basic_note_types[random.randint(0, type_amount - 1)])

        new_note = str(basic_notes[random.randint(0, note_amount - 1)])

        if octave_flag:
            new_note += str(basic_octaves[random.randint(0, octave_amount - 1)])
        else:
            new_note += 'x'

        if type_flag:
            new_note += str(basic_note_types[random.randint(0, type_amount - 1)])
        else:
            new_note += 'x'

        tmpList.append(new_note)

    return tmpList,


maxFitness = max_fitness(find_melody)
incorrectFitness = evaluate_melody(find_melody)

print(maxFitness)
print(incorrectFitness)

creator.create("Fitness", base.Fitness, weights=(1,))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("attr_note", random_note)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_note, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate_melody)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mut_melody, mutperc=0.2)
toolbox.register("select", tools.selNSGA2)


def main():
    MU = 250
    CXPB = 0.7
    MUTPB = 0.3

    pop = toolbox.population(n=MU)

    print("MaxFitness Value = " + str(maxFitness))
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
    solution_progress_list = []
    while max(fits) < maxFitness:
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

        if g % 100 == 0:
            solution_progress_list.append(pop[0])
            print(pop[0])
        elif g == 1:
            solution_progress_list.append(pop[0])

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    solution_progress_list.append(best_ind)
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

    player = musicalbeeps.Player(volume=0.1, mute_output=False)

    # To play an A on default octave n°4 for 0.2 seconds
    if octave_flag and type_flag:
        for i in best_ind:
            player.play_note(i)
    elif octave_flag:
        for i in best_ind:
            player.play_note(i[:2])
    else:
        for i in best_ind:
            player.play_note(i[0])


if __name__ == "__main__":
    main()
