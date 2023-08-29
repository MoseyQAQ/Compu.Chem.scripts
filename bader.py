import numpy as np
from xml.dom import minidom 
from sys import argv
from ase import io 

# I/O
valence_electron=[6,3]
atom_map = [18,12]
infile="CONTCAR"
outfile="CONTCAR.xsd"

# 读取bader结果
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