# Open Source Policy Bundle Documentation
By Moses Parente, KCNS Team

## Overview
This guide goes over the steps that is required to make an OPA Bundle that is hosted onto github and test it against Virtual Machines

## Prerequisites

### Please ensure you have the following: 
- Github account
- Terraform CLI installed
    - `% brew install terraform` 
- Ensure your cloud credentials are configured (AWS, Azure, GCP, Vsphere, etc)
    -  *Access Keys and Secret Keys are kept safe*
- Open Policy Agent installed
    - `% brew install opa` 

### Helpful links: 
- [OPA Bundle Documentation Link](https://www.openpolicyagent.org/docs/latest/management-bundles/)
- [OPA, Terraform and Guthub Workflow Intergration](https://medium.com/@ramrit10/open-policy-agent-opa-integration-with-github-actions-for-terraform-6e1b8e94065c)

## Creating Your OPA Bundle

- **Organize Your Policies**
    - Create a new directory where your polcies will be stored
    - ex: 
        - `mkdir rego_policies`

- **Create Your Policies** 
    - Write all your policies in a `rego` file and ensure that your policies and rules adheres to your applications requirements 

    - ex: `policy.rego` or `terraform.rego` 
    - `touch newpolicy.rego` for making a new file


- **Bundle Your OPA Policies**
    - Now you can create your bundle by archiving your directory that contains your polices. 
    - An OPA Policy bundle is a tarball that contains your polcies and or/data files
    - ` tar -czvf opa-bundle.tar.gz -C polcies .` 

- **Upload to Github**
    - Now that you have made your tarball, create a new Github Repository to store the OPA bundles
        - Go to your new Github Repo
        - Click on "Releases"
        - Click on "New Release"
        - Tag your release and give it a new name/title
        - Drag your tarball file in the "attach binaries"
        - Click "Publish Release" 
        - ***Make Sure your Github Repo is publically accessible to fetch the bundle*** 

- **Call back your OPA bundle** 
    - Make sure you can reference the URL of your newly created bundle on Github
    - To get your URL do the following steps: 
        - Find your tarball in the release assets  
            - ex: `your-bundle.tar.gz`
        - Right click on the download button 
        - Click on "Copy Link Address" 
        - Paste the URL in your YAML and .tf file where your configuration is suppoed to be.
        
### Testing the configuration ### 
There are 2 main commands that you can use to test your terraform configuratuon against an OPA Policy bundle hosted in a Github repo: 

`opa run` and `opa eval` 

`opa run` is more suited for when you want to: 
- run a server
- automatically testing policy and data loading
- interating with OPA from a HTTP API

`opa eval` is more suited for:
- one off evaluations
- quick testing
- ci/cd pipelines

Since we are doing a terraform configuration both commands can be used efficiently  

 - `opa Run`: the following command: `opa run -s -c config.yaml`
     - List the specific address and port that OPA will run on.
        - ex: localhost:8181
- `opa eval`: The following command `./opa eval -i tfplan.json -d policy/ --format pretty "data.terraform.allow" `

*Make sure all paths and policys are property adjusted and alligned together*


## Configuritng OPA Bundle into Github Workflows
The following outlines the steps to intergrate your Open Policy Agent configuration with Terraform using a github workflow. 
- Set up a new Github for your workflow
- Clone the Repo to your local machine. 
- Set your Terraform Configuration
- Set up your OPA policies 
- Create your Bundle 
    - Follow the steps above 
- Make a new directory for your workflow
- Create a new yaml file: 
- The following code for the YAML file used to test OPA against and EC2 instance: 

```
name: Terraform CI/CD with OPA

on:
  push:
    branches:
      - main
    paths:
      - '**/*.tf'
      - 'policies/*.rego'
  pull_request:
    branches:
      - main
    paths:
      - '**/*.tf'
      - 'policies/*.rego'

jobs:
  terraform_plan:
    runs-on: ubuntu-latest
    env:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    steps:
    - uses: actions/checkout@v2
      
    - name: Set up AWS credentials
      run: |
        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
        aws configure set default.region us-east-1

    - name: Set up Terraform
      uses: hashicorp/setup-terraform@v2

    - name: Terraform Init and Plan
      run: |
        terraform init
        terraform plan -out=tfplan

    - name: Save Terraform Plan
      run: terraform show -json tfplan > plan.json

    - name: Install OPA
      run: |
        curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64
        chmod +x opa

    - name: OPA Policy Evaluation
      run: |
        ./opa eval --bundle policies.tar.gz --input plan.json "data.terraform.allow"

  terraform_apply:
    needs: terraform_plan
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
    - uses: actions/checkout@v2

    - name: Set up AWS credentials
      run: |
        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
        aws configure set default.region us-east-1

    - name: Set up Terraform
      uses: hashicorp/setup-terraform@v2

    - name: Terraform Apply
      run: |
        terraform init
        terraform apply -auto-approve tfplan
```
## Running the OPA GIthub Workflow
 Whenever you make a change to your file and push it, github actions will trigger the workflow.
 
  Making even a small edit to your terraform files will trigger the github workflow. 
  
  If your policy check fails, you can review the actions in your Github
 repository to find detailed logs of the workflow run


## Pontential Errors

Be sure to check your Github Actions workflow for any errors. 

A common bug that can happen is when your directory includes extended/hidden/unknown attributes in the tarfile, which can happen when you are creating your bundles with a machine using MacOS. To fix this issue use the command `tar --exclude='._*' -czvf policies.tar.gz -C policies .` to clear the files of any attributes that can corrupt the bundle.

## Conclusion 

Intergrating Open Policy Agent with Terraform is a very effective way to enforce governance, risk and compliance policies ensuring only valid  configurations are applied resulting in a safe infrastructure.
