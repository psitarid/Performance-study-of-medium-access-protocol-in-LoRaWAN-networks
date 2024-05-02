import numpy as np
import math
import random


def select_nodes_to_transmit(time, node_list, nodes_transmitting, nodes_to_retransmit, lambd):      #Selects new nodes to transmit for the first time from node_list with poisson distribution
    num_to_transmit = -1                                                                              #and also checks whether a node tries to retransmit. It puts all the nodes willing to 
    new_nodes_to_retransmit = []
    nodes_attempted_to_retransmit = 0
    total_nodes_selected = 0
    
    #choose the number of nodes to transmit
    while(num_to_transmit<0 or num_to_transmit>len(node_list)):
        num_to_transmit = np.random.poisson(lambd*len(node_list))
    # num_to_transmit = np.abs(np.random.poisson(lambd * len(node_list)))
    # num_to_transmit = np.clip(num_to_transmit, a_min=0, a_max=1000)  # Ensure positive values
    
    # num_to_transmit = sum(1 for _ in range(len(node_list)) if random.random() < lambd)

    # if(num_to_transmit >0):
        # print('')
    #choose specific nodes to transmit
    for i in range(num_to_transmit):
        i = np.random.choice(node_list)     
        nodes_transmitting.append(i)
        node_list.remove(i)
    #check if any nodes want to retransmit
    if(len(nodes_to_retransmit)>0):
        for j in nodes_to_retransmit:
            if(time == (j.random_back_off)):
                nodes_transmitting.append(j)
                nodes_attempted_to_retransmit+=1
            else:
                new_nodes_to_retransmit.append(j)
        nodes_to_retransmit.clear()
        for i in new_nodes_to_retransmit:
            nodes_to_retransmit.append(i)
    
    total_nodes_selected = num_to_transmit + nodes_attempted_to_retransmit
    
    return total_nodes_selected




def check_collisions(nodes_transmitting, gateway, ack_duration):
        #check if any nodes transmit at the same time, including the gateway, and set them to "collided" or not.   
        if((len(nodes_transmitting)>=1 and gateway.get_state() == 'busy') or len(nodes_transmitting)>1 and gateway.get_state() == 'idle'):
            if(gateway.get_state() == 'busy'):
                gateway.change_node(ack_duration)
            for node in nodes_transmitting:
                if(node.collided == False):
                    node.collided = True
    
def check_uplink_finished(time, nodes_transmitting, RX_delay1, timeout_for_ack, waiting_for_ack):
#check if any node has finished transmitting. If anyone does, transfer them to the waiting_for_ack list
    new_nodes_transmitting = []
    if(len(nodes_transmitting)>0):
        for node in nodes_transmitting:
            if(node.time_left ==0):                                                 #check if nodes finished transmitting.
                waiting_for_ack.append(node)                                        #transfer the finished nodes to waiting_for_ack list. 
                node.RX_delay1_ends = time + RX_delay1
                node.timeout_ends = time + RX_delay1 + timeout_for_ack
            else:
                new_nodes_transmitting.append(node)
        nodes_transmitting.clear()
        for node in new_nodes_transmitting:
            node.time_left -= 1
            nodes_transmitting.append(node)




                    
                    

                
                












        





    
    
    
    
    
    
    
    
    