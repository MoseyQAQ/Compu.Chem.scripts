from ase.io import read
import numpy as np 
import sys 

# define the function read the BEC
def read_bec(file: str, bec: dict, chem_sym: list):

    # read the file
    with open(file,'r') as f:
        # find the BEC
        while True:
            if 'BORN EFFECTIVE CHARGES' in f.readline():
                break
        f.readline()
        # read the BEC
        for chem in chem_sym:
            f.readline()

            # read the BEC of an atom
            bec_atom = []
            for i in range(3):
                bec_atom.append([float(i) for i in f.readline().split()[1:]])
            bec_atom = np.array(bec_atom)
            bec[chem].append(bec_atom)
        
        # calculate the average BEC and standard deviation
        bec_mean, bec_std = {}, {}
        for chem in bec.keys():
            bec_mean[chem] = np.mean(bec[chem],axis=0)
            bec_std[chem] = np.std(bec[chem],axis=0)
    
    return bec_mean, bec_std

# define parameters
inputfile = sys.argv[1]
outputfile = sys.argv[2]

# read and get info.
atom = read(inputfile,format='vasp-out')
bec = {i: [] for i in set(atom.get_chemical_symbols())}
bec_mean, bec_std = read_bec(inputfile,bec,atom.get_chemical_symbols())
for chem in bec_mean.keys():
    print(f'Chemical symbol:\n {chem}')
    print(f'Mean BEC:\n {bec_mean[chem]}')
    print(f'Standard deviation:\n {bec_std[chem]}')

# write the BEC to a file
with open(outputfile,'w') as f:
    for chem in bec_mean.keys():
        f.write(f'{chem}\n')
        f.write(f'{bec_mean[chem][0,0], bec_mean[chem][1,1], bec_mean[chem][2,2]}\n')

