import numpy as np
from xml.dom import minidom 
from sys import argv
from ase import io 

# read ZVAL from POTCAR
def read_ZVAL(filename = "POTCAR"):
    with open(filename) as f:
        c = f.readlines()
    zval = []
    for i in c:
        if "ZVAL" in i:
            i = i.split()[5]
            zval.append(float(i))
    
    return zval 

# read ACF.dat
def read_ACF(filename="ACF.dat"):
    with open(filename,"r") as f:
        content = f.readlines()
    c = content[2:-4]
    new = []
    for i in c:
        i = i.split()
        i = [float(x) for x in i]
        new.append(i)
    charges = np.array(new)[:,4]
    count = 0 
    total_charge = []
    for i in valence_electron:
        total_charge+=[i]*atom_map[count]
        count += 1 
    return np.subtract(np.array(total_charge),charges)

# read atom num
def atom_read(filename="CONTCAR"):
    atom = io.read(filename)
    atom_list = list(atom.symbols)
    atom_set = set(atom_list)
    dic={}
    for i in atom_list:
        for a in atom_set:
            if i == a:
                if a not in dic:
                    dic[a] = 1
                else:
                    dic[a] += 1
    return atom_set,dic 

# IO
valence_electron = read_ZVAL()
atom_map = list(atom_read()[1].values())
infile = "CONTCAR"
outfile = "CONTCAR.xsd"

print(f"ZVAL = {valence_electron}")
print(f"ATOM = {atom_map}")
print("Please Check!")
# main

# 读取文件  
atom = io.read(infile,format="vasp")
io.write(outfile,images=atom,format="xsd")

# 解析XSD文件
doc =minidom.parse(outfile)
root = doc.documentElement
elements=root.getElementsByTagName("Atom3d")
c=0
charge=read_ACF()
for element in elements:
    element.setAttribute("Charge",f"{charge[c]}")
    c += 1 
# 写出XSD文件
with open(outfile, "w", encoding="utf-8") as f:
    doc.writexml(f, indent='', addindent='\t', newl='\n', encoding="utf-8")

# post-processing
average=[]
c = 0
t = 0 
i=0
all_atom = list(atom.symbols)
for a_c in charge:
    t += a_c
    c += 1 
    if c == atom_map[i]:
        average.append(t/atom_map[i])
        if i+1 == len(atom_map):
            break 
        i += 1 
        c = 0 
        t = 0 
with open("bader_data.csv","w") as f:
    f.write(f"average charge: ")
    for i in range(len(atom_map)):
        f.write(f"{average[i]};")
    f.write("\n")
    for i in range(sum(atom_map)):
        f.write(f"{all_atom[i]},{charge[i]}\n")

print(f"The average charge = {average}")