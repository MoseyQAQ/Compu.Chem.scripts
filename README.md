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

---
## 2. bader_new.py
> Description: A script for exporting the result of bader chage analysis (ACF.dat) to a .xsd file. This script is based on ASE package.

Required input files:
* CONTCAR
* POTCAR
* ACF.dat

### Usage:
```bash
> python3 bader_new.py 
ZVAL = [X, X, X]
ATOM = [Y, Y, Y]
Please Check!
The average charge = [Z, Z, Z]
```
The charge information obtained from Bader analysis will be written to a Materials Studio (.xsd) file automatically. Meanwhile, a "bader_data.csv" will be generated, which contains the charge information of each atom and the average charge of each element.

__A detailed tutorial of this script may be found in: [http://www.aleeqaq.cc/posts/2023/blog-6](http://www.aleeqaq.cc/posts/2023/blog-6)__

-- -

## 3. slow-growth.py
> Description: Analyzer for slow-growth data generated by VASP.
### Example:
```bash
> ls 
REPORT
> python3 slow-growth.py
3910 frames are found.
Energy Barrier: 1.5107054134975018 eV.
The data has been written to the slow-growth.csv.
> ls 
slow-growth.csv
```
You can open this script in any text editor and modify it.

Options in this script:
* PLOT = True   (Whether to visualize data automatically, matplotlib is used.)
* input_file = "REPORT" (The name of the input file. Only the VASP format "REPORT" file is supported)
* output_file = "slow-growth.csv"  (The name of the output file)
* output_img ="slow-growth.png"    (The name of the output image. This option only works when "PLOT = True")
  
-- -

## 4. parsedpgen.py
> Description: For parsing the log file of the dpgen (dpgen.log), and visualize the data.
