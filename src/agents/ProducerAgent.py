from thesimulator import *
import numpy as np
import h5py

def production_function(k, r):
    """ returns quantity of product produced as function of capital """

    return k * r * 1.5 

def policy(market_context):
    """ Agent policy that determines the price the agent proposes
        and the fraction of capital the agent invests at time t
    
    Params
    ------
    v_t_prime : float
        market signal v prime at time t

    Returns
    -------
    price_t : float
        price agent will charge 

    k_t : float
        proportion of total capital invested in production            
    """

    return 10, 0.5


def calculate_capital_update(k_t, R_t_m1, p_t, v_i):
    """ Calculates the agent's capital for the next timestep based
        on its own sales at its own price. 
        
        Params
        ------
        k_t : float
            proportion of capital invested
        
        R_t_m1 : float
            capital at timestep t-1
            
        p_t : float
            price proposed at timestep t

        v_i : int
            volume of goods sold at timestep t

        """
    
    return (1 - k_t) * R_t_m1 + p_t * v_i



class ProducerAgent: 

    # production_function = basic_production_function
    policy = policy


    """ Representing the behavior of the producer agent described in the Simulation 
    Agent Attributes: 
    
    """

    def configure(self, params):
        """ saving parameters to agent object """
        self.sim_duration = int(params['duration'])
        self.k_values = np.zeros(self.sim_duration)
        self.prices = np.zeros(self.sim_duration)
        self.capital = np.zeros(self.sim_duration)
        self.capital[0] = params['endowment']
        self.output_fp = params['output_fp']

    
    def receiveMessage(self, simulation, type, payload, source):
        """ agent behavior is defined relative to messaged received. """

        # Four possible messages: 
        # Simulation start: go to sleep wait for request from market for timestep 1
        # Market signal: context signal from the market to send a bid 
        # Resolved transaction: update capital, go to sleep and wait for request for next timestep
        # Simulation end: write out data, quit etc. 

        current_timestamp = simulation.currentTimestamp()

        if type == "EVENT_SIMULATION_START":
            print(self.name())
            # Just sleep here, I think
            pass
        elif type == "MARKET_SIGNAL":
            v_prime = payload["v_prime"][0]
            self.prices[current_timestamp], self.k_values[current_timestamp] = policy(v_prime)
            offer = production_function(self.k_values[current_timestamp], self.capital[current_timestamp-1])
            print("Name "+ self.name())
            print("Offer " + str(offer))
            print("Prices " + str(self.prices[current_timestamp]))
            print("Timestamp " + str(current_timestamp))
            
            simulation.dispatchGenericMessage(current_timestamp, 0, self.name(), "Market", "BID", {"price" : str(self.prices[current_timestamp]), "offer" : str(offer)})

        elif type == "RESOLVED_TRANSACTION":

            volume_sold = payload["realized_vol"]
            self.capital[current_timestamp] = (1 - self.k_values[current_timestamp]) * self.capital[current_timestamp - 1] + self.prices[current_timestamp] * float(volume_sold)
            # Then sleep
            
            pass
        elif type == "EVENT_SIMULATION_STOP":
            
            with h5py.File(self.output_fp + '/' + self.name() + '.h5', 'w') as f:
                f.create_dataset("prices", data=self.prices)
                f.create_dataset("capital", data=self.capital)
                f.create_dataset("k_values", data=self.k_values)
            
        

        else:
            print("Unknown message type recieved!")
        
        