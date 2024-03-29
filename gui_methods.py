from orca_parser.HyperFineMagneticParser import HyperFineMagneticParser
from orca_parser.ExcitationEnergyParser import ExcitationEnergyParser
from orca_parser.SinglePointEnergyParser import SinglePointEnergyParser
from orca_parser.GTensorParser import GTensorParser
from orca_parser.OrbitalEnergyParser import OrbitalEnergyParser
import os

"""
The purpose of this python module is to initialize functions that can be called from 
our driver which should integrate with our GUI. These functions should be accessible
by other modules. 

William Robinson March 29th 2024
"""


def hyperfine_run(directory):
    os.chdir(directory)
    cwd = os.getcwd()
    cwd_list = os.listdir(cwd)
    for output in cwd_list:
        if output.endswith('.out'):
            hfmp = HyperFineMagneticParser(output)
            hfmp.find_write_hfc_values()


def gtensor_run(directory):
    os.chdir(directory)
    gtp = GTensorParser(directory)
    gtp.iterate_over_outputs_parse_output_g_tensor()


def singlepoint_run(directory):
    os.chdir(directory)
    spep = SinglePointEnergyParser(directory)
    spep.iterate_over_outputs_parse_output_spe()


def orbital_energies_run(directory):
    os.chdir(directory)
    oep = OrbitalEnergyParser(directory)
    oep.iterate_over_outputs()


def excitations_run(directory):
    os.chdir(directory)
    eep = ExcitationEnergyParser(directory)
    eep.iterate_over_outputs()


def all_run(directory):
    gtensor_run(directory)
    singlepoint_run(directory)
    orbital_energies_run(directory)
    excitations_run(directory)


