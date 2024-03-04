#!/usr/bin/env python3

from mpi4py import MPI
from subprocess import call
import sys

def get_parameters_from_file(filename, rank):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Ensure the file has enough lines
    if rank < len(lines):
        return lines[rank].strip()
    else:
        return None

def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    # Specify the offset parameter (default to 0 if not provided)
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else size
    runs_per_round = int(sys.argv[2]) if len(sys.argv) > 2 else size

    print("size, rank, total = {0}, {1}, {2}".format(size, rank, runs))

    adjusted_rank = rank

    # Specify the file containing the parameters for each rank
    parameters_file = "parameters.txt"

    for i in range (int(runs/runs_per_round)):
        # Get the parameters for the current rank from the file
        parameters_for_rank = get_parameters_from_file(parameters_file, adjusted_rank)

        if parameters_for_rank is not None:    
            runstring = f"/global/homes/s/schenke/rcbk/build/bin/rcbk {parameters_for_rank}"
            print(runstring)

            call(runstring, shell=True)

        else:
            print(f"Error: Not enough lines in {parameters_file} for rank {adjusted_rank}")
        # Adjust rank based on the offset
        adjusted_rank = adjusted_rank + size
            
if __name__ == "__main__":
    main()


    

# #!/usr/bin/env python3

# from mpi4py import MPI
# from subprocess import call

# def get_parameters_from_file(filename, rank):
#     with open(filename, 'r') as file:
#         lines = file.readlines()

#     # Ensure the file has enough lines
#     if rank < len(lines):
#         return lines[rank].strip()
#     else:
#         return None

# comm = MPI.COMM_WORLD
# size = comm.Get_size()
# rank = comm.Get_rank()

# print("size, rank = {0}, {1}".format(size, rank))

# # Specify the file containing the parameters for each rank
# parameters_file = "parameters.txt"

# # Get the parameters for the current rank from the file
# parameters_for_rank = get_parameters_from_file(parameters_file, rank)

# if parameters_for_rank is not None:
#     # Run the "rcbk" program for each rank with different parameters
#     runstring = f"/global/homes/s/schenke/rcbk/build/bin/rcbk {parameters_for_rank}"
#     print(runstring)

#     call(runstring, shell=True)
# else:
#     print(f"Error: Not enough lines in {parameters_file} for rank {rank}")




# #!/usr/bin/env python3

# from mpi4py import MPI
# from subprocess import call

# comm = MPI.COMM_WORLD
# size = comm.Get_size()
# rank = comm.Get_rank()

# print("size, rank = {0}, {1}".format(size, rank))

# # Run the program for each rank
# runstring = "bash run_{0}.sh".format(rank)
# print(runstring)

# call(runstring, shell=True)
