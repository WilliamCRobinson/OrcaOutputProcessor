"""
This module will operate on a directory of orca formatted output files and parse the output files for the single point
energies.
"""

import os
import csv
import datetime


class SinglePointEnergyParser:

    def __init__(self, directory_of_outputs):
        self.directory_of_outputs = directory_of_outputs
        self.calc_names = []
        self.spe_values = []

    def iterate_over_outputs_parse_output_spe(self):
        """
        parses an output file for the line
        -------------------------   --------------------
        FINAL SINGLE POINT ENERGY     -yyyy.xxxxxxxxxxx
        -------------------------   --------------------
        :return: null, data is saved to class variables.
        """
        try:
            os.chdir(self.directory_of_outputs)
            cwd = os.getcwd()
            cwd_list = os.listdir(cwd)
            for outputfile in cwd_list:
                try:
                    with open(outputfile, 'r') as file:
                        self.calc_names.append(str(outputfile.split('.')[0]))
                        # there are many instances of the target line we only want the very last one
                        # solution is to just iterate through and overwrite.
                        dummy_energy = 0
                        for line in file.readlines():
                            if line.lower().strip().startswith("final"):
                                dummy_energy = line.split()[-1]
                        self.spe_values.append(dummy_energy)
                except Exception as e:
                    print(f"Error while parsing single point energy values:{e}")
        except Exception as e:
            print(f"Error while iterating over directory: {e}")
        # okay now that the data is saved into two arrays we ought to zip it up and send it to a timestamped output
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H")
        name_of_output_csv = f"Single_Point_Energies_{timestamp}.csv"
        data = list(zip(self.calc_names, self.spe_values))
        with open(name_of_output_csv, mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Single_Point_Energies "+timestamp])
            csv_writer.writerow(["Calculation Name", "Single Point Energy value"])
            csv_writer.writerows(data)
        return
