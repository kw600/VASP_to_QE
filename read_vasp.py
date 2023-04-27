import ase
from ase.calculators.espresso import Espresso
from ase.io import read, write

import os, sys

def vasp_to_qe(path):
	os.chdir(path)
	atoms = read('POSCAR')

	pseudos = {"Pb": "Pb.upf",
			"Te": "Te.upf",
			"Si": "Si.upf"}

	# Now we define the parameters for the espresso calculations
	input_params = {"calculation" : "scf", # The type of calculation
				"ecutwfc" : 60, # The plane-wave wave-function cutoff
				"ecutrho": 240, # The density wave-function cutoff,
				"conv_thr": 1e-6, # The convergence for the DFT self-consistency
				"tprnfor" : True, # Print the forces
				"tstress" : True, # Print the stress tensor
				"pseudo_dir" : "/work/e89/e89/kw2318/pseudo_espresso"
				}

	kpoints = (4,4,4) # The k-points mesh
	atoms.write('Si.pwi',input_data=input_params,pseudopotentials=pseudos,format='espresso-in',kpts=kpoints)

def sub():
	input='''#!/bin/bash
# Slurm job options (job-name, compute nodes, job time)
#SBATCH --nodes=4
#SBATCH --tasks-per-node=128
#SBATCH --job-name=qscaild
#SBATCH --account=e89-ic_m
#SBATCH --partition=standard
#SBATCH --qos=taskfarm
#SBATCH --time=04:00:00

export OMP_NUM_THREADS=1

module load quantum_espresso

srun --distribution=block:block --hint=nomultithread pw.x < Si.pwi > Si.pwo
'''
	with open('sub_qscaild','w') as f:
		f.write(input)

if __name__=='__main__':
	path = sys.argv[1] # path to the directory containing the POSCAR file
	vasp_to_qe(path)
	sub()