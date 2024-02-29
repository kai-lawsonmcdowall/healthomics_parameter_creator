# %%
import json
import requests
from bs4 import BeautifulSoup
import re


def extract_substrings(input_string, keyword):
    substrings = []
    start_pattern = re.escape("<code>--{}</code>".format(keyword))
    end_pattern = re.escape("<code>--")
    pattern = re.compile(r"{}(.*?){}".format(start_pattern, end_pattern), re.DOTALL)
    matches = pattern.findall(input_string)
    for match in matches:
        substrings.append(match.strip())
    return substrings


def process_json(input_string, json_data):
    for keyword in json_data.keys():
        print("Substrings for '{}':".format(keyword))
        substrings = extract_substrings(input_string, keyword)
        for idx, substring in enumerate(substrings, 1):
            if (
                'class="badge text-bg-warning mb-1" data-svelte-h="svelte-1t99nzu">required</span>'
                in substring
            ):
                json_data[keyword]["optional"] = False
            else:
                json_data[keyword]["optional"] = True


def create_parameters_json(nextflow_schema, nf_core_params_url, json_output_path):

    # Load the original JSON file
    with open(nextflow_schema, "r") as f:
        original_data = json.load(f)

    response = requests.get(nf_core_params_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        html_string = str(soup)

    # Initialize an empty dictionary to store extracted data
    extracted_data = {}

    # Iterate over each definition in the original JSON
    for definition_key, definition_value in original_data.get(
        "definitions", {}
    ).items():
        # Check if the definition has properties
        if "properties" in definition_value:
            # Iterate over each property in the definition
            for property_key, property_value in definition_value["properties"].items():
                # Extract title and description
                title = property_key
                description = property_value.get("description", "")

                # Set optional field to an empty string
                extracted_data[title] = {"optional": "", "description": description}

    # Example usage
    process_json(html_string, extracted_data)

    # Write the extracted data to a new JSON file
    with open(json_output_path, "w") as f:
        json.dump(extracted_data, f, indent=4)


# %%
create_parameters_json(
    "/home/kai/Desktop/cloud-health-omics/workflows/nf-core/workflows/differentialabundance/nextflow_schema.json",
    "https://nf-co.re/differentialabundance/1.4.0/parameters",
    "/home/kai/Desktop/cloud-health-omics/workflows/nf-core/workflows/differentialabundance/extracted_properties_final.json",
)

# %%
