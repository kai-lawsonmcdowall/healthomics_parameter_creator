# healthomics parameter creator

- A quick python script which creates the AWS HealthOmics parameter file for nf-core pipelines, as a prerequisite to uploading pipelines to [AWS HealtlhOmics](https://aws.amazon.com/healthomics/). It automates **Step 1 AWS HealthOmics Parameter file** in the workflow: [Migrating Nf-core Workflows Into AWS HealthOmics](https://catalog.us-east-1.prod.workshops.aws/workshops/76d4a4ff-fe6f-436a-a1c2-f7ce44bc5d17/en-US/workshop/create-healthomics-workflow)

<br>

- This file can be placed in the root directory of a nf-core pipline. It requires a nf-core pipeline which has a `nextflow_schema.json`, and the url of the parameters page of the nf-core pipeline in question. It gets the required params from the .json file, and determines if they are required or optional from the nf-core params page.

<br>

- it can either be executed as a command line utility (`parameter_extractor_command_line.py`) or via a notebook (`parameter_extractor_notebook.ipynb`)

<br>

- The current example illustrates how this might be done with the fetchngs pipeline. To do this, I simply fetched the raw `nextflow_schema.json` content and downloaded here. and used the URL https://nf-co.re/fetchngs/1.12.0/parameters.

<br>

- currently tests are faililng due to the fact that the `nextflow_schema` includes many of the additional core params of nf-core pipelines, (e.g. hook_url) which are universal to all pipelines, but were not considered when creating this pipeline. 

<br>

- install the necessary packages via `pip install -r requirements.txt`, and an example can be executed by running the `example_CLI_execution.sh` script, which generates the params for fetchngs.

## Updates 

Additionaltiy functionality has been added which automatically removes common parameters derived from nextflow_schema.json, which are not compatible with healthomics. These are the following: 

```
    exclude_parameters = [
        "outdir",
        "email",
        "custom_config_version",
        "custom_config_base",
        "config_profile_name",
        "config_profile_description",
        "config_profile_contact",
        "config_profile_url",
        "max_cpus",
        "max_memory",
        "max_time",
        "help",
        "version",
        "publish_dir_mode",
        "email_on_fail",
        "plaintext_email",
        "monochrome_logs",
        "hook_url",
        "validate_params",
        "validationShowHiddenParams",
        "validationFailUnrecognisedParams",
        "validationLenientMode",
    ]
```

## Folders: 

### Outputs

These are the outputs from testing the CLI and Notebook scripts, this is for fetchNGS and Sarek. 

### Tests

This includes the CLI scripts testing the fetchNGS and Sarek pipelines (The examples execution from the notebook are done in the notebook). It also includes the necessary nextflow_schema.json for the respective pipelines, and a python script testing a manually curated version of the sarek pipeline as well as the automated one. 

### Home directory

Contains the two scripts that can be used to generate the scripts (the CLI and Notebook version), this readme and the requirements.txt