from DependentPropertyValidator import DependentPropertyValidator
DPV = DependentPropertyValidator()
DPV.add_property_dependency([str, str])
test = DPV.validate('ff', 'dfd')
