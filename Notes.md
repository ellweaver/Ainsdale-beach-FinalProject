- Git Repo

- AWS Account
- CI/CD
	- GitHub Actions?
	 - makefile
- Docstrings
	- file structure
- terraform
	- backend
		- state file must be kept separately from rest of infrastructure
	- lambda
		- contain pythons app
		- etc
- gitignore
	- state.tf
	- .env
	- venv
	- pycache
	- look at previous ignore files
- requirements.txt
- readme.me
- daily housekeeping:
	- note taking, to form basis of documentation
- Monitoring and Performance
	- cloudwatch


##create a git repo
#create git repo and share neccesary crudentials

spec file-
repo file structure
branches created ?


#ci/cd
make file-template
pep8 compliance
pip-audit
bandit
black

## Terraform
-s3 buckey for data ingestion
-s3 buckey for processed data
--export busket names as params
--create cloudwatch alarm to be triggered on each call of func 1- emails on failure
--lambda -func 1 -triggered by cloudwatch-at every x mins
--lambda func 2 -triggered by upload into first s3 bucket
--create cloudwatch alarms on failure of func 2


##python
#ingest
#python func 1- retrieves data-uploads to s3-  provides info and error logs
def retrieve_data_and send to s3 ingestion()
#transform
#python fuc 2 () 
def transforms data from s3 ingestion and uploads to s3 proccesed
#load
#python func 3()
load data into datawarehouse


##Orchestration
step functions/ Scheduling 

##sql
#design data warehouse 
#create data warehouse
#jupiter file to demonstrate output capabilities


