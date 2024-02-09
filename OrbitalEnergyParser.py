import os
import csv
import datetime


class OrbitalEnergyParser:
    """
    This module operates on a directory of orca output files and parses them for data about the orbital energy levels.

    Attributes:
        directory_of_outputs (str): The path to the directory containing Orca-formatted output files.
        calc_names (list): A list to store the names of calculations.
        orbital_numbers(list): A list of the orbital numbers
        orbital_occupation(list): A list of the orbital occupations
        orbital_energies (list): A list of the orbital energies

    Methods:
        __init__(directory_of_outputs):
            Initializes the SinglePointEnergyParser with the specified directory of output files.

        iterate_over_outputs_parse_output_spe():
            Parses each output file in the directory for the final single point energy value and saves the results to class variables.
            Generates a timestamped CSV file with the single point energy values.

    Usage example:
    ```
    parser = SinglePointEnergyParser("output_directory")
    parser.iterate_over_outputs_parse_output_spe()
    ```

    Notes:
    - The timestamped CSV file is named "Single_Point_Energies_<timestamp>.csv".
    - The CSV file includes headers: "Calculation Name" and "Single Point Energy value".
    """

    def __init__(self, directory_of_outputs):

        # expected: absolute path of directory
        self.directory_of_outputs = directory_of_outputs
        self.calc_names = []

        # instance variables to make sure we are in the right section when the time comes
        self.in_orbitals_section = False

    def iterate_over_outputs(self):
        """
        Parses an output file for the last instance of lines matching:
        ----------------
        ORBITAL ENERGIES
        ----------------
                         SPIN UP ORBITALS  <---- could also look for second instance of this?
          NO   OCC          E(Eh)            E(eV)
           0   1.0000    -259.412061     -7058.9610
           1   1.0000    -259.409160     -7058.8821
           2   1.0000     -88.657523     -2412.4938
           .
           .
           .

                         SPIN DOWN ORBITALS
          NO   OCC          E(Eh)            E(eV)
           0   1.0000    -259.411701     -7058.9513
           1   1.0000    -259.408668     -7058.8687
           2   1.0000     -88.656249     -2412.4592
            .
            .
            .
        STOP when line starts with '-'

        :return:
        """
        eof_to_orbital_energy_list = []
        try:
            os.chdir(self.directory_of_outputs)
            cwd = os.getcwd()
            cwd_list = os.listdir(cwd)
            for outputfile in cwd_list:
                if outputfile.endswith(".out"):
                    try:
                        with open(outputfile, 'r') as file_to_read_data_from:
                            self.calc_names.append(outputfile.split('.')[0])
                            # read the whole file into the data variable
                            whole_file_data = file_to_read_data_from.readlines()
                            whole_file_data.reverse()
                            for line in whole_file_data:
                                # check to see if you hit the 'last
                                if line.strip() == "ORBITAL ENERGIES":
                                    break
                                eof_to_orbital_energy_list.append(line)

                            # once I have those read in reverse the list again
                            eof_to_orbital_energy_list.reverse()

                            # initiate a blank line counter
                            blank_lines_encountered = 0

                            # initialize iterator
                            i = 0

                            # initialize a list to write to output
                            list_to_write_to_output = []

                            while blank_lines_encountered != 2:
                                line = eof_to_orbital_energy_list[i]
                                if line.strip() == '\n':
                                    blank_lines_encountered += 1
                                    i += 1
                                elif line.startswith('-'):
                                    i += 1
                                else:
                                    list_to_write_to_output.append(line)
                                    i += 1
                        timestamp = datetime.datetime.now().strftime("%Y%m%d%H")
                        int_text_file_name = outputfile + "_orbital_energies" + timestamp + ".csv"
                        with open(int_text_file_name, 'w') as file:
                            csv_writer = csv.writer(file)
                            for line in eof_to_orbital_energy_list:
                                line.replace('\n', '')
                                if line.strip() == "SPIN UP ORBITALS":
                                    csv_writer.writerow(["Spin Up Orbitals"])
                                elif line.strip() == "SPIN DOWN ORBITALS":
                                    csv_writer.writerow(["Spin Down Orbitals"])
                                else:
                                    csv_writer.writerow(line.split())
                    except Exception as e:
                        print(f"error reading file:{e}")
        except Exception as e:
            print(f"error opening file:{e}")
