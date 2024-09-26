import numpy as np


def select_nodes_to_transmit(time, lambd, ToA, node_list, nodes_transmitting, nodes_to_retransmit):
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
        if (i.Toff >= ToA/i.duty_cycle - ToA):  # Wait long enough until the next transmission to comply with duty cycle policy    
            nodes_transmitting.append(i)
            node_list.remove(i)
        else:
            unable_to_transmit_because_of_duty_cycle += 1

    # Check if any nodes want to retransmit
    if(len(nodes_to_retransmit) > 0):
        for j in nodes_to_retransmit:
            if(time == (j.retransmission_time)):
                if (j.Toff >= ToA/j.duty_cycle - ToA):  # Wait long enough until the next transmission to comply with duty cycle policy
                    nodes_transmitting.append(j)
                    nodes_attempted_to_retransmit += 1
                else:
                    print("Can't transmit because of duty cycle. Time: ", time)
                    unable_to_transmit_because_of_duty_cycle += 1
                    j.retransmission_time = time + np.random.randint(1, 10000)
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
                node.RX_delay1_ends = time + RX_delay1
                node.timeout_for_ack = np.random.randint(min_timeout_for_ack, max_timeout_for_ack)
                node.timeout_ends = time + RX_delay1 + node.timeout_for_ack
                waiting_for_ack.append(node)  # Transfer the finished nodes to waiting_for_ack list
            else:
                new_nodes_transmitting.append(node)
            node.time_left -=1
        
        nodes_transmitting[:] = new_nodes_transmitting


def update_Toff(node_list, nodes_to_retransmit):

    lists = [node_list, nodes_to_retransmit]
    for nodes in lists:
        for node in nodes:
            node.Toff +=1
