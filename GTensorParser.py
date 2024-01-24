"""
This module will operate on a directory of orca formatted output files and parse the output files for the g-tensor
values.
"""

import os
import csv
import datetime


class GTensorParser:
    """
    This module operates on a directory of Orca-formatted output files and parses the output files for g-tensor values.

    Attributes:
        directory_of_outputs (str): The path to the directory containing Orca-formatted output files.
        calc_names (list): A list to store the names of calculations.
        g_tensor_values (list): A list to store the g-tensor values.

    Methods:
        __init__(directory_of_outputs):
            Initializes the GTensorParser with the specified directory of output files.

        iterate_over_outputs_parse_output_g_tensor():
            Parses each output file in the directory for g-tensor values and saves the results to class variables.
            Generates a timestamped CSV file with the g-tensor values.

    Usage example:
    ```
    parser = GTensorParser("output_directory")
    parser.iterate_over_outputs_parse_output_g_tensor()
    ```

    Note:
    - The timestamped CSV file is named "g-Tensor_values_<timestamp>.csv".
    - The CSV file includes headers: "Calc Names" and "g(tot)_iso value".
    """
    def __init__(self, directory_of_outputs):
        self.directory_of_outputs = directory_of_outputs
        self.calc_names = []
        self.g_tensor_values = []

    def iterate_over_outputs_parse_output_g_tensor(self):
        """
        Parses an output file for g-tensor, reports as g(tot)_iso.
        -------------------
        ELECTRONIC G-MATRIX
        -------------------
        .
        .
        .
         g(tot)       1.9329532    2.0181608    2.0752548 iso=  2.0087896

        Raises:
            Exception: If an error occurs during the parsing process.

        Returns:
            None
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
