from Common.astar import AStar
from cnet import CNET
from cnetGraph import CNETGraph
from gac import GAC

class Astar_GAC(object): 
	"""Astar_GAC integrates Astar and GAC"""
	def __init__(self, serachProblem, cnetGraph):
		self.serachProblem = serachProblem
		# cnet : cnet of searh problem
		self.cnet = self.convertToCNET(serachProblem)
		self.GAC = createGAC(self.cnet)
		self.graph = cnetGraph.CNETGraph()
		self.AStar = createAstar(self.graph, 'best_first')
		


	def createGAC(self, state):
		return GAC(self.initilizeState(self.cnet))

	def createAstar(self, graph, method):
		return AStar(cnetGraph, method)

############ TODO : implement the converter : (uncomplete) ################
# graph : serachProblem
	def convertToCNET(self, graph):

		variables = graph.getVariables()
		domains = graph.getDomains()
		exp = graph.getExpression()
		cNet = CNET()
		cNet.addVariable(variables, domains)
		# Do we add constraints here or in initilizeState???
		cNet.addConstraints(variables, exp)

		return cNet

	
############ TODO : implement the generateInitState ################
	def initializeState(self, cnet, expression):
		"""in initState each variable has its full domain. It will be set as root node
		initilizes cnet"""
		initState = 0
		# cNet = self.convertToCNET(self.serachProblem)
		# cNet.addVariable(variable, domain)
		return initState
##########################################################

	def search(self):
		# self.cnet: is representation of search problem convertet to a cnet
		self.currentState = self.initializeState(self.cnet, self.expression) #root node
		# refine initState
		self.GAC.initilize()
		self.GAC.filterDomain()

		if isSolution(self.currentState):
			return self.currentState

		elif isContradictory(self.currentState):
			print( 'Dismissed. There is no solution!')
			return False

		while not isContradictory(self.currentState) and not isSolution(self.currentState):
			
			# AStar må returnere den noden vi popper
			# − Popping search nodes from the agenda 
			self.currentState = self.AStar.iterateAStar()
			
			# assumption: a "logical" guess for assignment
            assumption = self.makeAssumption(self.currentState)


			# − Generating their successor states (by making assumptions)
			self.generateSucc(assumption)

			# − Enforcing the assumption in each successor state by reducing
			# the domain of the assumed variable to a singleton set − Calling GAC−Rerun on each newly−generated state
			self.GAC.rerun(self.currentState)

			# − Computing the f , g and h values for each new state ,
			# where h is based on the state of the CSP after the call to GAC−Rerun.

			

	def isContradictory(self, state):
		for d in state.domains:
			if len(d[1]) == 0:
				return True
		return False
				

	def isSolution(self, state):
		for dom in state.domains.items():
			if len( dom[1] ) > 1 || not len( dom[1] ):
				return False
		return True

	def computeHeuristic(self, node):
		domains = self.currentState.getDomains()
		heuristic = 0
		for dom in domains.values():
			l = len(dom) - 1
			heuristic += l
		return heuristic

##### TODO :  implement makeAssumption	
		# what is assumption based on?
	def makeAssumption(self, state):
		""" make a guess. start gussing value for variables with min. domain length"""
		assumption = None
		return assumption
		
##### TODO : implement generateSucc
# Should this be defined here or in cnetGraph?
    def generateSucc(self, assumption):
    	# generate succ. states by assumptions->
    	pass



