# import matplotlib.pyplot as plt
# from IPython.display import clear_output, display
# import numpy as np

# def initialize_plots(SF, lambd, node_step, time, fig, ax1, ax2, ax3, ax4, ax5, ax6):

#     # Add labels and title for each subplot
#     ax1.set(xlabel='Number of Nodes', ylabel='G', title='Plot of G')
#     ax2.set(xlabel='Number of Nodes', ylabel='S', title='Plot of S')
#     ax3.set(xlabel='G', ylabel='Collision_Rate', title='Plot of Collision Rate')
#     ax4.set(xlabel='G', ylabel='S', title='Plot of S')
#     ax5.set(xlabel='Number of Nodes', ylabel='Number of Nodes', title='Number of nodes in each list')
#     ax6.set(xlabel='Nodes existing', ylabel='Nodes selected', title='Nodes selected to transmit')

#     plt.tight_layout()
#     plt.subplots_adjust(right=0.95)
#     fig.text(0.63, 0.015, f'SF: {SF}\nlambd: {round(lambd*1000, 4)} pps\nnode step: 1 per {round(node_step/1000)} sec \nsim duration: {time/3600000}hours', fontsize=10, color='black')  # Adjust the position (3, 0.5) and other parameters as needed
#     ax5.legend()

# def update_plots(node_num, S, G, collision_rate, len_node_list, len_nodes_transmitting, len_waiting_for_ack, len_nodes_to_retransmit, nodes_selected, ax1, ax2, ax3, ax4, ax5, ax6, fig):

#     # Create x-axis for number of nodes
#     node_axis = np.linspace(1, node_num, len(S))
#     # Clear output and redraw the plots
#     clear_output(wait=True)
#     # Clear axes for updating
#     for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
#         ax.clear()

#     # Plot data on each subplot
#     ax1.plot(node_axis, G, label='G', color='blue')
#     ax2.plot(node_axis, S, label='S', color='blue')
#     ax3.plot(G, collision_rate, label='Collision Rate', color='blue')
#     ax4.plot(G, S, label='S', color='blue')
#     ax5.plot(node_axis, len_node_list, label='node_list length', color='blue')
#     ax5.plot(node_axis, len_nodes_transmitting, label='nodes_transmitting length', color='red')
#     ax5.plot(node_axis, len_waiting_for_ack, label='waiting_for_ack length', color='green')
#     ax5.plot(node_axis, len_nodes_to_retransmit, label='nodes_to_retransmit length', color='orange')
#     ax6.plot(node_axis, nodes_selected, label='Nodes_selected to Transmit', color='blue')
    
#     # Add labels and title for each subplot
#     ax1.set(xlabel='Number of Nodes', ylabel='G', title='Plot of G')
#     ax2.set(xlabel='Number of Nodes', ylabel='S', title='Plot of S')
#     ax3.set(xlabel='G', ylabel='Collision_Rate', title='Plot of Collision Rate')
#     ax4.set(xlabel='G', ylabel='S', title='Plot of S')
#     ax5.set(xlabel='Number of Nodes', ylabel='Number of Nodes', title='Number of nodes in each list')
#     ax6.set(xlabel='Nodes existing', ylabel='Nodes selected', title='Nodes selected to transmit')

#     ax1.legend()
#     ax2.legend()
#     ax3.legend()
#     ax4.legend()
#     ax5.legend()
#     ax6.legend()

#     plt.tight_layout()
#     plt.subplots_adjust(right=0.95)
#     # fig.text(0.63, 0.015, f'SF: {SF}\nlambd: {round(lambd*1000, 4)} pps\nnode step: 1 per {round(node_step/1000)} sec \nsim duration: {time/3600000} hours', fontsize=10, color='black')
    
#     display(fig)