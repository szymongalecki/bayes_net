class Node:
    
    # Node is created with name, parents, probabilities and empty children list
    def __init__(self, name, index, parents, probabilities):
        self.name = name
        self.parents = parents
        self.probabilities = probabilities
        self.index = index
        self.children = []

    # add Node's child, this method should be used in the loop, for adding only one child at a time
    def add_child(self, child):
        self.children.append(child)

    # print information about the Node
    def print(self):
        return "Name: {}; Parents: {}, Children: {}, Probabilities: {}".format(self.name, self.parents, self.children, self.probabilities)
    