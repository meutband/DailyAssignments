from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score, recall_score
from keras.utils import np_utils
import pandas as pd
import tensorflow
from tensorflow.python.ops import control_flow_ops
tensorflow.python.control_flow_ops = control_flow_ops


#Import data
df = pd.read_csv('data/churn.csv')

'''

1. Clean the data. Split X,y and split training and test set using train_test_split

'''

df.replace({'False.': 0, 'True.': 1, 'yes': 1, 'no': 0}, inplace=True)

#Drop the columns we wont use
df.drop(['Phone', 'Area Code', 'State'], axis = 1, inplace=True)

y = df['Churn?']
X = df.drop('Churn?', axis = 1)

#Normalize X
X = (X - X.mean(axis = 0)) / X.std(axis = 0, ddof = 1)

y = np_utils.to_categorical(y, 2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.30)


'''

2. Set up a function run_model() that takes in the training and test sets,
as well as default values of probability threshold of .20, 1 layer, 64 nodes,
and .50 dropouts. Return training and test precision and recal scores.

'''

def run_model(X_train, X_test, y_train, y_test, prob_threshold = 20, layers = 1, nodes = 64, dropout = 50):

    # Fit a sequential model with some given number of nodes.
    model = Sequential()

    # Fit the first hidden layer manually, becuase we have to fit it
    # with the x-shape by the node_count.
    model.add(Dense(nodes, init='uniform', input_dim=X_test.shape[1]))
    model.add(Activation('tanh'))
    model.add(Dropout(dropout / 100.0))

    # We can fit any additional layers like this, provided they
    # have the same node_count (except the last one).
    for layer in range(layers):
	    model.add(Dense(nodes, init='uniform'))
	    model.add(Activation('tanh'))
	    model.add(Dropout(dropout / 100.0))

    model.add(Dense(2, init='uniform'))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='mse', optimizer=sgd)

    model.fit(X_train.values, y_train, nb_epoch = 20, batch_size = 16, verbose = 0)

    # Get the training and test predictions from our model fit.
    train_predictions  = model.predict_proba(X_train.values)
    test_predictions = model.predict_proba(X_test.values)

    # Set these to either 0 or 1 based off the probability threshold we
    # passed in (divide by 100 becuase we passed in intergers).
    train_preds = (train_predictions[:, 1]) >= prob_threshold / 100.0
    test_preds = (test_predictions[:, 1]) >= prob_threshold / 100.0

    # Calculate the precision and recall. Only output until
    precision_score_train = precision_score(y_train[:, 1], train_preds)
    precision_score_test = precision_score(y_test[:, 1], test_preds)

    recall_score_train = recall_score(y_train[:, 1], train_preds)
    recall_score_test = recall_score(y_test[:, 1], test_preds)

    return precision_score_train, precision_score_test, recall_score_train, recall_score_test


'''

3. Run the model for the default parameters.

'''

p_train, p_test, r_train, r_test = run_model(X_train, X_test, y_train, y_test)

print "\nDefault Values"
print "Train Precision: \t", p_train
print "Test Precision: \t", p_test
print "Train Recall: \t", r_train
print "Train Recall: \t", r_test


'''

4. Run the model for probability thresholds between 10 to 60 by 5s.

'''

for prob in range(10,60,5):
    p_train, p_test, r_train, r_test = run_model(X_train, X_test, y_train, y_test, prob_threshold=prob)
    print "\nProbability thresholds: ", prob
    print "Train Precision: \t", p_train
    print "Test Precision: \t", p_test
    print "Train Recall: \t", r_train
    print "Train Recall: \t", r_test



'''

5. Run the model for 0,1,or 2 hidden layers.

'''

for layer in range(3):
    p_train, p_test, r_train, r_test = run_model(X_train, X_test, y_train, y_test, layers=layer)
    print "\nHidden Layers: \t ", layer
    print "Train Precision: \t", p_train
    print "Test Precision: \t", p_test
    print "Train Recall: \t", r_train
    print "Train Recall: \t", r_test


'''

6. Run the model for 2 to the power of (1 to 10) number of nodes.

'''

for num_nodes in range(1,10):
    p_train, p_test, r_train, r_test = run_model(X_train, X_test, y_train, y_test, nodes=(2**num_nodes))
    print "\nNumber of Nodes: \t ", num_nodes
    print "Train Precision: \t", p_train
    print "Test Precision: \t", p_test
    print "Train Recall: \t", r_train
    print "Train Recall: \t", r_test


'''

7. Run the model for different dropout rates, to 100 by 5.

'''

for drop in range(5,100,5):
    p_train, p_test, r_train, r_test = run_model(X_train, X_test, y_train, y_test, dropout=drop)
    print "\nDropout Rate: \t ", drop / 100.0
    print "Train Precision: \t", p_train
    print "Test Precision: \t", p_test
    print "Train Recall: \t", r_train
    print "Train Recall: \t", r_test
