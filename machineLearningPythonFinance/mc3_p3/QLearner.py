"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.radr=radr
        self.verbose = verbose
        self.num_actions = num_actions
        self.actions_range = range(num_actions)
        self.gamma = gamma
        self.s = 0
        self.rar = rar
        self.alpha = alpha
        self.lastAction = 3
        self.dyna = dyna
        self.qTable = {}

        self.tTable = {}
        self.Tc = {}
        self.rTable = {}

    def updateTTable(self, state, action, reward, s_prime):
        """
        add 1 to Tc[state, action, s']
        total = sum of all s' counts in Tc[s, a, :]
        for each s' in T[s, a]:
            T[s, a, s'] = Tc[s, a, s'] / total
        """
        previousR = self.rTable.get((state, action), None)
        self.rTable[(state, action)] = ((1 - self.alpha) * previousR) + (self.alpha * reward)
        for i in range(0,self.dyna):
            randomAction = rand.choice(self.actions_range)
            randomS = self.qTable.get((state, randomAction),0.0)

    def getQList(self, state):

        """
        table = {}
        if type == 'R':
            table = self.qTable
        else:
            table = self.rewardTable
        """

        qList = []
        for currentAction in self.actions_range:
            qList.append(self.qTable.get((state, currentAction),0.0))
        return qList

    def getAction(self, state):
        if rand.random() < self.rar:
            action = rand.choice(self.actions_range)
        else:
            qList = self.getQList(state)
            maxQValue = max(qList)
            bestList = []
            for currentAction in self.actions_range:
                if qList[currentAction] == maxQValue:
                    bestList.append(currentAction)
            selectedAction = rand.choice(bestList)
            action = self.actions_range[selectedAction]
        return action

    def updateQTable(self, state, action, reward, s_prime):
        previousQ = self.qTable.get((state, action), None)
        rewardGammaMax = reward + self.gamma * max(self.getQList(s_prime))
        if previousQ != None:
            self.qTable[(state, action)] = ((1 - self.alpha) * previousQ) + (self.alpha * rewardGammaMax)
        else:
            self.qTable[(state, action)] = reward

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """

        # querysetstate(s): Set state to s, return action for state s, but don't update Q-table.
        self.s = s
        action = self.getAction(s)
        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """

        # Update Q-table with <s, a, s_prime, r> and return new action for state s_prime.
        self.updateQTable(self.s, self.lastAction, r, s_prime)
        self.rar = self.rar * self.radr
        action = self.getAction(s_prime)
        self.lastAction = action
        self.s = s_prime

        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"