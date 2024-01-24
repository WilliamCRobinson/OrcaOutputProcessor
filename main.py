import HyperFineMagneticParser
from SinglePointEnergyParser import SinglePointEnergyParser
from GTensorParser import GTensorParser
import os
"""
The purpose of this package is to provide a user-friendly interface for parsing Orca-formatted output files.
"""


def main():
    """
    Main function to process Orca-formatted output files based on user input.

    Uses all of the other modules. The intention is that if you are interested in another peice of data,
    write a module and then add another branch in the if statement.

    Prompts the user for a spec for hyperfine data, g-tensor data, or single-point energy data.
    Asks for the absolute path of the output file directory and performs the chosen processing on the files.

    Returns:
        None
    """
    process_requested = input("hyperfine, g-tensor, or singlepoint:")
    output_path = input("please provide the absolute path of your output file directory:")
    if process_requested.lower() == "hyperfine":
        # keeping this simple for now, just the stuff that pulls the hyperfine coupling constants out.

        os.chdir(output_path)
        cwd = os.getcwd()
        cwd_list = os.listdir(cwd)
        for output in cwd_list:
            hfmp = HyperFineMagneticParser.HyperFineMagneticParser(output)
            hfmp.find_write_hfc_values()
    elif process_requested.lower() == "g-tensor":
        # implement g-tensor
        os.chdir(output_path)
        gtp = GTensorParser(output_path)
        gtp.iterate_over_outputs_parse_output_g_tensor()
    elif process_requested.lower() == "singlepoint":
        os.chdir(output_path)
        spep = SinglePointEnergyParser(output_path)
        spep.iterate_over_outputs_parse_output_spe()


if __name__ == "__main__":
    main()
