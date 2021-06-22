'''
NOTE:
    LUCAS HATTORI COSTA - 10335847
'''
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

    print "Start:", problem.getStartState() ==> Start: (5, 5)
    print "Is the start a goal?", problem.isGoalState(problem.getStartState()) ==> Is the start a goal? False
    print "Start's successors:", problem.getSuccessors(problem.getStartState()) ==> Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    """
    plan = util.Stack() # each item of plan consists on a tuple (state, actions)
    currState = problem.getStartState()
    actions = []
    plan.push((currState, actions))
    nodesVisited = []
    
    while not problem.isGoalState(currState):
        if currState not in nodesVisited:
            nodesVisited.append(currState)
            for (nextState,nextAction,cost) in problem.getSuccessors(currState):
                if (not nextState in nodesVisited) or (problem.isGoalState(nextState)):
                    plan.push((nextState, actions+[nextAction]))
        (currState, actions) = plan.pop()
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    plan = util.Queue()
    currState = problem.getStartState()
    actions = []
    plan.push((currState, actions))
    nodesVisited = []

    while not plan.isEmpty():
        (currState, actions) = plan.pop()
        if currState not in nodesVisited:
            nodesVisited.append(currState)
            if problem.isGoalState(currState):
                return actions         
            for (nextState, nextAction, cost) in problem.getSuccessors(currState):
                if (not nextState in nodesVisited):
                    plan.push((nextState, actions+[nextAction]))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    plan = util.PriorityQueue()
    currState = problem.getStartState() 
    actions = []
    plan.push((currState, actions, 0), 0)# initialize queue with first state with priority 0
    nodesVisited = []

    while not plan.isEmpty():
        (currState, actions, toCost) = plan.pop()
        if currState not in nodesVisited:
            nodesVisited.append(currState)
            if problem.isGoalState(currState):
                return actions
            for (nextState, nextAction, cost) in problem.getSuccessors(currState):
                newCost = toCost + cost
                plan.push((nextState, actions+[nextAction], newCost), newCost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    plan = util.PriorityQueue()
    currState = problem.getStartState() 
    actions = []
    plan.push((currState, actions, 0), 0)# initialize queue with first state with priority 0
    nodesVisited = []# dict of {state: cost}

    while not plan.isEmpty():
        (currState, actions, toCost) = plan.pop()
        if currState not in nodesVisited:
            nodesVisited.append(currState)
            if problem.isGoalState(currState):
                return actions                  
            for (nextState, nextAction, cost) in problem.getSuccessors(currState):
                newCost = toCost + cost
                plan.push((nextState, actions+[nextAction], newCost), newCost + heuristic(nextState, problem))

def learningRealTimeAStar(problem, heuristic=nullHeuristic):
    """Execute a number of trials of LRTA* and return the best plan found."""
    """
        NOTE:  This same function can be used to solve both problems, finding the corners in maze or the food.
        However, it requires a setting that impairs its readability. In this function, the state of the 
        problem is used as the key of a dict. In the food problem, this does not lead to any error, 
        because the state is simply the Pacman coordinates . But in the Corner problem, the state is defined
        by the coordinates and a list of visited corners. This second state cannot be used as the key of 
        a dict because it contains a list and for their mutable nature, they cannot be contained in such keys,
        raising a TypeError error in Python. So the alternative was to create an if/else that identifies the problem 
        being addressed and therefore accessing the dict correctly.
        This way, in both problems, the keys will be the tuples that identify the position of the Pacman. 
        Although that might undermine code comprehension, it was the solution that least changes the rest of
        the code.
    """
    if isinstance(problem.getStartState()[1], list):
        prob = 'Corner'
    else:
        prob = 'Food'

    MAXTRIALS = 10
    print 'Trials realizados: ', MAXTRIALS
    nodesVisited = {} # dict of {state: heuristics}
    if prob=='Food':
        nodesVisited[problem.getStartState()] = heuristic(problem.getStartState(), problem)
    elif prob=='Corner':
        nodesVisited[problem.getStartState()[0]] = heuristic(problem.getStartState(), problem)

    for _ in range(MAXTRIALS):
        (currState, actions, totalCost) = (problem.getStartState(), [], 0)
        while not problem.isGoalState(currState):
            minF = None
            for (nextState, NextAction, cost) in problem.getSuccessors(currState):
                try:
                    if prob=='Food':        
                        f = cost + nodesVisited[nextState]
                    elif prob=='Corner':        
                        f = cost + nodesVisited[nextState[0]]
                except KeyError: # next state hasn't been visited yet
                    if prob=='Food':        
                        nodesVisited[nextState] = heuristic(nextState, problem)    
                        f = cost + nodesVisited[nextState]
                    elif prob=='Corner':        
                        nodesVisited[nextState[0]] = heuristic(nextState, problem)    
                        f = cost + nodesVisited[nextState[0]]
                if (f < minF or minF is None):
                    minF = f
                    bestNextState = nextState
                    bestNextAction = NextAction
            if prob=='Food':        
                nodesVisited[currState] = max(nodesVisited[currState], minF)
            elif prob=='Corner':        
                nodesVisited[currState[0]] = max(nodesVisited[currState[0]], minF)
            actions.append(bestNextAction)
            currState = bestNextState

    return actions

# Abbreviations 
# *** DO NOT CHANGE THESE ***
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
lrta = learningRealTimeAStar
