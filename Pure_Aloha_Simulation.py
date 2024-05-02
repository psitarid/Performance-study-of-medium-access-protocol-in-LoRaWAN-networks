from Node_Class import Node
from Gateway_Class import Gateway
import Time_on_Air_Calculator as ToA_calc
from Tx_mode_functions import select_nodes_to_transmit, check_collisions, check_uplink_finished
from Rx_mode_functions import check_transmission_success
import matplotlib.pyplot as plt
import numpy as np
import math

BW = 125000    # Bandwidth in Hz
SF = 12        # Spreading Factor
preamble = 6   # length of preamble in bytes
payload = 25   # payload in bytes
header = 0     # Header: if enabled --> 0 |  if disabled --> 1
CRC = 1        # if enabled --> 1 | if disabled --> 0 | We enable this only during the uplink slot for error detection 
DE = 0         # when LowDataRateOptimize = 1 -->1 | otherwise --> 0
CR = 1         # Coding Rate: 4/5 --> 1 | 4/6 --> 2 | 4/7 --> 3 | 4/8 --> 4

ToA = round(ToA_calc.Time_on_Air(BW, SF, preamble, payload, header, CRC, DE, CR))  # Find the Time on Air based on the parameters
# ToA = 5
ack_duration = 530
# ack_duration = 2                                                                 # Duration of Gateway's acknowledgement transmission(530msec)
RX_delay1 = 1000
# RX_delay1 = 4                                                            # Duration of RX1 delay (1sec)
# T_node = ToA + ack_duration + RX_delay1                                            # Total time of a node's transmission including the RX delay and the acknowledgment
timeout_for_ack = 3000
# timeout_for_ack = 12                                                     # Maximum time waiting for acknowledgment to be received
T_retransmission = 36000
# T_retransmission = 144

time = 1                                                                   # Represents the time passed from the beggining of the simulation in msecs. Changes in the end of every cycle
node_num = 0                                                                # Holds the number of total nodes in the system. It increases based on the node_counter.
node_counter = 0                                                            # Counts cycles until the increasing of each node 
sim_duration =7200000
# sim_duration = 1000                                                       # Simulation duration in msecs
lambd = 1/20000 
# lambd = 1/5
node_step = 200000
# node_step = 3
k = round(node_step)

node_list = []                                                              #Holds the nodes that initiate new transmissions                                                      #Holds the nodes that chose to transmit, or retransmit
nodes_to_retransmit = []                                                    #Holds the nodes that will retransmit at a random moment of time
nodes_transmitting = []                                                     #Holds the node currently transmitting                                                       #Stores the collisions that occur in each cycle
waiting_for_ack = []                                                        #Holds the nodes that are in the waiting_for_ack state    
#---------------------------------------------------------------------------------------------------------------------------------------------
nodes_selected = []
len_node_list = []
len_nodes_transmitting = []
len_waiting_for_ack = []
len_nodes_to_retransmit = []
nodes_for_plots = []
#---------------------------------------------------------------------------------------------------------------------------------------------
S = []                                                                       #The throughput of the channel                                                                 #Holds the throughput of the channel for a single cycle
G = []                                                                       #The total traffic load of the channel                                                                 #Holds the total traffic load of the channel for each cycle
collision_rate = []

num_to_transmit = 0
successful_transmissions = 0                                                                  #Holds the collision probabillity for each cycle.
total_successful_transmissions = 0
total_num_to_transmit = 0
collisions = 0
total_collisions = 0

gateway = Gateway(ack_duration)

# while(time < sim_duration):
while(time < sim_duration and (num_to_transmit * ToA/node_step < 2)):
    # print(f'\ncycle: {time}')
    if(node_num < 1000):
        if(time%node_step == 1):                                           #increase the number of nodes every 20 msec until node number is equal to 1000.
            node_num += 1                       
            node_list.append(Node(node_num, ToA))

    
    num_to_transmit += select_nodes_to_transmit(time, node_list, nodes_transmitting, nodes_to_retransmit, lambd)

<<<<<<< HEAD
    check_collisions(nodes_transmitting, gateway, ack_duration)
=======
    collisions_with_ack = check_collisions(nodes_transmitting, gateway, ack_duration)
