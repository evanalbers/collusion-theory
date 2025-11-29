from thesimulator import *
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

def market_demand(price):
    """ returns volume demanded """

    return price / 5

def mean_function(price, quantity, scaling_factor, price_elas):
    """ returns the mean of the GP representing market context """

    return scaling_factor * quantity * price ** (-price_elas)


def sample_market_context(scaling_factor, quantity, price, price_elas):
    """ Samples the market context for a given quantity and price """

    # defining the kernel process
    kernel = RBF(length_scale=1.0)
    gp = GaussianProcessRegressor(kernel=kernel)

    # sampling GP to get mu, phi
    mu, phi = gp.predict([[price, quantity]], return_std=True)

    # calc prior relating mu to price, quantity
    prior = mean_function(price, quantity, scaling_factor, price_elas)

    sample_mu = prior + mu

    return np.random.normal(sample_mu, phi)

def calculate_market_share(num_agents, prices, softness):
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
    shares = np.zeros(num_agents)

    for agent in num_agents:

        numerator = np.exp(-prices[agent] / softness)

        denom = 0
        for a in prices:
            denom += np.exp(-prices[a] / softness)

        shares[agent] = numerator / denom

    return shares

def resolve_transactions(prices, offers, softness, demand_function):
    """ Transaction resolution for each agent in """

    winning_price = np.min(prices)

    market_demand = demand_function(winning_price)

    if softness == 0:
        shares = np.zeros(prices.size)
        winners = np.where(prices == winning_price)

        winning_shares = 1 / len(winners)

        shares[winners] = winning_shares

    else:
        shares = calculate_market_share(prices.size, prices, softness)

    return np.minimum(shares * market_demand, offers)

    
class MarketAgent: 
    """ Agent class representing the market where ProducerAgents transact

        Basic pattern is gather all price estimates from the market, process them, send back 
        quantities demanded. 
      
    """
    softness = 0
    num_agents = 0
    scaling_factor = 1
    price_elas = 1
    timestep_volume_bids = {}
    
    
    def configure(self, params):
        """ Configures the Market Agent with corresponding params"""
        print(params)
        self.softness = float(params['softness'])
        self.num_agents = int(params['num_agents'])
        self.scaling_factor = float(params['scaling_factor'])
        self.price_elas = float(params['price_elas'])
        self.sim_duration = int(params['duration'])
        self.market_contexts = np.zeros(self.sim_duration)
        self.init_quantity = int(params['initial_quantity'])
        self.init_price = int(params['initial_price'])

    def receiveMessage(self, simulation, type, payload, source):
        """ agent behavior is defined relative to messaged received. """

        current_timestamp = simulation.currentTimestamp()

        # Three possible types of message:

        # One: Simulation start - in this case, start getting bids for first timestep. 
        if type == "EVENT_SIMULATION_START":
            market_context = sample_market_context(self.scaling_factor, self.init_quantity, self.init_price, self.price_elas)
            self.market_contexts[current_timestamp] = market_context
            for agent in range(self.num_agents):
                print("dispatched signal to agent " + str(agent))
                simulation.dispatchGenericMessage(current_timestamp, 1, self.name(), str(agent), "MARKET_SIGNAL", {"v_prime" : str(market_context)})

        # Two: bid from an agent 
            # two subcases here: in first, don't have all orders, in second we do. 
            # in first, add the information then sleep
            # in second, we resolve transactions on the timestep and then send out info

        if type == "BID":

            self.timestep_volume_bids[source] = (payload['price'], payload['offer'])

            # if we have all the bids, need to resolve transactions
            if len(self.timestep_volume_bids.keys()) == self.num_agents:

                # create prices, volumes array 
                prices = np.zeros(self.num_agents)
                offers = np.zeros(self.num_agents)

                for key in self.timestep_volume_bids.keys():
                    prices[int(key)] = self.timestep_volume_bids[key][0]
                    offers[int(key)] = self.timestep_volume_bids[key][1]

                
                realized_volumes = resolve_transactions(prices, offers, self.softness, market_demand)

                # send out realized volumes 
                for agent in range(self.num_agents):
                    simulation.dispatchGenericMessage(current_timestamp, 0, self.name(), str(agent), "RESOLVED_TRANSACTION", {"realized_vol" : str(realized_volumes[agent])})

                # zero out timestep bids for next timestep
                self.timestep_volume_bids = {}
            
                market_context = sample_market_context(self.scaling_factor, self.init_quantity, self.init_price, self.price_elas)
                self.market_contexts[current_timestamp] = market_context
                for agent in range(self.num_agents):
                    print("dispatched signal to agent " + str(agent))
                    simulation.dispatchGenericMessage(current_timestamp, 1, self.name(), str(agent), "MARKET_SIGNAL", {"v_prime" : str(market_context)})

        #NEED TO HAVE WAKEUP MESSAGE THAT TRIGGERS THIS ALL AGAIN - RIGHT NOW SENDS OUT 4 FOR 

        if type == "EVENT_SIMULATION_STOP":
            pass

        # Three: simulation is over. write out data and quit.

