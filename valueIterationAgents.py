# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for state in self.mdp.getStates(): #get all the states
            self.values[state] = 0.0       #we set them all to 0.0

        for i in range(self.iterations):   #run for these many iterations
            new_values = self.values.copy() #copy the old values
            
            for state in self.mdp.getStates():
                state_values = util.Counter() #values for actions of this state
            
                for action in self.mdp.getPossibleActions(state):
                    state_values[action] = self.getQValue(state, action)
            
                new_values[state] = state_values[state_values.argMax()]  #update for each state
            
            self.values = new_values.copy() #copy back the new values
    
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        transition_probabilities = self.mdp.getTransitionStatesAndProbs(state, action) #gave you a list of states and probabilities
        Q_value = 0.0
        
        for transition in transition_probabilities:
            transition_state, probability = transition
            Q_value += probability * (self.mdp.getReward(state, action, transition_state) + self.discount * self.getValue(transition_state)) #make the sum of all transitions

        return Q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if (self.mdp.isTerminal(state)):
            return None
        else:
            Q_values = util.Counter()
            actions = self.mdp.getPossibleActions(state)
            
            for action in actions:
                Q_values[action] = self.computeQValueFromValues(state, action) #get the Q_value of the determined action
            
            Q_values = Q_values.argMax() #get the biggest value
            
            return Q_values

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
