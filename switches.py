class switch():
    
    def __init__(self, qsfp = 0, sfpp = 0):
        self.qsfp_count, self.sfpp_count = qsfp, sfpp
        self.qsfp_out_rate, self.qsfp_out = 0, 0
        self.sfpp_out_rate, self.sfpp_out = 0, 0
        
    def in_proc(self, qsfp = [], sfpp = []):
        self.qsfp_in = qsfp
        self.sfpp_in = sfpp
        
    def qsfp_out_proc(self, qsfp):
        self.qsfp_out_rate = (sum(self.sfpp_in) + sum(self.qsfp_in))/qsfp if qsfp != 0 else 0
        self.qsfp_out = qsfp
        return self.qsfp_out_rate, self.qsfp_out
    
    def sfpp_out_proc(self, sfpp):
        self.sfpp_out_rate = (sum(self.sfpp_in) + sum(self.qsfp_in))/sfpp if sfpp != 0 else 0
        self.sfpp_out = sfpp
        return self.sfpp_out_rate, self.sfpp_out
    
    def show(self):
        return (sum(self.sfpp_in) + sum(self.qsfp_in),
                self.qsfp_out_rate,
                self.qsfp_out,
                self.sfpp_out_rate,
                self.sfpp_out)

def create_topology(in_rate = 100,
                   boarder_spine_count = 1,
                   spine_count = 1,
                   leaf_count = 1):
    # Split trafic by 4 interfaces
    server_count = 10
    x = in_rate/4
    
    #Create boarder-spine switches
    Boarder_Spines = {}
    for i in range(boarder_spine_count):
        Boarder_Spines['bs_{0}'.format(i+1)] = switch(qsfp = 32)
        if i == 0:
            Boarder_Spines['bs_{0}'.format(i+1)].in_proc(qsfp = [x,x,x,x])
        else:
            Boarder_Spines['bs_{0}'.format(i+1)].in_proc()

    # Create spine switches
    Spines = {}
    for i in range(spine_count):
        Spines['sp_{0}'.format(i+1)] = switch(qsfp = 32)
        Spines['sp_{0}'.format(i+1)].in_proc([j.qsfp_out_proc(spine_count)[0] for j in Boarder_Spines.values()])
        
    # Create leaf switches
    Leafs = {}
    for i in range(leaf_count):
        Leafs['le_{0}'.format(i+1)] = switch(qsfp = 4, sfpp = 48)
        Leafs['le_{0}'.format(i+1)].in_proc([j.qsfp_out_proc(leaf_count)[0] for j in Spines.values()])
    
    # Return results 
    return (Boarder_Spines['bs_1'].qsfp_out_proc(spine_count)[0],
            Spines['sp_1'].qsfp_out_proc(leaf_count)[0],
            Leafs['le_1'].sfpp_out_proc(server_count)[0])
