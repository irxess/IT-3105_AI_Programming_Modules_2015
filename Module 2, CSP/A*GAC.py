from Common import astar
# from gac import initilize
import gac, csp

class Astar_GAC(object):
	"""Astar_GAC integrates Astar and GAC"""
	def __init__(self, searchProblem, graph):
		self.graph = graph
		self.searchProblem = searchProblem
		self.CI = gac.GAC(searchProblem) #????

	def generateInitState(self):
		pass

	def search(self):
		self.CI.initilize()
		self.CI.filterDomain()
		if not isContradictory(ci) and not isSolution(ci):
			# astar.Astar(graph, 'best_first')
			# − Popping search nodes from the agenda
			# − Generating their successor states (by making assumptions)
			# − Enforcing the assumption in each successor state by reducing
			# the domain of the assumed variable to a singleton set − Calling GAC−Rerun on each newly−generated state
			# − Computing the f , g and h values for each new state ,
			# where h is based on the state of the CSP after the call to GAC−Rerun.
		
			

	def isContradictory(self, ci):
		for d in ci.domains:
			if len(d) == 0:
				return True
		return False
				

	def isSolution(self, ci):
		pass
		return False

	def heuristic(self):
		pass