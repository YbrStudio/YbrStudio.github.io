import copy

class Node:
    def __init__(self, data: dict):
        self.data = data

    def clone(self) -> 'Node':
        return Node(copy.deepcopy(self.data))
    
node1 = Node({"A": 1})
node2 = node1.clone()
print(node1.data, node2.data)
node2.data["B"] = 2 
print(node1.data, node2.data)