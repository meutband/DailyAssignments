import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

with open('data/siteA.txt') as f:
    a_data = [int(line.strip()) for line in f]
with open('data/siteB.txt') as f:
    b_data = [int(line.strip()) for line in f]

# Function that fills plot between the lines
def plot_with_fill(x, y, label):
    lines = plt.plot(x, y, label=label, lw=2)
    plt.fill_between(x, 0, y, alpha=0.2, color=lines[0].get_c())

'''
1. Plotting the uniform prior distribution as a beta distribution
'''

x = np.arange(0, 1.01, 0.01)
y = stats.uniform.pdf(x)
plot_with_fill(x, y, 'Uniform Prior')
plt.ylim(0,2)
plt.savefig("imagesAB2/uniform_prior.png")

'''
2. Plotting the uniform prior distribution as a beta distribution (alpha/beta=1)
'''

alpha=1
beta=1
y = stats.beta.pdf(x, alpha, beta)
plot_with_fill(x, y, 'Uniform Prior')
plt.ylim(0,2)
plt.savefig("imagesAB2/uniform_prior2.png")

'''
3. Plotting the posterior distribution for the first 50 for siteA.
(alpha = number of conversions, beta = number of non-conversions)
'''

alpha = a_data[:50].count(1) + 1
beta = a_data[:50].count(0) + 1
y = stats.beta.pdf(x, alpha, beta)
plot_with_fill(x, y, 'Posterior after 50 views')
plt.savefig("imagesAB2/50siteA.png")

'''
4. Plot the prior with the posterior (previous graph) on top of each other
'''

alpha = 1
beta = 1
y = stats.beta.pdf(x, alpha, beta)
plot_with_fill(x, y, 'Uniform Prior')

alpha = a_data[:50].count(1) + 1
beta = a_data[:50].count(0) + 1
y = stats.beta.pdf(x, alpha, beta)
plot_with_fill(x, y, 'Posterior after 50 views')

plt.savefig("imagesAB2/uniform_50siteA.png")

'''
5. Overlay on the same graph the posterior after 0, 50, 100, 200, 400, 800 views.
'''
nums = [0,50,100,200,400,800]

for n in nums:
    alpha = a_data[:n].count(1) + 1
    beta = a_data[:n].count(0) + 1
    y = stats.beta.pdf(x, alpha, beta)
    plot_with_fill(x, y, 'Posterior after {} views'.format(n))

plt.xlim(0,0.4)
plt.legend()
plt.savefig("imagesAB2/all_posteriors.png")

'''
6. Plot siteA and siteB distributions
'''

alphaA = a_data.count(1)
betaA = a_data.count(0)
alphaB = b_data.count(1)
betaB = b_data.count(0)

yA = stats.beta.pdf(x, alphaA, betaA)
yB = stats.beta.pdf(x, alphaB, betaB)

plot_with_fill(x, yA, 'SiteA Data')
plot_with_fill(x, yB, 'SiteB Data')

plt.legend()
plt.xlim(0,0.2)

plt.savefig("imagesAB2/sitesA&B.png")

'''
7. Determine the probability that siteB is beter than siteA. Use beta distributions
using 10000 random points
'''

size = 10000
A = np.random.beta(alphaA, betaB, size)
B = np.random.beta(alphaB, betaB, size)

print '%f%% chance siteB is better than siteA' % (np.sum(B>A)/float(size))
# 0.992600%

'''
8. Determine the 95% equal-tailed interval for site A's beta distribution using
the simulations you just performed.
'''

print (stats.beta.ppf(.025, alphaA, betaA), stats.beta.ppf(.975, alphaA, betaA))
# (0.050079164645113493, 0.084472853496219802)

'''
9. What is the probability that siteB is 2 or more percentage points better than siteA?
'''

print '%f%% chance siteB is better than siteA' % (np.sum(B>A+0.02)/float(size))
# 0.828500%

'''
10. Compare your results to a ttest (frequentist approach)
'''

# H0 = siteB - siteA = 0
# H1 = siteB - siteA = 0.02

t_stat, p_val = stats.ttest_ind(a_data, b_data)
print p_val   # 0.00907734525729

# We can reject the null hypothesis
