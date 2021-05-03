#EARIN5 - Szymon Gałecki, Jakub Wojcieszuk

# Be sure to implement logic, which verifies whether the json defines a correct Bayesian network, that means:
# - there are no cycles in the graph, ---------------------------------------------------> NOT DONE
# - all nodes have defined probabilities, -----------------------------------------------> DONE
# - the probability tables are correct (i.e. the appropriate cases sum to 1). -----------> DONE

# Write a program that is able to perform basic inference in Bayesian networks using the MCMC algorithm with Gibbs sampling. The program should be a console application which:
# - reads a Bayesian network defined in the given JSON file (example provided below),----> DONE
# - is able to print out the nodes forming a Markov blanket for the selected variable.---> DONE
# - accepts evidence – which sets the observed variables of specific nodes, -------------> NOT DONE
# - is able to answer simple queries – i.e. it returns the probability distribution of the selected query variables,-------------------------------------------------------------------------------> NOT DONE
# allows you to set the number of steps performed by MCMC algorithm. --------------------> NOT DONE


# Your task is to implement the inference algorithm yourself, so no machine learning or graph packages are allowed (this also includes PyMC3). However, you can use basic linear algebra and math processing libraries (like numpy).



import json

class BayesNet:

    # create empty dictionary to store Nodes later on
    def __init__(self): 
        self.nodes = {}

    # read JSON file and store it in data attribute
    def load(self, filename):
        with open(filename, "r") as read_file:
            self.data = json.load(read_file)
    
    # check probability tables for each node
    def check_probabilities(self):
        for n in self.data["nodes"]:
            probs = [pr for pr in self.data["relations"][n]["probabilities"].values()]
            parents = [p for p in self.data["relations"][n]["parents"]]

            # check if number of probability values is correct
            if len(probs) != 2**(len(parents) + 1):
                print("Error in {}, probability table has incorrect number of values")
                break
            
            # check if probability values are correct - appropriate cases sum up to 1
            for i in range(0, len(probs), 2):
                if probs[i] + probs[i+1] != 1:
                    print("Error in {}, probabilities: {}, {}, do not add up to 1".format(n, probs[i], probs[i+1]))
                    break

    # create Node objects from JSON file and add them to dictionary 
    def create_nodes(self):
        for n in self.data["nodes"]:
            self.nodes[n] = Node(n, self.data["relations"][n]["parents"], self.data["relations"][n]["probabilities"])
    
    # print every Node object that belongs to the network
    def print_nodes(self):
        for n in self.nodes.keys():
            print(self.nodes[n].print())
        
    # add children lists to the Nodes in the network
    def find_children(self):
        for n in self.data["nodes"]:
            for p in self.data["relations"][n]["parents"]:
                self.nodes[p].add_child(n)
                
    # print markov blanket for specified Node of the network
    def markov_blanket(self, name):
        nd = self.nodes[name]
        mb = []
        mb.append(nd.parents)
        mb.append(nd.children)
        for child in nd.children:
            mb.append(self.nodes[child].parents)
        
        # markov blanket is temporary list used only for printing
        mb = [name for sublist in mb for name in sublist if name != nd.name]
        print(mb)



class Node:
    
    # Node is created with name, parents, probabilities and empty children list
    def __init__(self, name, parents, probabilities):
        self.name = name
        self.parents = parents
        self.probabilities = probabilities
        self.children = []

    # add Node's child, this method should be used in the loop, for adding only one child at a time
    def add_child(self, child):
        self.children.append(child)

    # print information about the Node
    def print(self):
        return "Name: {}; Parents: {}, Children: {}, Probabilities: {}".format(self.name, self.parents, self.children, self.probabilities)
    


# EXAMPLE USAGE: ____________________________________
net = BayesNet()
net.load(filename="alarm.json")
net.check_probabilities()
net.create_nodes()
net.find_children()
net.print_nodes()
net.markov_blanket("alarm")

# ___________________________________________________
