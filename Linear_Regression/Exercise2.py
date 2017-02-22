import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt

## Linear Regression Problem

'''
1. Load the data into a dataframe from `data/balance.csv`.
Make a scatter matrix of the variables.
'''

data = pd.read_csv('data/balance.csv', index_col=0)

pd.scatter_matrix(data)
plt.savefig('images2/balance_matrix.png')



# The dataset contains no null values
print data.isnull().sum()

# The dataset contains 3 categorical columns (Gender, Student, Married, Ethnicity)
# Ethinicity is the only column that contains more than 2 values.
print data.info()
print data['Gender'].unique()
print data['Student'].unique()
print data['Married'].unique()
print data['Ethnicity'].unique()

'''
2. Convert Gender, Student and Married to 1/0. Create dummy variables for the
Ethnicity column (pd.get_dummies()). After you create the model, drop the
African American dummy variable.
'''

data['Gender'] = data['Gender'].map({' Male':1, 'Female':0})
data['Married'] = data['Married'].map({'Yes':1, 'No':0})
data['Student'] = data['Student'].map({'Yes':1, 'No':0})

data = pd.get_dummies(data)
del data['Ethnicity_African American']

print data.info()

'''
3. Using all the feature variables, fit a linear regression model to predict
`Balance`. Make a residual plot by plotting the fitted y values against the
studentized residuals.
'''

x = data.copy()
y = x.pop('Balance')

all_model = sm.OLS(y,x).fit()
print all_model.summary()

resids = all_model.outlier_test()['student_resid']
y_pred = all_model.predict(x)

plt.scatter(y_pred, resids, label='Residual Plot')
plt.savefig('images2/all_model_residuals.png')

'''
4. Try a few other models by excluding some features from the full model.
Does the residual plot change?
'''

# Function that will fit and plot the model for any given x/y
def plot_model(x, y, label):
    model = sm.OLS(y,x).fit()
    resids = model.outlier_test()['student_resid']
    y_preds = model.predict(x)

    plt.scatter(y_preds, resids, label=label)
    plt.legend()
    plt.show()

# Loop through columns and remove each column and call plot function for each
# removal.
all_columns = x.columns
for col_name in all_columns:
    all_columns_copy = list(all_columns)
    all_columns_copy.remove(col_name)
    plot_model(x[all_columns_copy], y, 'Removed - ' + str(col_name))

# Removing Income or Student had the most change in residuals

# Looking at the Balance data, there are many values that are 0.
y.hist(bins=100)
plt.show()

'''
5. Re-plot the univariate scatter plot on a bigger figure size. Look for
variable(s) that can differentiate most zero balance observation from non-zero
balance observations.
'''

# Plots each column to find threshold limits to limit $0 for Balancec
for col in all_columns:
    data.plot(kind='scatter', y='Balance', x=col, edgecolor='none', figsize=(12, 5))
    plt.xlabel(col)
    plt.ylabel('Balance')
    plt.show()

# Limit > 2500, Rating > 200


'''
6. Remove the data points below the decided threshold of your chosen variable
and examine the number of zero observations that remain. Now re-fit the same
model and examine the residuals.
'''

cond1 = data['Limit'] >= 2500
new_data = data[cond1]
cond2 = new_data['Rating'] > 200
new_data = new_data[cond2]

print new_data.info()


x2 = new_data.copy()
y2 = x2.pop('Balance')

new_model = sm.OLS(y2,x2).fit()
print new_model.summary()

resids2 = new_model.outlier_test()['student_resid']
y_pred2 = new_model.predict(x2)

plt.scatter(y_pred2, resids2, label='Residual Plot')
plt.savefig('images2/new_model_residuals.png')


## Extra Credit

'''
1. Fit a linear model to predict `Balance` using `Income` as a predictor.
'''

y = new_data['Balance']
x = new_data['Income']

income_model = sm.OLS(y,x).fit()
print income_model.summary()


'''
2. Fit a second model using `Income` and `Student` as predictors.
'''

x = new_data[['Income', 'Student']]

inc_stu_model = sm.OLS(y,x).fit()
print inc_stu_model.summary()


'''
3. Finally fit a model using `Income`, `Student`, and `Income`*`Student`
to account for a possible interaction
'''

new_data['Income*Student'] = new_data['Income'] * new_data['Student']
x = new_data[['Income', 'Student', 'Income*Student']]

inc_stu_model = sm.OLS(y,x).fit()
print inc_stu_model.summary()

'''
4. Make a single plot with two regression lines, one for Student and one for non-Students.
'''

students = new_data['Student'] == 1
nonstudents = new_data['Student'] == 0

students_df = new_data.loc[students, ['Income', 'Balance']]
nonstudents_df = new_data.loc[nonstudents, ['Income', 'Balance']]

stu_x = students_df['Income']
stu_y = students_df['Balance']

nstu_x = nonstudents_df['Income']
nstu_y = nonstudents_df['Balance']

students_model = sm.OLS(stu_y,stu_x).fit()
stu_pred = students_model.predict(stu_x)
nonstudents_model = sm.OLS(nstu_y,nstu_x).fit()
nstu_pred = nonstudents_model.predict(nstu_x)

print students_model.summary()
print nonstudents_model.summary()

plt.scatter(stu_x, stu_y, color='r')
plt.plot(stu_x, stu_pred, color='r')

plt.scatter(nstu_x, nstu_y, color='b')
plt.plot(nstu_x, nstu_pred, color='b')

plt.xlabel('Income')
plt.ylabel('Balance')
plt.savefig('images2/student_v_nonstudent.png')
