import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Determine if the new_landing page can provide a 1% or more lift to sign-up rate.

'''
1. State your null hypothesis and alternative hypothesis? Is your alternative
hypothesis set up for a one-tailed or two-tailed test?
'''

# H0 = new_conversion - old_conversion = 0.001
# H1 = new_conversion - old_conversion > 0.001

# One-Tailed Test since we are primarily intersted in improvement

'''
2. Import the data into a pandas dataframe. Clean the data as appropriate.
'''

df = pd.read_csv("data/experiment.csv")

# print df.info()
# print df.head()
#
# print df['ab'].value_counts()
# print df['landing_page'].value_counts()

# Control group should only get old_page
# Treatment group should only get new_page

# Funcion finds if groups get proper page. Returns 0 if yes, 1 if mismatched
def find_mis(ab, landing):
    if ab == 'treatment' and landing == 'new_page':
        return 0
    elif ab == 'control' and landing == 'old_page':
        return 0
    else:
        return 1

# Apply find_mis function to each row of dataframe
find = lambda row: find_mis(row['ab'], row['landing_page'])

# Make new column in dataframe showcasing mismatched
df['mismatched'] = df.apply(find, axis=1)

# Keep rows that are not mismatched (=0)
df = df[df['mismatched'] == 0]
del df['mismatched']


'''
3. Calculate a p-value for a 1% lift from using the new page compare to the old page.
'''

# Make 2 dataframes, 1 for old and 1 for new
old = df[df['landing_page']=='old_page']
new = df[df['landing_page']=='new_page']

# Get number of pages of old/new (in float values)
num_old = old.shape[0] * 1. # 90815
num_new = new.shape[0] * 1. # 95574

# Get number of converted for old/new
old_convert = old[old['converted'] == 1].shape[0]   # 9049
new_convert = new[new['converted'] == 1].shape[0]   # 9527

# Get proportions of converted for old/new
old_conversion = old_convert / num_old  # 0.0996421296041
new_conversion = new_convert / num_new  # 0.0996819218616


# Calculate zscore for 2 proportions
conversion = (old_conversion * num_old + new_conversion * num_new) / \
             (num_old + num_new)

se = np.sqrt(conversion * (1 - conversion) * (1 / num_old + 1 / num_new))

z_score = (new_conversion - old_conversion - 0.001) / se    # -0.691727618087

# Because we are looking for greater than we need 1 minus
p_val = 1 - scs.norm.cdf(z_score)   # 0.755445800229

print z_score, p_val

# Not statistical significant based on the data.
