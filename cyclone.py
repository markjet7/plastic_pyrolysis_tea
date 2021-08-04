import biosteam as bst

class Cyclone(bst.Unit):
    _N_ins = 1
    _N_outs = 2
    _N_heat_utilities = 0
    _BM = {'Heaters':1}
    _units = {'Area', 'm^2'}
    
    def __init__(self, ID='', ins=None, outs=(), efficiency=0.99, *args, **kwargs):
        bst.Unit.__init__(self, ID, ins, outs, bst.settings.get_thermo())
        self._multistream = bst.MultiStream(None, thermo=self.thermo, phases=['g', 'l', 's'])
        self.efficiency = efficiency
        self.T = self.ins[0].T
        self.P = self.ins[0].P
        self._BM = {'Heaters':1}
        
    def _setup(self):
        vap, sol = self.outs
        vap.phase = 'g'
        sol.phase = 's'
        
    def _run(self):
        feed = self.ins[0]
        vap = self.outs[0]
        sol = self.outs[1]
        
        ms = self._multistream
        ms.imol['g'] = feed.mol
        for k in ms.available_chemicals:
            if k.get_phase(T=feed.T, P=feed.P) == 's':
                sol.imol[ str(k)] = ms.imol['g', str(k)]*self.efficiency
                vap.imol[ str(k)] = ms.imol['g',  str(k)]*(1-self.efficiency)
            else:
                vap.imol[ str(k)] = ms.imol['g',  str(k)]

#         vap.mol[:] = ms.imol['l']
#         sol.mol[:] = ms.imol['s']
        
        vap.T = self.T
        vap.P = self.P
        
        sol.T = self.T
        sol.P = self.P
        
        ms.empty()

    def _design(self):

        # Design requirements are stored here
        self.design_results['Area'] = 0
        self.design_results['N'] = 0

    def _cost(self):
        # Design requirements are stored here
        self.design_results['Area'] = 0
        self.design_results['N'] = 0

        # Itemized purchase costs are stored here
        self.purchase_costs['Cyclone'] = 0