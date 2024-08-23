"""
The purpose of this module is fill in a gap, the SPE energy parser grabs the final energy output,
this value for determining exchange coupling constants is not the correct value. For these broken symmetry EPR spectra
calcs, the energy we want is the raw SCF energy of the different configurations. The SPE module might be useful for
something like pulling energies to apply Truhlars corrections to for thermochem but not this project so I wont overwrite
it, instead opting to start from a new approach entirely and then embed this into the workflow as an option.
"""
import re
import csv
import datetime
import os

class SCFEnergyParser:

    # object must be initialized with a directory of output files as per normal in this package.

    def __init__(self, directory_of_outputs):
        self.directory_of_outputs = directory_of_outputs
        self.calc_names = []
        self.scf_energy_values = []
        # very literal use of regular expressions
        self.success_pattern = re.compile(r"               \*                     SUCCESS                       \*")
        self.tse_pattern = re.compile(r"^TOTAL SCF ENERGY$")
        self.te_pattern = re.compile(r"Total Energy\s+:\s+([-.\d]+) Eh\s+([-.\d]+) eV")

    def extract_energies_after_success(self, filename):
        energies_ev = []
        # boolean flags
        in_success_block = False
        in_tot_scf_energy_block = False

        with open(filename, 'r') as file:
            for line in file:
                # check to see if we are in a succesfull SCF block.
                # if we are go to next line
                if self.success_pattern.search(line):
                    # raise flag so our data is caught correctly.
                    in_success_block = True
                # check if the line refers to the tse_pattern
                elif in_success_block and self.tse_pattern.search(line):
                    in_tot_scf_energy_block = True
                # check if all three conditions are true
                elif in_success_block and in_tot_scf_energy_block and self.te_pattern.search(line):
                    match = self.te_pattern.search(line)
                    if match:
                        energies_ev.append(match.group(1))
                        # lower flag when our data passes
                        in_success_block = False
                        in_tot_scf_energy_block = False
        return energies_ev

    def file_processor_success(self):
        results = []
        row_entry = []
        for file in os.listdir(self.directory_of_outputs):
            if file.endswith('.out'):
                filepath = os.path.join(self.directory_of_outputs, file)
                energies_ev = self.extract_energies_after_success(filepath)
                row_entry.append(file)
                for energy_ev in energies_ev:
                    #results.append([file, energy_ev])
                    # expecting 3 values
                    row_entry.append(energy_ev)
                results.append(row_entry)
                row_entry = []
        return results

    def csv_writer(self, output_filename, results):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")
        with open(output_filename + timestamp + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Expecting scf1 is preopt, scf2 is postopt prespinflip, and scf3 is spinflip
            writer.writerow(['Filename','scf energies found in order'])
            writer.writerows(results)