import json
import sys
import numpy as np
import os

import lxml.etree as ET
BASIC_TEMPLATE = """<Simulation start="0" duration="10000">
    
</Simulation> """

VERBOSE = True
SOFTNESS = 0
HOMOGENOUS = True
CAPITAL_MU = 1000
CAPITAL_SD = 10
MARKET_AGENT_FP = '/Users/evaers/Documents/Repos/collusion-theory/src/agents/MarketAgent.py'
PRODUCER_AGENT_FP = '/Users/evaers/Documents/Repos/collusion-theory/src/agents/ProducerAgent.py'

def addExchangeXMLElements(simulation_root):
    """ Adds market agent to XML structure """

    global VERBOSE

    ET.SubElement(simulation_root, "MarketAgent")
    simulation_root[0].set('name', 'Market')
    simulation_root[0].set('softness', str(SOFTNESS))
    simulation_root[0].set('verbose', str(VERBOSE))
    simulation_root[0].set('file', MARKET_AGENT_FP)
    simulation_root[0].tail = "\n  "

def addAgentXMLElements(simulation_root, num_agents):
    """ adds requisite number of agents to xml object """

    for num in range(num_agents):

        ET.SubElement(simulation_root, "ProducerAgent")
        simulation_root[num + 1].set('file', PRODUCER_AGENT_FP)
        simulation_root[num + 1].set('name', "AGENT" + str(num))
        
        simulation_root[num + 1].set('market', 'MarketAgent')
        # generate random endowment 
        capital = np.random.normal(CAPITAL_MU, CAPITAL_SD, 1)
        simulation_root[num + 1].set('endowment', str(capital[0]))
        simulation_root[num + 1].tail = "\n  "


def generateSimulation(name, num_agents):
    """ generates simulation XML file! """

    ##set up initial XML file object

    sim = ET.fromstring(BASIC_TEMPLATE)

    addExchangeXMLElements(sim)

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