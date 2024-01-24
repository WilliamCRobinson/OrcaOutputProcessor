Documentation for Orca Output Processor

William Robinson 2024

Project overview

The purpose of this python package of modules is to parse output  files and return relevant properties to a csv file
for data compilation purposes very useful for large scale project.

Modules
1. HyperFineMagneticParser

    Parses Orca-formatted output files for hyperfine and magnetic properties.
    Saves the relevant data, such as A(iso) values and atom IDs, in a CSV file.

2. GTensorParser

    Operates on a directory of Orca-formatted output files.
    Parses the output files for g-tensor values and generates a timestamped CSV file with the results.

3. SinglePointEnergyParser

    Operates on a directory of Orca-formatted output files.
    Parses the output files for the final single point energy values and generates a timestamped CSV file with the results.

Dependencies

os module for manipulating directories
csv module for writing and reading csv
datetime module for writing timestamps to differentiate output files.

Handy resources:
https://education.molssi.org/python_scripting_cms/02-file_parsing/index.html

# Orca Output Parser

The Orca Output Parser is a package designed to provide a user-friendly interface for parsing Orca-formatted output files. It includes modules to extract hyperfine coupling constants, g-tensor values, and single-point energy data from a directory of Orca output files.

## Usage

1. Clone the repository:

```bash
git clone <repository_url>
cd orca-output-parser


1. Start program with your output directory ready to rock and roll.
2. enter what type of output data you want to parse for
3. Kickback for like 2 ms
4. Get your data and perform further analysis.
5. Be happy you got data.

Weirdness:
If you run this in sequence it generates entries for the other data.csv files.

Contributing

If you'd like to contribute to the development of the Orca Output Parser, please follow these steps:

    Fork the repository.
    Create a new branch for your feature: git checkout -b feature-name
    Commit your changes: git commit -m 'Add some feature'
    Push to the branch: git push origin feature-name
    Submit a pull request.

 License

 I dont know just be cool. Use it, add to it, and keep it open source.
