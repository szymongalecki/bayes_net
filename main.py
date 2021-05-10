#EARIN5 - Szymon Gałecki, Jakub Wojcieszuk

# Be sure to implement logic, which verifies whether the json defines a correct Bayesian network, that means:
# - there are no cycles in the graph, ---------------------------------------------------> NOT DONE
# - all nodes have defined probabilities, -----------------------------------------------> DONE
# - the probability tables are correct (i.e. the appropriate cases sum to 1). -----------> DONE and for the non - binary JSON ---> DONE

# Write a program that is able to perform basic inference in Bayesian networks using the MCMC algorithm with Gibbs sampling. The program should be a console application which:
# - reads a Bayesian network defined in the given JSON file (example provided below),----> DONE
# - is able to print out the nodes forming a Markov blanket for the selected variable.---> DONE
# - accepts evidence – which sets the observed variables of specific nodes, -------------> NOT DONE
# - is able to answer simple queries – i.e. it returns the probability distribution of the selected query variables,-------------------------------------------------------------------------------> NOT DONE
# allows you to set the number of steps performed by MCMC algorithm. --------------------> NOT DONE


# Your task is to implement the inference algorithm yourself, so no machine learning or graph packages are allowed (this also includes PyMC3). However, you can use basic linear algebra and math processing libraries (like numpy).

from bayes_net import BayesNet
# EXAMPLE USAGE: ____________________________________
net = BayesNet()
net.load(filename="alarm.json") 
net.print_nodes()
if net.is_cyclic():
    print('Graph has a cycle')
net.mcmc({"burglary": "T"}, ["John_calls"], 10)
net.markov_blanket("alarm")
# ___________________________________________________
