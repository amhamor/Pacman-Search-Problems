# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	print "Start's successors:", problem.getSuccessors(problem.getStartState())
	"""
	"*** YOUR CODE HERE ***"
	def get_zipped_depth_with_successor_list(depth, successors_list):
		successors_count = len(successors_list)
		return list(zip([depth]*successors_count, successors_list))

	frontier_states_list = get_zipped_depth_with_successor_list(1, problem.getSuccessors(problem.getStartState()))
	states_visited_list = []
	path_actions_list = []
	depth = 0
	expanding_node_position = problem.getStartState()
	
	while not problem.isGoalState(expanding_node_position):
		if frontier_states_list == []: return None		

		depth, next_state_triple = frontier_states_list.pop()

		path_actions_list = path_actions_list[:depth-1]

		expanding_node_position = next_state_triple[0]
		states_visited_list.append(expanding_node_position)
		path_actions_list.append(next_state_triple[1])

		for successor_state_triple in problem.getSuccessors(expanding_node_position):
			if successor_state_triple[0] not in states_visited_list:
				frontier_states_list.append((depth+1, successor_state_triple))

	return path_actions_list

def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	"*** YOUR CODE HERE ***"
	frontier_state_triples_list = problem.getSuccessors(problem.getStartState())
	expanding_node_position = problem.getStartState()

	states_visited_list = [problem.getStartState()]
	state_triples_path_list = [[]] * len(frontier_state_triples_list)
	expanding_path = state_triples_path_list[0].copy()

	while not problem.isGoalState(expanding_node_position, expanding_path):
		if frontier_state_triples_list == []: return None
		
		next_state_triple = frontier_state_triples_list[0]
		frontier_state_triples_list = frontier_state_triples_list[1:]
		
		expanding_node_position = next_state_triple[0]
		states_visited_list.append(expanding_node_position)
		
		expanding_path = state_triples_path_list[0].copy()
		expanding_path.append(next_state_triple[1])
		#print("expanding_path: " + str(expanding_path))
		state_triples_path_list = state_triples_path_list[1:]
		
		for successor_triple in problem.getSuccessors(expanding_node_position):
			if successor_triple[0] not in states_visited_list:
				frontier_state_triples_list.append(successor_triple)
				state_triples_path_list.append(expanding_path.copy())

		'''if (expanding_node_position in problem.corners_list) and not problem.isGoalState(expanding_node_position):
			problem.corners_list.remove(expanding_node_position)
			problem.startingPosition = expanding_node_position
			expanding_path += breadthFirstSearch(problem)
		elif problem.isGoalState(expanding_node_position):
			return expanding_path'''
	return expanding_path
	#return [state_triple[1] for state_triple in expanding_path]

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	"*** YOUR CODE HERE ***"
	def sort_triples_by_ascending_cost(triples_list, frontier_state_triples_list):
		def sort(triples_list, iteration_index):
			temporarily_stored_element = triples_list[iteration_index]
			triples_list[iteration_index] = triples_list[iteration_index+1]
			triples_list[iteration_index+1] = temporarily_stored_element

		for triple_index in range(0, len(triples_list)-1):
			for iteration_index in range(triple_index, len(triples_list)-1):
				primary_total_cost = sum([triple[2] for triple in triples_list[iteration_index]])
				secondary_total_cost = sum([triple[2] for triple in triples_list[iteration_index+1]])

				if primary_total_cost > secondary_total_cost:
					sort(triples_list, iteration_index)
					sort(frontier_state_triples_list, iteration_index)
		return (triples_list, frontier_state_triples_list)

	frontier_state_triples_list = problem.getSuccessors(problem.getStartState())
	expanding_node_position = problem.getStartState()

	states_visited_list = [problem.getStartState()]
	state_triples_path_list = [[]] * len(frontier_state_triples_list)

	while not problem.isGoalState(expanding_node_position):
		if frontier_state_triples_list == []: return None
		
		state_triples_path_list, frontier_state_triples_list = sort_triples_by_ascending_cost(state_triples_path_list, frontier_state_triples_list)
		
		next_state_triple = frontier_state_triples_list[0]
		frontier_state_triples_list = frontier_state_triples_list[1:]

		expanding_node_position = next_state_triple[0]
		states_visited_list.append(expanding_node_position)

		expanding_path = state_triples_path_list[0].copy()
		expanding_path.append(next_state_triple)
		state_triples_path_list = state_triples_path_list[1:]

		for successor_triple in problem.getSuccessors(expanding_node_position):
			if successor_triple[0] not in states_visited_list:
				frontier_state_triples_list.append(successor_triple)
				state_triples_path_list.append(expanding_path.copy())

	return [state_triple[1] for state_triple in expanding_path]

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	"*** YOUR CODE HERE ***"
	def sort_triples_by_ascending_cost(triples_list, frontier_state_triples_list):
		def sort(triples_list, iteration_index):
			temporarily_stored_element = triples_list[iteration_index]
			triples_list[iteration_index] = triples_list[iteration_index+1]
			triples_list[iteration_index+1] = temporarily_stored_element

		for triple_index in range(0, len(triples_list)-1):
			for iteration_index in range(triple_index, len(triples_list)-1):				
				primary_total_cost = sum([triple[2]+heuristic(triple[0], problem) for triple in triples_list[iteration_index]])
				secondary_total_cost = sum([triple[2]+heuristic(triple[0], problem) for triple in triples_list[iteration_index+1]])

				if primary_total_cost > secondary_total_cost:
					sort(triples_list, iteration_index)
					sort(frontier_state_triples_list, iteration_index)
		return (triples_list, frontier_state_triples_list)

	frontier_state_triples_list = problem.getSuccessors(problem.getStartState())
	expanding_node_position = problem.getStartState()

	states_visited_list = [problem.getStartState()]
	state_triples_path_list = [[]] * len(frontier_state_triples_list)

	while not problem.isGoalState(expanding_node_position):
		if frontier_state_triples_list == []: return None
		
		state_triples_path_list, frontier_state_triples_list = sort_triples_by_ascending_cost(state_triples_path_list, frontier_state_triples_list)
		
		next_state_triple = frontier_state_triples_list[0]
		frontier_state_triples_list = frontier_state_triples_list[1:]

		expanding_node_position = next_state_triple[0]
		states_visited_list.append(expanding_node_position)

		expanding_path = state_triples_path_list[0].copy()
		expanding_path.append(next_state_triple)
		state_triples_path_list = state_triples_path_list[1:]

		for successor_triple in problem.getSuccessors(expanding_node_position):
			if successor_triple[0] not in states_visited_list:
				frontier_state_triples_list.append(successor_triple)
				state_triples_path_list.append(expanding_path.copy())

	return [state_triple[1] for state_triple in expanding_path]

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
