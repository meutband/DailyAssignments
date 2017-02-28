import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

data = pd.read_csv('data/non_sep.csv', index_col=0, header=None)

# Index is the 0th columns
x = data[[1,2]].values
y = data[3].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=300)

'''     Part 1                          '''
'''     Preprocessing data for SVM      '''

'''
1. Scale x1 and x2 using StandardScaler. Use Pipeline to specify the step
following the StandardScaler, which would be fitting the scaled feature to a
linear kernel SVC to predict y.
'''

scaled = SVC(kernel='linear')
p_scaled = Pipeline([('scaler', StandardScaler()), ('svc', scaled)])
p_scaled.fit(x_train, y_train)
print p_scaled.score(x_test, y_test)    # 0.967741935484
print scaled.coef_  # [[ 1.70675832  0.39972152]]

'''
2. Plot the decision boundary along with the data points.
'''

coefs = scaled.coef_.squeeze()
dist = abs(scaled.intercept_ + np.dot(x_train, coefs)) / np.linalg.norm(coefs)
label_sizes = dist.ravel()

# get the separating hyperplane
w = scaled.coef_[0]
a = -w[0] / w[1]
xx = np.linspace(min(x_train[:,0]), max(x_train[:,0]))
yy = a * xx - (scaled.intercept_[0]) / w[1]

# plot the parallels to the separating hyperplane that pass through the
# support vectors
margin = 1 / np.sqrt(np.sum(scaled.coef_ ** 2))
yy_down = yy + a * margin
yy_up = yy - a * margin

# plot the line, the points, and the nearest vectors to the plane
colors = ['red' if i else 'blue' for i in y_train]
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)

ax.scatter(x_train[:,0], x_train[:,1], color=colors, s=label_sizes*40, alpha=0.5)
ax.plot(xx, yy, 'k-')
ax.plot(xx, yy_down, 'k--')
ax.plot(xx, yy_up, 'k--')
plt.ylim(-10,10)
plt.title('SVM Decision Boundary - Scaled')
plt.xlabel('X1')
plt.ylabel('X2')
plt.savefig('images/decision_scaled.png')

'''
3. Use Pipeline which would be fitting the scaled feature to a linear kernel SVC
to predict y (unscaled).
'''

unscaled = SVC(kernel='linear')
p_unscaled = Pipeline([('svc', unscaled)])
p_unscaled.fit(x_train, y_train)
print p_unscaled.score(x_test, y_test)    # 0.967741935484
print unscaled.coef_  # [[ 1.51246697  0.46149849]]

'''
4. Plot the decision boundary along with the data points.
'''

coefs = unscaled.coef_.squeeze()
dist = abs(unscaled.intercept_ + np.dot(x_train, coefs)) / np.linalg.norm(coefs)
label_sizes = dist.ravel()

# get the separating hyperplane
w = unscaled.coef_[0]
a = -w[0] / w[1]
xx = np.linspace(min(x_train[:,0]), max(x_train[:,0]))
yy = a * xx - (unscaled.intercept_[0]) / w[1]

# plot the parallels to the separating hyperplane that pass through the
# support vectors
margin = 1 / np.sqrt(np.sum(unscaled.coef_ ** 2))
yy_down = yy + a * margin
yy_up = yy - a * margin

# plot the line, the points, and the nearest vectors to the plane
colors = ['red' if i else 'blue' for i in y_train]
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)

ax.scatter(x_train[:,0], x_train[:,1], color=colors, s=label_sizes*40, alpha=0.5)
ax.plot(xx, yy, 'k-')
ax.plot(xx, yy_down, 'k--')
ax.plot(xx, yy_up, 'k--')
plt.ylim(-10,10)
plt.title('SVM Decision Boundary - Unscaled')
plt.xlabel('X1')
plt.ylabel('X2')
plt.savefig('images/decision_unscaled.png')

'''
5. Use cross_val_score to compute the average `accuracy` of a 5-fold
cross validation of the scaled model.
'''

print np.mean(cross_val_score(scaled, x_train, y_train, scoring='accuracy', cv=5))
# 0.9


'''     Part 2              '''
'''     Hyperparameter C    '''

'''
1. Find the `C` with the highest cross-validated accuracy.
`C` should be in the range of `.001` and `.01`
'''

C = np.linspace(0.001,0.01,10)
accuracy = []
for i in C:
    model = SVC(kernel='linear', C=i)
    score = np.mean(cross_val_score(model, x_train, y_train, scoring='accuracy', cv=10))
    accuracy.append(score)
print C, accuracy
# [ 0.001  0.002  0.003  0.004  0.005  0.006  0.007  0.008  0.009  0.01 ]
# [0.51428571428571423, 0.51428571428571423, 0.51428571428571423, 0.52678571428571419,
# 0.6339285714285714, 0.78571428571428581, 0.856547619047619, 0.86904761904761896,
# 0.84404761904761894, 0.86071428571428577]

'''
2. Plot the values of `C` against the respective model scores.
'''

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)
ax.plot(C, accuracy)
plt.title('Accuracy vs C Values')
plt.xlabel('C Values')
plt.ylabel('Accuracy')
plt.savefig('images/hyperparameters.png')


'''     Part 3          '''
'''     Kernel Tricks   '''

# Function that wil plot the decision boundaries for each of the Kernels.

def decision_boundary(clf, X, Y, name, h=.02):

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1, figsize=(10, 7))
    plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=Y, edgecolors='k', cmap=plt.cm.Paired)

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title('SVM Decision Boundary - {}'.format(name))
    plt.xticks(())
    plt.yticks(())
    plt.savefig('images/{}.png'.format(name))

'''
1. Retrain your model using the RBF kernel. Plot the decision boundary
'''

rbf = SVC(kernel='rbf')
p_rbf = Pipeline([('svc', rbf)])
p_rbf.fit(x_train, y_train)
score = np.mean(cross_val_score(rbf, x_train, y_train, scoring='accuracy', cv=10))
print score # 0.889880952381
decision_boundary(rbf, x_train, y_train, 'RBF')

'''
2. Retrain your model using the polynomial kernel. Plot the decision boundary
'''

poly = SVC(kernel='poly')
p_poly = Pipeline([('svc', poly)])
p_poly.fit(x_train, y_train)
score = np.mean(cross_val_score(poly, x_train, y_train, scoring='accuracy', cv=10))
print score # 0.898214285714
decision_boundary(poly, x_train, y_train, 'Polynomial')


'''     Part 4          '''
'''     GridSearchCV    '''

'''
1. Perform GridSearchCV for an Polynomial Kernel with varying hyperparameters and
degrees. Find the best parameters. Plot the decision boundary
'''

s = SVC(kernel='poly')
g = GridSearchCV(s, {'C':np.linspace(.001, 3, 20), 'degree':[1,2,3,4]}, cv=10).fit(x_train,y_train)
print g.best_params_ # {'C': 0.31668421052631579, 'degree': 1}
print g.score(x_test, y_test) # 0.935483870968
decision_boundary(g.best_estimator_, x_train, y_train, 'Best_Poly')

'''
2. Perform GridSearchCV for an RBF Kernel with varying hyperparameters and
gamma. Find the best parameters. Plot the decision boundary
'''

s = SVC(kernel='rbf')
g = GridSearchCV(s, {'C':np.linspace(.001, 3, 20), 'gamma':np.linspace(0,5,20)}, cv=10).fit(x_train,y_train)
print g.best_params_ # {'C': 0.1588421052631579, 'gamma': 0.26315789473684209}
print g.score(x_test, y_test) # 0.967741935484
decision_boundary(g.best_estimator_, x_train, y_train, 'Best_RBF')
