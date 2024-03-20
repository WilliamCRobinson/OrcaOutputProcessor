import csv
import os

class ExcitationEnergyParser:
    def __init__(self, directory_of_outputs):
        self.directory_of_outputs = directory_of_outputs
        self.calc_names = []
        self.in_orbitals_section = False

    def iterate_over_outputs(self):
        start_block = "TD-DFT/TDA EXCITED STATES"
        end_block = "CALCULATED SOLVENT SHIFTS"

        try:
            os.chdir(self.directory_of_outputs)
            cwd = os.getcwd()
            cwd_list = os.listdir(cwd)
        except Exception as e:
            print(f"Error while changing directory: {e}")
            return  # Stop execution if changing directory fails

        for outputfile in cwd_list:
            if outputfile.endswith('.out'):
                with open(outputfile, 'r') as file_to_read_data_from:
                    lines = file_to_read_data_from.readlines()
                    inside_block = False
                    output_lines = []

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
                    output_lines = output_lines[4:-3]
                    # now write the csv for this output file.
                    try:
                        output_csv_path = os.path.join(self.directory_of_outputs, f"{outputfile.split('.')[0]}_excitations.csv")
                        with open(output_csv_path, 'w', newline='') as csvfile:
                            csv_writer = csv.writer(csvfile, delimiter=',')
                            # write the header line to differentiate data upon manual compilation
                            csv_writer.writerow([outputfile.split('.')[0]])
                            csv_writer.writerow(['State', 'Energy (au)', 'Energy (eV)', 'Energy (cm**-1)', 'Transition', 'Transition Coefficient', 'Transition Weight'])

                            state_num, energy_au, energy_ev, energy_cm = None, None, None, None

                            # Iterate over lines to extract and write data
                            for outline in output_lines:
                                # Skip any blank lines encountered
                                if not outline.strip():
                                    continue

                                try:
                                    if outline.startswith('STATE'):
                                        state_data = outline.split()
                                        if len(state_data) >= 8:
                                            state_num = state_data[1][:-1]
                                            energy_au = state_data[3]
                                            energy_ev = state_data[5]
                                            energy_cm = state_data[7]
                                    elif "->" in outline:
                                        # Process transition lines with flexible element extraction
                                        transition_info = outline.split(':')
                                        if len(transition_info) >= 2:
                                            transition_data = transition_info[0].strip().split()
                                            transition = f"{transition_data[0]} -> {transition_data[2]}"

                                            # Extract transition coefficient and weight
                                            coefficient_and_weight = transition_info[1].strip().split('c=')
                                            coefficient = coefficient_and_weight[0].strip().replace("(", "")
                                            transition_weight = ''
                                            if len(coefficient_and_weight) > 1:
                                                transition_weight = coefficient_and_weight[1].strip().replace(")", "")

                                            # Write to CSV
                                            csv_writer.writerow([state_num, energy_au, energy_ev, energy_cm, transition, coefficient, transition_weight])
                                except Exception as e:
                                    print(f"Error processing line in file {outputfile}: {outline}")
                                    print(f"Exception: {e}")
                                    continue

                        #print(f'Data written to {output_csv_path}')

                    except Exception as e:
                        print(f"Unknown error: {e}")

