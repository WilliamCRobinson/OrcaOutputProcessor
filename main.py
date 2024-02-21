import HyperFineMagneticParser
import ExcitationEnergyParser
from SinglePointEnergyParser import SinglePointEnergyParser
from GTensorParser import GTensorParser
import OrbitalEnergyParser
import os
"""
The purpose of this package is to provide a user-friendly interface for parsing Orca-formatted output files.

TODO:
cleanup output filenames for orbital energies
make a better menu

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
    process_requested = input("hyperfine, g-tensor, orbital energies, singlepoint, or excitations:")
    output_path = input("please provide the absolute path of your output file directory:")
    if process_requested.lower() == "hyperfine":
        # keeping this simple for now, just the stuff that pulls the hyperfine coupling constants out.
        os.chdir(output_path)
        cwd = os.getcwd()
        cwd_list = os.listdir(cwd)
        for output in cwd_list:
            if output.endswith('.out'):
                hfmp = HyperFineMagneticParser.HyperFineMagneticParser(output)
                hfmp.find_write_hfc_values()
    elif process_requested.lower().strip() == "g-tensor":
        # implement g-tensor
        os.chdir(output_path)
        gtp = GTensorParser(output_path)
        gtp.iterate_over_outputs_parse_output_g_tensor()
    elif process_requested.lower().strip() == "singlepoint":
        os.chdir(output_path)
        spep = SinglePointEnergyParser(output_path)
        spep.iterate_over_outputs_parse_output_spe()
    elif process_requested.lower().strip() == 'all':
        # hyperfine
        os.chdir(output_path)
        cwd = os.getcwd()
        cwd_list = os.listdir(cwd)
        for output in cwd_list:
            if output.endswith('.out'):
                hfmp = HyperFineMagneticParser.HyperFineMagneticParser(output)
                hfmp.find_write_hfc_values()
        # g-tensor
        os.chdir(output_path)
        gtp = GTensorParser(output_path)
        gtp.iterate_over_outputs_parse_output_g_tensor()
        #  singlepoint
        os.chdir(output_path)
        spep = SinglePointEnergyParser(output_path)
        spep.iterate_over_outputs_parse_output_spe()
        # orbital energy
        os.chdir(output_path)
        oep = OrbitalEnergyParser.OrbitalEnergyParser(output_path)
        oep.iterate_over_outputs()
        # excitations from TDDFT
        os.chdir(output_path)
        eep = ExcitationEnergyParser.ExcitationEnergyParser(output_path)
        eep.iterate_over_outputs()
    elif process_requested.lower().strip() == "orbitalenergies":
        os.chdir(output_path)
        oep = OrbitalEnergyParser.OrbitalEnergyParser(output_path)
        oep.iterate_over_outputs()
    elif process_requested.lower().strip() == "excitations":
        os.chdir(output_path)
        eep = ExcitationEnergyParser.ExcitationEnergyParser(output_path)
        eep.iterate_over_outputs()


if __name__ == "__main__":
    main()

