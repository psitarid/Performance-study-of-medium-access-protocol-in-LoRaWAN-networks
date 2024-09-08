import numpy as np

class Node:
    id = 0                                  #The ID of each Node
    time_lived = 0                          #The time that a node has existed in the network
    time_left = 0                           #The time left for transmission when a node is in transmitting state
    random_back_off = 0                     #The random time interval before a node retransmits after a collision
    retransmission_time =0                  #The time that a node will retransmit after a collision
    retransmission_num = 0                  #The number of retransmissions for each self. Should be less that 40         
    RX_delay1_ends = 0                      #The moment of time when the RX delay ends and the waiting-for-ack state begins
    timeout_ends = 0                        #The moment of time when the timeout for ack waiting is over. 
    collided = False
    ack_received = False
    timeout_for_ack = 0
    duty_cycle = 0.01



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

    
    def set_backoff_interval(self, ToA, time):     #Sets the back-off interval of a node randomly chosen while complying with duty cycle constraints 
        if (self.time_lived <= 3600000):
            self.duty_cycle = 0.01
        elif(self.time_lived >3600 and self.time_lived <= 36000000):
            self.duty_cycle = 0.01
        elif(self.time_lived >36000000):
            self.duty_cycle = 0.01
        # max_back_off = int((ToA/self.duty_cycle)-ToA)
        # max_back_off  = int(self.random_back_off +0.4 * self.random_back_off)
        # if max_back_off == 1:
        #     max_back_off +=1
        choice = 0
        # if(self.retransmission_num >= 15):
            # self.random_back_off = np.random.randint(ToA *( 1/self.duty_cycle - 1), ToA *( 1/self.duty_cycle - 1) + 2000)
        
        while(choice<1):
            choice =  int(np.random.poisson(5000))
            # self.random_back_off = int(np.random.normal(ToA *( 1/self.duty_cycle - 1), 1 ,size= None))
            # self.random_back_off = np.random.randint(1, 8700)
        self.random_back_off = choice   
        self.retransmission_time = time + self.random_back_off


    def set_retransmitting_state(self, time, ToA, init_T_retransmission):
        self.time_left = ToA
        self.retransmission_num += 1
        # self.random_back_off = time + np.random.randint(1, (2**(self.retransmission_num)-1)) #set random back-off time for retransmission, based on the exponential back-off algorithm
        # self.random_back_off = time + np.random.randint(1, self.retransmission_num * 500)
        self.set_backoff_interval(ToA, time)
        self.RX_delay1_ends = 0
        self.timeout_ends = 0
        self.collided = False
        self.ack_received = False
        self.timeout_for_ack = 0


    
    

