#### This template will help us to convert the CSV file into the data frames from the aws s3 bucket. We are using python with boto3 to fetch the file from the aws s3 bucket and convert this into the data frame .

You just need to run the below commands:
### Steps:
1. First you should configure the aws in your system:


        aws configure

2. You should create a s3 bucket and upload a CSV file in the bucket.

3. Run this python file with the below command:

        python3 main.py