# Ainsdale-Beach-ETL

## Summary
tldr - project overview

## Extract
what we pulled
converted to csv
upload to bucket
## Transform
from bucket
generate tables to fit desired star schema - fact_sales_order
upload parquet files to bucket
## Load
from bucket
puts back into rds pg db
## Data Visualisation
read db
some implementation of tableau or looker
pull some analysis
- could perhaps use matplotlib
## Hosting
AWS:
- lambda
- s3
- rds
- Cloudwatch
## Orchestration
CICD - GitHub Actions
Terraform
Step Function - Event Scheduler
## Terraform Structure
file structure
Resources provisioned outside Terraform:
- backend bucket:
    - tf state
- Lambda buckets:
    - python
    - layers
## Logging
Cloudwatch logs















