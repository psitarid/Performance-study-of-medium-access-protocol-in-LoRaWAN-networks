import numpy as np
from Node_Class import Node
from Simulation_Class import Simulation


def select_nodes_to_transmit(time, lambd, ToA, node_list, nodes_transmitting, nodes_to_retransmit):
    """
    Selects new nodes to transmit for the first time from node_list with Poisson distribution.
    Also checks whether a node tries to retransmit. It puts all the nodes willing to transmit
    in the nodes_transmitting list and removes them from the node_list.
    
    Args:
        time (int): Current simulation time.
        node_list (list): list of all nodes.
        nodes_transmitting (list): list of nodes currently transmitting.
        nodes_to_retransmit (list): list of nodes attempting to retransmit.
        lambd (float): Poisson distribution parameter.
        ToA (int): Time on air for transmission.
    
    Returns:
        int: Total number of nodes selected to transmit.
    """
    num_to_transmit = -1  # Number of nodes to transmit
    new_nodes_to_retransmit = []  # Nodes attempting to retransmit
    nodes_attempted_to_retransmit = 0  # Number of nodes attempting to retransmit
    total_nodes_selected = 0  # Total number of nodes selected to transmit
    unable_to_transmit_because_of_duty_cycle = 0  # Number of nodes unable to transmit due to duty cycle
    
    # Choose the number of nodes to transmit using Poisson distribution
    while(num_to_transmit < 0 or num_to_transmit > len(node_list)):
        num_to_transmit = np.random.poisson(lambd * len(node_list))
        
    for _ in range(num_to_transmit):
        i = np.random.choice(node_list)
        if (i.time_transmitted + ToA) <= i.allowed_transmission_time:  # Checking if the node exceeds the duty cycle
            i.time_transmitted += ToA
            nodes_transmitting.append(i)
            node_list.remove(i)
        else:
            unable_to_transmit_because_of_duty_cycle += 1

    # Check if any nodes want to retransmit
    if(len(nodes_to_retransmit) > 0):
        for j in nodes_to_retransmit:
            if(time == (j.retransmission_time)):
                if (j.time_transmitted + ToA) <= j.allowed_transmission_time:  # Checking if the node exceeds the duty cycle
                    j.time_transmitted += np.round(ToA)
                    nodes_transmitting.append(j)
                    nodes_attempted_to_retransmit += 1
                else:
                    unable_to_transmit_because_of_duty_cycle += 1
                    new_nodes_to_retransmit.append(j)
            else:
                new_nodes_to_retransmit.append(j)
        nodes_to_retransmit[:] = new_nodes_to_retransmit
    
    total_nodes_selected = num_to_transmit + nodes_attempted_to_retransmit - unable_to_transmit_because_of_duty_cycle
    
    return total_nodes_selected


def check_collisions(gateway, nodes_transmitting):
    """
    Check if any nodes transmit at the same time, including the gateway, and set them to "collided" or not.
    
    Args:
        nodes_transmitting (list): list of nodes currently transmitting.
        gateway (object): Gateway object.
        ack_duration (int): Duration of acknowledgment.
    """
    if((len(nodes_transmitting) >= 1 and gateway.get_state() == 'busy') or len(nodes_transmitting) > 1 and gateway.get_state() == 'idle'):
        if(gateway.get_state() == 'busy'):
            gateway.ack_collided = True
        for node in nodes_transmitting:
            if(node.collided == False):
                node.collided = True


def check_uplink_finished(time, nodes_transmitting, RX_delay1, min_timeout_for_ack, max_timeout_for_ack, waiting_for_ack):
    """
    Check if any node has finished transmitting. If anyone does, transfer them to the waiting_for_ack list.
    
    Args:
        time (int): Current simulation time.
        nodes_transmitting (list): list of nodes currently transmitting.
        RX_delay1 (int): Delay for receiving acknowledgment.
        min_timeout_for_ack (int): Minimum timeout duration for acknowledgment.
        max_timeout_for_ack (int): Maximum timeout duration for acknowledgment.
        waiting_for_ack (list): list of nodes waiting for acknowledgment.
    """
    new_nodes_transmitting = []
    if(len(nodes_transmitting) > 0):
        for node in nodes_transmitting:
            if(node.time_left == 0):  # Check if nodes finished transmitting
                waiting_for_ack.append(node)  # Transfer the finished nodes to waiting_for_ack list
                node.RX_delay1_ends = time + RX_delay1
                node.timeout_for_ack = np.random.randint(min_timeout_for_ack, max_timeout_for_ack)
                node.timeout_ends = time + RX_delay1 + node.timeout_for_ack
            else:
                new_nodes_transmitting = np.append(new_nodes_transmitting, node)
        nodes_transmitting.clear()
        for node in new_nodes_transmitting:
            node.time_left -= 1
            nodes_transmitting.append(node)


def change_d_c_phases(node_list, nodes_to_retransmit, waiting_for_ack, nodes_transmitting):
    """
    Update the time lived, duty cycle, and allowed transmission time for each node in the given lists.

    Parameters:
    - node_list (list): A list of nodes.
    - nodes_to_retransmit (list): A list of nodes to retransmit.
    - waiting_for_ack (list): A list of nodes waiting for acknowledgment.
    - nodes_transmitting (list): A list of nodes currently transmitting.

    Returns:
    None
    """
    lists = [node_list, nodes_to_retransmit, waiting_for_ack, nodes_transmitting]
    for nodes in lists:
        if len(nodes) > 0:
            for node in nodes:
                node.time_lived += 1                                                                        
                if node.time_lived <= 3600000:                                                                    
                    node.duty_cycle = 0.01                                                                                       
                    node.allowed_transmission_time = 36000                                                                            
                elif node.time_lived > 3600000 and node.time_lived <= 36000000:                                                                    
                    node.duty_cycle = 0.001                                                                                      
                    node.allowed_transmission_time = 36000                                                                           
                elif node.time_lived > 36000000:                                                                                                
                    node.duty_cycle = 0.0001                                                                             
                    node.allowed_transmission_time = 8700                                                                       
                if(node.time_lived % np.round(node.allowed_transmission_time/node.duty_cycle) == 0):       #reset transmission time in each duty cycle phase                          
                    node.time_transmitted = 0                  


