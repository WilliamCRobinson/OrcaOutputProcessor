"""
This module will operate on a directory of orca formatted output files and parse the output files for the g-tensor
values.
"""

import os
import csv
import datetime


class GTensorParser:

    def __init__(self, directory_of_outputs):
        self.directory_of_outputs = directory_of_outputs
        self.calc_names = []
        self.g_tensor_values = []

    def iterate_over_outputs_parse_output_g_tensor(self):
        """
        parses an output file for g-tensor, report as g(tot)_iso
        -------------------
        ELECTRONIC G-MATRIX
        -------------------
        .
        .
        .
         g(tot)       1.9329532    2.0181608    2.0752548 iso=  2.0087896
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
                        for line in file.readlines():
                            if line.lower().strip().startswith("g(tot)"):
                                self.g_tensor_values.append(line.split()[-1])
                except Exception as e:
                    print(f"Error while parsing g-tensor values:{e}")
        except Exception as e:
            print(f"Error while iterating over directory: {e}")
        # okay now that the data is saved into two arrays we ought to zip it up and send it to a timestamped output
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H")
        name_of_output_csv = f"g-Tensor_values_{timestamp}.csv"
        data = list(zip(self.calc_names, self.g_tensor_values))
        with open(name_of_output_csv, mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["g(tot)_iso values "+timestamp])
            csv_writer.writerow(["Calc Names", "g(tot)_iso value"])
            csv_writer.writerows(data)
        return
