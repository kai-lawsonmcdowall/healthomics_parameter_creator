# %%
import re
import json
import requests
from bs4 import BeautifulSoup


def extract_substrings(input_string: str, keyword: str):
    """
    Extracts substrings enclosed between <code>--{keyword}</code> and <code>-- tags
    from the given input_string. These substrings and their contents are unique to each nf-core parameter listed on the nf-core
    page, therefore, we can use them to determine if a parameter is required or optional.

    Args:
        input_string (str): The html content of the workflow nf-core params page, as a giant string
        keyword (str): The keyword to identify substrings between <code>--{keyword}</code> tags.

    Returns:
        list: A list of extracted substrings, each of which will contain the optional or required statement of each parameter
        listed in the nf-core workflow params page.
    """

    substrings = []
    start_pattern = re.escape(f"<code>--{keyword}</code>")
    end_pattern = re.escape("<code>--")
    pattern = re.compile(r"{}(.*?){}".format(start_pattern, end_pattern), re.DOTALL)
    matches = pattern.findall(input_string)
    for match in matches:
        substrings.append(match.strip())
    return substrings


def process_json(input_string: str, json_data: dict):
    """
    Process the input string to update the 'optional' status in the eventual parameter-description.json
    based on the presence of specific substrings associated with each keyword. This function modifies the
    'optional' status in the 'json_data' dictionary in place.


    Args:
        input_string (str): The input string to search for substrings.
        json_data (dict): A dictionary containing keyword-substring mappings.

    Returns:
        None


    """
    for keyword in json_data.keys():
        print(f"getting required status for {keyword}")
        substrings = extract_substrings(input_string, keyword)
        for idx, substring in enumerate(substrings, 1):
            if (
                'class="badge text-bg-warning mb-1" data-svelte-h="svelte-1t99nzu">required</span>'
                in substring
            ):
                json_data[keyword]["optional"] = False
            else:
                json_data[keyword]["optional"] = True


def create_parameters_json(
    nextflow_schema: str, nf_core_params_url: str, json_output_path: str
):
    """
    Create a JSON file containing parameters extracted from a Nextflow schema and nf-core parameters URL.

    Parameters:
        nextflow_schema (str): Path to the Nextflow schema JSON file.
        nf_core_params_url (str): URL of the nf-core parameters page of the workflow.
        json_output_path (str): Path to write the output JSON file containing extracted parameters.

    Returns:
        None

    This function loads the original Nextflow schema JSON file and fetches the HTML content of the nf-core parameters
    page. It extracts parameter titles and descriptions from the Nextflow schema and determines if each parameter is
    required or optional based on the HTML content. The extracted data is written to a new JSON file.
    """

    # Load the original JSON file
    with open(nextflow_schema, "r") as f:
        original_data = json.load(f)

    # fetching the html content of the workflow's nf-core params page.
    response = requests.get(nf_core_params_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        html_string = str(soup)

    # Initialize an empty dictionary to store extracted data
    extracted_data = {}

    # Iterate over each definition in the nextflow Schema
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

    # getting if the parameter is required or optional.
    process_json(html_string, extracted_data)

    # Write the extracted data to a new JSON file
    with open(json_output_path, "w") as f:
        json.dump(extracted_data, f, indent=4)


# %%
# example usage
create_parameters_json(
    "fetchngs_nextflow_schema.json",
    "https://nf-co.re/fetchngs/1.12.0/parameters",
    "notebook_fetchngs_parameters_description.json",
)
# %%
