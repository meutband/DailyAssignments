import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, confusion_matrix, roc_curve
from sklearn.model_selection import train_test_split

data = pd.read_csv("data/churn.csv")

'''
1. Convert the "no", "yes" values to booleans (True/False) as well as any
booleans that are stored as strings.
'''

print data.head(5)

data['Churn?'] = data['Churn?'].map({'True.':True, 'False.':False})
data["Int'l Plan"] = data["Int'l Plan"].map({'yes':True, 'no':False})
data["VMail Plan"] = data["VMail Plan"].map({'yes':True, 'no':False})

print data.head(5)

'''
2. Remove the features which aren't continuous or boolean.
'''

print data.info()

data = data.drop(['State', 'Phone'], axis=1)


'''
3. Make a numpy array called `y` containing the churn values.
'''

y = data.pop('Churn?').values

'''
4. Make a 2 dimensional numpy array containing the feature data
(everything except the labels) called `x`.
'''

x = data.values

'''
5. Split into train and test set.
'''

x_train, x_test, y_train, y_test = train_test_split(x,y)

'''
6. Build a model of your data. Start by using the defaults for all of the parameters.
What is the accuracy score on the test data?
'''

rfc1 = RandomForestClassifier()
rfc1.fit(x_train, y_train)

print rfc1.score(x_test, y_test)
# 0.947242206235

'''
7. Draw a confusion matrix for the results. What is the precision_score and
recall_score?
'''

pred = rfc1.predict(x_test)
print confusion_matrix(y_test, pred)

'''
    TN | FP    710 | 11
    FN | TP     33 | 80
'''

print precision_score(y_test, pred)
# 0.879120879121

print recall_score(y_test, pred)
# 0.70796460177

'''
8. Build the `RandomForestClassifier` again setting the out of bag parameter --
to be `True`. Compare the out of bag score of the training set with the
accuracy on the test set.
'''

rfc2 = RandomForestClassifier(n_estimators=30, oob_score=True)
rfc2.fit(x_train, y_train)

print rfc2.score(x_test, y_test)
# default (10) trees : 0.938848920863  (too few trees error)
# 30 trees : 0.948441247002

print rfc2.oob_score_
# default (10) trees : 0.924369747899  (too few trees error)
# 30 trees : 0.944777911164

'''
9. Get the feature importances. What are the top five features?
'''

importances = np.argsort(rfc1.feature_importances_)
print data.columns[importances[-1:-6:-1]]

# ['Day Mins', 'CustServ Calls', 'Day Charge', 'Eve Mins', 'Int'l Plan']

'''
10. Try modifying the number of trees. The default is 10 trees. Try 5-10 different
values for the number of trees and make a graph of the number of trees versus
the accuracy score. Is there a point where creating more trees doesn't seem to help anymore?
'''


num_trees = range(5,50,5)
accuracies = []

for n in num_trees:
    tot_acc = 0

    #Creates 5 models and calculate the average accuracy of the models for each n
    for i in xrange(5):
        rf = RandomForestClassifier(n_estimators=n)
        rf.fit(x_train, y_train)
        tot_acc += rf.score(x_test, y_test)
    accuracies.append(tot_acc/5)

plt.plot(num_trees, accuracies)
plt.savefig("images/estimators.png")

# Decreases initially after 15 trees

'''
11. Try modifying the max features parameter. Try all the different possible values
and make a graph of the number of features versus the accuracy score.
Is there a point where using additional features doesn't seem to help?
'''

num_features = range(1, len(data.columns) + 1)
accuracies = []
for n in num_features:
    tot_acc = 0

    #Creates 5 models and calculate the average accuracy of the models for each n
    for i in xrange(5):
        rf = RandomForestClassifier(max_features=n)
        rf.fit(x_train, y_train)
        tot_acc += rf.score(x_test, y_test)
    accuracies.append(tot_acc / 5)

plt.plot(num_features, accuracies)
plt.savefig("images/features.png")

# Levels off around 6 features

'''
12. Plot roc curve for the RandomForestClassifier with n_estimators=15,
and max_features=6
'''

rf = RandomForestClassifier(n_estimators=15, max_features=6)
rf.fit(x_train, y_train)
probabilities = rf.predict_proba(x_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_true=y_test, y_score=probabilities)

plt.plot(fpr, tpr)
plt.xlabel("False Positive Rate (1 - Specificity)")
plt.ylabel("True Positive Rate (Sensitivity, Recall)")
plt.title("ROC plot of admissions data")
plt.savefig('images/roc_curve.png')
