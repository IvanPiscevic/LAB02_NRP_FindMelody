import random

from deap import base
from deap import creator
from deap import tools

import os
print("PYTHONPATH:", os.environ.get('PYTHONPATH'))
print("PATH:", os.environ.get('PATH'))

basic_notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # List of all existing notes
find_melody = ['E', 'D', 'C', 'D', 'E', 'E', 'E', 'D', 'D', 'D', 'E', 'G', 'G']  # Melody that is trying to be found
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
    fitness_value = 0.0
    counter_pos = 0

    # | (broj_nota - razlika_pozicija)/broj_nota - razlika_ascii | = 169
    for note in individual:
        fitness_value += (IND_SIZE - find_difference_pos(note, counter_pos) / IND_SIZE -
                             abs(ord(find_melody[counter_pos]) - ord(note)))
        counter_pos += 1
    return fitness_value


creator.create("Fitness", base.Fitness, weights=1.0)
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("attr_note", random_note)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_note, n=IND_SIZE)

print(evaluate_melody(test_melody))

#
#
# player = musicalbeeps.Player(volume=0.1, mute_output=False)
#
# # To play an A on default octave n°4 for 0.2 seconds
# for i in find_melody:
#     player.play_note(i)
