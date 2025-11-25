from thesimulator import *
import numpy as np



def calculate_market_share(agent, prices, softness):
    """ calculates the market share of the given agent based on the given prices 
    Params
    ------
    agent : int
        index represent the id of the agent
    
    prices : np.array
        array of prices submitted by each agent
    
    softness : float
        representing how "soft" the market is as defined in paper (lambda)

    Returns
    -------
    share : float
        market share of given agent 

    """

    numerator = np.exp(-prices[agent] / softness)

    denom = 0
    for a in prices:
        denom += np.exp(-prices[a] / softness)

    return numerator / denom

def resolve_transactions():
    """ Transaction resolution for each agent in """

class MarketAgent: 
    """ Agent class representing the market where ProducerAgents transact

        Basic pattern is gather all price estimates from the market, process them, send back 
        quantities demanded. 
      
    """

    softness = 0
    
    def configure(self, params):
        """ Configures the Market Agent with corresponding params"""

        self.softness = float(params['softness'])

        print("Softness of the market: " + str(self.softness))

    def receiveMessage(self, simulation, type, payload, source):
        """ agent behavior is defined relative to messaged received. """