from IPython.display import display, clear_output
from Node_Class import Node
from Gateway_Class import Gateway
from Simulation_Class import Simulation
import Time_on_Air_Calculator as ToA_calc
from Tx_mode_functions import select_nodes_to_transmit, check_collisions, check_uplink_finished, update_Toff
from Rx_mode_functions import check_transmission_success
import matplotlib.pyplot as plt
import numpy as np

# plt.ion()

BW = 125000    # Bandwidth in Hz
SF = 12        # Spreading Factor
preamble = 8   # length of preamble in bytes
payload = 25   # payload in bytes
header = 0     # Header: if enabled --> 0 |  if disabled --> 1
CRC = 1        # if enabled --> 1 | if disabled --> 0 | We enable this only during the uplink slot for error detection 
DE = 1         # when LowDataRateOptimize = 1 -->1 | otherwise --> 0
CR = 1         # Coding Rate: 4/5 --> 1 | 4/6 --> 2 | 4/7 --> 3 | 4/8 --> 4

#Time related parameters
time = 0
RX_delay1 = 1000
min_timeout_for_ack = 1000
max_timeout_for_ack = 3000

#Node_related_parameters
lambd = 1/5000
node_step = int(25600000)
duty_cycle = 0.01

#Lists to store nodes in different states
node_list = []
nodes_to_retransmit = []
nodes_transmitting = []
waiting_for_ack = []

#Lists to store metrics for the plots
S = []
G = []
collision_rate = []
nodes_selected = []
len_node_list = []
len_nodes_transmitting = []
len_waiting_for_ack = []
len_nodes_to_retransmit = []

# Calculate Time on Air, payload duration, and ack duration
ToA = round(ToA_calc.Time_on_Air(BW, SF, preamble, payload, header, CRC, DE, CR))
T_payload = round(ToA_calc.find_payload_no_error_bits(BW, SF, payload, header, CRC, DE, CR))
ack_duration = round(ToA_calc.find_ack_duration(BW, SF, preamble))

#Create Simulation and Gateway instances
sim = Simulation()
gateway = Gateway(ack_duration)


fig, ((ax1, ax2, ax3), (ax4, ax6, ax5)) = plt.subplots(2, 3, figsize=(12, 6))
node_axis = np.linspace(1, sim.node_num, len(S))

line_G, = ax1.plot([], [], label='G', color='blue')
line_S, = ax2.plot([], [], label='S', color='blue')
line_collision_rate, = ax3.plot([], [], label='Collision Rate', color='blue')
line_S_vs_G, = ax4.plot([], [], label='S', color='blue')
line_node_list, = ax5.plot([], [], label='node_list length', color='blue')
line_nodes_transmitting, = ax5.plot([], [], label='nodes_transmitting length', color='red')
line_waiting_for_ack, = ax5.plot([], [], label='waiting_for_ack length', color='green')
line_nodes_to_retransmit, = ax5.plot([], [], label='nodes_to_retransmit length', color='orange')
line_nodes_selected, = ax6.plot([], [], label='Nodes_selected to Transmit', color='blue')

# Add labels and title for each subplot
ax1.set(xlabel='Number of Nodes', ylabel='G', title='Plot of G')
ax2.set(xlabel='Number of Nodes', ylabel='S', title='Plot of S')
ax3.set(xlabel='G', ylabel='Collision_Rate', title='Plot of Collision Rate')
ax4.set(xlabel='G', ylabel='S', title='Plot of S')
ax5.set(xlabel='Number of Nodes', ylabel='Number of Nodes', title='Number of nodes in each list')
ax6.set(xlabel='Nodes existing', ylabel='Nodes selected', title='Nodes selected to transmit')

ax5.legend()

plt.tight_layout()
plt.subplots_adjust(right=0.95)
fig.text(0.63, 0.015, f'SF: {SF}\nlambd: {round(lambd*1000, 4)} pps\nnode step: 1 per {round(node_step/1000)} sec \nsim duration: {time/3600000}hours', fontsize=10, color='black')  # Adjust the position (3, 0.5) and other parameters as needed

