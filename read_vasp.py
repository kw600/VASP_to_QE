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
	atoms.write('input.pwi',input_data=input_params,pseudopotentials=pseudos,format='espresso-in',kpts=kpoints)

if __name__=='__main__':
	path = sys.argv[1] # path to the directory containing the POSCAR file
	vasp_to_qe(path)