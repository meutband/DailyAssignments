Hypothesis Testing was done using scipy.stats.ttest_ind function with the equal_var parameter set to False. Images from this 
data are included in the imagesHT folder.

AB Testing was done by calculating the pooled estimate and the standard error of the estimate (of 2 proportions)
and then calculating the zscore and pvalue of using scipy.stats.norm.cdf function.

AB Testing2 was done using a Bayesian Approach by finding posteriors of beta distributions. It then compares to a Frequentist Approach using scipy.stats.ttest_ind. 

Multi Arm Bandit implements 4 main strategies: epsilon-greedy, softmax, ucb1 and bayesian bandits. 2 Classes (Bandits and BanditsStrategy) as well as the stratiegies were given for use.
