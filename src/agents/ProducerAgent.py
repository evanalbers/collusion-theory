from thesimulator import *

def policy():
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

def calculate_capital_investment():
    """ Calculates agent capital investment at time t"""
    pass

def calculate_capital_update():
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



class ProducerAgent: 

    production_function = None
    policy = None


    """ Representing the behavior of the producer agent described in the Simulation 
    Agent Attributes: 


    
    
    
    """

    def configure(self, params):
        """ saving parameters to agent object """
        pass
    
    def receiveMessage(self, simulation, type, payload, source):
        """ agent behavior is defined relative to messaged received. """