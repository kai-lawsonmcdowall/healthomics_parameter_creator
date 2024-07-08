import json
import sys
import os

# importing functions:
parent_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(parent_dir, ".."))
sys.path.append(root_dir)
from parameter_extractor_command_line import *

# %%
create_parameters_json(
    "sarek_nextflow_schema.json",
    "https://nf-co.re/sarek/3.4.0/parameters",
    "automated_sarek_parameter-template.json",
)


def compare_json_files(file1_path, file2_path):
    # Load JSON data from the first file
    with open(file1_path, "r") as file1:
        data1 = json.load(file1)

    # Load JSON data from the second file
    with open(file2_path, "r") as file2:
        data2 = json.load(file2)

    # Remove entries with empty "optional" value
    data1 = {
        k: v
        for k, v in data1.items()
        if v.get("optional") is not None and v.get("optional") != ""
    }
    data2 = {
        k: v
        for k, v in data2.items()
        if v.get("optional") is not None and v.get("optional") != ""
    }

    # Sort dictionaries alphabetically
    sorted_data1 = dict(sorted(data1.items()))
    sorted_data2 = dict(sorted(data2.items()))

    # Compare the sorted dictionaries
    if sorted_data1 == sorted_data2:
        print(
            "The JSON files are identical after removing empty 'optional' entries and sorting."
        )
    else:
        print(
            "The JSON files are different after removing empty 'optional' entries and sorting."
        )


# Paths to the JSON files
file1_path = "automated_sarek_parameter-template.json"
file2_path = "manual_sarek_parameter-template.json"

# Compare the JSON files
compare_json_files(file1_path, file2_path)
