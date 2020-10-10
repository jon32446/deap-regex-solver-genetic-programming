#!/usr/bin/env python3

import argparse
import multiprocessing
import operator
import random
import string

import editdistance
import numpy
import regex
from deap import algorithms, base, creator, gp, tools

# Handle command line arguments
parser = argparse.ArgumentParser(
    description="Evolve a genetic program to match and avoid the given inputs.")
parser.add_argument('N', type=int, nargs="?", default=10000,
                    help='the number of individuals in the population')
parser.add_argument('G', type=int, nargs="?", default=10,
                    help='the number of generations to evolve')
parser.add_argument('--match', type=str, nargs="*", default="amazing",
                    help='the input strings that the regex should match')
parser.add_argument('--avoid', type=str, nargs="*", default="terrible",
                    help='the input strings that the regex should not match')
parser.add_argument('--threads', type=int, nargs="?", default="4",
                    help='the number of threads to use during evolution, set to your number of cores')


args = parser.parse_args()


def join(left, right):
    return left + right


def regex_or(left, right):
    return f"({left})|({right})"


def regex_plus(unary):
    return f"({unary})++"  # possessive to avoid catastrophic backtracking


def regex_star(unary):
    return f"({unary})*+"  # possessive to avoid catastrophic backtracking


def regex_optional(unary):
    return f"({unary})?+"  # possessive to avoid catastrophic backtracking


pset = gp.PrimitiveSet("MAIN", 0)
pset.addPrimitive(join, 2)
pset.addPrimitive(regex_or, 2)
pset.addPrimitive(regex_plus, 1)
pset.addPrimitive(regex_star, 1)
pset.addPrimitive(regex_optional, 1)
for i in string.ascii_lowercase:
    pset.addTerminal(i)

pset.addTerminal(r"\w")
pset.addTerminal(r"\s")
pset.addTerminal(".")  # regex dot

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def get_match(candidate_regex, input_str):
    result = regex.match(candidate_regex, input_str)
    return result[0] if result else ""


def evalSymbReg(individual):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression and the real function
    sqerrors = 0
    for goal in args.match:
        result = get_match(func, goal)
        sqerrors += editdistance.eval(goal, result)**2
    for avoid in args.avoid:
        result = get_match(func, avoid)
        sqerrors += editdistance.eval("", result)**2
    return sqerrors,


toolbox.register("evaluate", evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


def main():
    # Get some multi-threading for performance
    pool = multiprocessing.Pool(args.threads)
    toolbox.register("map", pool.map)

    random.seed(318)

    N = args.N
    G = args.G
    print(f"Running with population N={N} and generations G={G}\n"
          f"to evolve matches for: {args.match}\n"
          f"and avoid these: {args.avoid}\n")

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
    final_regex = toolbox.compile(hof[0])
    print(final_regex)
    pool.close()

    # Print out final summary and the lists in a table
    print(f"Completed the evolution run with population N={N} and generations G={G}")
    padding = max(len(i) for i in args.match) + 4
    fmt = f"{{:>{padding}}}  | {{}}"
    print(fmt.format("match", "avoid"))
    print(fmt.format("-----", "-----"))
    final_regex = f"^({final_regex})$"  # for final evaluation, match all-or-nothing
    for i in range(max(len(args.match), len(args.avoid))):
        m = ""
        if i < len(args.match):
            in_match = args.match[i]
            m = in_match + " " + ("✅" if in_match == get_match(final_regex, in_match) else "❌")
        a = ""
        if i < len(args.avoid):
            in_avoid = args.avoid[i]
            a = in_avoid + " " + ("✅" if "" == get_match(final_regex, in_avoid) else "❌")
        print(fmt.format(m, a))

    return pop, log, hof


if __name__ == "__main__":
    main()
