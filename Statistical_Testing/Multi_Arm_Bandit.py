import numpy as np
import matplotlib.pyplot as plt

from bandits import Bandits
from banditstrategy import BanditStrategy, max_mean, random_choice, \
                           epsilon_greedy, softmax, ucb1, \
                           bayesian_bandit

'''
1. See how many wins you have of the 1000 trials using each of the six strategies
Use arrays [0.1, 0.1, 0.1, 0.1, 0.9], [0.1, 0.1, 0.1, 0.1, 0.12],
[0.1, 0.2, 0.3, 0.4, 0.5]
'''

p_arrays = [[0.1, 0.1, 0.1, 0.1, 0.9], [0.1, 0.1, 0.1, 0.1, 0.12],
            [0.1, 0.2, 0.3, 0.4, 0.5]]

functions = max_mean, random_choice, epsilon_greedy, softmax, ucb1, bayesian_bandit

# loops over arrays
for i, array in enumerate(p_arrays):
    print "%d: %r" % (i, array)

    # applies each array to each of the Bandits functions and calculates wins
    for func in functions:
        bandits = Bandits(array)
        strat = BanditStrategy(bandits, func)
        strat.sample_bandits(1000)
        print "    %d wins with %s" % (strat.wins.sum(), func.__name__)
    print

'''
2. Use matplotlib to plot the total regret (for given function) over time of
each algorithm.
'''

def regret(probabilities, choices):
    p_opt = np.max(probabilities)
    return np.cumsum(p_opt - probabilities[choices])



p_array = np.array([0.05, 0.03, 0.06])

# applies the array to each of the Bandits functions and calculate the regret
for func in functions:
    bandits = Bandits(p_array)
    strat = BanditStrategy(bandits, func)
    strat.sample_bandits(1000)
    theregret = regret(p_array, strat.choices.astype(int))
    plt.plot(theregret, label=func.__name__)

plt.legend(loc=2)
plt.xlabel('number of trials')
plt.ylabel('regret')
plt.savefig("imagesMAB/total_regret.png")


'''
3. Now plot the percentage of time the optimal bandit was chosen over time
'''

def optimal_percent(probabilities, choices):
    p_opt = np.max(probabilities)
    count_correct = np.cumsum(probabilities[choices] == p_opt)
    # divide by the array [1, 2, ...] to get the average from the totals
    return count_correct / np.arange(1, len(choices) + 1).astype(float)


p_array = np.array([0.05, 0.03, 0.06])

# applies the array to each of the Bandits functions and calculates the percent
# correct over time
for func in functions:
    bandits = Bandits(p_array)
    strat = BanditStrategy(bandits, func)
    strat.sample_bandits(1000)
    percents = optimal_percent(p_array, strat.choices.astype(int))
    plt.plot(percents, label=func.__name__)

plt.legend(loc=2)
plt.xlabel('number of trials')
plt.ylabel('percent correct')
plt.savefig("imagesMAB/percent_bandit.png")
