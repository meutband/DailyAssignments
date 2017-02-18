from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_curve
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold
import pandas as pd
import numpy as np
from statsmodels.discrete.discrete_model import Logit
from statsmodels.tools import add_constant
from itertools import izip

grad = pd.read_csv('data/grad.csv')

'''

1. Get some preliminary summary statistics on the data. In particular look at
the mean values of the features.

'''

print grad.describe()


'''

2. See how many applicants from each rank of school were accepted. (Use crosstab).
Make a bar plot of the percent of applicants from each rank who were accepted.

'''

cross = pd.crosstab(grad['admit'], grad['rank'])
print cross

(cross / cross.apply(sum)).plot(kind="bar")
plt.savefig('images/avg_accepted_rank.png')


'''

3. Run a logistic regression model, and look at the results. (With statsmodels)

'''

x = grad[['gre', 'gpa', 'rank']].values
x = add_constant(x, prepend=True)
y = grad['admit'].values

# Calling .values converts dataframe into numpy array

logit_model = Logit(y, x).fit()
print logit_model.summary()


'''

4. Use KFolds cross validation to get the average accuracies, precisions, and
recalls of a LogisticRegression model.

'''

kfold = KFold(n_splits=3)
model = LogisticRegression()

accuracies = []
precisions = []
recalls = []

for train_index, test_index in kfold.split(x):
    model.fit(x[train_index], y[train_index])
    y_predict = model.predict(x[test_index])
    y_true = y[test_index]
    accuracies.append(accuracy_score(y_true, y_predict))
    precisions.append(precision_score(y_true, y_predict))
    recalls.append(recall_score(y_true, y_predict))


print 'Average Accuracy: ', np.mean(accuracies)
print 'Average Precision: ', np.mean(precisions)
print 'Average Recall: ', np.mean(recalls)

'''

5. Create binary indicator varaibles for 'rank'. Redo accuracy, recal, and
precision scores to compare (to part 4).

'''

rank = pd.get_dummies(grad['rank'], prefix='rank')

x2 = grad[['gre','gpa']].join(rank.ix[:,'rank_2':]).values
x2 = add_constant(x2, prepend=True)

accuracies = []
precisions = []
recalls = []

# Same kfold from above
for train_index, test_index in kfold.split(x):
    model.fit(x2[train_index], y[train_index])
    y_predict = model.predict(x2[test_index])
    y_true = y[test_index]
    accuracies.append(accuracy_score(y_true, y_predict))
    precisions.append(precision_score(y_true, y_predict))
    recalls.append(recall_score(y_true, y_predict))

print 'Average Accuracy: ', np.mean(accuracies)
print 'Average Precision: ', np.mean(precisions)
print 'Average Recall: ', np.mean(recalls)

# Worse than before

'''

6. Make a plot of the ROC curve (using your function defined in part 4)

'''

X_train, X_test, y_train, y_test = train_test_split(x, y)

model = LogisticRegression()
model.fit(X_train, y_train)

probabilities = model.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_true=y_test, y_score=probabilities)


plt.plot(fpr, tpr)
plt.xlabel("False Positive Rate (1 - Specificity)")
plt.ylabel("True Positive Rate (Sensitivity, Recall)")
plt.title("ROC plot of admissions data")
plt.savefig('images/roc_curve.png')


'''

7. Fit a Logistic model on the data. What are the beta coefficients?

'''

x = grad[['gre', 'gpa', 'rank']]
y = grad['admit']

model = LogisticRegression()
model.fit(x,y)

for name, coef in izip(x.columns, model.coef_[0]):
    print '%s: %f' % (name, coef)


'''

8. Compute the change in odds ration from one unit change in each feature

'''


for name, coef in izip(x.columns, model.coef_[0]):
    print '%s: %f' % (name, np.exp(coef))

# Increasing the GRE score by 1 point increases the chance of getting in by a factor of 1.00189.
# Increasing the GPA score by 1 point increases the chance of getting in by a factor of 1.37614.
# Improving the school's rank by 1 point (means decreasing the number) increases the chance of getting in by a factor of 1/0.54587=1.8319.


'''

9. What change is required to double my chances of admission?

'''

for name, coef in izip(x.columns, model.coef_[0]):
    print '%s: %f' % (name, np.log(2)/coef)