>>>>>>> f024348b50d3669833f469bb85e47900c46ef58f

    check_uplink_finished(time, nodes_transmitting, RX_delay1, timeout_for_ack, waiting_for_ack)

    results_by_cycle = check_transmission_success(time, gateway, waiting_for_ack, node_list, nodes_to_retransmit, ToA, T_retransmission, ack_duration)
    
    if(results_by_cycle == 1):
<<<<<<< HEAD
        successful_transmissions += 1
=======
        successful_transmissions += 2
>>>>>>> f024348b50d3669833f469bb85e47900c46ef58f
    elif(results_by_cycle == -1):
        collisions +=1
    

    if(time%node_step == 1):
<<<<<<< HEAD
        
        num_to_transmit = collisions + successful_transmissions
=======
        collisions += collisions_with_ack
        num_to_transmit = collisions + successful_transmissions + gateway.num_to_transmit
>>>>>>> f024348b50d3669833f469bb85e47900c46ef58f
        nodes_selected.append(num_to_transmit)
        
        G.append(num_to_transmit * ToA/node_step)
        S.append(ToA * successful_transmissions/node_step)
        

        if(total_num_to_transmit > 0):
            collision_rate.append(collisions/num_to_transmit)
        else:
            collision_rate.append(0)
        

        len_node_list.append(len(node_list))
        len_nodes_transmitting.append(len(nodes_transmitting))
        len_waiting_for_ack.append(len(waiting_for_ack))
        len_nodes_to_retransmit.append(len(nodes_to_retransmit))

        total_successful_transmissions += successful_transmissions
        total_collisions += collisions
        total_num_to_transmit += num_to_transmit
        num_to_transmit = 0
        successful_transmissions = 0
        collisions = 0
<<<<<<< HEAD
=======
        gateway.num_to_transmit = 0
        collisions_with_ack = 0
>>>>>>> f024348b50d3669833f469bb85e47900c46ef58f
    
    time += 1
        

print(f'Total_successful_transmissions: {total_successful_transmissions}')
print(f'Total_collisions: {total_collisions}')
print(f'Total_num_to_transmit: {total_num_to_transmit}')
print(f'\nnode_num = {node_num}')



# Create a figure and a grid of 2x1 subplots
fig, ((ax1, ax2, ax3), (ax4, ax6, ax5)) = plt.subplots(2, 3, figsize=(12, 6))
node_axis = np.linspace(1, node_num, len(S))


# Plot data on each subplot
ax1.plot(node_axis, G)
ax1.scatter(node_axis, G)
ax2.plot(node_axis, S)
ax2.scatter(node_axis, S)
ax3.plot(node_axis, collision_rate)
ax3.scatter(node_axis, collision_rate)
ax4.plot(G, S)
ax4.scatter(G, S)
ax5.plot(node_axis, len_node_list, label='node_list length')
ax5.plot(node_axis, len_nodes_transmitting, label='nodes_transmitting length')
ax5.plot(node_axis, len_waiting_for_ack, label='waiting_for_ack length')
ax5.plot(node_axis, len_nodes_to_retransmit, label='nodes_to_retransmit length')
ax6.plot(node_axis, nodes_selected)
ax6.scatter(node_axis, nodes_selected)


ax1.set(xlabel='Number of Nodes', ylabel='G', title='Plot of G')
ax2.set(xlabel='Number of Nodes', ylabel='S', title='Plot of S')
ax3.set(xlabel='Number of Nodes', ylabel='Collision_Rate', title='Plot of Collision Rate')
ax4.set(xlabel='G', ylabel='S', title='Plot of S')
ax5.set(xlabel='Number of Nodes', ylabel='Number of Nodes', title='Number of nodes in each list')
ax6.set(xlabel='Number of Nodes Selected', ylabel='Nodes selected to transmit', title='Number of Nodes Existing')

ax5.legend()

plt.tight_layout()
plt.subplots_adjust(right=0.95)

fig.text(0.63, 0.015, f'SF: {SF}\nlambd: {round(lambd*1000, 4)} pps\nnode step: 1 per {round(node_step/1000)} sec \nsim duration: {sim_duration/60000}mins', fontsize=10, color='black')  # Adjust the position (3, 0.5) and other parameters as needed
<<<<<<< HEAD

plt.show()













=======
>>>>>>> f024348b50d3669833f469bb85e47900c46ef58f

plt.show()