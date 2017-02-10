





class Node(object):
	def __init__(self, inbound_nodes = []):

		#Nodes coming in to this node i.e. nodes from which this node recives value 
		self.inbound_nodes = inbound_nodes 

		# Nodes going out of this node, i.e. nodes to which this node passes value
		self.outbound_nodes = []

		for n in self.inbound_nodes:
			n.outbound_nodes.append(self)

		#The calulate output value 
		self.value = None


	def forward(self):
		#Implements forward propogation  
		#Compute the value based on the inbound nodes and store in the value variable

		raise NotImplemented



class Input(Node):
	def __init__(self):
		# An input node has no inbound nodes, 
		# so no need to pass anything to the instatiator
		Node.__init__(self)


	def forward(self, value=None):
		# Overwrite the value if something is passed in 
		if value is not None:
			self.value = value



class Add(Node):
	def __init__(self,*input):

		Node.__init__(self,[x,y])

		#Note: 

	def forward(self):
		self.value = self.inbound_nodes[0].value + self.inbound_nodes[1].value



class Linear(Node):
	def __init__(self, inputs, weights,bias):
		Node.__init__(self,[inputs, weights,bias])

	def forward(self):
		inputs = self.inbound_nodes[0].value 
		weights =self.inbound_nodes[1].value 
		bias = self.inbound_nodes[2].value 
		self.value = bias.value
		for x,w in zip(inputs,weights):
			self.value += x*w 





def topological_sort(feed_dict):
    """
    Sort generic nodes in topological order using Kahn's Algorithm.

    `feed_dict`: A dictionary where the key is a `Input` node and the value is the respective value feed to that node.

    Returns a list of sorted nodes.
    """

    input_nodes = [n for n in feed_dict.keys()]

    G = {}
    nodes = [n for n in input_nodes]
    while len(nodes) > 0:
        n = nodes.pop(0)
        if n not in G:
            G[n] = {'in': set(), 'out': set()}
        for m in n.outbound_nodes:
            if m not in G:
                G[m] = {'in': set(), 'out': set()}
            G[n]['out'].add(m)
            G[m]['in'].add(n)
            nodes.append(m)

    L = []
    S = set(input_nodes)
    while len(S) > 0:
        n = S.pop()

        if isinstance(n, Input):
            n.value = feed_dict[n]

        L.append(n)
        for m in n.outbound_nodes:
            G[n]['out'].remove(m)
            G[m]['in'].remove(n)
            # if no other incoming edges add to S
            if len(G[m]['in']) == 0:
                S.add(m)
    return L



def forward_pass(output_node, sorted_nodes):

	"""
	Performs a forward pass through a list of sorted nodes.

	Aurguments: 
	'output node': 
	'sorted_nodes': 

	Returns the nodes output value
	"""

	for n in sorted_nodes:
		n.forward()

	return output_node.value
