import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
import plotly.plotly as py
import plotly.graph_objs as go
from statsmodels.graphics import regressionplots as smg


prestige = sm.datasets.get_rdataset("Duncan", "car", cache=True).data
credit_card = sm.datasets.ccard.load_pandas().data

## Part 1: Linear Regression Diagnostics

'''
1. Explore the dataset with a scatter_matrix and a boxplot. Fit a linear
regression model to each of the datasets. Print and examine the summaries of
the models.
'''

#Scatter Matrix
pd.scatter_matrix(prestige, diagonal='kde')
plt.savefig('images1/prest_matrix.png')
pd.scatter_matrix(credit_card, diagonal='kde')
plt.savefig('images1/credit_matrix.png')

#Boxplot
prestige.boxplot('income')
plt.savefig('images1/prest1_boxplot.png')
prestige.boxplot('income', by = 'type')
plt.savefig('images1/prest2_boxplot.png')

credit_card.boxplot('AGE', by = 'OWNRENT')
plt.savefig('images1/credit1_boxplot.png')
credit_card.boxplot('AVGEXP', by = 'OWNRENT')
plt.savefig('images1/credit2_boxplot.png')
credit_card.boxplot('INCOME', by = 'OWNRENT')
plt.savefig('images1/credit3_boxplot.png')
credit_card.boxplot('INCOMESQ', by = 'OWNRENT')
plt.savefig('images1/credit4_boxplot.png')
credit_card.boxplot('AVGEXP')
plt.savefig('images1/credit5_boxplot.png')


#Models
y1 = prestige['prestige']
x1 = prestige[['income', 'education']].astype(float)
x1 = sm.add_constant(x1)

prest_model = sm.OLS(y1,x1).fit()
summary1 = prest_model.summary()

print summary1

y2 = credit_card['AVGEXP']
x2 = credit_card[['AGE', 'INCOME', 'INCOMESQ', 'OWNRENT']].astype(float)
x2 = sm.add_constant(x2)

credit_model = sm.OLS(y2,x2).fit()
summary2 = credit_model.summary()

print summary2


'''
2. Plot the studentized residuals against the fitted y-values.
'''

res1 = prest_model.outlier_test()['student_resid']
res2 = credit_model.outlier_test()['student_resid']


plt.scatter(prest_model.fittedvalues, res1)
plt.xlabel('studentized residuals')
plt.ylabel('predicted response')
plt.axhline(y=0, c='r', ls='--')
plt.savefig('images1/prest_residuals.png')

plt.scatter(credit_model.fittedvalues, res2)
plt.xlabel('studentized residuals')
plt.ylabel('predicted response')
plt.axhline(y=0, c='r', ls='--')
plt.savefig('images1/credit_residuals.png')



'''
3. Take the log of `AVGEXP` in `credit card` data. Re-fit the model,re-plot the
residuals.
'''

#Prestige Log
y3 = np.log(y1)
prest_model2 = sm.OLS(y3,x1).fit()
res1_log = prest_model2.outlier_test()['student_resid']

plt.scatter(prest_model2.fittedvalues, res1_log)
plt.xlabel('studentized residuals with log response')
plt.ylabel('predicted log response')
plt.axhline(y=0, c='r', ls='--')
plt.savefig('images1/logprest_residuals.png')


#Credit Card Log
y4 = np.log(y2)
credit_model2 = sm.OLS(y4,x2).fit()
res2_log = credit_model2.outlier_test()['student_resid']

plt.scatter(credit_model2.fittedvalues, res2_log)
plt.xlabel('studentized residuals with log response')
plt.ylabel('predicted log response')
plt.axhline(y=0, c='r', ls='--')
plt.savefig('images1/logcredit_residuals.png')


'''
4. Make Q-Q plots for the studentized residuals of the `prestige` and `credit card`.
'''

sm.graphics.qqplot(res1, line='45', fit=True)
plt.savefig('images1/pres1_qqplot.png')
sm.graphics.qqplot(res2, line='45', fit=True)
plt.savefig('images1/credit1_qqplot.png')
sm.graphics.qqplot(res1_log, line='45', fit=True)
plt.savefig('images1/pred2_qqplot.png')
sm.graphics.qqplot(res2_log, line='45', fit=True)
plt.savefig('images1/credit2_qqplot.png')

'''
5. Use the Variance Inflation Factor (VIF) to measure how collinear a
particular feature is with the rest of the features. (VIF > 10)
'''

#Prestige
prest_vif = []
for index in range(x1.shape[1]):
    prest_vif.append(round(variance_inflation_factor(x1.values, index),2))

print prest_vif

#Credit Card
credit_vif = []
for index in range(x2.shape[1]):
    credit_vif.append(round(variance_inflation_factor(x2.values, index),2))

print credit_vif


## Part 2: Outlier Detection

#Use of prestige dataset only the rest of assignment

'''
1. Plot (plotly) your residual plot for the prestige dataset. Identify and note
the points that are more than 2 / -2 studentized residuals.
'''

trace = go.Scatter(
    x = prest_model.fittedvalues,
    y = res1,
    mode = 'markers'
)

data = [trace]

py.image.save_as({'data':data}, 'images1/inc_v_edu_iplot', format='png')

'''
2. Plot (plotly) the x-variables (income and education respectively) against
the studentized residuals. Examine the outliers you have identified in `1`
in the plots and explain why the points are identified as outliers
'''
trace1 = go.Scatter(
    x = x1['income'],
    y = res1,
    mode = 'markers'
)

trace2 = go.Scatter(
    x = x1['education'],
    y = res1,
    mode = 'markers'
)

data = [trace1, trace2]

py.image.save_as({'data':data}, 'images1/prest_iplot', format='png')


'''
3. Make an influence plot and identify the outliers, the influential points,
and the outliers with high influence.
'''

smg.influence_plot(prest_model)
plt.savefig('images1/influence_plot.png')

'''
4. Remove the influential (high leverage) points identified in `3` and re-fit
the model.
'''
prestige = prestige.drop(['conductor', 'RR.engineer', 'minister'])

y = prestige['prestige']
x = prestige[['income', 'education']].astype(float)
x = sm.add_constant(x)

prest_model2 = sm.OLS(y,x).fit()
print prest_model2.summary()
