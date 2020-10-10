import argparse
import math
import operator
import random
import string

import editdistance
import numpy
from deap import algorithms, base, creator, gp, tools


class InputStringCleanup(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(InputStringCleanup, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, "".join(i for i in values if i in string.ascii_lowercase))


parser = argparse.ArgumentParser(description="Evolve a genetic program to yield the given input.")
parser.add_argument('input_string', type=str, nargs="?", default="amazing",
                    action=InputStringCleanup, help='the input string to evolve')

args = parser.parse_args()


def char_join(left, right):
    return left + right


pset = gp.PrimitiveSet("MAIN", 0)
pset.addPrimitive(char_join, 2)
#pset.addPrimitive(char_rotate, 1)
for i in string.ascii_lowercase:
    pset.addTerminal(i)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalSymbReg(individual):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function
    result = func
    goal = args.input_string
    sqerrors = editdistance.eval(goal, result)**2
    return sqerrors,


toolbox.register("evaluate", evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


def main():
    random.seed(318)

    # The evolution is more likely to fail, the more unique characters there are in the input.
    difficulty = len(set(args.input_string)) / len(string.ascii_lowercase) + 0.1

    N = int(300 * len(args.input_string)**0.5)
    G = int(difficulty * 10 * len(args.input_string)**1.05)
    print(f"Running with population N={N} and generations G={G} "
          f"to evolve the goal: {args.input_string}")

    pop = toolbox.population(n=N)
    hof = tools.HallOfFame(1)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, G, stats=mstats,
                                   halloffame=hof, verbose=True)
    # print log
    print(hof[0])
    print(toolbox.compile(hof[0]))
    print(f"Completed the evolution run with population N={N} and generations G={G}")
    return pop, log, hof


if __name__ == "__main__":
    main()
