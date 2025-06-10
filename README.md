# Ainsdale-Beach-ETL

## Summary
The Ainsdale Beach ETL project is an Extract Transform Load pipeline, using Python, hosted in AWS.
The primary function of the pipeline is to ingest and transform data from an OLTP optimised database into an OLAP optimised data warehouse. 
The main objectives of this project are to be able to handle regular data updates and execute performant TDD code (Test Driven Development), providing an effective, usable star schema output with robust versioning.
An additional feature of this project is to have an S3 bucket containing processed data in Parquet, that mirrors our processed data to permit further analysis better suited to that format.
Our aim with this project is to enable analysis of important business data without compromising performance for day-to-day transactional operations.


## Extract
Our initial data is stored in an RDS database, and contains 11 tables of normalised OLTP data. 
Our extract function ingests and converts each table into `.csv` format using the polars library. Using boto3, each `.csv` file is uploaded to an S3 bucket with a key containing the ingestion timestamp and the original name of the table. This key convention enables simple versioning and reduces the chance of mishandling data. 

Our key produces a psuedo file system based on year, month, day and a timestamp. The timestamp is then used as a batch id and each individual file is labelled with this id:
```python
upload_file(
    s3_client,
    file=out_buffer.getvalue(),
    bucket_name=bucket,
    key=f"data/{current_year}/{current_month}/{current_day}/{time_now}/{time_now}_{table}.csv",
    )
```

## Transform
The purpose of our transform function is to reshape our ingested S3 data towards an OLAP optimised format. Polars performantly reshapes our 11 initial `.csv` files, into 7 dataframes that form the basis of a star schema. During the transformation process, relevant dataframes are held in dictionaries. This facilitates easy looping and improves readability. Pyarrow  converts the dataframes to `.parquet`:

```python
for table, value in processed_dict.items():
    out_buffer = BytesIO()
    value.write_parquet(out_buffer)

```

The transformed files are uploaded to the destination bucket using boto3:
```python
upload_file(
    s3_client,
    file=out_buffer.getvalue(),
    bucket_name=destination_bucket,
    key=f"{key}{batch_id}_{table}.parquet",
    )
```


## Load
from bucket
puts back into rds pg db
what libraries were used?

## Data Visualisation
read db
some implementation of tableau or looker
pull some analysis
- could perhaps use matplotlib


## Hosting
Our infrastructure has been provisioned in AWS, employing the following services: 
- RDS 
- IAM
- Step Functions
- Lambda
- Secrets Manager
- CloudWatch
- S3
- Amazon EventBridge Scheduler
- SNS


## Orchestration
Our project employs GitHub actions to adhere to CICD principles (Continuous Integration Continuous Development). GitHub Actions enables robust, automated testing and deployment. Using our make file tests for: functionality (pytest), formatting (black), coverage (coverage), and security (bandit) can all be actioned before any resources are deployed or changes made to the production code. If those tests are all successful the infrastructure is automatically deployed by terraform into the AWS cloud. This helps maintain the functionality and consistency of the code in a continuous development process.


## Terraform Structure
Terraform deploys our infrastructure in AWS. This allows for scalable and granular control of infrastucture and easy co-operation between developers on the project. Terraform is also the basis of our CICD infrastructure. The file structure for our terraform directory is relatively conventional: cloudwatch, data, events, iam, lambda, main, s3, sns, stepfunction,vars. The `terraform.tfstate` file is held in S3 to better enable remote coworking and to enable easy switching of the backend `terraform.tfstate` file.   


Resources provisioned outside Terraform:
- backend bucket:
    - tf state
- Lambda buckets:
    - python
    - layers
- Amazon Elastic container Registry

## Logging
Cloudwatch retains our project's logs and, error messages are received using SNS.

## Requirements
Python version 3.13
Major packages include:
- Polars
- Pyarrow 
- Boto3 
- Black
- Coverage
- Pytest
- Bandit
- adbc
a full list of packages and dependencies can be found requirements.txt

















