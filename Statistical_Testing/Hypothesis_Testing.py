import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as scs
from itertools import combinations


'''
We will use hypothesis testing to analyze Click Through Rate (CTR) on the NYT website.
We are going to determine if there is statistically significant difference
between the mean CTR for the following groups:
1. Signed in users vs. Not signed in users
2. Male vs. Female
3. Each of 7 age groups against each other (7 choose 2 = 21 tests)
'''


'''
1. Calculate the adjustment needed to account for multiple testing at the
0.05 significance level.
'''

alpha = 0.05 / 23
# 0.002173913

'''
2. Load data. Make sure the data types are valid and there are no null values.
'''

df = pd.read_csv('data/nyt1.csv')
print df.info()

# We are good, no null values

'''
3. Make new CTR columns. Remove any rows with 0 Impressions
'''

df = df[df.Impressions != 0]
df['CTR'] = df['Clicks'] / df['Impressions'].astype(float)

'''
4. Plot the distribution of each column in the dataframe.
'''

df.hist()
plt.savefig("imagesHT/columns_distributions.png")

'''
5. Make 2 dataframes - one a dataframe of 'users who are signed in' and a
second of 'users who are not signed in'. Plot the distributions of the
columns in each of the dataframes.
'''

dfsign_in = df[df.Signed_In == 1]
dfsign_out = df[df.Signed_In == 0]

dfsign_in.hist()
plt.savefig("imagesHT/signedin_distributions.png")
dfsign_out.hist()
plt.savefig("imagesHT/signedout_distributions.png")

# All people who are signed out are female with age 0. This could suggest that
# the gender and age are not registered unless the user is signed in.

'''
6. Use a Welch's t-test to determine if the mean CTR between the signed-in users
and the non-signed-in users is statistically different.

Welch t-test assumes the two populations have different variances.
'''

print "signed in CTR mean: ", np.mean(dfsign_in['CTR']) # 0.0142536352321
print "signed out CTR mean: ", np.mean(dfsign_out['CTR']) # 0.0283549070617

t_stat, p_val = scs.ttest_ind(dfsign_in['CTR'], dfsign_out['CTR'], equal_var=False)
print p_val # 0.0

# Yes, significant

'''
7. Determine if the mean CTR between male users and female users is
statistically different.
'''

dfmale = dfsign_in[dfsign_in.Gender == 1]
dffemale = dfsign_in[dfsign_in.Gender == 0]

print "male CTR mean: ", np.mean(dfmale['CTR']) # 0.0139185242976
print "female CTR mean: ", np.mean(dffemale['CTR']) # 0.0146220121839

t_stat, p_val = scs.ttest_ind(dfmale['CTR'], dffemale['CTR'], equal_var=False)
print p_val # 0.00100285273131

# Yes significant, but not as significant than signin/signout

'''
8. Calculate a new column called AgeGroup, which bins Age into the following buckets
   (7, 18], (18, 24], (24, 34], (34, 44], (44, 54], (54, 64], (64, 1000]
'''

dfsign_in['Age_Group'] = pd.cut(dfsign_in['Age'], [7, 18, 24, 34, 44, 54, 64, 1000])

dfsign_in['Age_Group'].value_counts().sort_index().plot(kind='bar', grid=False)
plt.xlabel('Age Group')
plt.ylabel('Number of users')
plt.savefig("imagesHT/age_groups.png")


'''
9. Determine the pairs of age groups where the difference in mean CTR is
statistically significant.
'''

dffinal = pd.DataFrame()
combos = combinations(pd.unique(dfsign_in['Age_Group']), 2)

for g1, g2 in combos:

    ctr1 = dfsign_in[dfsign_in['Age_Group'] == g1]['CTR']
    ctr2 = dfsign_in[dfsign_in['Age_Group'] == g2]['CTR']

    t_stat, p_val = scs.ttest_ind(ctr1, ctr2, equal_var=False)
    mean1 = np.mean(ctr1)
    mean2 = np.mean(ctr2)
    diff = np.abs(mean1-mean2)

    dffinal = dffinal.append(dict(Group1=g1, Group2=g2, Mean1=mean1,
                                    Mean2=mean2, Diff=diff, Pval=p_val), ignore_index=True)

dffinal = dffinal[['Group1', 'Group2', 'Mean1', 'Mean2', 'Diff', 'Pval']]

# Rank in descending order of difference in means where statistically significant
print dffinal[dffinal['Pval'] < alpha].sort('Diff', ascending=False)

# Rank in ascending order of difference in means where statistically insignificant
print dffinal[dffinal['Pval'] > alpha].sort('Diff', ascending=True)
