import biosteam as bst

class RYield(bst.Unit):
    _N_ins = 2
    _N_outs = 1
    _N_heat_utilities = 1
    _F_BM_default = {'Heaters':1}
    _units = {'Area', 'm^2'}
    
    def __init__(self, ID='', ins=None, outs=(), yields=None, *args, **kwargs):
        bst.Unit.__init__(self, ID, ins, outs, bst.settings.get_thermo())
        self._multistream = bst.MultiStream(None, thermo=self.thermo)
        self._multistream.T = self.ins[0].T
        self.yields = yields
        
    def _setup(self):
        self.outs[0].T = self.ins[0].T+5
        vap = self.outs[0]
        vap.phase = 'g'
        
    def _run(self):
        feed = self.ins[0]
        vap = self.outs[0]
        
        ms = self._multistream
        ms.imass['g'] = feed.F_mass*self.yields
        vap.mass[:] = feed.F_mass*self.yields
        vap.T = feed.T+5
        vap.P = feed.P+5
        ms.empty()


    def _design(self):
        # Calculate heat utility requirement (please read docs for HeatUtility objects)
        T_operation = self._multistream.T
        duty = self.H_out - self.H_in
        # if duty < 0:
        #     raise RuntimeError(f'{repr(self)} is cooling.')
        hu = self.heat_utilities[0]
        hu(duty, T_operation)

        # Temperature of utility at entrance
        # T_utility = hu.inlet_utility_stream.T
        T_utility = 298.15

        # Temeperature gradient
        dT = T_utility - T_operation

        # Heat transfer coefficient kJ/(hr*m2*K)
        U = 8176.699

        # Area requirement (m^2)
        # A = duty/(U*dT)
        A = 1

        # Maximum area per unit
        A_max = 743.224

        # Number of units
        N = max([int(A/A_max),1])

        # Design requirements are stored here
        self.design_results['Area'] = A/N
        self.design_results['N'] = N

    def _cost(self):
        A = self.design_results['Area']
        N = self.design_results['N']

        # Long-tube vertical boiler cost correlation from
        # "Product process and design". Warren et. al. (2016) Table 22.32, pg 592
        purchase_cost = N*bst.CE*3.086*A**0.55

        # Itemized purchase costs are stored here
        self.purchase_costs['Pyrolyzer'] = purchase_cost