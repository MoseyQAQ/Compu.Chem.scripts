## Settings ##
PLOT = True                            # Whether to visualize data automatically
input_file = "REPORT"                  # The name of the input file. Only the VASP format "REPORT" file is supported.
output_file = "slow-growth.csv"        # The name of the output file
output_img ="slow-growth.png"          # The name of the output image. This option only works when "PLOT = True"
## END Settings ##

x = []
y = []

def intergral(x,y):
    # Only the Eular Method is implemented here
    free_energy = [0]
    for i in range(len(x)-1):
        dx=x[i+1]-x[i]
        free_energy.append(free_energy[-1]+dx*y[i])
    return free_energy

with open(input_file,"r") as f:
    raw_data = f.readlines()

for i in range(len(raw_data)):
    temp = raw_data[i].split()
    if len(temp) == 0:
        continue

    if temp[0] == 'b_m>':
        y.append(float(temp[1]))

    if temp[0] == "cc>":
        x.append(float(temp[2]))
        

free_energy=intergral(x,y)
energy_barrier = max(free_energy)-free_energy[0]

with open(output_file,"w") as f:
    f.write(f"Energy_Barrier,{energy_barrier}.\n")
    f.write(f"CV,lambad,Free_Energy\n")
    for i in range(len(free_energy)):
        f.write(f"{x[i]},{y[i]},{free_energy[i]}\n")
print(f"{len(free_energy)} frames are found.")
print(f"Energy Barrier: {energy_barrier}.\nThe data has been written to the {output_file}.")

if PLOT == True:
    import matplotlib.pyplot as plt
    plt.plot(x,y)
    plt.plot(x,free_energy)
    plt.legend(["Lambda","Free Energy"])
    plt.xlabel("CV")
    plt.ylabel("Lambda / Free Energy (eV)")
    plt.savefig(output_img,dpi=300)
    plt.show()

