terraform{
    required_providers {
        aws= {
            source="hashicorp/aws"
            version = "~> 5.0"
        }
    }  
backend "s3" {
    bucket="ainsdale-beach-tf-state"
    key="terraform/state"
    region="eu-west-2"
}
}

provider "aws"{
     region="eu-west-2"
}
