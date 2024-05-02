import numpy as np

class Node:
    id = 0                                  #The ID of each Node
    time_left = 0                           #The time left for transmission when a node is in transmitting state
    random_back_off = 0                     #The random time interval before a node retransmits after a collision
    retransmission_num = 0                  #The number of retransmissions for each self. Should be less that 40         
    RX_delay1_ends = 0                      #The moment of time when the RX delay ends and the waiting-for-ack state begins
    timeout_ends = 0                        #The moment of time when the timeout for ack waiting is over. 
    collided = False
    ack_received = False



    def __init__(self, node_ID, ΤοΑ):       #Node instance constructor
        self.id = node_ID
        self.time_left = ΤοΑ
        self.retransmission_num = 0
        self.RX1_delay1_ends = 0
        self.timeout_ends = 0
        self.collided = False
        self.ack_received = False

    def set_initial_state(self, ToA):
        self.time_left = ToA
        self.random_back_off = 0
        self.retransmission_num = 0
        self.RX_delay1_ends = 0
        self.timeout_ends = 0
        self.collided = False
        self.ack_received = False

    def set_retransmitting_state(self, time, ToA, T_retransmission):
        self.time_left = ToA
        self.random_back_off = time + np.random.randint(1, T_retransmission)
        self.RX_delay1_ends = 0
        self.timeout_ends = 0
        self.collided = False
        self.ack_received = False

