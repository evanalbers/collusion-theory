import json
import sys
import numpy as np
import os

import lxml.etree as ET
BASIC_TEMPLATE = """<Simulation start="0" duration="10000">
    
</Simulation> """

DURATION = 10000
VERBOSE = True
SOFTNESS = 0
HOMOGENOUS = True
CAPITAL_MU = 1000
CAPITAL_SD = 10
MARKET_AGENT_FP = '/Users/evaers/Documents/Repos/collusion-theory/src/agents/MarketAgent.py'
PRODUCER_AGENT_FP = '/Users/evaers/Documents/Repos/collusion-theory/src/agents/ProducerAgent.py'
OUTPUT_FP = '/Users/evaers/Documents/Repos/collusion-theory/data/test_data'
SCALING_FACTOR = 1
PRICE_ELASTICITY = 1
INITIAL_QUANTITY = 100
INITIAL_PRICE = 5


def addExchangeXMLElements(simulation_root, num_agents):
    """ Adds market agent to XML structure """

    global VERBOSE

    ET.SubElement(simulation_root, "MarketAgent")
    simulation_root[0].set('name', 'Market')
    simulation_root[0].set('softness', str(SOFTNESS))
    simulation_root[0].set('verbose', str(VERBOSE))
    simulation_root[0].set('file', MARKET_AGENT_FP)
    simulation_root[0].set('num_agents', str(num_agents))
    simulation_root[0].set('price_elas', str(PRICE_ELASTICITY))
    simulation_root[0].set('scaling_factor', str(SCALING_FACTOR))
    simulation_root[0].set('duration', str(DURATION))
    simulation_root[0].set('initial_quantity', str(INITIAL_QUANTITY))
    simulation_root[0].set('initial_price', str(INITIAL_PRICE))
    simulation_root[0].set('output_fp', OUTPUT_FP)
    simulation_root[0].tail = "\n  "

def addAgentXMLElements(simulation_root, num_agents):
    """ adds requisite number of agents to xml object """

    for num in range(num_agents):

        ET.SubElement(simulation_root, "ProducerAgent")
        simulation_root[num + 1].set('file', PRODUCER_AGENT_FP)
        simulation_root[num + 1].set('name', str(num))
        simulation_root[num + 1].set('market', 'MarketAgent')
        # generate random endowment 
        capital = np.random.normal(CAPITAL_MU, CAPITAL_SD, 1)
        simulation_root[num + 1].set('endowment', str(capital[0]))
        simulation_root[num + 1].set('duration', str(DURATION))
        simulation_root[num + 1].set('output_fp', OUTPUT_FP)
        simulation_root[num + 1].tail = "\n  "


def generateSimulation(name, num_agents):
    """ generates simulation XML file! """

    ##set up initial XML file object

    sim = ET.fromstring(BASIC_TEMPLATE)

    addExchangeXMLElements(sim, num_agents)

    addAgentXMLElements(sim, num_agents)

    # os.chdir(name)

    ## currently using default length of time 

    ## save file to simulation folder to run it  

    simulation_tree = ET.ElementTree(sim)

    # os.chdir("../")

    # "maxe/build/TheSimulator/TheSimulator/" 

    simulation_tree.write(name + '.xml', pretty_print=True, 
                         xml_declaration=True, 
                         encoding='UTF-8')

    


def main():

    global NUM_NOISY

    simulation_name = sys.argv[1]
    number_agents = int(sys.argv[2])
    generateSimulation(simulation_name, number_agents)

main()