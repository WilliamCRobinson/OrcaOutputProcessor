import csv


class HyperFineMagneticParser:
    """
    The purpose of this module is to parse an Orca-formatted output file and save the relevant hyperfine and magnetic
    properties.

    Dependencies:
        - OS for manipulating file structures and finding files
        - Pandas for data handling
        - CSV for data saving.

    Attributes:
        output_file (str): The path to the Orca-formatted output file.

    Methods:
        __init__(output_file):
            Initializes the HyperFineMagneticParser with the specified output file.

        find_write_hfc_values():
            Finds and writes the A(iso) value and the atom ID for a given output file.
            Generates a CSV file for the corresponding output.

    Usage example:
    ```
    parser = HyperFineMagneticParser("example_output.orca")
    parser.find_write_hfc_values()
    ```

    Note:
    - The output CSV file is named after the input file with a ".csv" extension.
    - The CSV file includes headers: "Atom ID" and "A(iso) value".
    """
    def __init__(self, output_file):
        self.output_file = output_file

    def find_write_hfc_values(self):
        """
        Finds and writes the A(iso) value and the atom ID for a given output file.
        Generates a CSV file for the corresponding output.

        Raises:
            Exception: If an error occurs during the parsing process.

        Returns:
            None
        """
        try:
            # this is the bulk of the work to be done
            # open the file safely in read mode
            with open(self.output_file, 'r') as file_to_read_data_from:

                # make some variables that check conditions which will be changed if lines are encountered.
                in_target_block = False
                atom_id_list = []
                a_iso_value_list = []

                # read the whole file into the data variable
                whole_file_data = file_to_read_data_from.readlines()

                # for a given output there should be only one of these files.
                line_to_search_for = "ELECTRIC AND MAGNETIC HYPERFINE STRUCTURE"

                # iterate through data and  search for line.
                # assuming the line input formats are
                # 'Nucleus   4H : A:ISTP=    1 I=  0.5 P=533.5514 MHz/au**3'
                # and
                #  A(Tot)         -2.9721              -4.6379              -5.1823    A(iso)=   -4.2641

                for line in whole_file_data:
                    # check to see if we are entering the right section
                    # print(line.strip())
                    if line.strip() == line_to_search_for:
                        in_target_block = True
                    # if we are in the right section get some shit done.
                    # print(f"in_target_block:{in_target_block}")
                    if in_target_block:
                        # Handle the two mutually exclusive cases.
                        print(line)
                        if line.strip().startswith("Nucleus"):
                            split_line = line.split()
                            atom_id = split_line[1]
                            atom_id_list.append(atom_id)
                        elif line.strip().startswith("A(Tot)"):
                            split_line = line.split()
                            a_iso_value = split_line[-1]
                            a_iso_value_list.append(a_iso_value)

                # now we have two list full of data that should be sequentially organized in how it was found.
                # we need to save these two things as list.
                name_of_output_csv = self.output_file.split(".")[0] + ".csv"
                data = list(zip(atom_id_list, a_iso_value_list))
                with open(name_of_output_csv, mode='w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow([f"data for {self.output_file.split('.')[0]}"])
                    csv_writer.writerow(["Atom ID", "A(iso) value"])
                    csv_writer.writerows(data)
        except Exception as e:
            print(f"Error while parsing:{e}")
        return
