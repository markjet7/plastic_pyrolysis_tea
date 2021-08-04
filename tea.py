import biosteam as bst

class PyrolysisTEA(bst.TEA):
    """
    Create a TEA object for techno-economic analysis of a biorefinery.
    """

    __slots__ = ('labor_cost', 'fringe_benefits', 'maintenance',
                 'property_tax', 'property_insurance', '_FCI_cached',
                 'supplies', 'maintanance', 'administration')

    def __init__(self, system, IRR, duration, depreciation, income_tax,
                 operating_days, lang_factor, construction_schedule, WC_over_FCI,
                 labor_cost, fringe_benefits, property_tax,
                 property_insurance, supplies, maintenance, administration):
        super().__init__(system, IRR, duration, depreciation, income_tax,
                         operating_days, lang_factor, construction_schedule,
                         startup_months=0, startup_FOCfrac=0, startup_VOCfrac=0,
                         startup_salesfrac=0, finance_interest=0, finance_years=0,
                         finance_fraction=0, WC_over_FCI=WC_over_FCI)
        self.labor_cost = labor_cost
        self.fringe_benefits = fringe_benefits
        self.property_tax = property_tax
        self.property_insurance = property_insurance
        self.supplies= supplies
        self.maintenance = maintenance
        self.administration = administration

    def _other_supplies(self):
        other = {
            "Cooling Tower Chemicals": 33.85*4627*200/2000,
            "Catalyst": 0 # 9.75*344*8400*200/2000
        }

    def _DPI(self, installed_equipment_cost):
        installed_equipment_cost = {"Waste separation": 6.326732190701745e7, "Ex-Situ pyrolysis": 8.581839843306549e6, "Product recovery": 551086.0909225765, "Product separation": 3.2710061041138573e6, "Utilities": 2.0486561379415173e7, "Off-site": 5.422913306315782e6}
        return sum(installed_equipment_cost.values())
        # return installed_equipment_cost

    def _TDC(self, DPI):
        return DPI

    def _FCI(self, TDC):
        self._FCI_cached = TDC
        return TDC

    def _FOC(self, FCI):
        # for f in [self.labor_cost, self.fringe_benefits, self.property_tax, self.property_insurance, self.supplies, self.maintenance, self.administration]:
        #     print(f)
        # return (FCI*(self.property_tax + self.property_insurance + self.maintenance + self.administration)
                # + self.labor_cost*(1+self.fringe_benefits+self.supplies) + self._other_supplies)
        return (FCI*(self.property_tax + self.maintenance + self.administration)
                + self.labor_cost*(1+self.fringe_benefits+self.supplies) )