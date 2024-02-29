# healthomics_parameter_creator
A quick python script which creates the AWS HealthOmics parameter file for nf-core pipelines, as a prerequisite to uploading pipelines to AWS HealtlhOmics

This file can be placed in the root directory of a nf-core pipline which has been pulled down. It requires a nf-core pipeline which has a nextflow_schema.json, and the url of the parameters page of the nf-core pipeline in question. 

Currently, it is executed as a python notebook in vs-code. However, I will make this a command line utility. 
