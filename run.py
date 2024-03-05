import os
import numpy as np
from pyDOE import lhs

# Specify the path to the C++ executable
#path_to_executable = "/global/homes/s/schenke/rcbk/build/bin/rcbk"
path_to_executable = "/global/cfs/cdirs/m1820/rcbk/job_MPI_wrapper.py"

# Number of instances to run
total_runs = runs = 2560
num_instances = 512
num_per_node = 64

# Sample parameter values
# MV: Qs0, gamma
Qs0_range = 2.0  # from 0 to 2
gamma_range = 2.
gamma_offset = 0.5
ec_exp_range = 2.
ec_offset = 1./2.718281828459045
C2_range = 100
C2_offset = 0.1

# Latin hypercube sampling in the parameter space
parameters_lhc = lhs(4, samples=runs, criterion='c') * np.array([Qs0_range, gamma_range, ec_exp_range, C2_range])

# compute ec from ex_exp
parameters_lhc[:,2] = 10.**parameters_lhc[:,2]

# Add any offsets
parameters_lhc[:, 1] += gamma_offset
parameters_lhc[:, 2] += ec_offset
parameters_lhc[:, 3] += C2_offset

# Slurm script template
slurm_script = """#!/bin/bash
#SBATCH --qos debug
#SBATCH -J rcbk-latin
#SBATCH -o rcbkl.%j.out
#SBATCH -e rcbkl.%j.err
#SBATCH -A m1820
#SBATCH -t 00:30:00
#SBATCH --nodes=8
#SBATCH --ntasks={0}
#SBATCH --ntasks-per-node={1}
#SBATCH --constraint=cpu

# Loop to launch instances with different parameters using MPI
""".format(num_instances, num_per_node)

slurm_script += "srun -n {0} python {1} {2} {3}\n".format(num_instances, path_to_executable, total_runs, num_instances)

# Append MPI command to the run script
params = ""

for i in range(runs):
    # Define your command line parameters here
    Qs0, gamma, ec, C2 = parameters_lhc[i]
    
    #params += "-minr 1e-6 -rc BALITSKY -alphas_scaling {0} -output datafile_MV_{1} -fast -maxy 5 -ic MV {2} {3} 0.01 {4}\n".format(C2, i, Qs0, gamma, ec)
    params += "-minr 1e-6 -rc BALITSKY -alphas_scaling {0} -output datafile_GBW_{1} -fast -maxy 5 -ic GBW {2} {3} 0.01\n".format(C2, i, Qs0, gamma)

        
with open("parameters.txt", "w") as run_file:
    run_file.write(params)
        
# Wait for all instances to finish
#slurn_script += "wait\n"

# Save the Slurm script to a file
with open("submit_script.sh", "w") as script_file:
    script_file.write(slurm_script)


print("Slurm script generated: submit_script.sh")
print("Parameter file generated: parameters.txt")
