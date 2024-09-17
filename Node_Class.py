import numpy as np
from numba import njit
class Node:
    id = 0                                  #The ID of each Node
    time_lived = 0                          #The time that a node has existed in the network
    time_left = 0                           #The time left for transmission when a node is in transmitting state
    random_back_off = 0                     #The random time interval before a node retransmits after a collision
    retransmission_time = 0                 #The time that a node will retransmit after a collision
    retransmission_num = 0                  #The number of retransmissions for each self. Should be less that 40         
    RX_delay1_ends = 0                      #The moment of time when the RX delay ends and the waiting-for-ack state begins
    timeout_ends = 0                        #The moment of time when the timeout for ack waiting is over. 
    collided = False
    ack_received = False
    timeout_for_ack = 0
    duty_cycle = 0.01
    time_transmitted = 0
    allowed_transmission_time = 36000


    
    def __init__(self, node_ID, ToA):       #Node instance constructor
        self.id = node_ID
        self.time_left = ToA
        self.retransmission_num = 0
        self.RX1_delay1_ends = 0
        self.timeout_ends = 0
        self.collided = False
        self.ack_received = False
        self.timeout_for_ack = 0
        self.time_lived = 0
        self.duty_cycle = 0.01
        self.random_back_off = 5000
        self.retransmission_time = 0
        self.time_transmitted = 0
        self.allowed_transmission_time = 36000
    
    def set_initial_state(self, ToA):
        self.time_left = ToA
        self.random_back_off = 5000
        self.retransmission_num = 0
        self.RX_delay1_ends = 0
        self.timeout_ends = 0
        self.collided = False
        self.ack_received = False
        self.timeout_for_ack = 0
        self.retransmission_time = 0
        self.time_transmitted = 0
        self.allowed_transmission_time = 36000
        self.time_lived = 0

    
    def set_retransmitting_state(self, time, ToA):
        self.time_left = ToA
        self.retransmission_num += 1
        self.random_back_off = int(np.random.randint(8700))
        self.retransmission_time = time + self.random_back_off
        self.RX_delay1_ends = 0
        self.timeout_ends = 0
        self.collided = False
        self.ack_received = False
        self.timeout_for_ack = 0
    

