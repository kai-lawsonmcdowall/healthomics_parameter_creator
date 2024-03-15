# healthomics parameter creator

- A quick python script which creates the AWS HealthOmics parameter file for nf-core pipelines, as a prerequisite to uploading pipelines to [AWS HealtlhOmics](https://aws.amazon.com/healthomics/). It automates **Step 1 AWS HealthOmics Parameter file** in the workflow: [Migrating Nf-core Workflows Into AWS HealthOmics](https://catalog.us-east-1.prod.workshops.aws/workshops/76d4a4ff-fe6f-436a-a1c2-f7ce44bc5d17/en-US/workshop/create-healthomics-workflow)
<br>

- his file can be placed in the root directory of a nf-core pipline. It requires a nf-core pipeline which has a `nextflow_schema.json`, and the url of the parameters page of the nf-core pipeline in question.
<br>
- it can either be executed as a command line utility (`parameter_extractor_command_line.py`) or via a notebook (`parameter_extractor_notebook.py`)

<br>

- The current example illustrates how this might be done with the fetchngs pipeline. To do this, I simply fetched the raw `nextflow_schema.json` content and downloaded here. and used the URL https://nf-co.re/fetchngs/1.12.0/parameters.

<br>

- currently tests are faililng due to the fact that the `nextflow_schema` includes many of the additional core params of nf-core pipelines, (e.g. hook_url) which are universal to all pipelines, but were not considered when creating this pipeline. 

<br>

- install the necessary packages via `pip install -r requirements.txt`