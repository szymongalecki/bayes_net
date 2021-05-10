import json
from collections import defaultdict
from node import Node
import random
class BayesNet:

    # create empty dictionary to store Nodes later on
    def __init__(self): 
        self.nodes = {}
        self.graph = defaultdict(list)
        self.V = 0

    # read JSON file and store it in data attribute
    def load(self, filename):
        with open(filename, "r") as read_file:
            self.data = json.load(read_file)

        if self.check_probabilities(): 
            self.create_nodes()
            self.find_children() 
        else: 
            print("FAILED TO CREATE A NETWORK")
    
    # check probability tables for each node
    def check_probabilities(self):
        for n in self.data["nodes"]:
            keys = [k for k in self.data["relations"][n]["probabilities"].keys()]
            #print(keys[0][0])
            
            if keys[0][0] == "T" or keys[0][0] == "F":
                return self.check_binary()
            else:
                return self.check_non_binary()

    # checks non-binary JSON files
    def check_non_binary(self):
        
        # probabilities and parents of the node
        for n in self.data["nodes"]:
            probs = [pr for pr in self.data["relations"][n]["probabilities"].values()]
            parents = [p for p in self.data["relations"][n]["parents"]]

            # probabilities of a node having no parents must sum to 1    
            if len(parents) == 0:
                if sum(probs) != 1:
                    print(f"{n=} probability values {probs=} do not add up to 1")
                    return False
            # non-binary child has parents
            else:
                max_set = 1
                # child probability values must be divisible by the number of parent probability values 
                for p in parents:
                    par_values = [pr for pr in self.data["relations"][p]["probabilities"].values()]
                    if len(probs) % len(par_values) == 0 and len(probs)/len(parents) > max_set:
                        max_set = len(probs)//len(par_values)
                    if len(probs) % len(parents) != 0:
                        print(f"{n=} has {len(probs)=} probability values which is not a multiplicity of {len(par_values)=}")
                        return False

                plist = list(probs)
 
                # print(f"{max_set=}")    
                # print(plist[0:2], plist[2:4], plist[4:6])
                
                plist = [plist[i:i + max_set] for i in range(0, len(plist), max_set)]

                # sublist of n elements where n is greatest child probability values divisor, must sum to 1
                for sublist in plist:
                    if sum(sublist) != 1:
                        print(f"{n=} probability values {sublist=} do not add up to 1")
                        return False

        return True        

    # function to check binary JSON files 
    def check_binary(self):
        for n in self.data["nodes"]:
            probs = [pr for pr in self.data["relations"][n]["probabilities"].values()]
            parents = [p for p in self.data["relations"][n]["parents"]]
            

            # check if number of probability values is correct
            if len(probs) != 2**(len(parents) + 1):
                print(f"{n=} has {len(probs)=} probability values instead of {2**(len(parents) + 1)=}")
                return False
            
            # check if probability values are correct - appropriate cases sum up to 1
            for i in range(0, len(probs), 2):
                if probs[i] + probs[i+1] != 1:
                    print(f"{n=} probability values: {probs[i]=}, {probs[i+1]=}, do not add up to 1")
                    return False
        
        return True
    


    # create Node objects from JSON file and add them to dictionary 
    def create_nodes(self):
        for n in self.data["nodes"]:
            self.nodes[n] = Node(n, self.V, self.data["relations"][n]["parents"], self.data["relations"][n]["probabilities"])
            self.V += 1

    # print every Node object that belongs to the network
    def print_nodes(self):
        for n in self.nodes.keys():
            print(self.nodes[n].print())
        
    # add children lists to the Nodes in the network
    def find_children(self):
        for n in self.data["nodes"]:
            for p in self.data["relations"][n]["parents"]:
                self.nodes[p].add_child(n)
                self.addEdge(self.nodes[p].index, self.nodes[n].index)

    def addEdge(self, u, v):
        self.graph[u].append(v)

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

    def is_cyclic(self):
        visited = [False] * self.V
        rec_stack = [False] * self.V
        for node in range(self.V):
            if visited[node] == False:
                if self.is_cyclic_util(node, visited, rec_stack) == True:
                    return True
        return False
    
    def is_cyclic_util(self, v, visited, rec_stack):
        visited[v] = True
        rec_stack[v] = True

        for neighbour in self.graph[v]:
            if visited[neighbour] == False:
                if self.is_cyclic_util(neighbour, visited, rec_stack) == True:
                    return True
            elif rec_stack[neighbour] == True:
                return True
        
        rec_stack[v] = False
        return False



    def mcmc(self, evidence, query, steps):
        sample_network = {}
        non_evidence_nodes = {}

        #set values of observed variables
        for k, v in evidence.items():
            sample_network[k] = v
        #others drawn randomly
        for key in self.nodes.keys():
            if key in sample_network:
                continue
            keys_list = list(self.nodes[key].probabilities.keys())
            if self.nodes[key].parents:
                counter = 0
                for i in keys_list:
                    j = i.split(',')
                    keys_list[counter] = j[-1]
                    counter+=1
            
            print(keys_list)
            sample_network[key] = random.choice(keys_list)
            non_evidence_nodes[key] = sample_network[key]

        #set counters for query nodes
        counter_dict = defaultdict(list)
        for query_node in query:
            keys_list = list(self.nodes[query_node].probabilities.keys())
            if self.nodes[key].parents:
                counter = 0
                for i in keys_list:
                    j = i.split(',')
                    keys_list[counter] = j[-1]
                    counter+=1
                print(keys_list)
                for i in keys_list:
                    counter_dict[query_node].append((i, 0))
        #random walking
        for i in range(steps):
            #pick random node from non evidence nodes
            node = random.choice(list(non_evidence_nodes))
            non_evidence_nodes[node] = self.sample_markovblanket(node, sample_network) 
            #increase counter 
            #for query_node in query:
                #counter[query_node][query_node.value] += 1.0 / steps



        #return normalized counters to get probability distribution
        



    def sample_markovblanket(self, node, sample_network):
        keys_list = list(self.nodes[node].probabilities.keys())
        print("Node:", node)

        #store in keys_list all possible values for given node
        if self.nodes[node].parents:
            counter = 0
            for i in keys_list:
                j = i.split(',')
                keys_list[counter] = j[-1]
                counter+=1

        probs = defaultdict(list)
        res = 0
        for key in keys_list:
            temp_list = []
            # get parent values for given node and concatenate it with given value for current node
            for parent in self.nodes[node].parents:
                temp_list.append(sample_network[parent])
            temp_list.append(key)
            temp_list = ','.join(temp_list)
            # store probability value in res variable
            res = self.nodes[node].probabilities[temp_list]
            res_child = 1.0
            # iterate over children of given node and mulitply its probabilites by res
            for child in self.nodes[node].children:
                temp_list = []
                for parent in self.nodes[child].parents:
                    if parent == node:
                        temp_list.append(key)
                    else:
                        temp_list.append(sample_network[parent])
                temp_list.append(sample_network[child])
                temp_list = ','.join(temp_list)
                res_child = self.nodes[child].probabilities[temp_list]
                res = res * res_child      
            
            # append calculated probability for picked value
            probs[key].append(res)
        print(probs)
        #normalize probabilites for given node
        #return normalized probabilites
        
        