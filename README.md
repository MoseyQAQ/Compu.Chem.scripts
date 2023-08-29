# Useful scripts in VASP
> Please contact me if you have any problem.
> Email: admin@aleeqaq.cc

## 1. nebgen.py
> Description: A initial strcture generator for the NEB calculations. Both LST and IDPP method are supported. This script is based on ASE package.

### Usage:
```bash
python3 nebgen.py -i init_structure_file end_structure_file -m IDPP -n 4
```
Options:
* -i: specify 2 structures
* -m: specify the method used, 'IDPP' and 'Li' are supported.
* -n: number of structures being generated.

### 2. bader.py
> Description: A script for export the result of bader chage analysis (ACF.dat) to a .xsd file. This script is based on ASE package.

### Usage:
```bash
python3 bader.py 
```
__A detailed tutorial of this script may be found in: [https://github.com/MoseyQAQ/Compu.Chem.scripts/tree/main](https://github.com/MoseyQAQ/Compu.Chem.scripts/tree/main)__