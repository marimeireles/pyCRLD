# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/Environments/12_MultipleObsSocialDilemma.ipynb.

# %% auto 0
__all__ = ['MultipleObsSocialDilemma']

# %% ../../nbs/Environments/12_MultipleObsSocialDilemma.ipynb 5
from .Base import ebase

from fastcore.utils import *
from fastcore.test import *

from .HeterogeneousObservationsEnv import HeterogeneousObservationsEnv

import numpy as np

# %% ../../nbs/Environments/12_MultipleObsSocialDilemma.ipynb 6
class MultipleObsSocialDilemma(HeterogeneousObservationsEnv):
    """
    Symmetric 2-agent 2-action Social Dilemma Matrix Game.
    """
    def __init__(self,
                 rewards,  # rewards of mutual cooperation
                 temptations,  # temptations of unilateral defection
                 suckers_payoffs,  # sucker's payoff of unilateral cooperation
                 punishments,  # punishment of mutual defection
                 pC=0.5,
                 observation_opacity=None):

        # Normalize inputs to be lists of length 2
        self.rewards = [rewards, rewards] if isinstance(rewards, int) else rewards
        self.temptations = [temptations, temptations] if isinstance(temptations, int) else temptations
        self.suckers_payoffs = [suckers_payoffs, suckers_payoffs] if isinstance(suckers_payoffs, int) else suckers_payoffs
        self.punishments = [punishments, punishments] if isinstance(punishments, int) else punishments

        # Ensuring all are lists of size 2 for consistency
        if not all(len(lst) == 2 for lst in [self.rewards, self.temptations, self.suckers_payoffs, self.punishments]):
            raise ValueError("All parameters must either be a single integer or a list of two integers.")

        # TODO: these variables are expected to be already initialized in the parent class
        # causing a recursive calling and causing the dependency on them to fail
        # therefore we need to initialize them here
        self.n_agents = 2
        self.n_agent_actions = 2
        self.n_states = 2 # TODO: I'm not entirely sure on why we have 2 states here
        

        self.pC = pC  # prop. contract TODO: no idea what this is    
        self.state = 0 # initial state
        super().__init__(observation_opacity=observation_opacity)


# %% ../../nbs/Environments/12_MultipleObsSocialDilemma.ipynb 7
@patch
def transition_tensor(self:MultipleObsSocialDilemma):
    """Calculate the Transition Tensor"""
    Tsas = np.ones((2, 2, 2, 2)) * (-1)
    Tsas[:, :, :, 0] = 1 - self.pC
    Tsas[:, :, :, 1] = self.pC
    return Tsas

@patch
def reward_tensor(self:MultipleObsSocialDilemma):
    """Get the Reward Tensor R[i,s,a1,...,aN,s']."""

    R = np.zeros((self.n_agents, self.n_states, self.n_agent_actions, self.n_agent_actions, self.n_states))

    # TODO: the way these arrays are defined is invalid code and I dont want to figure out why

    # TODO: in general i don't understand the construction of these arrays. What does : do anyway?
    # ok so the cmd above creates two arrays (n_agents) of a two dimensional space that is indicating the number
    # of states, for each action an agent can take... So we have one matrix that contains all actions C 
    # and another matrix containing all actions D. So I'm assuming a game can be in either C state or D state?
    # though I thought IPD only had one state '.'. This is where my confusion lies.
    # I also don't fully understand how these arrays are filled. I should print R and check.
    
    # set reward matrix for agent 0
    R[0, 0, :, :, 0] = [[self.rewards[0], self.suckers_payoffs[0]],
                        [self.temptations[0], self.punishments[0]]]
    R[1, 0, :, :, 0] = [[self.rewards[0], self.temptations[0]],
                        [self.suckers_payoffs[0], self.punishments[0]]]
    R[:, 0, :, :, 1] = R[:, 0, :, :, 0]

    # set reward matrix for agent 1 in the second state
    R[0, 1, :, :, 1] = [[self.rewards[1], self.suckers_payoffs[1]],
                        [self.temptations[1], self.punishments[1]]]
    R[1, 1, :, :, 1] = [[self.rewards[1], self.temptations[1]],
                        [self.suckers_payoffs[1], self.punishments[1]]]
    R[:, 1, :, :, 0] = R[:, 1, :, :, 1]
    
    return R

@patch
def actions(self:MultipleObsSocialDilemma):
    """The action sets"""
    return [['c', 'd'] for _ in range(self.n_agents)]

@patch
def states(self:MultipleObsSocialDilemma):
    """Default state set representation."""
    # States for two agents in a IPD game never change
    return ['.', '.']

@patch
def id(self:MultipleObsSocialDilemma):
    """
    Returns id string of environment
    """
    # Default
    id = f"{self.__class__.__name__}_"+\
        f"{self.temptations}_{self.rewards}_{self.punishments}_{self.suckers_payoffs}"
    return id
