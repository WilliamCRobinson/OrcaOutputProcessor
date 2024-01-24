Documentation for Orca Output Processor

William Robinson 2024

Project overview

The purpose of this python package of modules is to parse output  files and return relevant properties to a csv file
for data compilation purposes very useful for large scale project.



Handy resources:
https://education.molssi.org/python_scripting_cms/02-file_parsing/index.html

Project Structure


1.    (hyperfine_parser.py)
        Responsibility: defines a set of methods to be used by a driver method to return a data array of the hyperfine
                        coupling constant and gtensor from an Orca output file, name of output file should be included
                        for traceability.This traceability should make it easy to trace back to the input file and make
                        insights easily.
        Class Variable(s) :
            output_file : the output file that will be read and manipulated. Specified by absolute path.
        Methods:
            find_hfc_gtensor_values(self):

            data_to_csv(self, data_values):

2.      g-tensor_parser.py