#simulation loop that represents duration of 1 msec
while(sim.num_to_transmit * ToA/node_step <= 0.3):
    if(sim.node_num < 1000):                        #Maximum node number allowed is 1000
        if(time % node_step == 1):              #After every node_step interval add one node to the node_array 
            sim.node_num += 1
            node_list.append(Node(sim.node_num, ToA, duty_cycle))
    
    #Calculate the number of nodes about to transmit or retransmit within this msec
    sim.num_to_transmit += select_nodes_to_transmit(time, lambd, ToA, node_list, nodes_transmitting, nodes_to_retransmit)
    
    #Check if any collisions occur from the transmission attempts of this msec 
    check_collisions(gateway, nodes_transmitting)
    
    #check if any transmissions have just finished and if so, set the appropriate nodes to waiting_for_ack state
    check_uplink_finished(time, nodes_transmitting, RX_delay1, min_timeout_for_ack, max_timeout_for_ack, waiting_for_ack)
    
    #Calculate the successful transmission number and the collision number within this msec
    Tx_results = check_transmission_success(time, node_list, nodes_to_retransmit, waiting_for_ack, gateway, ToA, ack_duration)
    
    #Update the metrics from the results of this msec
    sim.update_metrics_per_cycle(Tx_results, gateway)

    if(time% node_step == 1):
        #Every node_step interval, update the metrics for the plots
        sim.update_metrics_per_node_step(node_step, gateway, ToA, G, S, node_list, nodes_to_retransmit, nodes_transmitting, waiting_for_ack, collision_rate, len_node_list, len_nodes_transmitting, len_waiting_for_ack, len_nodes_to_retransmit, nodes_selected, ack_duration)
        
        # # Clear output and redraw the plots
        # clear_output(wait=True)

        # node_axis = np.linspace(1, sim.node_num, len(S))

        # # Plot data on each subplot
        # line_G.set_data(node_axis, G)
        # line_S.set_data(node_axis, S)
        # line_collision_rate.set_data(G, collision_rate)
        # line_S_vs_G.set_data(G, S)
        # line_node_list.set_data(node_axis, len_node_list)
        # line_nodes_transmitting.set_data(node_axis, len_nodes_transmitting)
        # line_waiting_for_ack.set_data(node_axis, len_waiting_for_ack)
        # line_nodes_to_retransmit.set_data(node_axis, len_nodes_to_retransmit)
        # line_nodes_selected.set_data(node_axis, nodes_selected)

        # # Adjust plot limits and redraw
        # for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
        #     ax.relim()
        #     ax.autoscale_view()
        # plt.pause(0.01)
        
        #After plotting the results of node step interval, update the total successful_transmissions, the total collisions and the total number of transmissions 
        sim.update_total_metrics()
        
        #After plotting the results of node step interval, reset the metrics for the next node step interval
        sim.reset_metrics(gateway)
    
    #At the end of every msec, check if the nodes comply with the duty cycle policies and update the time lived for each node
    update_Toff(node_list, nodes_to_retransmit)
    time += 1
# plt.ioff()


node_axis = np.linspace(1, sim.node_num, len(S))

line_G.set_data(node_axis, G)
line_S.set_data(node_axis, S)
line_collision_rate.set_data(G, collision_rate)
line_S_vs_G.set_data(G, S)
line_node_list.set_data(node_axis, len_node_list)
line_nodes_transmitting.set_data(node_axis, len_nodes_transmitting)
line_waiting_for_ack.set_data(node_axis, len_waiting_for_ack)
line_nodes_to_retransmit.set_data(node_axis, len_nodes_to_retransmit)
line_nodes_selected.set_data(node_axis, nodes_selected) 


plt.show()
print(f'Total_successful_transmissions: {sim.total_successful_transmissions}')
print(f'Total_collisions: {sim.total_collisions}')
print(f'Total_num_to_transmit: {sim.total_num_to_transmit}')
print(f'\nnode_num = {sim.node_num}')

fig.text(0.63, 0.015, f'SF: {SF}\nlambd: {round(lambd*1000, 4)} pps\nnode step: 1 per {round(node_step/1000)} sec \nsim duration: {time/3600000}mins', fontsize=10, color='black')  # Adjust the position (3, 0.5) and other parameters as needed