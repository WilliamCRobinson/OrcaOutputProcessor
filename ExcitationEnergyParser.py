import csv
import os


class ExcitationEnergyParser:
    """
    This module is intended to work on the output of a TD-DFT job. It should pull the information within the TD-DFT/TDA excited states

    UNDER CONSTRUCTION
    """
    def __init__(self, directory_of_outputs):

        # expected: absolute path of directory
        self.directory_of_outputs = directory_of_outputs
        self.calc_names = []

        # instance variables to make sure we are in the right section when the time comes
        self.in_orbitals_section = False

    def iterate_over_outputs(self):

        # block to start data collection
        start_block = "TD-DFT/TDA EXCITED STATES"
        # block to end data collection
        end_block = "CALCULATED SOLVENT SHIFTS"
        output_lines = []

        try:
            os.chdir(self.directory_of_outputs)
            cwd = os.getcwd()
            cwd_list = os.listdir(cwd)
            for outputfile in cwd_list:
                if outputfile.endswith('.out'):
                    with open(outputfile, 'r') as file_to_read_data_from:
                        lines = file_to_read_data_from.readlines()
                        inside_block = False
                        for line in lines:
                            if line.strip() == start_block:
                                inside_block = True
                                continue
                            elif line.strip() == end_block:
                                inside_block = False
                                continue
                            elif inside_block:
                                output_lines.append(line.strip())
                        # snip off the first and last element as those will end up being just dashes.
                        # BE CAUTIOUS HERE WE DON'T WANT TO SNIP DATA THAT MAY BE IMPORTANT.
                        output_lines = output_lines[4:-3]
                    with open(outputfile.split(".")[0] + "_excitations.csv", 'w', newline='') as csvfile:
                        # Create a CSV writer object
                        csv_writer = csv.writer(csvfile, delimiter=',')

                        # Write header
                        csv_writer.writerow(['State', 'Energy (au)', 'Energy (eV)', 'Energy (cm**-1)', 'Transition', 'Transition Coefficient'])

                        # Iterate over lines to extract and write data
                        for line in lines:
                            if line.startswith('STATE'):
                                state_data = line.split()
                                state_num = state_data[1][:-1]  # Extract the state number
                                energy_au = state_data[3]       # Extract energy in atomic units
                                energy_ev = state_data[5]       # Extract energy in electron volts
                                energy_cm = state_data[7]       # Extract energy in cm**-1
                            elif line.strip():  # Process transition lines
                                transition_data = line.split()
                                transition = f"{transition_data[1]} -> {transition_data[3]}"  # Extract transition
                                coefficient = transition_data[-2]  # Extract transition coefficient
                                # Write to CSV
                                csv_writer.writerow([state_num, energy_au, energy_ev, energy_cm, transition, coefficient])
                    print(f'Data written to {outputfile.split(".")[0] + "_excitations.csv"}')
        except Exception as e:
            print(f"Error collecting Excitation energies:{e}")
