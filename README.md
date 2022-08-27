# Bayes Net for EARIN Course

Write a program that is able to perform basic inference in Bayesian networks using the MCMC algorithm with Gibbs sampling. The program should be a console application which:
• reads a Bayesian network defined in the given JSON file (example provided below),
• is able to print out the nodes forming a Markov blanket for the selected variable.
• accepts evidence – which sets the observed variables of specific nodes,
• is able to answer simple queries – i.e. it returns the probability distribution of the
selected query variables,
• allows you to set the number of steps performed by MCMC algorithm.
