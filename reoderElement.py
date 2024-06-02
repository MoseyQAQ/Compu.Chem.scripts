from ase.io import read, write
import sys 
import numpy as np 

# read the input file
atom = read(sys.argv[1])
element_list = atom.get_chemical_symbols()
element_order = []
for e in element_list:
    if e not in element_order:
        element_order.append(e)

# new order
new_order = sys.argv[3].split(',')
if len(new_order) != len(element_order):
    raise ValueError('The number of elements in the input file is not equal to the number of elements in the new order')

# reoder the element
index_map = {element: i for i, element in enumerate(new_order)}
sort_indices = np.argsort([index_map[element] for element in element_list])
atom = atom[sort_indices]

# write the new POSCAR
write(sys.argv[2], atom)
