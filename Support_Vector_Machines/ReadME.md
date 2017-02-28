All SVCs were calculated using sklearn.svm.SVC method. Linear, RBF, and Polynomial Kernels were explored with 
varying Hyperparameters, gamma values (for RBF), and varying degrees (for Polynomial). 

Pipeline (sklearn.pipeline.Pipeline) was used for each model as well as Scaling the data using Standard Scaler 
(sklearn.preprocessing.StandardScaler). GridSearchCV (sklearn.model_selection.GridSearchCV) was used to find 
the best parameters/ accuracy during k-fold cross validation.
