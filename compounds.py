import biosteam as bst

def define_chemical_phase(chemical, phase, **constants):
    c = bst.Chemical(chemical)
    c.at_state(phase=phase)
    return c

# %% Define common chemicals
# PET = "PubChem=8441"
# PP = "PubChem=76958"
# PE = "CAS=9002-88-4"
# Carbon = "PubChem=5462310"
# Aluminum = "PubChem=5359268"
# Heptene = "PubChem=11610"
customChemicals = {
    "PET":"C10H10O4",
    "PP" : "C22H42O3",
    "PE" : "C2H4",
    "Carbon" : "C",
    "Al" : "Al"
}

# Gases
(CH4, CO2, O2) = [ define_chemical_phase(c, 'g')
    for c in ["CH4", 'CO2',  'O2']]

# Fluids
(Heptane, Benzene, Heptene, H2O) = [ c
    for c in bst.Chemicals(['Heptane', 'Benzene', "C7H14", "Water"])]

# Solids
(PET, PP, PE, Char, Al) = [define_chemical_phase(c, 's') 
    for c in customChemicals.values()]

# Use the PE model for the PP saturation pressure model
[PP.Psat.add_model(p) for p in PE.Psat] 

chemicals = bst.Chemicals([CH4, H2O, CO2, O2, PET, PP, PE, Char, Al, Benzene, Heptane, Heptene], cache=True)
for chemical in chemicals:
    chemical.default()

chemicals.compile()
for (k,v) in customChemicals.items():
    chemicals.set_synonym(v, k)

chemicals.set_synonym("C7H14", "Heptene")
bst.settings.set_thermo(chemicals, cache=True)